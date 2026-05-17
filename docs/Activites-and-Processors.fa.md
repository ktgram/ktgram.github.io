---
---
title: Activites And Processors
---

### Introduction

`Activity` در واژگان این کتابخانه موجودیت انتزاعی است که تعمیمی از موجودیت‌هایی مانند `@CommandHandler`، `@InputHandler`، `@UnprocessedHandler`، `@CommonHandler`، `@UpdateHandler` و `@WizardHandler` می‌باشد.

همچنین به مقالهٔ [handlers article](Handlers.md) نگاهی بیندازید.

### Collecting activities

فعالیت‌ها در **زمان کامپایل** توسط پردازشگر KSP **ktnip** کشف و به‌هم متصل می‌شوند. استثنای یکی تنها وجود دارد — هندلرهای تعریف‌شده از طریق `bot.setFunctionality { ... }` در زمان اجرا ثبت می‌گردند.

اگر می‌خواهید محدودهٔ جستجوی بسته را محدود کنید، می‌توانید به افزونه پارامتری بدهید:

```gradle
ktGram {
    packages = listOf("com.example.mybot")
}
```

یا بدون افزونه از طریق ksp:

```gradle
ksp {
    arg("package", "com.example.mybot")
}
```

توجه داشته باشید که در چنین حالتی، برای اینکه اقدامات جمع‌آوری‌شده به‌درستی پردازش شوند، باید بسته را در خود نمونه نیز مشخص کنید.

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.mybot")

    bot.handleUpdates()
    // start long-polling listener
}
```

این گزینه برای امکان اجرای چندین نمونهٔ بات اضافه شده است:

```gradle
ktGram {
    packages = listOf("com.example.mybot", "com.example.mybot2")
}
```


یا اگر از افزونه استفاده نمی‌کنید و می‌خواهید بسته‌های مختلف را مشخص کنید، باید آن‌ها را با جداکنندهٔ `;` بنویسید:

```gradle
ksp {
    arg("package", "com.example.mybot;com.example.mybot2")
}
```

### Processing

#### Webhooks

در کنترلر خود (یا هر مکان دیگری که `webhook` پردازش می‌شود)، فراخوانی می‌کنید: [`bot.update.parseAndHandle(webhookString)`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.core/-tg-update-handler/index.html#706360827%2FFunctions%2F-880831646)

#### Long polling

فراخوانی کنید: `bot.handleUpdates()` یا از طریق `bot.update.setListener { handle(it) }`


### See also

* [Update parsing](Update-parsing.md)
* [Activity invocation](Activity-invocation.md)
* [Actions](Actions.md)

---