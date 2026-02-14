---
---
title: Activites And Processors
---

### 介绍

在本库的术语中，`Activity` 是抽象实体，是对诸如 `@CommandHandler`、`@InputHandler`、`@UnprocessedHandler` 和 `@CommonHandler` 等实体的泛化。

另请参阅[处理器文章](Handlers.md)。

### 收集 activities

Activities 在编译时被收集和准备所有上下文（除了通过函数式 DSL 定义的那些）。

如果你想限制搜索包的范围，可以将参数传递给插件：

```gradle
ktGram {
    packages = listOf("com.example.mybot")
}
```

或通过 ksp 而不使用插件：

```gradle
ksp {
    arg("package", "com.example.mybot")
}
```

注意，在这种情况下，要正确处理收集的操作，你还必须在实例本身中指定包。

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.mybot")

    bot.handleUpdates()
    // 启动长轮询监听器
}
```

添加此选项是为了能够运行多个 bot 实例：

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

在你的控制器（或处理 `webhook` 的其他地方），调用：[`bot.update.parseAndHandle(webhookString)`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.core/-tg-update-handler/index.html#706360827%2FFunctions%2F-880831646)

#### 长轮询

调用：`bot.handleUpdates()` 或通过 `bot.update.setListener { handle(it) }`


### 另请参阅

* [更新解析](Update-parsing.md)
* [Activity 调用](Activity-invocation.md)
* [Actions](Actions.md)

---