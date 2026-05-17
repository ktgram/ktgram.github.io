---
---
title: Web Starters (Spring And Ktor)
---

### Spring starter

ماژول Spring Starter برای کتابخانه یک ماژول پیکربندی خودکار است که قابلیت‌های بات تلگرام را به برنامه‌های Spring Boot یکپارچه می‌کند. این ماژول از توانایی تزریق وابستگی‌ها و ویژگی‌های پیکربندی Spring Boot استفاده می‌کند تا بات‌های تلگرام را بر اساس پیکربندی ارائه‌شده به‌صورت خودکار پیکربندی کند. این کتابخانه به‌ویژه برای توسعه‌دهندگانی مفید است که می‌خواهند بات‌های تلگرام را با استفاده از Kotlin و Spring Boot بسازند و یک رویکرد بهینه برای توسعه و مدیریت بات ارائه می‌دهد.

### Key Features

- **Auto-Configuration**: کتابخانه به‌صورت خودکار بات‌های تلگرام را بر اساس ویژگی‌های پیکربندی ارائه‌شده تنظیم می‌کند و نیاز به تنظیم دستی را از بین می‌برد.
- **Configuration Properties**: از ویژگی‌های پیکربندی برای سفارشی‌سازی آسان تنظیمات بات، مانند توکن‌های بات، نام بسته‌ها و شناسه‌ها پشتیبانی می‌کند.
- **Spring Integration**: به‌صورت یکپارچه با اکوسیستم Spring ترکیب می‌شود و از تزریق وابستگی Spring و Context برنامه برای مدیریت نمونه‌های بات استفاده می‌کند.
- **Coroutine Support**: از coroutineهای Kotlin برای عملیات غیرهمزمان بات بهره می‌گیرد و اجرای کارآمد و غیرمسدودکننده را تضمین می‌کند.

### Getting Started

برای استفاده از کتابخانه Spring Starter برای بات‌های تلگرام، باید آن را به‌عنوان یک وابستگی در پروژه Spring Boot خود وارد کنید. این کتابخانه برای کار با برنامه‌های Spring Boot طراحی شده است و به فریم‌ورک Spring Boot برای عملکرد نیاز دارد.

#### Dependency

وابستگی زیر را به فایل `build.gradle` یا `pom.xml` خود اضافه کنید:

```gradle
dependencies {
    implementation 'eu.vendeli:spring-starter:<version>'
}
```

`<version>` را با آخرین نسخه کتابخانه جایگزین کنید.

#### Configuration

کتابخانه از `@ConfigurationProperties` مربوط به Spring Boot برای بایند کردن ویژگی‌های پیکربندی استفاده می‌کند. می‌توانید پیکربندی‌های بات خود را در فایل `application.properties` یا `application.yml` برنامه Spring Boot تعریف کنید.

```yaml
ktgram:
 autoStartPolling: true
 shareHttpClient: true
 bot:
    - token: YOUR_BOT_TOKEN
      pckg: com.example.bot
      identifier: MyBot
```

#### Usage

پس از اینکه کتابخانه وارد و پیکربندی شد، به‌صورت خودکار نمونه‌های بات تلگرام را بر اساس پیکربندی ارائه‌شده می‌سازد و تنظیم می‌کند.

همچنین از چندین نمونه بات پشتیبانی می‌کند؛ برای مقداردهی چندین بات کافی است آنها را به‌صورت ورودی جدید در بخش bot تعریف کنید:

```yaml
ktgram:
 bot:
    - token: YOUR_BOT_TOKEN
    - token: SECOND_BOT_TOKEN
```

### Advanced Configuration

برای پیکربندی‌های پیشرفته‌تر، مانند سفارشی‌سازی رفتار بات یا یکپارچه‌سازی با سایر کامپوننت‌های Spring، می‌توانید کلاس `BotConfiguration` را گسترش دهید و پیکربندی بات را از طریق متد `applyCfg` تغییر دهید؛ مثال را می‌توانید در [اینجا](https://github.com/vendelieu/telegram-bot_template/blob/spring-bot/src/main/kotlin/com/example/springbot/configuration/BotConfig.kt) ببینید.

> [!TIP]
> برای پیکربندی هر نمونه‌ی اولیه‌شده با تنظیمات سفارشی، آنها را با شناسه‌ی خود متمایز کنید (کلاس BotConfiguration نیز دارای یک شناسه است).

### Ktor

این ماژول برای ساده‌سازی ایجاد یک سرور webhook برای بات‌های تلگرام طراحی شده است. به توسعه‌دهندگان اجازه می‌دهد سرور را شامل تنظیمات SSL/TLS پیکربندی کنند و چندین بات تلگرام را با تنظیمات سفارشی اعلام کنند. فرآیند راه‌اندازی انعطافی است و به توسعه‌دهندگان امکان می‌دهد سرور را متناسب با نیازهای خاص خود تنظیم کنند.

### Installation

برای نصب Ktor starter، وابستگی زیر را به وابستگی اصلی اضافه کنید:

```gradle
dependencies {
    implementation("eu.vendeli:ktor-starter:x.y.z") // there
    // change x.y.z to current library version
}
```

### Key Components

`serveWebhook` Function

تابع `serveWebhook` هسته کتابخانه است. این تابع سرور webhook را برای بات‌های تلگرام راه‌اندازی و اجرا می‌کند. دو پارامتر می‌پذیرد:

- `wait`: یک Boolean که مشخص می‌کند آیا سرور باید قبل از خاتمه برنامه منتظر بماند یا نه. پیش‌فرض `true` است.
- `serverBuilder`: یک تابع لامبدا که سرور را پیکربندی می‌کند. پیش‌فرض یک لامبدا خالی است.

### Configuration

* `WEBHOOK_PREFIX`: پارامتری است که به‌عنوان پیشوند آدرس برای مسیر listener webhook استفاده می‌شود. (پیش‌فرض `"/"`)

#### Server Setup

- `server`: روشی برای تنظیم پیکربندی سرور با استفاده از `EnvConfiguration` یا `ManualConfiguration`.
- `engine`: روشی برای پیکربندی موتور برنامه Netty.
- `ktorModule`: روشی برای افزودن ماژول‌های Ktor به برنامه.

کتابخانه مجموعه‌ای گسترده از پارامترهای پیکربندی‌پذیر برای سرور فراهم می‌کند، از جمله host، port، تنظیمات SSL و غیره. دو گزینه‌ی مشخص برای پیکربندی وجود دارد:

* `EnvConfiguration`: مقادیر پیکربندی را از محیط با پیشوند `KTGRAM_` می‌خواند.
* `ManualConfiguration`: امکان تنظیم دستی مقادیر پیکربندی را می‌دهد؛ پارامترهای خود را در تابع `server {}` تنظیم کنید.

لیستی از پارامترهای قابل تنظیم:

- `HOST`: نام میزبان یا آدرس IP سرور.
- `PORT`: شماره پورت سرور.
- `SSL_PORT`: شماره پورت برای اتصال‌های SSL/TLS.
- `PEM_PRIVATE_KEY_PATH`: مسیر فایل کلید خصوصی PEM.
- `PEM_CHAIN_PATH`: مسیر فایل زنجیره گواهی PEM.
- `PEM_PRIVATE_KEY`: رمز عبور کلید خصوصی PEM به صورت آرایه کاراکتری.
- `KEYSTORE_PATH`: مسیر فایل Java KeyStore.
- `KEYSTORE_PASSWORD`: رمز عبور KeyStore.
- `KEY_ALIAS`: نام مستعار کلید در KeyStore.
- `SSL_ON`: یک Boolean که نشان می‌دهد آیا SSL/TLS باید فعال باشد یا نه. پیش‌فرض `true`.

> [!TIP]
> اگر گواهینامه‌های PEM موجود باشند، ماژول خود به‌صورت خودکار یک ذخیره‌سازی jks از آنها در مسیر مشخص‌شده ایجاد می‌کند.

#### Bot Configuration:

برای پیکربندی بات، `declareBot {}` را فراخوانی کنید که پارامترهای زیر را دارد:

- `token`: توکن بات.
- `pckg`: نام بسته برای بات.
- `configuration`: یک لامبدا برای پیکربندی بات.
- `handlingBehaviour`: یک لامبدا برای تنظیم رفتار پردازش بات.
- `onInit`: یک لامبدا که هنگام مقداردهی اولیه بات اجرا می‌شود.

### Example Usage

برای استفاده از این ماژول، تابع `serveWebhook` را فراخوانی کنید، آن را با تنظیمات دلخواه پیکربندی کنید و بات‌ها را اعلام کنید. در ادامه یک مثال ساده آورده شده است:

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
> فراموش نکنید وب‌هوک را تنظیم کنید تا همه چیز کار کند. :)

به‌طور پیش‌فرض ماژول نقاط انتهایی گوش دادن وب‌هوک را به صورت `host/BOT_TOKEN` سرو می‌کند.


---