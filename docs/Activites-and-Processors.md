# Introduction

`Activity` in the terms of this library is the abstract entity that serves as concept that represents a generalization of entities such as `@CommandHandler`, `@InputHandler`, `@UnprocessedHandler`, and `@CommonHandler`.

Also take a look at [handlers article](Handlers).

# Collecting activities

Activities are collected and prepared all context in compile time.

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

# Processors

You have two types of flow processing updates:

## Functional 

You establish the processing behavior through the lambda parameter function [`bot.handleUpdates() {}`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot/-telegram-bot/handle-updates.html), or through [`bot.update.setListener`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.core/-tg-update-handler/set-listener.html).

You can read more about  functional processing in a [related article](Functional-Dsl).

See [`FunctionalHandlingDsl`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.core/-functional-handling-dsl/index.html).

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

## Annotation

Annotation depends on the selected processing mode: 

### Webhooks

In your controller (or another place where the `webhook` is processed), you call: [`bot.update.parseAndHandle(webhookString)`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.core/-tg-update-handler/index.html#706360827%2FFunctions%2F-880831646)

By default it will use processor for annotations, but if you want to have some custom behaviour it also can be set through [`setBehaviour`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.core/-tg-update-handler/set-behaviour.html) (it is not necessary to assign the behavior in the controller itself every time, it is enough to assign it once during configuration):

```kotlin
bot.update.setBehaviour {
   // ...any other actions
   update(it) // run annotation processor
}
```

### Long polling

Call: `bot.handleUpdates()` or through `bot.update.setListener { handle(it) }`

## Both

Also, if desired, both these approaches can be combined using the same `setListener {}`, in such an approach even the same command can be processed twice, processing will be done in the order they are called.

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "eu.vendeli.samples.controller")

    bot.update.setListener {
        handle(it) // Here we send the update for annotation processing.
        handle(it) { // Here we functionally process it afterwards.
            onMessage {
                message { update.text }.send(update.user, bot)
            }
        }
}
```
Example of combining usage you can see in a [poll sample](https://github.com/vendelieu/telegram-bot_template/blob/poll/src/main/kotlin/com/example/poll/PollApplication.kt).

or in webhook handling you can set through `setBehaviour` as described before.


# See also

* [Update parsing](Update-parsing)
* [Activity invocation](Activity-invocation)
* [Actions](Actions)
