---
---
title: Activites And Processors
---

### Introduction

`Activity` 在本库中指的是一个抽象实体，它是对 `@CommandHandler`、`@InputHandler`、`@UnprocessedHandler`、`@CommonHandler`、`@UpdateHandler` 和 `@WizardHandler` 等实体的概括。

另请参阅 [handlers article](Handlers.md)。

### Collecting activities

Activities 在 **编译时** 由 **ktnip** KSP 处理器发现并进行连接。唯一例外是 [Functional DSL](Handlers#functional-dsl.md) —— 通过 `bot.setFunctionality { ... }` 定义的 handlers 在运行时注册。

如果你想限制搜索的包范围，可以向插件传递参数：

```gradle
ktGram {
    packages = listOf("com.example.mybot")
}
```

或者在不使用插件的情况下通过 ksp：

```gradle
ksp {
    arg("package", "com.example.mybot")
}
```

注意，在这种情况下，为了让收集的 actions 能够正确处理，你还必须在实例本身中指定包名。

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.mybot")

    bot.handleUpdates()
    // start long-polling listener
}
```

此选项的加入是为了能够运行多个 bot 实例：

```gradle
ktGram {
    packages = listOf("com.example.mybot", "com.example.mybot2")
}
```


如果不使用插件而需要指定不同的包，则需要使用 `;` 分隔符：

```gradle
ksp {
    arg("package", "com.example.mybot;com.example.mybot2")
}
```

### Processing

#### Webhooks

在你的控制器（或处理 `webhook` 的其他位置），调用：[`bot.update.parseAndHandle(webhookString)`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.core/-tg-update-handler/index.html#706360827%2FFunctions%2F-880831646)

#### Long polling

调用：`bot.handleUpdates()` 或通过 `bot.update.setListener { handle(it) }`


### See also

* [Update parsing](Update-parsing.md)
* [Activity invocation](Activity-invocation.md)
* [Actions](Actions.md)

---