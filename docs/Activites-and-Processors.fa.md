---
---
title: فعالیت‌ها و پردازش‌گرها
---

### مقدمه

`Activity` در اصطلاح این کتابخانه موجودیت انتزاعی است که تعمیمی از موجودیت‌هایی مانند `@CommandHandler`، `@InputHandler`، `@UnprocessedHandler` و `@CommonHandler` می‌باشد.

همچنین به مقاله [handlers](Handlers.md) هم نگاهی بیندازید.

### جمع‌آوری فعالیت‌ها

فعالیت‌ها در زمان کامپایل جمع‌آوری و تمام متن‌بست برای آن‌ها آماده می‌شود (به جز آن‌هایی که از طریق DSL توابعی تعریف شده‌اند).

اگر می‌خواهید حوزه‌ای را محدود کنید که بسته در آن جستجو شود، می‌توانید پارامتری به پلاگین ارسال کنید:

```gradle
ktGram {
    packages = listOf("com.example.mybot")
}
```

یا بدون پلاگین از طریق KSP:

```gradle
ksp {
    arg("package", "com.example.mybot")
}
```

توجه داشته باشید که در چنین حالتی، برای اینکه اقدامات جمع‌آوری شده به درستی پردازش شوند، باید بسته را در خود نمونه هم مشخص کنید.

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.mybot")

    bot.handleUpdates()
    // شروع لیست‌گیری طولانی
}
```

این گزینه برای این اضافه شده تا بتوانید چند نمونه ربات را اجرا کنید:

```gradle
ktGram {
    packages = listOf("com.example.mybot", "com.example.mybot2")
}
```

یا اگر از پلاگین استفاده نمی‌کنید و بسته‌های متفاوتی را مشخص می‌کنید، باید آن‌ها را با جداکننده `;` مشخص کنید:

```gradle
ksp {
    arg("package", "com.example.mybot;com.example.mybot2")
}
```

### پردازش

#### Webhooks

در کنترلر خود (یا مکانی دیگری که `webhook` در آن پردازش می‌شود)، فراخوانی کنید: [`bot.update.parseAndHandle(webhookString)`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.core/-tg-update-handler/index.html#706360827%2FFunctions%2F-880831646)

#### Long polling

فراخوانی کنید: `bot.handleUpdates()` یا از طریق `bot.update.setListener { handle(it) }`


### همچنین ببینید

* [پردازش به‌روزرسانی](Update-parsing.md)
* [فراخوانی فعالیت](Activity-invocation.md)
* [اقدامات](Actions.md)