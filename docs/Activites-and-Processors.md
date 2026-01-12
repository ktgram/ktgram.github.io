---
title: Activites And Processors
---

### Introduction

`Activity` in the terms of this library is the abstract entity that is a generalization of entities such as `@CommandHandler`, `@InputHandler`, `@UnprocessedHandler`, and `@CommonHandler`.

Also take a look at [handlers article](Handlers.md).

### Collecting activities

Activities are collected and prepared all context in compile time (except for those defined through functional dsl).

If you want to limit the area in which the package will be searched, you can pass a parameter to plugin:

```gradle
ktGram {
    packages = listOf("com.example.mybot")
}
```

or without plugin through ksp:

```gradle
ksp {
    arg("package", "com.example.mybot")
}
```

note in such a case, in order for the collected actions to be processed correctly, you must also specify the package in the instance itself.

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.mybot")

    bot.handleUpdates()
    // start long-polling listener
}
```

this option is added to be able to run multiple bot instances:

```gradle
ktGram {
    packages = listOf("com.example.mybot", "com.example.mybot2")
}
```


or if you're not using plugin to specify different packages you need to specify them with `;` separator:

```gradle
ksp {
    arg("package", "com.example.mybot;com.example.mybot2")
}
```

### Processing

#### Webhooks

In your controller (or another place where the `webhook` is processed), you call: [`bot.update.parseAndHandle(webhookString)`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.core/-tg-update-handler/index.html#706360827%2FFunctions%2F-880831646)

#### Long polling

Call: `bot.handleUpdates()` or through `bot.update.setListener { handle(it) }`


### See also

* [Update parsing](Update-parsing.md)
* [Activity invocation](Activity-invocation.md)
* [Actions](Actions.md)
