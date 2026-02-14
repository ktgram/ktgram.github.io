---
---
title: Полезные утилиты и советы
---


### Работа с ProcessedUpdate

[`ProcessedUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processed-update/index.html) — это обобщенный класс для обновлений, который в зависимости от исходных данных может предоставляться в разных типах ([`MessageUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-message-update/index.html), [`CallbackQueryUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-callback-query-update/index.html) и т. д.)

Таким образом вы можете проверять тип входящих данных и дальше манипулировать определенными данными с помощью smartcasts, например:

```kotlin
// ...
if (update !is MessageUpdate) {
    message { "Only messages are allowed" }.send(user, bot)
    return
}
// Далее ProcessedUpdate будет восприниматься как MessageUpdate.
```

Также внутри есть интерфейс [`UserReference`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-user-reference/index.html), который позволяет определить, есть ли внутри ссылка на пользователя, пример использования:

```kotlin
val user = if(update is UserReference) update.user else null

```

При необходимости внутри всегда есть оригинальный [`update`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types/-update/index.html) в параметре update.


### Внедрение зависимостей

Библиотека использует простой механизм для инициализации классов, где ваши методы обработки обновлений аннотированы предоставленными аннотациями.

[`ClassManagerImpl`](https://github.com/vendelieu/telegram-bot/blob/master/telegram-bot/src/commonMain/kotlin/eu/vendeli/tgbot/implementations/ClassManagerImpl.kt) используется по умолчанию для вызова аннотированных методов.

Но если вы хотите использовать другие библиотеки для этого, вы можете переопределить интерфейс [`ClassManager`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-manager/index.html), <br/>используя ваш предпочитаемый механизм и передать его при инициализации бота.

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.controllers") {
        classManager = ClassManagerImpl()
    }

    bot.handleUpdates()
}
```

### Фильтрация обновлений

Если нет сложных условий, вы можете просто отфильтровать некоторые обновления для обработки:

```kotlin
// функция где определено условие фильтрации обновлений
fun filteringFun(update: Update): Boolean = update.message?.text.isNullOrBlank()

fun main() = runBlocking {
  val bot = TelegramBot("BOT_TOKEN")

  // установка более специфичного потока обработки для обновлений
  bot.update.setListener {
    if(filteringFun(it)) return@setListener

    // так просто, если слушатель покинул область видимости до достижения функции обработчика, то это фильтрация.
    // на самом деле вы можете даже написать условие if прямо там с return@setListener или расширить фильтрацию в отдельный класс.

    handle(it) // или ручной способ обработки с блоком
  }
}
```

чтобы включить фильтрацию в ваш процесс сопоставления или исключения команд, взгляните на guards или `@CommonHandler`.

### Обобщение опций для разных методов

Если вам часто приходится применять одни и те же необязательные параметры, вы можете написать похожую функцию, которая вам подходит, и облегчить код-болерплейт :)

Некоторые общие свойства разделены на [разные интерфейсы](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.options/-options/index.html).

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


// ... и в вашем коде

message { "test" }.markdownMode().send(to, via)

```