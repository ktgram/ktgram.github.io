---
title: Useful Utilities And Tips
---

### Aide Compiler Plugin [🔬]

_feature disabled by default, to use it enable in plugin parameters_

### Configuration  
Configure Aide in your `build.gradle.kts`:

```kotlin
ktGram {
    // Enable AIDE compiler extensions (Automatic .send() chaining)
    aideEnabled = true
    
}
```

---

### Usage Example

##### Simple case
```kotlin
@CommandHandler
suspend fun handler(user: User, bot: TelegramBot) {
    // With aideAutoSend=true
    message {
        "Auto-sent message"
    } // ← Compiler adds .send(user, bot)
    
    // Explicit control
    message { 
        "Manual send"
    }.send(user, bot) // ← No auto-add when present
}
```

> [!CAUTION]
> Be aware that even if you do not use an explicit `send`, you still need to have `suspend` function keyword, otherwise you will get an error.

##### Complex Case (Manual Handling Required)

```kotlin
@InputHandler
fun handleInput(user: User, bot: TelegramBot) {
    // Requires manual .send()
    val savedAction = message {
        "Stored action"
    }
    
    // Valid usage with explicit send
    savedAction.send(user, bot)
}
```

###### Validation Rules

* Auto-Send Applies When:

    * Action is directly returned from handler
    * No intermediate variable assignment
    * No existing `.send()` call

---

#### Requirements

- Handler must declare parameters:
  - `User` for general actions (simple action require just `TelegramBot`)
  - `TelegramBot` for all actions
- Annotated with `@CommandHandler`, `@InputHandler`, etc (any supported annotation).

### Operating with ProcessedUpdate

The [`ProcessedUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processed-update/index.html) is a generic class for updates which, depending on the original data, can be provided in different types ([`MessageUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-message-update/index.html), [`CallbackQueryUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-callback-query-update/index.html), etc.)

So you can check the type of incoming data and further manipulate certain data with smartcasts, for example:

```kotlin
// ...
if (update !is MessageUpdate) {
    message { "Only messages are allowed" }.send(user, bot)
    return
}
// Further on, ProcessedUpdate will be perceived as MessageUpdate.
```

There's also an [`UserReference`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-user-reference/index.html) interface inside that lets you determine if there's a user reference inside, example use case:

```kotlin
val user = if(update is UserReference) update.user else null

```

If needed inside there is always the original [`update`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types/-update/index.html) in the update parameter.


### Dependency injection

The library uses simple mechanism to initialize classes where your update processing methods are annotated with the provided annotations.

[`ClassManagerImpl`](https://github.com/vendelieu/telegram-bot/blob/master/telegram-bot/src/commonMain/kotlin/eu/vendeli/tgbot/implementations/ClassManagerImpl.kt) is used by default to invoke annotated methods.

But if you want to use some other libraries for that you can redefine the [`ClassManager`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-manager/index.html) interface, <br/>using your preferred mechanism and pass it on when initializing the bot.

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.controllers") {
        classManager = ClassManagerImpl()
    }

    bot.handleUpdates()
}
```

### Filtering updates

If there's no complex conditions you can simply filter some updates for being processed:

```kotlin
// function where updates filtering condition defined
fun filteringFun(update: Update): Boolean = update.message?.text.isNullOrBlank()

fun main() = runBlocking {
  val bot = TelegramBot("BOT_TOKEN")

  // setting more specific processing flow for updates
  bot.update.setListener {
    if(filteringFun(it)) return@setListener

    // so simply, if the listener left the scope before reaching the handler function, that it is filtering.
    // actually you can even write directly if-condition there with return@setListener or extend filtering to separate class.

    handle(it) // or manual handling way with block
  }
}
```

to include filtering in your command matching or excluding process take a look at guards or `@CommonHandler`.

### Generalize options for different methods

If you have to apply the same optional parameters often, you can write a similar function that suits you and lighten the boilerplate code :)

Some common properties are separated to [different interfaces](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.options/-options/index.html).

```kotlin
@Suppress("NOTHING_TO_INLINE")
inline fun <T, R, O> T.markdownMode(crossinline block: O.() -> Unit = {}): T
        where               T : TgAction<R>,
                            T : OptionsFeature<T, O>,
                            O : Options,
                            O : OptionsParseMode =
    options {
        parseMode = ParseMode.Markdown
        block()
    }


// ... and in your code

message { "test" }.markdownMode().send(to, via)

```

### Processing context (Matched Regex, Parsed Parameters)

There's also context collected while processing, for example you can access matches in `@CommonHandler.Regex` through `update._getRegexMatch()`.

Or to get raw parsed parameters you can turn collecting them through config `processingCtxTargets` and access them through `update._getParsedParameters()`
