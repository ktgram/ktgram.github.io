---
---
title: Activites And Processors
---

### 介绍

在这个库的术语中，`Activity` 是以下实体的抽象实体：
`@CommandHandler`、`@InputHandler`、`@UnprocessedHandler` 和 `@CommonHandler`。

另请参阅 [handlers 文章](Handlers.md)。

### 收集活动

活动在编译时收集和准备所有上下文（通过功能 DSL 定义的除外）。

如果你想限制搜索包的范围，你可以向插件传递参数：

```gradle
ktGram {
    packages = listOf("com.example.mybot")
}
```

或者不通过插件通过 ksp：

```gradle
ksp {
    arg("package", "com.example.mybot")
}
```

注意：在这种情况下，为了正确处理收集的操作，你还必须在实例本身中指定包。

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.mybot")

    bot.handleUpdates()
    // 启动长轮询监听器
}
```

此选项是为了能够运行多个 bot 实例：

```gradle
ktGram {
    packages = listOf("com.example.mybot", "com.example.mybot2")
}
```

或者如果你不使用插件来指定不同的包，你需要用 `;` 分隔符指定它们：

```gradle
ksp {
    arg("package", "com.example.mybot;com.example.mybot2")
}
```

### 处理

#### Webhooks

在控制器（或处理 `webhook` 的其他位置），你可以调用：
[`bot.update.parseAndHandle(webhookString)`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.core/-tg-update-handler/index.html#706360827%2FFunctions%2F-880831646)

#### 长轮询

调用：`bot.handleUpdates()` 或通过 `bot.update.setListener { handle(it) }`


### 另请参阅

* [更新解析](Update-parsing.md)
* [Activity 调用](Activity-invocation.md)
* [Actions](Actions.md)

---