---
---
title: Useful Utilities And Tips
---


### Operating with ProcessedUpdate

[`ProcessedUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processed-update/index.html) یک کلاس جنریک برای آپدیت‌ها است که بسته به دادهٔ اصلی می‌تواند در انواع مختلفی ارائه شود ([`MessageUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-message-update/index.html)، [`CallbackQueryUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-callback-query-update/index.html) و غیره).

بنابراین می‌توانید نوع دادهٔ ورودی را بررسی کنید و دادهٔ خاصی را با smartcast‌ها دستکاری کنید، برای مثال:

```kotlin
// ...
if (update !is MessageUpdate) {
    message { "Only messages are allowed" }.send(user, bot)
    return
}
// Further on, ProcessedUpdate will be perceived as MessageUpdate.
```

همچنین یک رابط [`UserReference`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-user-reference/index.html) وجود دارد که به شما امکان می‌دهد تعیین کنید آیا یک مرجع کاربر داخل آن وجود دارد یا نه؛ نمونهٔ استفاده:

```kotlin
val user = if(update is UserReference) update.user else null

```

در صورت نیاز همیشه می‌توانید به [`update`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types/-update/index.html) اصلی در پارامتر آپدیت دسترسی داشته باشید.


### Dependency injection

کتابخانه از یک مکانیزم ساده برای مقداردهی اولیهٔ کلاس‌ها استفاده می‌کند که روش‌های پردازش آپدیت شما با انوتیشن‌های ارائه‌شده علامت‌گذاری می‌شوند.

[`ClassManagerImpl`](https://github.com/vendelieu/telegram-bot/blob/master/telegram-bot/src/commonMain/kotlin/eu/vendeli/tgbot/implementations/ClassManagerImpl.kt) به‌صورت پیش‌فرض برای فراخوانی متدهای علامت‌گذاری‌شده استفاده می‌شود.

اما اگر می‌خواهید از کتابخانه‌های دیگری برای این کار استفاده کنید می‌توانید رابط [`ClassManager`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-manager/index.html) را بازتعریف کنید، <br/>با استفاده از مکانیزم دلخواه خود و هنگام مقداردهی اولیهٔ بات آن را پاس دهید.

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.controllers") {
        classManager = ClassManagerImpl()
    }

    bot.handleUpdates()
}
```

### Filtering updates

اگر شرایط پیچیده‌ای ندارید می‌توانید به‌سادگی برخی آپدیت‌ها را برای پردازش فیلتر کنید:

```kotlin
// function where updates filtering condition defined
fun filteringFun(update: Update): Boolean = update.message?.text.isNullOrBlank()

fun main() = runBlocking {
  val bot = TelegramBot("BOT_TOKEN")

  // setting more specific processing flow for updates
  bot.update.setListener {
    if(filteringFun(it)) return@setListener

    // so simply, if the listener left the scope before reaching the handler function, that it is filtering.
    // actually you can even write directly if-condition there with return@setListener or extend filtering to separate class.

    handle(it) // or manual handling way with block
  }
}
```

برای گنجاندن فیلترینگ در تطبیق دستورات یا حذف فرآیند، به نگهدارنده‌ها یا `@CommonHandler` نگاهی بیندازید.

### Generalize options for different methods

اگر مجبورید پارامترهای اختیاری یکسان را بارها اعمال کنید، می‌توانید تابع مشابهی بنویسید که مناسب شما باشد و کدهای تکراری را سبک کنید :)

برخی ویژگی‌های مشترک به [رابط‌های مختلف](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.options/-options/index.html) تقسیم شده‌اند.

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


// ... and in your code

message { "test" }.markdownMode().send(to, via)

```


---