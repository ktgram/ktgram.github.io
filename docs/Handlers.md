---
title: Handlers
---


### Variety of Handlers

In bot development, particularly in systems involving user interactions, it is crucial to manage and process commands and events efficiently.

These annotations mark functions designed to process specific commands, inputs, or updates and provide metadata such as command keywords, scopes, and guards.

### Annotations Overview

#### CommandHandler

The `CommandHandler` annotation is used to mark functions that process specific commands. This annotation includes properties that define the command's keywords and scopes.

-   **value**: Specifies the keywords associated with the command.
-   **scope**: Determines the context or scope in which the command will be checked.

```kotlin
@CommandHandler(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommandHandler.CallbackQuery

A specialized version of the `CommandHandler` annotation designed specifically for handling callback queries. It includes similar properties as `CommandHandler`, with a focus on callback-related commands.

_It's actually the same as just `@CommandHandler` with a preset `UpdateType.CALLBACK_QUERY` scope_.

-   **value**: Specifies the keywords associated with the command.
-   **autoAnswer**: Reply to `callbackQuery` automatically (call `answerCallbackQuery` before handling).


```kotlin
@CommandHandler.CallbackQuery(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### CommonHandler

The `CommonHandler` annotation is intended for functions that process commands with lower priority compared to `CommandHandler` and `InputHandler`. It is used at the source level and provides a flexible way to define common command handlers.

**Be aware, priority works within just `@CommonHandler`'s itself  (ie. not affects other handlers).**

##### CommonHandler.Text

This annotation specifies text matching against updates. It includes properties to define the matching text, filtering conditions, priority, and scope.

-   **value**: The text to match against incoming updates.
-   **filter**: A class that defines conditions used in the matching process.
-   **priority**: The priority level of the handler, where 0 is the highest priority.
-   **scope**: The context or scope in which the text matching will be checked.

```kotlin
@CommonHandler.Text(["text"], filter = isNewUserFilter::class, priority = 10)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommonHandler.Regex

Similar to `CommonHandler.Text`, this annotation is used for matching updates based on regular expressions. It includes properties for defining the regex pattern, options, filtering conditions, priority, and scope.

-   **value**: The regex pattern used for matching.
-   **options**: Regex options that modify the behavior of the regex pattern.
-   **filter**: A class that defines conditions used in the matching process.
-   **priority**: The priority level of the handler, where 0 is the highest priority.
-   **scope**: The context or scope in which the regex matching will be checked.

```kotlin
@CommonHandler.Regex("^\d+$", scope = [UpdateType.EDITED_MESSAGE])
suspend fun test(update: EditedMessageUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### InputHandler

The `InputHandler` annotation marks functions that process specific input events. It is intended for functions that handle inputs at runtime and includes properties for defining input keywords and scopes.

-   **value**: Specifies the keywords associated with the input event.

```kotlin
@InputHandler("text")
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UnprocessedHandler

The `UnprocessedHandler` annotation is used to mark functions that handle updates not processed by other handlers. It ensures that any unprocessed updates are managed appropriately, with only one processing point possible for this handler type.

```kotlin
@UnprocessedHandler
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UpdateHandler

The `UpdateHandler` annotation marks functions that handle specific types of incoming updates. It provides a way to categorize and process different update types systematically.

-   **type**: Specifies the types of updates the handler function will process.
-   **messageKind** *(added in 9.5)*: Optional set of [`MessageKind`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-message-kind/index.html)s that narrow dispatch to message-bearing updates whose detected kind matches. Empty (the default) means any kind matches.

```kotlin
@UpdateHandler([UpdateType.PRE_CHECKOUT_QUERY])
suspend fun test(update: PreCheckoutQueryUpdate, user: User, bot: TelegramBot) {
    //...
}
```

##### Filtering by `MessageKind`

Use the `messageKind` parameter to react only to a specific subset of message updates (photos, text, service events, …) instead of inspecting nullable fields by hand:

```kotlin
@UpdateHandler(type = [UpdateType.MESSAGE], messageKind = [MessageKind.PHOTO])
suspend fun onPhoto(update: MessageUpdate, bot: TelegramBot) {
    //...
}
```
### Handler Companion Annotations

There are also additional annotations that are optional to the handlers, complementing the optional behavior of the handlers itself.

They can be placed both on functions to which a handler is applied and on classes, in the latter case they will be automatically applied to all handlers in that class, but if there is a need it is possible to have separate behavior for some functions.

I.e. the applying has such a priority, `Function` > `Class`, where function have higher priority.

#### Rate Limiting

In addition, let us also disclose the rate limiting mechanism described in the annotations.

You can set general limits for each user:

```kotlin
// ...
val bot = TelegramBot("BOT_TOKEN") {
    rateLimiter { // general limits
        limits = RateLimits(period = 10000, rate = 5)
    }
}
```

###### Handler specific

Limits on certain actions can be defined using the `RateLimits` annotation, supported `@CommandHandler`, `@CommandHandler.CallbackQuery`, `@InputHandler`, `@CommonHandler`.

```kotlin
@CommandHandler(["/start"])
@RateLimits(period = 1000L, rate = 1L)
suspend fun start(user: User, bot: TelegramBot) {
    // ...
}
```

#### Guard

You can define guards separately to control access to handlers, supported `@CommandHandler`, `@CommandHandler.CallbackQuery`, `@InputHandler` :

```kotlin
@CommandHandler(["text"])
@Guard(isAdminGuard::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### ArgParser

You can define custom argument parser separately to change parameters parsing behaviour for handlers, supported `@CommandHandler`, `@CommandHandler.CallbackQuery`, `@CommonHandler`:

```kotlin
@CommandHandler(["text"])
@ArgParser(SpaceArgParser::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

**see also [`defaultArgParser`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.common/default-arg-parser.html)**

### Functional DSL

Every annotation above has a counterpart in the **Functional DSL**, an alternative way to declare handlers at runtime via `bot.setFunctionality { … }`. Both approaches share the same `ActivityRegistry` and can be combined freely in the same bot.

| Annotation | DSL counterpart |
|------------|-----------------|
| `@CommandHandler` | `onCommand(...)` |
| `@CommandHandler.CallbackQuery` | `onCommand(..., scope = [UpdateType.CALLBACK_QUERY])` |
| `@InputHandler` / input chains | `onInput(...)` / `inputChain(...)` |
| `@CommonHandler` | `common(...)` |
| `@UpdateHandler` | `onUpdate(...)` |
| `@UnprocessedHandler` | `whenNotHandled { ... }` |

Minimal example:

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

Inside an `onCommand` block, parsed parameters are available as `Map<String, String>` shaped by the active `commandParsing` configuration.

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

See [`bot.inputListener`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot/-telegram-bot/input-listener.html) for the storage API.

#### Input chains

For multi-step input flows use `inputChain`:

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

The chain auto-advances unless a break condition matches; when `repeat = true` (default), a matching break keeps the user on the current step.

> For richer multi-step flows with typed state and validation, prefer the [`@WizardHandler`](FSM-and-Conversation-handling.md) instead.

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

Rate limits, guards, and argument parsers are passed directly as named parameters instead of separate annotations:

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

The two styles coexist — register the same way, dispatch the same way:

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

These annotations provide robust and flexible tools for handling commands, inputs, and events, while allowing for separate configurations of rate limits and guards, enhancing the overall structure and maintainability of bot development.

### See also

* [Activities & Processors](Activites-and-Processors.md)
* [Activity invocation](Activity-invocation.md)
* [FSM and Conversation handling](FSM-and-Conversation-handling.md)
* [Sessions](Sessions.md)
* [Update parsing](Update-parsing.md)
