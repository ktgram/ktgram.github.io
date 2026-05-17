---
---
title: F.A.Q
---

### `AbstractMethodError` exception

اگر این استثنا را در هنگام راه‌اندازی برنامه خود دریافت می‌کنید:

```kotlin
Exception in thread "DefaultDispatcher-worker-1" java.lang.AbstractMethodError: 'kotlinx.serialization.KSerializer[] kotlinx.serialization.internal.GeneratedSerializer.typeParametersSerializers()'
	at eu.vendeli.tgbot.types.options.GetUpdatesOptions$$serializer.typeParametersSerializers(GetUpdatesOptions.kt:6)
```

به این دلیل رخ می‌دهد که سیستم ساخت شما کتابخانه‌ی قدیمی Serialization را که مکانیک‌های داخلی آن متفاوت است، حل می‌کند.
برای رفع آن باید نسخه جدیدتری استفاده کنید، برای مثال با افزودن موارد زیر به اسکریپت ساخت خود:

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

(اگر این موضوع به خوبی در changelog توضیح داده می‌شد، هرگز آن را ارتقا نمی‌دادم چون گزارش‌های زیادی در این باره می‌دیدم)

### How do I get the method's response?

برای دریافت پاسخ و امکان کار بر روی آن، باید به‌جای `send` از `sendReturning` در انتهای متد استفاده کنید.

در این حالت کلاس `Response` برگردانده می‌شود که شامل پاسخ، موفقیت یا شکست است؛ سپس باید یا خطا را مدیریت کنید یا فقط `getOrNull()` را صدا بزنید.

بخش مربوطه: [Processing responses](https://github.com/vendelieu/telegram-bot#processing-responses).

### I'm getting error while using `spring-boot-devtools`

این مشکل به این دلیل است که `spring-boot-devtools` دارای `classloader` اختصاصی خود است و روش‌ها را پیدا نمی‌کند.

باید مورد زیر را به `resources/META-INF/spring-devtools.properties` اضافه کنید:

```properties
restart.include.generated=/eu.vendeli
```

### How to change ktor engine

اگر می‌خواهید موتور استفاده‌شده توسط کلاینت را تغییر دهید، می‌توانید به‌سادگی [پارامتر](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/ktor-jvm-engine.html) را در [تنظیمات افزونه](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/index.html) تغییر دهید.

### How to use my favorite logging provider

این کتابخانه از `slf4j-api` استفاده می‌کند و برای استفاده از ارائه‌دهنده کافیست آن را به وابستگی‌ها اضافه کنید.

افزونه کتابخانه به‌طور خودکار استفاده از ارائه‌دهنده را تشخیص می‌دهد؛ اگر ارائه‌دهنده موجود نباشد، به‌صورت پیش‌فرض `logback` استفاده خواهد شد.

### Catch network exceptions within long-polling handler

به‌عنوان مثال اگر اتصال ناپایداری دارید و نیاز به کشیدن خطا دارید، شاید این رویکرد برای شما مفید باشد:

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

همچنین می‌توانید نگاهی به نحوه پیاده‌سازی آن در [spring-starter](https://github.com/vendelieu/telegram-bot/blob/1584d40f9a94a8c31bba9e7614c0070155630a52/spring-ktgram-starter/src/jvmMain/kotlin/eu/vendeli/spring/starter/TelegramAutoConfiguration.kt#L53) بیندازید.

---