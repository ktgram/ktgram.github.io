---
---
title: سوالات متداول
---

### استثنا‌ی `AbstractMethodError`

اگر هنگام شروع برنامه‌تان چنین استثنایی دریافت کردید:

```kotlin
Exception in thread "DefaultDispatcher-worker-1" java.lang.AbstractMethodError: 'kotlinx.serialization.KSerializer[] kotlinx.serialization.internal.GeneratedSerializer.typeParametersSerializers()'
	at eu.vendeli.tgbot.types.options.GetUpdatesOptions$$serializer.typeParametersSerializers(GetUpdatesOptions.kt:6)
```

این مسئله به این دلیل رخ می‌دهد که سیستم ساخت کتابخانه‌ی قدیمی‌تری را که مکانیزم داخلی آن متفاوت است، حل می‌کند.
برای حل این مشکل باید از نسخه‌ی جدیدتری استفاده کند، به عنوان مثال با اضافه کردن این کد به buildscript:

```kotlin
configurations.all {
    resolutionStrategy.eachDependency {
        val serdeVer = "x.x.x" // should be >= 1.8.0
        when(requested.module.toString()) {
            // json serialiazaton
            "org.jetbrains.kotlinx:kotlinx-serialization-json" -> useVersion(serdeVer)
            "org.jetbrains.kotlinx:kotlinx-serialization-json-jvm" -> useVersion(serdeVer)
            "org.jetbrains.kotlinx:kotlinx-serialization-core" -> useVersion(serdeVer)
            "org.jetbrains.kotlinx:kotlinx-serialization-core-jvm" -> useVersion(serdeVer)
            "org.jetbrains.kotlinx:kotlinx-serialization-bom" -> useVersion(serdeVer)
        }
    }
}
```

(اگر این موضوع در تاریخچه توضیح داده شده بود، من هرگز ارتقا نمی‌دادم چون من به اندازه‌ی کافی گزارش در مورد این مشکل دریافت می‌کنم)

### چگونه پاسخ متد را دریافت کنم؟

برای دریافت پاسخ و قابلیت عمل بر روی آن، باید در انتهای متد به جای `send` از `sendReturning` استفاده کنید.

در این حالت کلاس `Response` برگردانده می‌شود که حاوی پاسخ موفق یا شکست است، سپس باید یا شکست را مدیریت کنید یا صرفاً `getOrNull()` را صدا بزنید.

یک بخش در مورد این موضوع وجود دارد: [Processing responses](https://github.com/vendelieu/telegram-bot#processing-responses).

### هنگام استفاده از `spring-boot-devtools` خطایی دریافت می‌کنم

این اتفاق به این دلیل رخ می‌دهد که `spring-boot-devtools` خودش `classloader` دارد و متدها را پیدا نمی‌کند.

باید به `resources/META-INF/spring-devtools.properties` اضافه کنید:

```properties
restart.include.generated=/eu.vendeli
```

### چگونه موتور ktor را تغییر دهم

اگر می‌خواهید موتور مورد استفاده توسط کلاینت را تغییر دهید، می‌توانید ساده‌ترین راه تغییر [پارامتر](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/ktor-jvm-engine.html) در [تنظیمات پلاگین](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/index.html) است.

### چگونه از ارائه‌دهنده‌ی ورودی خروجی مورد علاقه‌ام استفاده کنم

کتابخانه از `slf4j-api` استفاده می‌کند و برای استفاده از ارائه‌دهنده فقط کافی است آن را به وابستگی‌ها اضافه کنید.

پلاگین کتابخانه به صورت خودکار استفاده از ارائه‌دهنده را تشخیص می‌دهد، اگر ارائه‌دهنده وجود نداشت، `logback` به صورت پیش‌فرض استفاده خواهد شد.

### گرفتن استثنا‌های شبکه درون handler long-polling

برای مثال اگر اتصال ناپایداری دارید و نیاز به گرفتن خطا به دلیل این موضوع دارید، شاید این روش به شما کمک کند:

```kotlin
fun main() {
    val bot = TelegramBot("TOKEN")

    try {
        bot.handleUpdates()
    } catch (e: Exception) {
        // handle if needed
        
        bot.update.stopListener()
        bot.handleUpdates()
    }
}
```

همچنین می‌توانید نگاهی به نحوه‌ی اجرای آن در [spring-starter](https://github.com/vendelieu/telegram-bot/blob/1584d40f9a94a8c31bba9e7614c0070155630a52/spring-ktgram-starter/src/jvmMain/kotlin/eu/vendeli/spring/starter/TelegramAutoConfiguration.kt#L53) بیندازید.