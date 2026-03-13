---
---
title: Функциональный Dsl
---

### До ~~бесконечности~~ функционального dsl и дальше!

Бот поддерживает как аннотационный, так и функциональный подход к настройке контекста. Вы можете комбинировать оба подхода.

### Функциональный DSL

Функциональный DSL — это просто другой способ определения контекста бота.

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

### Команды и Ввод

Вы можете обрабатывать как `команды`, так и `ввод` с помощью функционального DSL.

#### Команды

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

    bot.setFunctionality {
        // Обычная команда
        onCommand("/start") {
            message { "Hello" }.send(user, bot)
        }
        
        // Регулярное выражение для команд
        onCommand("""(red|green|blue)""".toRegex()) {
            message { "you typed ${update.text} color" }.send(user, bot)
        }
    }
}
```

В `onCommand`, распарсенные параметры доступны как `Map<String, String>` в зависимости от вашей конфигурации.

#### Ввод

Вы можете использовать ввод через [`bot.inputListener`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot/-telegram-bot/input-listener.html).

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

#### Цепочки ввода

Для многошаговых потоков ввода используйте `inputChain`:

```kotlin
bot.setFunctionality {
    inputChain("conversation") {
        message { "Nice to meet you, ${update.text}" }.send(user, bot)
        message { "What is your favorite food?" }.send(user, bot)
    }.breakIf({ update.text == "peanut butter" }) { // условие остановки цепочки
        message { "Oh, too bad, I'm allergic to it." }.send(user, bot)
        // действие, которое будет применено при совпадении условия
    }.andThen {
        // следующий шаг, если условие остановки не сработало
        message { "Great choice!" }.send(user, bot)
    }
}
```

Цепочка автоматически переходит к следующему шагу, если не сработало условие остановки. Если условие остановки сработало и `repeat` равен `true` (по умолчанию), пользователь остается на текущем шаге.

#### Обработчики типов обновлений

Обрабатывайте конкретные типы обновлений напрямую:

```kotlin
bot.setFunctionality {
    onUpdate(UpdateType.MESSAGE, UpdateType.CALLBACK_QUERY) {
        // Обрабатываем оба типа обновлений: сообщения и запросы обратного вызова
        println("Received update: ${update.type}")
    }
}
```

#### Общие матчеры

Сопоставляйте текстовое содержимое (не только команды) с помощью `common`:

```kotlin
bot.setFunctionality {
    // Сопоставление строк
    common("hello") {
        message { "Hi there!" }.send(user, bot)
    }
    
    // Сопоставление по регулярному выражению
    common("""\d+""".toRegex()) {
        message { "You sent a number!" }.send(user, bot)
    }
}
```

#### Обработчик по умолчанию

Обрабатывайте обновления, которые не были обработаны ни одним из обработчиков:

```kotlin
bot.setFunctionality {
    whenNotHandled {
        message { "I didn't understand that." }.send(user, bot)
    }
}
```

### Расширенная конфигурация

#### Ограничение частоты

Применяйте ограничения частоты к любому обработчику:

```kotlin
bot.setFunctionality {
    onCommand("/expensive", rateLimits = RateLimits(5, 60)) {
        // Эта команда может вызываться только 5 раз за 60 секунд
        message { "Processing..." }.send(user, bot)
    }
}
```

#### Ограничения доступа

Используйте ограничения для добавления пользовательской логики валидации:

```kotlin
bot.setFunctionality {
    onCommand("/admin", guard = AdminGuard::class) {
        message { "Admin command executed" }.send(user, bot)
    }
}
```

#### Парсер аргументов

Настраивайте способ парсинга аргументов команд:

```kotlin
bot.setFunctionality {
    onCommand("/custom", argParser = CustomArgParser::class) {
        // параметры будут распарсены с помощью CustomArgParser
        message { "Parameters: $parameters" }.send(user, bot)
    }
}
```

### Комбинирование функционального и аннотационного подходов

Вы можете использовать оба подхода в одном боте:

```kotlin
// Обработчик на основе аннотаций
@CommandHandler(["/register"])
suspend fun register(ctx: CommandContext) {
    message { "Registration started" }.send(ctx.user, ctx.bot)
}

// Функциональный обработчик
bot.setFunctionality {
    onCommand("/help") {
        message { "Available commands: /register, /help" }.send(user, bot)
    }
}
```

Оба обработчика регистрируются в одном `ActivityRegistry` и работают вместе без проблем.

### См. также

* [Action](Actions.md)
* [Useful utilities](Useful-utilities-and-tips.md)
---