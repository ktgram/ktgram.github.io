---
title: Functional-Dsl
---

# To ~~infinity~~ functional handling and beyond!
Although the basic mechanism of working with the bot involves working with annotations, but nevertheless it does not prevent the use of functional update processing.

Moreover, the flexibility of the bot interface also allows you to combine the two modes.

## Functional handling DSL

In most functional processing methods differ in the types of [`Update`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types/-update/index.html) supported, in simple terms you can put a listener on a certain type of data.

By way of example:

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

    bot.handleUpdates() {
        onChosenInlineResult {
            println("got a result ${update.chosenInlineResult.resultId} from ${update.user}")
        }
    }
}
```

## Commands and Inputs

It is also possible to process both `commands` and `inputs`.

See example:

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN")

    bot.handleUpdates() {
            // regular command
        onCommand("/start") {
            message { "Hello" }.send(user, bot)
        }
        onCommand("""(red|green|blue)""".toRegex()) {
            message { "you typed ${update.text} color" }.send(user, bot)
        }
    }
}
```

In the context of the `onCommand` function, parameters in the format `Map<String, String>` are passed, \
parsed appropriately specified in configuration. 

### Inputs
It is also possible to use inputs through the familiar [`bot.inputListener`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot/-telegram-bot/input-listener.html) mechanism.

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN")

    bot.handleUpdates() {
            // regular command
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
Also, you can use input chaining:
```kotlin
inputChain("conversation") {
     message { "Nice to meet you, ${update.text}" }.send(user, bot)
     message { "What is your favorite food?" }.send(user, bot)
}.breakIf({ update.text == "peanut butter" }) { // chain break condition
     message { "Oh, too bad, I'm allergic to it." }.send(user, bot)
     // action that will be applied when match
}.andThen {
     // next input point if break condition doesn't match
}
```

You can read more about methods in the [`FunctionalHandlingDsl`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.core/-functional-handling-dsl/index.html) class documentation.

> [!CAUTION]
> Be aware that if you use both processors (functional, annotation) inputs may work not as it seems to be (each processor clears input after being processed, if you want another behavior change inputAutoRemoval configuration).

# See also

* [Action](/Actions)
* [Useful utilities](/Useful-utilities-and-tips)