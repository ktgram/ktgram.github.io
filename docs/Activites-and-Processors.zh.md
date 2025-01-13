---
title: 活动与处理器
---

### 介绍

在本库的术语中，`Activity` 是一个抽象实体，作为一个概念，代表了 `@CommandHandler`、`@InputHandler`、`@UnprocessedHandler` 和 `@CommonHandler` 等实体的概括。

还可以查看 [处理器文章](Handlers.md)。

### 收集活动

活动在编译时被收集和准备所有上下文。

如果您想限制搜索包的区域，可以向插件传递一个参数：

```gradle
ktGram {
    packages = listOf("com.example.mybot")
}
```

或者通过 ksp 而不使用插件：

```gradle
ksp {
    arg("package", "com.example.mybot")
}
```

请注意，在这种情况下，为了使收集的操作能够正确处理，您还必须在实例本身中指定包。

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.mybot")

    bot.handleUpdates()
    // 启动长轮询监听器
}
```

此选项的添加是为了能够运行多个机器人实例：

```gradle
ktGram {
    packages = listOf("com.example.mybot", "com.example.mybot2")
}
```


或者如果您不使用插件来指定不同的包，则需要使用 `;` 分隔符指定它们：

```gradle
ksp {
    arg("package", "com.example.mybot;com.example.mybot2")
}
```

### 处理器

您有两种类型的流处理更新：

### 功能性

您通过 lambda 参数函数 [`bot.handleUpdates() {}`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot/-telegram-bot/handle-updates.html) 或通过 [`bot.update.setListener`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.core/-tg-update-handler/set-listener.html) 建立处理行为。

您可以在 [相关文章](Functional-DSL.md) 中阅读更多关于功能性处理的信息。

请参见 [`FunctionalHandlingDsl`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.core/-functional-handling-dsl/index.html)。

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN")

    bot.handleUpdates {
         onMessage {
             message { update.text }.send(update.user, bot)
         }
   }
}
```

### 注解

注解取决于所选的处理模式：

#### Webhooks

在您的控制器（或处理 `webhook` 的其他地方），您调用: [`bot.update.parseAndHandle(webhookString)`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.core/-tg-update-handler/index.html#706360827%2FFunctions%2F-880831646)

默认情况下，它将使用注解处理器，但如果您想要一些自定义行为，也可以通过 [`setBehaviour`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.core/-tg-update-handler/set-behaviour.html) 设置（在控制器本身中不必每次都分配行为，只需在配置期间分配一次即可）：

```kotlin
bot.update.setBehaviour {
   // ...其他操作
   update(it) // 运行注解处理器
}
```

#### 长轮询

调用: `bot.handleUpdates()` 或通过 `bot.update.setListener { handle(it) }`

### 两者

此外，如果需要，这两种方法可以结合使用相同的 `setListener {}`，在这种方法中，即使相同的命令也可以被处理两次，处理将按照调用的顺序进行。

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "eu.vendeli.samples.controller")

    bot.update.setListener {
        handle(it) // 在这里我们发送更新进行注解处理。
        handle(it) { // 在这里我们随后进行功能性处理。
            onMessage {
                message { update.text }.send(update.user, bot)
            }
        }
}
```
您可以在 [投票示例](https://github.com/vendelieu/telegram-bot_template/blob/poll/src/main/kotlin/com/example/poll/PollApplication.kt) 中看到结合使用的示例。

或者在 webhook 处理时，您可以像之前描述的那样通过 `setBehaviour` 设置。


###  另请参见

* [更新解析](Update-parsing.md)
* [活动调用](Activity-invocation.md)
* [动作](Actions.md)