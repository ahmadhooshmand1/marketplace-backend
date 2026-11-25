Marketplace - API Design (v1)

==================================================
1. Auth & Users
==================================================

POST /v1/auth/login
ورود یا ثبت‌نام کاربر با شماره موبایل (وضعیت داشتن غرفه هم تغییر میکنه تا دکمه بالای سایت مشخص بشه)
Request: phone_number
Response: access_token, token_type, user (id, full_name, phone_number, has_booth)
Status Codes: 200 (موفق), 400 (فرمت شماره موبایل غلط است)


GET /v1/users/me
گرفتن اطلاعات کاربر برای نمایش در صفحه پروفایل
Request: Token
Response: id, full_name, phone_number, email, has_booth, created_at
Status Codes: 200 (موفق), 401 (کاربر لاگین نیست)


PATCH /v1/users/me
ویرایش نام و ایمیل کاربر در صفحه پروفایل بعد از زدن دکمه ذخیره تغییرات
Request: full_name, email (optional)
Response: id, full_name, phone_number, email
Status Codes: 200 (موفق), 400 (ورودی نامعتبر), 401, 409 (ایمیل تکراری است)


==================================================
2. User Addresses
==================================================

GET /v1/users/me/addresses
گرفتن لیست آدرس‌های ثبت‌شده کاربر برای نمایش در پروفایل و انتخاب آدرس موقع خرید
Request: Token
Response: List of addresses (id, recipient_name, phone_number, province, city, address_line, plaque)
Status Codes: 200 (موفق), 401


POST /v1/users/me/addresses
ثبت آدرس جدید وقتی کاربر دکمه افزودن آدرس جدید رو می‌زنه
Request: recipient_name, phone_number, province, city, address_line, plaque (optional)
Response: id, recipient_name, phone_number, province, city, address_line, plaque, created_at
Status Codes: 201 (ثبت شد), 400 (فیلدهای اجباری ناقص است), 401


DELETE /v1/users/me/addresses/{address_id}
حذف یکی از آدرس‌های کاربر
Request: address_id (in path)
Response: Empty
Status Codes: 204 (حذف شد), 403 (آدرس متعلق به این کاربر نیست), 404 (پیدا نشد), 409 (قبلاً در یک سفارش ثبت شده و قابل حذف نیست)


==================================================
3. Wallets & Transactions
==================================================

GET /v1/users/me/wallet
نمایش موجودی کیف پول کاربر در پروفایل (فقط موجودی رو برمی‌گردونه تا پاسخ سبک بمونه)
Request: Token
Response: id, balance, updated_at
Status Codes: 200 (موفق), 401


POST /v1/users/me/wallet/transactions
افزایش موجودی کیف پول با کلید یکتا تا از ثبت تراکنش تکراری جلوگیری بشه
Request: amount, transaction_type (deposit), idempotency_key
Response: id, wallet_id, amount, transaction_type, idempotency_key, new_balance, created_at
Status Codes: 201 (شارژ انجام شد), 400 (مبلغ نامعتبر), 401, 409 (این کلید تراکنش قبلاً ثبت شده)


GET /v1/users/me/wallet/transactions
نمایش لیست واریز و برداشت‌های کیف پول کاربر
Request: page, limit (query)
Response: List of transactions (id, amount, transaction_type, created_at)
Status Codes: 200 (موفق), 401


==================================================
4. Booths
==================================================

GET /v1/booths
گرفتن لیست غرفه‌های فعال برای نمایش در صفحه اصلی و جستجو بین غرفه‌ها (بدون توضیحات طولانی)
Request: search, city, page, limit (query)
Response: List of booths (id, name, slug, city, products_count, average_rating), total, page
Status Codes: 200 (موفق)


GET /v1/booths/{slug}
باز کردن صفحه اختصاصی یک غرفه و نمایش اطلاعات کامل اون غرفه
Request: slug (in path)
Response: id, user_id, name, slug, city, description, products_count, average_rating, reviews_count, created_at
Status Codes: 200 (موفق), 404 (غرفه پیدا نشد)


POST /v1/booths
ساخت غرفه جدید بعد از پر کردن فرم ایجاد غرفه و زدن دکمه ثبت
Request: name, slug, city, description
Response: id, user_id, name, slug, city, description, created_at
Status Codes: 201 (غرفه ساخته شد), 400 (اطلاعات ناقص), 401, 409 (اسلاگ تکراریه یا کاربر قبلاً غرفه ساخته)


PATCH /v1/booths/me
ویرایش مشخصات غرفه توسط غرفه‌دار از داخل پنل غرفه
Request: name, city, description (optional)
Response: id, name, slug, city, description
Status Codes: 200 (موفق), 403 (کاربر غرفه ندارد), 404


==================================================
5. Products & Reviews
==================================================

GET /v1/products
گرفتن لیست جدیدترین محصولات در صفحه اصلی و نوار جستجوی بالای سایت (بدون توضیحات طولانی)
Request: search, min_price, max_price, in_stock, sort, page, limit (query)
Response: List of products (id, title, price, stock, lead_time_days, booth summary), total, page
Status Codes: 200 (موفق), 400 (پارامتر فیلتر نامعتبر)


GET /v1/booths/{booth_id}/products
گرفتن لیست محصولات یک غرفه خاص (هم برای صفحه غرفه با فیلترهاش، هم برای پنل غرفه‌دار)
Request: booth_id (in path), search, in_stock, min_price, max_price (query)
Response: List of products (id, title, price, stock, lead_time_days, created_at)
Status Codes: 200 (موفق), 404 (غرفه پیدا نشد)


GET /v1/products/{product_id}
باز کردن صفحه جزئیات محصول و نمایش کامل مشخصات و اطلاعات غرفه مربوطه
Request: product_id (in path)
Response: id, booth_id, title, description, price, stock, lead_time_days, average_rating, reviews_count, created_at, booth info
Status Codes: 200 (موفق), 404 (محصول پیدا نشد)


POST /v1/products
اضافه کردن محصول جدید توسط غرفه‌دار با زدن دکمه ذخیره و انتشار محصول
Request: title, description, price, stock, lead_time_days
Response: id, booth_id, title, description, price, stock, lead_time_days, created_at
Status Codes: 201 (محصول ثبت شد), 400 (قیمت یا موجودی منفی), 403 (کاربر غرفه ندارد)


PATCH /v1/products/{product_id}
ویرایش قیمت، موجودی یا مشخصات محصول در پنل غرفه‌دار
Request: title, description, price, stock, lead_time_days (optional)
Response: Updated product object
Status Codes: 200 (موفق), 400, 403 (محصول متعلق به این غرفه نیست), 404


DELETE /v1/products/{product_id}
حذف محصول توسط غرفه‌دار در پنل مدیریت غرفه
Request: product_id (in path)
Response: Empty
Status Codes: 204 (حذف شد), 403, 404, 409 (قبلاً سفارش خورده و قابل حذف نیست)


GET /v1/products/{product_id}/reviews
نمایش نظرات و امتیازهای خریداران در پایین صفحه محصول
Request: product_id (in path), page, limit (query)
Response: List of reviews (id, user_name, rating, comment, created_at)
Status Codes: 200 (موفق), 404


POST /v1/products/{product_id}/reviews
ثبت نظر و امتیاز جدید (بین ۱ تا ۵) توسط خریدار برای یک محصول
Request: rating (1 to 5), comment
Response: id, user_id, product_id, rating, comment, created_at
Status Codes: 201 (نظر ثبت شد), 400 (امتیاز خارج از بازه ۱ تا ۵ است), 401, 404


==================================================
6. Carts & Cart Items
==================================================

GET /v1/carts/me
باز کردن صفحه سبد خرید (شامل آیتم‌های فعال دسته‌بندی‌شده بر اساس غرفه، سبد خرید بعدی و جمع کل قیمت‌ها)
Request: Token
Response: cart_id, active_items_count, saved_for_later_count, booths_group, saved_items, summary (items_total, shipping_fee, service_fee, payable_before_discount)
Status Codes: 200 (موفق), 401


POST /v1/carts/me/items
اضافه کردن کالا به سبد خرید با زدن دکمه افزودن به سبد خرید در صفحه محصول
Request: product_id, quantity
Response: id, cart_id, product_id, quantity, is_saved_for_later, created_at
Status Codes: 201 (به سبد اضافه شد), 400 (موجودی انبار کافی نیست), 401, 404


PATCH /v1/carts/me/items/{item_id}
تغییر تعداد کالا یا انتقال اون به سبد خرید بعدی در صفحه سبد خرید
Request: quantity, is_saved_for_later (optional)
Response: Updated item, new summary
Status Codes: 200 (موفق), 400 (تعداد درخواستی بیشتر از موجودی است), 404


DELETE /v1/carts/me/items/{item_id}
حذف کامل کالا از سبد خرید با زدن آیکون سطل زباله
Request: item_id (in path)
Response: Empty
Status Codes: 204 (حذف شد), 404


==================================================
7. Coupons & Orders
==================================================

POST /v1/coupons/validate
بررسی اعتبار کد تخفیف بعد از وارد کردن کد و زدن دکمه اعمال در سبد خرید
Request: code
Response: valid, coupon_id, code, booth_id, discount_amount, final_amount
Status Codes: 200 (کد معتبر است), 400 (به حداقل مبلغ سفارش نرسیده یا متعلق به این غرفه نیست), 404 (کد وجود ندارد)


POST /v1/orders
ثبت نهایی سفارش با زدن دکمه تأیید و ادامه (کسر موجودی انبار و پرداخت از کیف پول یا درگاه آنلاین)
Request: address_id, coupon_code (optional), payment_method (online / wallet)
Response: id, user_id, address_id, items_total, discount_amount, shipping_fee, service_fee, final_amount, payment_method, status, created_at
Status Codes: 201 (سفارش ثبت شد), 400 (سبد خالیه یا موجودی کیف پول/انبار کمه), 401, 404


GET /v1/users/me/orders
نمایش تاریخچه خریدهای کاربر در تب سفارش‌های من در صفحه پروفایل
Request: Token
Response: List of orders with order_items (product_id, quantity, price_at_purchase)
Status Codes: 200 (موفق), 401


GET /v1/booths/me/orders
نمایش سفارش‌های مشتریان غرفه در تب سفارش‌های مشتریان پنل غرفه‌دار
Request: Token
Response: List of orders containing this booth's products + shipping address
Status Codes: 200 (موفق), 403 (کاربر غرفه ندارد)


PATCH /v1/booths/me/orders/{order_id}
تغییر وضعیت ارسال سفارش توسط غرفه‌دار (مثلاً تغییر وضعیت به ارسال شده)
Request: status
Response: id, status
Status Codes: 200 (وضعیت تغییر کرد), 400 (وضعیت نامعتبر), 403, 404