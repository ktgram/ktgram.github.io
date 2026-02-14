---
---
title: Functional Dsl
---

### To ~~infinity~~ functional dsl and beyond!

Бот поддерживает как аннотационный, так и функциональный подход к настройке контекста. Вы можете комбинировать оба подхода.

### Functional DSL

Functional DSL — это просто другой способ определения контекста бота.

Пример:

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

### Commands and Inputs

Вы можете обрабатывать как `commands`, так и `inputs` с использованием функционального DSL.

#### Commands

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

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
}
```

В `onCommand`, разобранные параметры доступны как `Map<String, String>` в зависимости от вашей конфигурации.

#### Inputs

Вы можете использовать inputs через [`bot.inputListener`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot/-telegram-bot/input-listener.html).

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

#### Input Chains

Для многошаговых потоков ввода используйте `inputChain`:

```kotlin
bot.setFunctionality {
    inputChain("conversation") {
        message { "Nice to meet you, ${update.text}" }.send(user, bot)
        message { "What is your favorite food?" }.send(user, bot)
    }.breakIf({ update.text == "peanut butter" }) { // chain break condition
        message { "Oh, too bad, I'm allergic to it." }.send(user, bot)
        // action that will be applied when condition matches
    }.andThen {
        // next input point if break condition doesn't match
        message { "Great choice!" }.send(user, bot)
    }
}
```

Цепочка автоматически переходит к следующему шагу, если не сработало условие прерывания. Если условие прерывания срабатывает и `repeat` равен `true` (по умолчанию), пользователь остается на текущем шаге.

#### Update Type Handlers

Обрабатывайте конкретные типы обновлений напрямую:

```kotlin
bot.setFunctionality {
    onUpdate(UpdateType.MESSAGE, UpdateType.CALLBACK_QUERY) {
        // Handle both message and callback query updates
        println("Received update: ${update.type}")
    }
}
```

#### Common Matchers

Совпадение с текстовым содержимым (не только командами) с использованием `common`:

```kotlin
bot.setFunctionality {
    // String matching
    common("hello") {
        message { "Hi there!" }.send(user, bot)
    }
    
    // Regex matching
    common("""\d+""".toRegex()) {
        message { "You sent a number!" }.send(user, bot)
    }
}
```

#### Fallback Handler

Обрабатывайте обновления, которые не были обработаны ни одним обработчиком:

```kotlin
bot.setFunctionality {
    whenNotHandled {
        message { "I didn't understand that." }.send(user, bot)
    }
}
```

### Advanced Configuration

#### Rate Limiting

Применяйте ограничения частоты к любому обработчику:

```kotlin
bot.setFunctionality {
    onCommand("/expensive", rateLimits = RateLimits(5, 60)) {
        // This command can only be called 5 times per 60 seconds
        message { "Processing..." }.send(user, bot)
    }
}
```

#### Guards

Используйте guards для добавления пользовательской логики валидации:

```kotlin
bot.setFunctionality {
    onCommand("/admin", guard = AdminGuard::class) {
        message { "Admin command executed" }.send(user, bot)
    }
}
```

#### Argument Parsing

Настраивайте способ разбора аргументов команд:

```kotlin
bot.setFunctionality {
    onCommand("/custom", argParser = CustomArgParser::class) {
        // parameters will be parsed using CustomArgParser
        message { "Parameters: $parameters" }.send(user, bot)
    }
}
```

### Combining Functional and Annotation-Based setting

Вы можете использовать оба подхода в одном боте:

```kotlin
// Annotation-based handler
@CommandHandler(["/register"])
suspend fun register(ctx: CommandContext) {
    message { "Registration started" }.send(ctx.user, ctx.bot)
}

// Functional handler
bot.setFunctionality {
    onCommand("/help") {
        message { "Available commands: /register, /help" }.send(user, bot)
    }
}
```

Оба обработчика зарегистрированы в одном `ActivityRegistry` и работают вместе без проблем.

### See also

* [Action](Actions.md)
* [Useful utilities](Useful-utilities-and-tips.md)
---