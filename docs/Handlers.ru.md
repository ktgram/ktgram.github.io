---
---
title: Handlers
---


### Variety of Handlers

При разработке ботов, особенно в системах, где взаимодействуют пользователи, важно эффективно управлять и обрабатывать команды и события.

Эти аннотации помечают функции, предназначенные для обработки конкретных команд, входных данных или обновлений, и предоставляют метаданные, такие как ключевые слова команд, области действия и охранники.

### Annotations Overview

#### CommandHandler

Аннотация `CommandHandler` используется для пометки функций, обрабатывающих конкретные команды. Эта аннотация включает свойства, определяющие ключевые слова и области действия команды.

-   **value**: Указывает ключевые слова, связанные с командой.
-   **scope**: Определяет контекст или область, в которой будет проверяться команда.

```kotlin
@CommandHandler(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommandHandler.CallbackQuery

Специализированная версия аннотации `CommandHandler`, предназначенная специально для обработки callback‑запросов. Она содержит те же свойства, что и `CommandHandler`, с акцентом на команды, связанные с callback.

_На самом деле это то же самое, что просто `@CommandHandler` с предустановленной областью `UpdateType.CALLBACK_QUERY`_.

-   **value**: Указывает ключевые слова, связанные с командой.
-   **autoAnswer**: Автоматически отвечать на `callbackQuery` (вызвать `answerCallbackQuery` перед обработкой).


```kotlin
@CommandHandler.CallbackQuery(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### CommonHandler

Аннотация `CommonHandler` предназначена для функций, обрабатывающих команды с более низким приоритетом по сравнению с `CommandHandler` и `InputHandler`. Она используется на уровне исходного кода и предоставляет гибкий способ определения общих обработчиков команд.

**Имейте в виду, приоритет работает только внутри `@CommonHandler` (т.е. не влияет на другие обработчики).**

##### CommonHandler.Text

Эта аннотация задаёт сопоставление текста с обновлениями. Она включает свойства для определения текста сопоставления, условий фильтрации, приоритета и области действия.

-   **value**: Текст, с которым будет сравниваться входящее обновление.
-   **filter**: Класс, определяющий условия, используемые в процессе сопоставления.
-   **priority**: Уровень приоритета обработчика, где 0 — наивысший приоритет.
-   **scope**: Контекст или область, в которой будет проверяться сопоставление текста.

```kotlin
@CommonHandler.Text(["text"], filter = isNewUserFilter::class, priority = 10)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommonHandler.Regex

Аналогично `CommonHandler.Text`, эта аннотация используется для сопоставления обновлений по регулярным выражениям. Она включает свойства для определения шаблона regex, опций, условий фильтрации, приоритета и области действия.

-   **value**: Регулярное выражение, используемое для сопоставления.
-   **options**: Опции regex, изменяющие поведение шаблона.
-   **filter**: Класс, определяющий условия, используемые в процессе сопоставления.
-   **priority**: Уровень приоритета обработчика, где 0 — наивысший приоритет.
-   **scope**: Контекст или область, в которой будет проверяться сопоставление regex.

```kotlin
@CommonHandler.Regex("^\d+$", scope = [UpdateType.EDITED_MESSAGE])
suspend fun test(update: EditedMessageUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### InputHandler

Аннотация `InputHandler` помечает функции, обрабатывающие конкретные входные события. Она предназначена для функций, обрабатывающих ввод во время выполнения, и включает свойства для определения ключевых слов ввода и областей действия.

-   **value**: Указывает ключевые слова, связанные с событием ввода.

```kotlin
@InputHandler("text")
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UnprocessedHandler

Аннотация `UnprocessedHandler` используется для пометки функций, обрабатывающих обновления, не обработанные другими обработчиками. Она гарантирует, что любые необработанные обновления будут управляться корректно, при этом для этого типа обработчика может существовать только одна точка обработки.

```kotlin
@UnprocessedHandler
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UpdateHandler

Аннотация `UpdateHandler` помечает функции, обрабатывающие определённые типы входящих обновлений. Она предоставляет способ систематически классифицировать и обрабатывать разные типы обновлений.

-   **type**: Указывает типы обновлений, которые будет обрабатывать функция‑обработчик.
-   **messageKind** *(added in 9.5)*: Необязательный набор [`MessageKind`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-message-kind/index.html)s, сужающий диспетчиризацию до обновлений, содержащих сообщения, чей обнаруженный тип совпадает. Пустой набор (по умолчанию) означает, что подходит любой тип.

```kotlin
@UpdateHandler([UpdateType.PRE_CHECKOUT_QUERY])
suspend fun test(update: PreCheckoutQueryUpdate, user: User, bot: TelegramBot) {
    //...
}
```

##### Filtering by `MessageKind`

Используйте параметр `messageKind`, чтобы реагировать только на конкретный подмножество обновлений сообщений (фото, текст, сервисные события и т.п.), вместо ручного анализа nullable‑полей:

```kotlin
@UpdateHandler(type = [UpdateType.MESSAGE], messageKind = [MessageKind.PHOTO])
suspend fun onPhoto(update: MessageUpdate, bot: TelegramBot) {
    //...
}
```
### Handler Companion Annotations

Существуют также дополнительные аннотации, являющиеся опциональными для обработчиков и дополняющие их поведение.

Их можно размещать как на функциях, к которым применяется обработчик, так и на классах; в последнем случае они будут автоматически применены ко всем обработчикам в этом классе, но при необходимости можно задать отдельное поведение для отдельных функций.

Т. е. приоритет применения такой же, `Function` > `Class`, где функция имеет более высокий приоритет.

#### Rate Limiting

Кроме того, раскроем механизм ограничения частоты, описанный в аннотациях.

Вы можете задать общие ограничения для каждого пользователя:

```kotlin
// ...
val bot = TelegramBot("BOT_TOKEN") {
    rateLimiter { // general limits
        limits = RateLimits(period = 10000, rate = 5)
    }
}
```

###### Handler specific

Ограничения на определённые действия можно определить с помощью аннотации `RateLimits`, поддерживаемой `@CommandHandler`, `@CommandHandler.CallbackQuery`, `@InputHandler`, `@CommonHandler`.

```kotlin
@CommandHandler(["/start"])
@RateLimits(period = 1000L, rate = 1L)
suspend fun start(user: User, bot: TelegramBot) {
    // ...
}
```

#### Guard

Вы можете определить guard‑ы отдельно для контроля доступа к обработчикам, поддерживается `@CommandHandler`, `@CommandHandler.CallbackQuery`, `@InputHandler` :

```kotlin
@CommandHandler(["text"])
@Guard(isAdminGuard::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### ArgParser

Вы можете определить пользовательский парсер аргументов отдельно, изменяя поведение разбора параметров для обработчиков, поддерживается `@CommandHandler`, `@CommandHandler.CallbackQuery`, `@CommonHandler`:

```kotlin
@CommandHandler(["text"])
@ArgParser(SpaceArgParser::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

**see also [`defaultArgParser`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.common/default-arg-parser.html)**

### Functional DSL

Каждая из перечисленных аннотаций имеет аналог в **Functional DSL**, альтернативный способ объявления обработчиков во время выполнения через `bot.setFunctionality { … }`. Оба подхода используют один и тот же `ActivityRegistry` и могут свободно комбинироваться в одном боте.

| Annotation | DSL counterpart |
|------------|-----------------|
| `@CommandHandler` | `onCommand(...)` |
| `@CommandHandler.CallbackQuery` | `onCommand(..., scope = [UpdateType.CALLBACK_QUERY])` |
| `@InputHandler` / input chains | `onInput(...)` / `inputChain(...)` |
| `@CommonHandler` | `common(...)` |
| `@UpdateHandler` | `onUpdate(...)` |
| `@UnprocessedHandler` | `whenNotHandled { ... }` |

Минимальный пример:

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

Внутри блока `onCommand` разобранные параметры доступны как `Map<String, String>`, сформированный текущей конфигурацией `commandParsing`.

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

См. [`bot.inputListener`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot/-telegram-bot/input-listener.html) для API хранилища.

#### Input chains

Для многошаговых потоков ввода используйте `inputChain`:

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

Цепочка автоматически переходит к следующему шагу, если условие прерывания не сработало; при `repeat = true` (по умолчанию) совпадение условия прерывания оставляет пользователя на текущем шаге.

> Для более богатых многошаговых потоков с типизированным состоянием и валидацией предпочтительнее использовать [`@WizardHandler`](FSM-and-Conversation-handling.md).

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

Ограничения частоты, guard‑ы и парсеры аргументов передаются напрямую как именованные параметры вместо отдельных аннотаций:

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

Оба стиля сосуществуют — регистрируются одинаково, диспетчеризуются одинаково:

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

Эти аннотации предоставляют надёжные и гибкие инструменты для обработки команд, вводов и событий, позволяя одновременно задавать отдельные конфигурации ограничений частоты и guard‑ов, улучшая общую структуру и поддерживаемость разработки ботов.

### See also

* [Activities & Processors](Activites-and-Processors.md)
* [Activity invocation](Activity-invocation.md)
* [FSM and Conversation handling](FSM-and-Conversation-handling.md)
* [Sessions](Sessions.md)
* [Update parsing](Update-parsing.md)

---