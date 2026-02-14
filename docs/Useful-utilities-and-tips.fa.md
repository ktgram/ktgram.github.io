---
---
title: ابزارهای مفید و نکات
---


### کار با ProcessedUpdate

[`ProcessedUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processed-update/index.html) یک کلاس جنریک برای آپدیت‌ها است که بسته به داده اصلی، می‌تواند در انواع مختلفی ارائه شود ([`MessageUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-message-update/index.html)، [`CallbackQueryUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-callback-query-update/index.html) و غیره.)

بنابراین می‌توانید نوع داده دریافتی را بررسی کنید و با smartcasts داده‌های خاصی را بیشتر دستکاری کنید، به عنوان مثال:

```kotlin
// ...
if (update !is MessageUpdate) {
    message { "Only messages are allowed" }.send(user, bot)
    return
}
// در ادامه، ProcessedUpdate به عنوان MessageUpdate درک می‌شود.
```

همچنین یک اینترفیس [`UserReference`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-user-reference/index.html) درون آن وجود دارد که به شما امکان می‌دهد تعیین کنید آیا یک مرجع کاربری درون آن وجود دارد، مورد استفاده:

```kotlin
val user = if(update is UserReference) update.user else null

```

اگر لازم باشد، همیشه آپدیت اصلی [`update`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types/-update/index.html) در پارامتر update وجود دارد.


### تزریق وابستگی‌ها

کتابخانه از یک مکانیسم ساده برای مقداردهی کلاس‌ها استفاده می‌کند که روش‌های پردازش آپدیت شما با annotation‌های ارائه شده برچسب‌گذاری شده‌اند.

[`ClassManagerImpl`](https://github.com/vendelieu/telegram-bot/blob/master/telegram-bot/src/commonMain/kotlin/eu/vendeli/tgbot/implementations/ClassManagerImpl.kt) به طور پیش‌فرض برای فراخوانی روش‌های برچسب‌گذاری شده استفاده می‌شود.

اما اگر می‌خواهید از کتابخانه‌های دیگری برای این منظور استفاده کنید، می‌توانید اینترفیس [`ClassManager`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-manager/index.html) را مجدداً تعریف کنید، <br/>با استفاده از مکانیسم مورد نظر خود و هنگام مقداردهی ربات آن را ارسال کنید.

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.controllers") {
        classManager = ClassManagerImpl()
    }

    bot.handleUpdates()
}
```

### فیلتر کردن آپدیت‌ها

اگر شرایط پیچیده‌ای ندارید، می‌توانید به سادگی برخی آپدیت‌ها را برای پردازش فیلتر کنید:

```kotlin
// تابعی که شرط فیلتر کردن آپدیت‌ها در آن تعریف شده است
fun filteringFun(update: Update): Boolean = update.message?.text.isNullOrBlank()

fun main() = runBlocking {
  val bot = TelegramBot("BOT_TOKEN")

  // تنظیم جریان پردازشی خاص‌تر برای آپدیت‌ها
  bot.update.setListener {
    if(filteringFun(it)) return@setListener

    // پس از اینکه لیسنر از حوزه خارج شده و قبل از رسیدن به تابع handler، فیلتر کرده است.
    // در واقع می‌توانید حتی شرط if را مستقیماً در آنجا با return@setListener بنویسید یا فیلتر کردن را به کلاس جداگانه گسترش دهید.

    handle(it) // یا روش دستی مدیریت با بلوک
  }
}
```

برای شامل کردن فیلتر کردن در فرآیند تطبیق یا حذف دستورات، به guardها یا `@CommonHandler` نگاه کنید.

### گزینه‌هایی برای تعمیم دادن روش‌های مختلف

اگر باید پارامترهای اختیاری یکسان را اغلب اعمال کنید، می‌توانید یک تابع مشابه بنویسید که برای شما مناسب است و کد boilerplate را سبک کنید :)

برخی خواص رایج به [اینترفیس‌های مختلف](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.options/-options/index.html) جدا شده‌اند.

```kotlin
@Suppress("NOTHING_TO_INLINE")
inline fun <T, R, O> T.markdownMode(crossinline block: O.() -> Unit = {}): T
        where               T : TgAction<R>,
                            T : OptionsFeature<T, O>,
                            O : Options,
                            O : OptionsParseMode =
    options {
        parseMode = ParseMode.Markdown
        block()
    }


// ... و در کد شما

message { "test" }.markdownMode().send(to, via)

```