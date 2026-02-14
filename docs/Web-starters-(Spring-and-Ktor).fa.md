---
---
title: Web Starters (Spring And Ktor)
---

### Spring starter

ماژول Spring Starter برای کتابخانه یک ماژول خودکار-پیکربندی است که قابلیت‌های ربات تلگرام را در برنامه‌های Spring Boot یکپارچه می‌کند. این ماژول از قدرت حقن وابستگی Spring Boot و خصوصیات پیکربندی برای پیکربندی خودکار ربات‌های تلگرام بر اساس پیکربندی ارائه شده استفاده می‌کند. این کتابخانه به‌ویژه برای توسعه‌دهندگانی که می‌خواهند ربات‌های تلگرام را با استفاده از Kotlin و Spring Boot بسازند مفید است و رویکردی ساده‌تری برای توسعه و مدیریت ربات ارائه می‌دهد.

### قابلیت‌های کلیدی

- **پیکربندی خودکار**: کتابخانه بر اساس خصوصیات پیکربندی ارائه شده ربات‌های تلگرام را خودکار پیکربندی می‌کند، بدون نیاز به راه‌اندازی دستی.
- **خصوصیات پیکربندی**: پشتیبانی از خصوصیات پیکربندی برای سفارشی‌سازی آسان تنظیمات ربات مانند توکن‌های ربات، نام بسته‌ها و شناسه‌ها را فراهم می‌کند.
- **یکپارچگی Spring**: به‌طور یکپارچه با اکوسیستم Spring ادغام می‌شود و از حقن وابستگی Spring و زمینه برنامه برای مدیریت نمونه‌های ربات استفاده می‌کند.
- **پشتیبانی Coroutines**: از Coroutines Kotlin برای عملیات‌های غیرهمزمان ربات استفاده می‌کند تا اجرای کارآمد و غیرمسدود را تضمین کند.

### شروع کار

برای استفاده از کتابخانه Spring Starter برای ربات‌های تلگرام، باید آن را به عنوان وابستگی در پروژه Spring Boot خود اضافه کنید. این کتابخانه برای کار با برنامه‌های Spring Boot طراحی شده است و برای کار کردن نیاز به چارچوب Spring Boot دارد.

#### وابستگی

خط زیر را به فایل `build.gradle` یا `pom.xml` خود اضافه کنید:

```gradle
dependencies {
    implementation 'eu.vendeli:spring-starter:<version>'
}
```

`<version>` را با آخرین نسخه کتابخانه جایگزین کنید.

#### پیکربندی

کتابخانه از `@ConfigurationProperties` Spring Boot برای اتصال خصوصیات پیکربندی استفاده می‌کند. می‌توانید پیکربندی‌های ربات خود را در فایل `application.properties` یا `application.yml` برنامه Spring Boot خود تعریف کنید.

```yaml
ktgram:
 autoStartPolling: true
 shareHttpClient: true
 bot:
    - token: YOUR_BOT_TOKEN
      pckg: com.example.bot
      identifier: MyBot
```

#### استفاده

پس از اضافه کردن و پیکربندی کتابخانه، به‌طور خودکار نمونه‌های ربات تلگرام را بر اساس پیکربندی ارائه شده می‌سازد و پیکربندی می‌کند.

همچنین پشتیبانی از چندین نمونه ربات را دارد، برای راه‌اندازی چند نمونه فقط آن را به عنوان ورودی جدید در بخش bot اعلام کنید:

```yaml
ktgram:
 bot:
    - token: YOUR_BOT_TOKEN
    - token: SECOND_BOT_TOKEN
```

### پیکربندی پیشرفته

برای پیکربندی‌های پیشرفته‌تر مانند سفارشی‌سازی رفتار ربات یا ادغام با کامپوننت‌های دیگر Spring، می‌توانید کلاس `BotConfiguration` را گسترش دهید و پیکربندی ربات را از طریق متد `applyCfg` آن تغییر دهید، می‌توانید نمونه‌ای را [در اینجا](https://github.com/vendelieu/telegram-bot_template/blob/spring-bot/src/main/kotlin/com/example/springbot/configuration/BotConfig.kt) ببینید.

> [!TIP]
> برای پیکربندی هر نمونه مقداردهی شده با پیکربندی سفارشی، آن‌ها را بر اساس شناسه متمایز کنید (کلاس BotConfiguration نیز شناسه دارد).

### Ktor

ماژول برای تسهیل ایجاد سرور webhook برای ربات‌های تلگرام طراحی شده است. به توسعه‌دهندگان امکان می‌دهد سرور را پیکربندی کنند، شامل تنظیمات SSL/TLS، و چندین ربات تلگرام با پیکربندی‌های سفارشی اعلام کنند. فرآیند راه‌اندازی منعطف است و به توسعه‌دهندگان امکان می‌دهد سرور را بر اساس نیازهای خاص خود سفارشی کنند.

### نصب

برای نصب نسخه Ktor به وابستگی اصلی اضافه کنید:

```gradle
dependencies {
    implementation("eu.vendeli:ktor-starter:x.y.z") // there
    // change x.y.z to current library version
}
```

### کامپوننت‌های کلیدی

تابع `serveWebhook`

تابع serveWebhook هسته کتابخانه است. سرور webhook را برای ربات‌های تلگرام تنظیم و راه‌اندازی می‌کند. دو پارامتر قبول می‌کند:

- `wait`: یک بولین که نشان می‌دهد آیا سرور باید قبل از خاموش شدن منتظر توقف برنامه بماند. به طور پیش‌فرض true است.
- `serverBuilder`: یک تابع لاندا برای پیکربندی سرور. به طور پیش‌فرض یک لاندا خالی است.

### پیکربندی

* `WEBHOOK_PREFIX`: پارامتری است که برای پیشوند آدرس مسیر گوش‌دهنده webhook استفاده می‌شود. (به طور پیش‌فرض "/")

#### راه‌اندازی سرور

- `server`: یک متد برای تنظیم پیکربندی سرور با استفاده از EnvConfiguration یا ManualConfiguration.
- `engine`: یک متد برای پیکربندی موتور برنامه Netty.
- `ktorModule`: یک متد برای اضافه کردن ماژول‌های Ktor به برنامه.

کتابخانه مجموعه گسترده‌ای از پارامترهای قابل تنظیم برای سرور فراهم می‌کند، شامل میزبان، پورت، تنظیمات SSL و غیره. دو گزینه واضح برای پیکربندی آن وجود دارد:

* `EnvConfiguration`: مقادیر پیکربندی را از محیط با پیشوند `KTGRAM_` می‌خواند.
* `ManualConfiguration`: امکان تنظیم دستی مقادیر پیکربندی را فراهم می‌کند، پارامترهای خود را در تابع `server {}` تنظیم کنید.

فهرستی از پارامترهایی که می‌توان تنظیم کرد:

- `HOST`: نام میزبان یا آدرس IP سرور.
- `PORT`: شماره پورت برای سرور.
- `SSL_PORT`: شماره پورت برای اتصالات SSL/TLS.
- `PEM_PRIVATE_KEY_PATH`: مسیر فایل کلید خصوصی PEM.
- `PEM_CHAIN_PATH`: مسیر فایل زنجیره گواهی PEM.
- `PEM_PRIVATE_KEY`: رمز کلید خصوصی PEM به عنوان آرایه کاراکتر.
- `KEYSTORE_PATH`: مسیر فایل KeyStore جاوا.
- `KEYSTORE_PASSWORD`: رمز برای KeyStore.
- `KEY_ALIAS`: نام مستعار برای کلید در KeyStore.
- `SSL_ON`: یک بولین که نشان می‌دهد آیا SSL/TLS باید فعال شود. به طور پیش‌فرض true است.

> [!TIP]
> اگر گواهی‌های pem وجود داشته باشند، ماژول خودش ذخیره‌گاه jks را از آن‌ها در مسیر مشخص شده می‌سازد.

#### پیکربندی ربات:

برای پیکربندی ربات، تابع `declareBot {}` را فراخوانی کنید که چنین پارامترهایی دارد:

- `token`: توکن ربات.
- `pckg`: نام بسته برای ربات.
- `configuration`: یک تابع لاندا برای پیکربندی ربات.
- `handlingBehaviour`: یک تابع لاندا برای تنظیم رفتار مدیریت ربات.
- `onInit`: یک تابع لاندا که زمانی که ربات مقداردهی اولیه می‌شود اجرا می‌شود.

### نمونه استفاده

برای استفاده از این ماژول، تابع `serveWebhook` را فراخوانی کنید، آن را با تنظیمات دلخواه پیکربندی کنید، ربات‌های خود را اعلام کنید. در اینجا یک نمونه ساده‌سازی شده آورده شده است:

```kotlin
fun main() = runBlocking {
    serveWebhook {
        server {
            HOST = "0.0.0.0"
            PORT = 8080
            SSL_PORT = 8443

            PEM_PRIVATE_KEY_PATH = "/etc/letsencrypt/live/example.com/privkey.pem"
            PEM_CHAIN_PATH = "/etc/letsencrypt/live/example.com/fullchain.pem"
            PEM_PRIVATE_KEY = "pem_changeit".toCharArray()

            KEYSTORE_PATH = "/etc/ssl/certs/java/cacerts/bot_keystore.jks"
            KEYSTORE_PASSWORD = "changeit".toCharArray()
            // Set other configuration parameters as needed
        }
        declareBot {
            token = "YOUR_BOT_TOKEN"
            // Configure other bot settings
        }
        // Add more bots or set other parameters if needed
    }
}
```

> [!CAUTION]
> فراموش نکنید webhook را تنظیم کنید تا همه چیز کار کند. :)

به طور پیش‌فرض ماژول endpoints گوش‌دهنده webhook را به عنوان `host/BOT_TOKEN` ارائه می‌دهد


---