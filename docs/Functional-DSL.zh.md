---
title: 功能性 DSL
---

### 到 ~~无穷~~ 功能处理及更远的地方！
尽管与机器人工作的基本机制涉及使用注解，但这并不妨碍使用功能性更新处理。

此外，机器人的接口灵活性还允许您将这两种模式结合起来。

### 功能处理 DSL

在大多数功能处理方法中，支持的 [`Update`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types/-update/index.html) 类型有所不同，简单来说，您可以在特定类型的数据上设置监听器。

举个例子：

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

    bot.handleUpdates() {
        onChosenInlineResult {
            println("获得结果 ${update.chosenInlineResult.resultId} 来自 ${update.user}")
        }
    }
}
```

### 命令和输入

也可以处理 `commands` 和 `inputs`。

示例：

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN")

    bot.handleUpdates() {
            // 常规命令
        onCommand("/start") {
            message { "你好" }.send(user, bot)
        }
        onCommand("""(red|green|blue)""".toRegex()) {
            message { "你输入了 ${update.text} 颜色" }.send(user, bot)
        }
    }
}
```

在 `onCommand` 函数的上下文中，参数以 `Map<String, String>` 格式传递，<br/>
根据配置适当解析。

#### 输入
也可以通过熟悉的 [`bot.inputListener`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot/-telegram-bot/input-listener.html) 机制使用输入。

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN")

    bot.handleUpdates() {
            // 常规命令
        onCommand("/start") {
            message { "你好，你叫什么名字？" }.send(user, bot)
            bot.inputListener[user] = "testInput"
        }
        onInput("testInput") {
            message { "嘿，很高兴见到你，${update.text}" }.send(user, bot)
        }
    }
}
```
您还可以使用输入链：
```kotlin
inputChain("conversation") {
     message { "很高兴见到你，${update.text}" }.send(user, bot)
     message { "你最喜欢的食物是什么？" }.send(user, bot)
}.breakIf({ update.text == "peanut butter" }) { // 链中断条件
     message { "哦，太糟糕了，我对它过敏。" }.send(user, bot)
     // 匹配时将应用的操作
}.andThen {
     // 如果中断条件不匹配，则下一个输入点
}
```

您可以在 [`FunctionalHandlingDsl`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.core/-functional-handling-dsl/index.html) 类文档中阅读更多关于方法的信息。

> [!CAUTION]
> 请注意，如果同时使用两种处理器（功能性、注解），输入可能不会如预期那样工作（每个处理器在处理后会清除输入，如果您想要其他行为，请更改 inputAutoRemoval 配置）。

### 另请参见

* [动作](Actions.md)
* [有用的工具和提示](Useful-utilities-and-tips.md)