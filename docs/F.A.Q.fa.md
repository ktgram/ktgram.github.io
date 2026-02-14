---
---
عنوان: سؤالات متداول
---

### استثنا `AbstractMethodError`

اگر در زمان شروع برنامه خود با این استثنا مواجه شدید:

```kotlin
Exception in thread "DefaultDispatcher-worker-1" java.lang.AbstractMethodError: 'kotlinx.serialization.KSerializer[] kotlinx.serialization.internal.GeneratedSerializer.typeParametersSerializers()'
	at eu.vendeli.tgbot.types.options.GetUpdatesOptions$$serializer.typeParametersSerializers(GetUpdatesOptions.kt:6)
```

این اتفاق به دلیل استفاده کتابخانه سازی قدیمی serialization توسط سیستم ساخت شما رخ می‌دهد که مکانیزم داخلی آن متفاوت است.
برای حل این مشکل باید از نسخه‌ای جدیدتر استفاده کنید، برای مثال با اضافه کردن این کد به buildscript:

```kotlin
configurations.all {
    resolutionStrategy.eachDependency {
        val serdeVer = "x.x.x" // باید >= 1.8.0 باشد
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

(اگر این موضوع در log چابک توضیح داده شده بود، من هرگز ارتقا نمی‌دادم چون چنین تعداد زیادی گزارش در مورد این مشکل دریافت می‌کنم)

### چگونه پاسخ متد را دریافت کنم؟

برای دریافت پاسخ و قابلیت عمل بر روی آن، باید در انتهای متد از `sendReturning` استفاده کنید به جای `send`.

در این حالت کلاس `Response` برگردانده می‌شود که شامل پاسخ، موفق یا ناموفق است و شما باید یا ناتوانی را مدیریت کنید یا فقط `getOrNull()` را صدا بزنید.

بخشی در مورد: [پردازش پاسخ‌ها](https://github.com/vendelieu/telegram-bot#processing-responses) وجود دارد.

### من هنگام استفاده از `spring-boot-devtools` خطا دریافت می‌کنم

این اتفاق به این دلیل رخ می‌دهد که `spring-boot-devtools` خودش `classloader` دارد و متدها را پیدا نمی‌کند.

باید به `resources/META-INF/spring-devtools.properties` اضافه کنید:

```properties
restart.include.generated=/eu.vendeli
```

### چگونه موتور ktor را تغییر دهم

اگر می‌خواهید موتور مورد استفاده توسط کلاینت را تغییر دهید، می‌توانید به سادگی [پارامتر](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/ktor-jvm-engine.html) را در [تنظیمات پلاگین](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/index.html) تغییر دهید.

### چگونه از تهیه‌کننده logging مورد علاقه‌ام استفاده کنم

کتابخانه از `slf4j-api` استفاده می‌کند و برای استفاده از تهیه‌کننده باید آن را به وابستگی‌ها اضافه کنید.

پلاگین کتابخانه به طور خودکار استفاده از تهیه‌کننده را تشخیص می‌دهد، اگر تهیه‌کننده وجود نداشت، `logback` به طور پیش‌فرض استفاده می‌شود.

### گرفتن استثنا‌های شبکه درون handler long-polling

برای مثال اگر اتصال ناپایداری دارید و نیاز به گرفتن خطا به دلیل آن دارید، شاید این رویکرد به شما کمک کند:

```kotlin
fun main() {
    val bot = TelegramBot("TOKEN")

    try {
        bot.handleUpdates()
    } catch (e: Exception) {
        // مدیریت در صورت نیاز
        
        bot.update.stopListener()
        bot.handleUpdates()
    }
}
```

همچنین می‌توانید نگاهی بیندازید که چگونه در [spring-starter](https://github.com/vendelieu/telegram-bot/blob/1584d40f9a94a8c31bba9e7614c0070155630a52/spring-ktgram-starter/src/jvmMain/kotlin/eu/vendeli/spring/starter/TelegramAutoConfiguration.kt#L53) انجام شده است.

---