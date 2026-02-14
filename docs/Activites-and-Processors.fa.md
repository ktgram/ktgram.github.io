---
---
title: فعالیت‌ها و پردازنده‌ها
---

### مقدمه

`Activity` در اصطلاح این کتابخانه موجودیت انتزاعی است که تعمیمی از موجودیت‌هایی مانند `@CommandHandler`، `@InputHandler`، `@UnprocessedHandler` و `@CommonHandler` است.

همچنین مقاله [handlers](Handlers.md) را نیز بررسی کنید.

### جمع‌آوری فعالیت‌ها

فعالیت‌ها در زمان کامپایل جمع‌آوری و کلیه متن در آن‌ها آماده می‌شوند (به جز آن‌هایی که از طریق functional dsl تعریف شده‌اند).

اگر می‌خواهید منطقه‌ای را که بسته در آن جستجو می‌شود محدود کنید، می‌توانید پارامتری را به پلاگین ارسال کنید:

```gradle
ktGram {
    packages = listOf("com.example.mybot")
}
```

یا بدون پلاگین از طریق ksp:

```gradle
ksp {
    arg("package", "com.example.mybot")
}
```

توجه داشته باشید که در چنین حالتی، برای اینکه اقدامات جمع‌آوری شده به درستی پردازش شوند، باید بسته را در خود نمونه نیز مشخص کنید.

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.mybot")

    bot.handleUpdates()
    // شروع گوش‌دهنده long-polling
}
```

این گزینه برای این اضافه شده است که بتوان نمونه‌های چندگانه بات را اجرا کرد:

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

در کنترلر خود (یا مکانی دیگری که `webhook` در آن پردازش می‌شود)، فراخوانی می‌کنید: [`bot.update.parseAndHandle(webhookString)`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.core/-tg-update-handler/index.html#706360827%2FFunctions%2F-880831646)

#### Long polling

فراخوانی کنید: `bot.handleUpdates()` یا از طریق `bot.update.setListener { handle(it) }`


### همچنین ببینید

* [پردازش آپدیت](Update-parsing.md)
* [فراخوانی فعالیت](Activity-invocation.md)
* [اقدامات](Actions.md)