from psycopg import Connection


def get_user_by_phone(db: Connection, phone_number: str) -> dict | None:
    query = """
        SELECT
            u.id,
            u.full_name,
            u.phone_number,
            u.email,
            u.created_at,
            EXISTS (SELECT 1 FROM booths b WHERE b.user_id = u.id) AS has_booth
        FROM users u
        WHERE u.phone_number = %s
    """
    return db.execute(query, (phone_number,)).fetchone()


def get_user_by_id(db: Connection, user_id: int) -> dict | None:
    query = """
        SELECT
            u.id,
            u.full_name,
            u.phone_number,
            u.email,
            u.created_at,
            EXISTS (SELECT 1 FROM booths b WHERE b.user_id = u.id) AS has_booth
        FROM users u
        WHERE u.id = %s
    """
    return db.execute(query, (user_id,)).fetchone()


def get_user_by_email(db: Connection, email: str) -> dict | None:
    query = "SELECT id, email FROM users WHERE email = %s"
    return db.execute(query, (email,)).fetchone()


def create_user_by_phone(
    db: Connection, phone_number: str, full_name: str = "New User"
) -> dict:
    query = """
        INSERT INTO users (full_name, phone_number)
        VALUES (%s, %s)
        RETURNING id, full_name, phone_number, email, created_at, FALSE AS has_booth
    """
    return db.execute(query, (full_name, phone_number)).fetchone()


def update_user(
    db: Connection, user_id: int, full_name: str | None, email: str | None
) -> dict | None:
    query = """
        UPDATE users
        SET
            full_name = COALESCE(%s, full_name),
            email = COALESCE(%s, email)
        WHERE id = %s
        RETURNING id, full_name, phone_number, email
    """
    return db.execute(query, (full_name, email, user_id)).fetchone()