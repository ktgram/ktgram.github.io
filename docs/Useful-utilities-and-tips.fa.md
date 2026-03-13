---
---
title: ابزارهای و ترفندهای مفید
---


### عمل با ProcessedUpdate

کلاس [`ProcessedUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processed-update/index.html) یک کلاس عمومی برای آپدیت‌ها است که بسته به داده اصلی، می‌تواند در انواع مختلفی ارائه شود ([`MessageUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-message-update/index.html)، [`CallbackQueryUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-callback-query-update/index.html) و غیره)

بنابراین می‌توانید نوع داده ورودی را بررسی کنید و داده‌های خاص را با smartcasts اداره کنید، به عنوان مثال:

```kotlin
// ...
if (update !is MessageUpdate) {
    message { "Only messages are allowed" }.send(user, bot)
    return
}
// در ادامه، ProcessedUpdate به عنوان MessageUpdate در نظر گرفته می‌شود.
```

همچنین یک اینترفیس [`UserReference`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-user-reference/index.html) درونی وجود دارد که به شما اجازه می‌دهد مشخص کنید آیا یک مرجع کاربری درونی وجود دارد یا خیر، مورد استفاده مثال:

```kotlin
val user = if(update is UserReference) update.user else null

```

در صورت نیاز، همیشه آپدیت اصلی [`update`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types/-update/index.html) در پارامتر آپدیت وجود دارد.


### تزریق وابستگی‌ها

کتابخانه از یک مکانیزم ساده برای مقداردهی کلاس‌ها استفاده می‌کند که در آن متدهای پردازش آپدیت شما با annotation‌های ارائه شده برچسب‌گذاری می‌شوند.

[`ClassManagerImpl`](https://github.com/vendelieu/telegram-bot/blob/master/telegram-bot/src/commonMain/kotlin/eu/vendeli/tgbot/implementations/ClassManagerImpl.kt) به طور پیش‌فرض برای فراخوانی متدهای annotatd استفاده می‌شود.

اما اگر می‌خواهید از کتابخانه‌های دیگری برای این منظور استفاده کنید، می‌توانید اینترفیس [`ClassManager`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-manager/index.html) را دوباره تعریف کنید، <br/>با استفاده از مکانیزم مورد نظر خود و آن را هنگام مقداردهی اولیه ربات ارسال کنید.

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.controllers") {
        classManager = ClassManagerImpl()
    }

    bot.handleUpdates()
}
```

### فیلتر کردن آپدیت‌ها

اگر شرایط پیچیده‌ای ندارید، می‌توانید ساده‌ترین روش فیلتر کردن برخی آپدیت‌ها برای پردازش باشد:

```kotlin
// تابعی که شرط فیلتر کردن آپدیت‌ها تعریف شده است
fun filteringFun(update: Update): Boolean = update.message?.text.isNullOrBlank()

fun main() = runBlocking {
  val bot = TelegramBot("BOT_TOKEN")

  // تنظیم جریان پردازش دقیق‌تر برای آپدیت‌ها
  bot.update.setListener {
    if(filteringFun(it)) return@setListener

    // بنابراین ساده، اگر listener قبل از رسیدن به متد handler از حدود خارج شود، این فیلتر کردن است.
    // در واقع می‌توانید حتی یک if-condition مستقیم در آنجا با return@setListener بنویسید یا فیلتر کردن را به یک کلاس جداگانه توسعه دهید.

    handle(it) // یا روش دستی پردازش با بلوک
  }
}
```

برای شامل کردن فیلتر کردن در فرآیند تطبیق یا استثنا دستورات، به guardها یا `@CommonHandler` نگاه کنید.

### گسترش گزینه‌ها برای متدهای مختلف

اگر باید پارامترهای اختیاری یکسان را اغلب اعمال کنید، می‌توانید یک تابع مشابه که برای شما مناسب است بنویسید و کد boilerplate را سبک‌تر کنید :)

بعضی خصوصیات رایج به [اینترفیس‌های مختلف](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.options/-options/index.html) تفکیک شده‌اند.

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