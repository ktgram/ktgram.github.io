---
---
title: Handlers
---


### Variety of Handlers

在机器人开发中，尤其是涉及用户交互的系统中，如何高效地管理和处理指令与事件至关重要。

这些注解标记用于处理特定指令、输入或更新的函数，并提供诸如指令关键字、作用域和守卫等元数据。

### Annotations Overview

#### CommandHandler

`CommandHandler` 注解用于标记处理特定指令的函数。该注解包括定义指令关键字和作用域的属性。

-   **value**: 指定与指令关联的关键字。
-   **scope**: 确定指令检查所在的上下文或作用域。

```kotlin
@CommandHandler(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommandHandler.CallbackQuery

专用于处理回调查询的 `CommandHandler` 注解的特化版本。它包含与 `CommandHandler` 相似的属性，侧重于回调相关指令。

_它实际上等同于带有预设 `UpdateType.CALLBACK_QUERY` 作用域的 `@CommandHandler`_。

-   **value**: 指定与指令关联的关键字。
-   **autoAnswer**: 自动回复 `callbackQuery`（在处理前调用 `answerCallbackQuery`）。

```kotlin
@CommandHandler.CallbackQuery(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### CommonHandler

`CommonHandler` 注解用于相对于 `CommandHandler` 和 `InputHandler` 优先级较低的指令处理函数。它在源码层面使用，提供一种灵活的方式来定义通用指令处理器。

**需注意，优先级仅在 `@CommonHandler` 本身内部生效（即不影响其他处理器）。**

##### CommonHandler.Text

此注解对更新进行文本匹配。它包含用于定义匹配文本、过滤条件、优先级和作用域的属性。

-   **value**: 用于匹配传入更新的文本。
-   **filter**: 定义匹配过程中使用的条件类。
-   **priority**: 处理器的优先级，0 为最高优先级。
-   **scope**: 文本匹配检查的上下文或作用域。

```kotlin
@CommonHandler.Text(["text"], filter = isNewUserFilter::class, priority = 10)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommonHandler.Regex

类似于 `CommonHandler.Text`，此注解基于正则表达式匹配更新。它包含用于定义正则模式、选项、过滤条件、优先级和作用域的属性。

-   **value**: 用于匹配的正则模式。
-   **options**: 修改正则模式行为的选项。
-   **filter**: 定义匹配过程中使用的条件类。
-   **priority**: 处理器的优先级，0 为最高优先级。
-   **scope**: 正则匹配检查的上下文或作用域。

```kotlin
@CommonHandler.Regex("^\d+$", scope = [UpdateType.EDITED_MESSAGE])
suspend fun test(update: EditedMessageUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### InputHandler

`InputHandler` 注解标记处理特定输入事件的函数。它用于在运行时处理输入，并提供定义输入关键字和作用域的属性。

-   **value**: 指定与输入事件关联的关键字。

```kotlin
@InputHandler("text")
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UnprocessedHandler

`UnprocessedHandler` 注解用于标记处理其他处理器未处理的更新的函数。它确保未处理的更新得到适当管理，并且此处理器类型只能有一个处理点。

```kotlin
@UnprocessedHandler
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UpdateHandler

`UpdateHandler` 注解标记处理特定类型传入更新的函数。它提供了一种系统化分类和处理不同更新类型的方式。

-   **type**: 指定处理函数将处理的更新类型。
-   **messageKind** *(added in 9.5)*: 可选的 [`MessageKind`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-message-kind/index.html) 集合，用于将分派限制在检测到的类型匹配的携带消息的更新上。空（默认）表示匹配任何类型。

```kotlin
@UpdateHandler([UpdateType.PRE_CHECKOUT_QUERY])
suspend fun test(update: PreCheckoutQueryUpdate, user: User, bot: TelegramBot) {
    //...
}
```

##### Filtering by `MessageKind`

使用 `messageKind` 参数只响应特定子集的消息更新（照片、文本、服务事件等），而无需手动检查可空字段：

```kotlin
@UpdateHandler(type = [UpdateType.MESSAGE], messageKind = [MessageKind.PHOTO])
suspend fun onPhoto(update: MessageUpdate, bot: TelegramBot) {
    //...
}
```
### Handler Companion Annotations

还有一些可选的注解可与处理器一起使用，补充处理器本身的可选行为。

它们既可以放在应用了处理器的函数上，也可以放在类上；后者会自动应用到该类的所有处理器，但如果需要，也可以为某些函数单独指定行为。

即：应用的优先级为 `Function` > `Class`，函数优先级更高。

#### Rate Limiting

此外，还需说明注解中描述的速率限制机制。

你可以为每个用户设置通用限制：

```kotlin
// ...
val bot = TelegramBot("BOT_TOKEN") {
    rateLimiter { // general limits
        limits = RateLimits(period = 10000, rate = 5)
    }
}
```

###### Handler specific

可以使用 `RateLimits` 注解为特定操作定义限制，支持 `@CommandHandler`、`@CommandHandler.CallbackQuery`、`@InputHandler`、`@CommonHandler`。

```kotlin
@CommandHandler(["/start"])
@RateLimits(period = 1000L, rate = 1L)
suspend fun start(user: User, bot: TelegramBot) {
    // ...
}
```

#### Guard

你可以单独定义守卫以控制对处理器的访问，支持 `@CommandHandler`、`@CommandHandler.CallbackQuery`、`@InputHandler` ：

```kotlin
@CommandHandler(["text"])
@Guard(isAdminGuard::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### ArgParser

你可以单独定义自定义参数解析器，以改变处理器的参数解析行为，支持 `@CommandHandler`、`@CommandHandler.CallbackQuery`、`@CommonHandler`：

```kotlin
@CommandHandler(["text"])
@ArgParser(SpaceArgParser::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

**see also [`defaultArgParser`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.common/default-arg-parser.html)**

### Functional DSL

上述每个注解都有在 **Functional DSL** 中的对应写法，这是一种通过 `bot.setFunctionality { … }` 在运行时声明处理器的替代方式。两种方式共享同一 `ActivityRegistry`，并可在同一机器人中自由组合使用。

| Annotation | DSL counterpart |
|------------|-----------------|
| `@CommandHandler` | `onCommand(...)` |
| `@CommandHandler.CallbackQuery` | `onCommand(..., scope = [UpdateType.CALLBACK_QUERY])` |
| `@InputHandler` / input chains | `onInput(...)` / `inputChain(...)` |
| `@CommonHandler` | `common(...)` |
| `@UpdateHandler` | `onUpdate(...)` |
| `@UnprocessedHandler` | `whenNotHandled { ... }` |

最小示例：

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

### Commands

```kotlin
bot.setFunctionality {
    // Regular command
    onCommand("/start") {
        message { "Hello" }.send(user, bot)
    }

    // Regex-based command matching
    onCommand("""(red|green|blue)""".toRegex()) {
        message { "you typed ${update.text} color" }.send(user, bot)
    }
}
```

在 `onCommand` 块内，解析后的参数以 `Map<String, String>` 形式提供，受当前 `commandParsing` 配置影响。

### Inputs

```kotlin
bot.setFunctionality {
    onCommand("/start") {
        message { "Hello, what's your name?" }.send(user, bot)
        bot.inputListener[user] = "testInput"
    }

    onInput("testInput") {
        message { "Hey, nice to meet you, ${update.text}" }.send(user, bot)
    }
}
```

请参阅 [`bot.inputListener`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot/-telegram-bot/input-listener.html) 了解存储 API。

#### Input chains

对于多步骤输入流程使用 `inputChain`：

```kotlin
bot.setFunctionality {
    inputChain("conversation") {
        message { "Nice to meet you, ${update.text}" }.send(user, bot)
        message { "What is your favorite food?" }.send(user, bot)
    }.breakIf({ update.text == "peanut butter" }) {     // chain break condition
        message { "Oh, too bad, I'm allergic to it." }.send(user, bot)
    }.andThen {
        // next step when the break condition didn't match
        message { "Great choice!" }.send(user, bot)
    }
}
```

链条会自动前进，除非匹配到中断条件；当 `repeat = true`（默认）时，匹配的中断会保持用户在当前步骤。

> 对于具有类型化状态和验证的更丰富的多步骤流程，建议使用 [`@WizardHandler`](FSM-and-Conversation-handling.md)。

### Update type handlers

```kotlin
bot.setFunctionality {
    onUpdate(UpdateType.MESSAGE, UpdateType.CALLBACK_QUERY) {
        println("Received update: ${update.type}")
    }
}
```

### Common matchers

```kotlin
bot.setFunctionality {
    common("hello") {
        message { "Hi there!" }.send(user, bot)
    }

    common("""\d+""".toRegex()) {
        message { "You sent a number!" }.send(user, bot)
    }
}
```

### Fallback handler

```kotlin
bot.setFunctionality {
    whenNotHandled {
        message { "I didn't understand that." }.send(user, bot)
    }
}
```

### Companion options

速率限制、守卫和参数解析器可以直接作为命名参数传入，而不是使用单独的注解：

```kotlin
bot.setFunctionality {
    onCommand("/expensive", rateLimits = RateLimits(rate = 5, period = 60_000)) {
        message { "Processing..." }.send(user, bot)
    }

    onCommand("/admin", guard = AdminGuard::class) {
        message { "Admin command executed" }.send(user, bot)
    }

    onCommand("/custom", argParser = CustomArgParser::class) {
        message { "Parameters: $parameters" }.send(user, bot)
    }
}
```

### Combining DSL and annotations

两种风格可以共存 —— 注册方式相同，分发方式相同：

```kotlin
@CommandHandler(["/register"])
suspend fun register(user: User, bot: TelegramBot) {
    message { "Registration started" }.send(user, bot)
}

bot.setFunctionality {
    onCommand("/help") {
        message { "Available commands: /register, /help" }.send(user, bot)
    }
}
```

### Conclusion

这些注解提供了强大且灵活的指令、输入和事件处理工具，并支持对速率限制和守卫进行独立配置，提升了机器人开发的整体结构性和可维护性。

### See also

* [Activities & Processors](Activites-and-Processors.md)
* [Activity invocation](Activity-invocation.md)
* [FSM and Conversation handling](FSM-and-Conversation-handling.md)
* [Sessions](Sessions.md)
* [Update parsing](Update-parsing.md)

---