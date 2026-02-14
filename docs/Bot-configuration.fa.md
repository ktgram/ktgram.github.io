---
---
title: Bot Configuration
---

کتابخانه گزینه‌های بسیاری برای پیکربندی فراهم می‌کند، می‌توانید به مرجع API در کلاس [`BotConfiguration`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.configuration/-bot-configuration/index.html) مراجعه کنید.

دو رویکرد برای پیکربندی ربات وجود دارد:

### Lambda Configurator

```kotlin
// ...
val bot = TelegramBot("BOT_TOKEN") {
  inputListener = RedisInputListenerImpl()
  classManager = KoinClassManagerImpl()
  logging {
      botLogLevel = LogLvl.DEBUG
  }
}
// ...
```

### رابط ConfigLoader

همچنین امکان پیکربندی از طریق رابط خاص [`ConfigLoader`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.helper/-config-loader/index.html) وجود دارد،<br/> که می‌توانید برای بارگذاری تنظیمات از منابع خارجی (`properties`, `command line args`, و غیره) استفاده کنید.

پیاده‌سازی این رابط می‌تواند از طریق سازنده ثانویه منتقل شود و نمونه مطابق آن پیکربندی خواهد شد.

```kotlin
val bot = TelegramBot(ConfigLoaderImpl)
```

در حال حاضر چندین ماژول ارائه شده که این رابط را پیاده‌سازی می‌کند مانند `ktgram-config-env`، `ktgram-config-toml`.

### BotConfiguration Overview

#### BotConfiguration

کلاس `BotConfiguration` مرکز اصلی برای پیکربندی ربات است. شامل خواصی برای شناسایی ربات، تنظیم میزبان API، تعیین اینکه آیا ربات در محیط آزمایشی فعال است، مدیریت ورودی‌ها، مدیریت کلاس‌ها و کنترل حذف خودکار ورودی است. علاوه بر این، خواص درونی برای محدودیت نرخ، پیکربندی کلاینت HTTP، لاگینگ، گوش دادن به آپدیت‌ها و تجزیه دستورات ارائه می‌کند.

##### Properties

- `identifier`: شناسایی نمونه‌های مختلف ربات در طول پردازش چند رباتی.
- `apiHost`: میزبان API تلگرام.
- `isTestEnv`: پرچمی که نشان می‌دهد آیا ربات در محیط آزمایشی فعال است.
- `inputListener`: نمونه‌ای از کلاس مدیریت ورودی.
- `classManager`: مدیریتی که برای دریافت کلاس‌ها استفاده می‌شود.
- `inputAutoRemoval`: پرچمی که حذف خودکار نقطه ورودی در طول پردازش را تنظیم می‌کند.
- `exceptionHandlingStrategy`: استراتژی برای مدیریت استثناها را تعریف می‌کند.
    * `CollectToChannel` - جمع‌آوری به `TgUpdateHandler.caughtExceptions`.
    * `Throw` - دوباره پرتاب با لفاف `TgException`.
    * `DoNothing` - هیچ کاری انجام نده :)
    * `Handle` - تنظیم کننده سفارشی.
- `throwExOnActionsFailure`: استثنا پرتاب می‌کند وقتی هر درخواست رباتی شکست می‌خورد.

##### Configuration Blocks

`BotConfiguration` همچنین توابعی برای پیکربندی کامپوننت‌های درونی خود ارائه می‌دهد:

- `httpClient(block: HttpConfiguration.() -> Unit)`: کلاینت HTTP را پیکربندی می‌کند.
- `logging(block: LoggingConfiguration.() -> Unit)`: لاگینگ را پیکربندی می‌کند.
- `rateLimiter(block: RateLimiterConfiguration.() -> Unit)`: محدودیت درخواست را پیکربندی می‌کند.
- `updatesListener(block: UpdatesListenerConfiguration.() -> Unit)`: گوش‌دهنده آپدیت‌ها را پیکربندی می‌کند.
- `commandParsing(block: CommandParsingConfiguration.() -> Unit)`: الگوی تجزیه دستورات را مشخص می‌کند.

### کلاس‌های پیکربندی مرتبط

#### RateLimiterConfiguration

محدودیت نرخ جهانی را پیکربندی می‌کند.

- `limits`: محدودیت‌های نرخ جهانی.
- `mechanism`: مکانیزمی که برای محدودیت نرخ استفاده می‌شود، پیش‌فرض الگوریتم TokenBucket است.
- `exceededAction`: عملی که زمانی اعمال می‌شود که محدودیت تجاوز شود.

#### HttpConfiguration

تنظیمات کلاینت HTTP ربات را شامل می‌شود.

- `requestTimeoutMillis`: مهلت درخواست به میلی‌ثانیه.
- `connectTimeoutMillis`: مهلت اتصال به میلی‌ثانیه.
- `socketTimeoutMillis`: مهلت سوکت به میلی‌ثانیه.
- `maxRequestRetry`: حداکثر تلاش برای درخواست‌های HTTP.
- `retryStrategy`: استراتژی برای تلاش مجدد، قابل سفارشی‌سازی.
- `retryDelay`: ضریب برای timeout در هر تلاش مجدد.
- `proxy`: تنظیمات پروکسی برای تماس‌های HTTP.
- `additionalHeaders`: هدرهایی که به هر درخواست اعمال می‌شوند.

#### LoggingConfiguration

سطح لاگینگ را برای اقدامات ربات و درخواست‌های HTTP مدیریت می‌کند.

- `botLogLevel`: سطح لاگ‌ها برای اقدامات ربات.
- `httpLogLevel`: سطح لاگ‌ها برای درخواست‌های HTTP.

#### UpdatesListenerConfiguration

پارامترهای مربوط به کشیدن آپدیت‌ها را پیکربندی می‌کند.

- `dispatcher`: dispatcher برای جمع‌آوری آپدیت‌های ورودی.
- `processingDispatcher`: dispatcher برای پردازش آپدیت‌ها.
- `pullingDelay`: تاخیر بعد از هر درخواست کشیدن.
- `updatesPollingTimeout`: گزینه timeout برای مکانیزم long-polling.

#### CommandParsingConfiguration

پارامترهایی برای تجزیه دستورات را مشخص می‌کند.

- `commandDelimiter`: جداکننده بین دستور و پارامترها.
- `parametersDelimiter`: جداکننده بین پارامترها.
- `parameterValueDelimiter`: جداکننده بین کلید و مقدار پارامتر.
- `restrictSpacesInCommands`: پرچمی که نشان می‌دهد آیا فضاهای در دستورات باید به عنوان پایان دستور در نظر گرفته شوند.
- `useIdentifierInGroupCommands`: از شناسه ربات برای مطابقت دستورات حاوی @ استفاده می‌کند.

### مثال پیکربندی

در اینجا مثالی از نحوه پیکربندی ربات با استفاده از این کلاس‌ها آورده شده است:

```kotlin
val bot = TelegramBot("TOKEN") {
    identifier = "MyBot",
    apiHost = "https://api.telegram.org",
    isTestEnv = true,
    inputListener = InputListenerMapImpl(),
    classManager = ClassManagerImpl(),

    httpClient {
        requestTimeoutMillis = 5000L
        connectTimeoutMillis = 3000L
        socketTimeoutMillis = 2000L
    }
    logging {
        botLogLevel = LogLvl.DEBUG
        httpLogLevel = HttpLogLevel.BODY
    }
    updatesListener {
        dispatcher = Dispatchers.IO
        processingDispatcher = Dispatchers.Unconfined
        pullingDelay = 1000L
    }
    commandParsing {
        commandDelimiter = '*'
        parametersDelimiter = '&'
        restrictSpacesInCommands = true
    }
}
```

این پیکربندی رباتی با شناسه‌های خاص، حالت محیط آزمایشی را فعال، محدودیت نرخ را پیکربندی، تنظیمات کلاینت HTTP، سطوح لاگینگ، پارامترهای گوش‌دهنده آپدیت و قوانین تجزیه دستورات را تنظیم می‌کند.

با بهره‌بردن از این گزینه‌های پیکربندی، توسعه‌دهندگان می‌توانند ربات‌های خود را برای برآورده کردن نیازهای خاص و بهینه‌سازی عملکرد در سناریوهای عملیاتی مختلف تنظیم کنند.

---