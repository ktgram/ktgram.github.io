---
---
title: Functional Dsl
---

### 迈向 ~~无限~~ 函数式 dsl！

机器人同时支持基于注解和函数式 dsl 的设置上下文。你可以结合使用这两种方法。

### 函数式 DSL

函数式 DSL 是定义机器人上下文的另一种方式。

示例：

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

    bot.setFunctionality {
        onChosenInlineResult {
            println("got a result ${update.chosenInlineResult.resultId} from ${update.user}")
        }
    }
}
```

### 命令和输入

你可以使用函数式 DSL 处理 `命令` 和 `输入`。

#### 命令

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

    bot.setFunctionality {
        // 常规命令
        onCommand("/start") {
            message { "Hello" }.send(user, bot)
        }
        
        // 基于正则表达式的命令匹配
        onCommand("""(red|green|blue)""".toRegex()) {
            message { "you typed ${update.text} color" }.send(user, bot)
        }
    }
}
```

在 `onCommand` 中，解析的参数可用作 `Map<String, String>`，具体取决于你的配置。

#### 输入

你可以通过 [`bot.inputListener`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot/-telegram-bot/input-listener.html) 使用输入。

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

    bot.setFunctionality {
        onCommand("/start") {
            message { "Hello, what's your name?" }.send(user, bot)
            bot.inputListener[user] = "testInput"
        }
        
        onInput("testInput") {
            message { "Hey, nice to meet you, ${update.text}" }.send(user, bot)
        }
    }
}
```

#### 输入链

对于多步骤输入流程，使用 `inputChain`：

```kotlin
bot.setFunctionality {
    inputChain("conversation") {
        message { "Nice to meet you, ${update.text}" }.send(user, bot)
        message { "What is your favorite food?" }.send(user, bot)
    }.breakIf({ update.text == "peanut butter" }) { // 链式中断条件
        message { "Oh, too bad, I'm allergic to it." }.send(user, bot)
        // 当条件匹配时应用的操作
    }.andThen {
        // 如果中断条件不匹配，则进入下一个输入点
        message { "Great choice!" }.send(user, bot)
    }
}
```

链式结构会自动进入下一步，除非遇到中断条件。如果中断条件匹配且 `repeat` 为 `true`（默认），用户会停留在当前步骤。

#### 更新类型处理器

直接处理特定更新类型：

```kotlin
bot.setFunctionality {
    onUpdate(UpdateType.MESSAGE, UpdateType.CALLBACK_QUERY) {
        // 处理消息和回调查询更新
        println("Received update: ${update.type}")
    }
}
```

#### 通用匹配器

使用 `common` 匹配文本内容（不仅仅是命令）：

```kotlin
bot.setFunctionality {
    // 字符串匹配
    common("hello") {
        message { "Hi there!" }.send(user, bot)
    }
    
    // 正则表达式匹配
    common("""\d+""".toRegex()) {
        message { "You sent a number!" }.send(user, bot)
    }
}
```

#### 回退处理器

处理未被任何处理器处理的更新：

```kotlin
bot.setFunctionality {
    whenNotHandled {
        message { "I didn't understand that." }.send(user, bot)
    }
}
```

### 高级配置

#### 速率限制

对任何处理器应用速率限制：

```kotlin
bot.setFunctionality {
    onCommand("/expensive", rateLimits = RateLimits(5, 60)) {
        // 此命令每 60 秒只能调用 5 次
        message { "Processing..." }.send(user, bot)
    }
}
```

#### 守卫

使用守卫添加自定义验证逻辑：

```kotlin
bot.setFunctionality {
    onCommand("/admin", guard = AdminGuard::class) {
        message { "Admin command executed" }.send(user, bot)
    }
}
```

#### 参数解析

自定义命令参数的解析方式：

```kotlin
bot.setFunctionality {
    onCommand("/custom", argParser = CustomArgParser::class) {
        // 参数将使用 CustomArgParser 进行解析
        message { "Parameters: $parameters" }.send(user, bot)
    }
}
```

### 结合函数式和基于注解的设置

你可以在同一个机器人中使用这两种方法：

```kotlin
// 基于注解的处理器
@CommandHandler(["/register"])
suspend fun register(ctx: CommandContext) {
    message { "Registration started" }.send(ctx.user, ctx.bot)
}

// 函数式处理器
bot.setFunctionality {
    onCommand("/help") {
        message { "Available commands: /register, /help" }.send(user, bot)
    }
}
```

两种处理器都注册在同一个 `ActivityRegistry` 中，并无缝协作。

### 另请参阅

* [Action](Actions.md)
* [Useful utilities](Useful-utilities-and-tips.md)
---