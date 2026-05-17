---
---
title: Useful Utilities And Tips
---


### Operating with ProcessedUpdate

`ProcessedUpdate` (<https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processed-update/index.html>) — это обобщённый класс для обновлений, который в зависимости от исходных данных может быть представлен в разных типах ([`MessageUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-message-update/index.html), [`CallbackQueryUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-callback-query-update/index.html) и т.д.)

Таким образом, вы можете проверить тип входящих данных и дальше работать с определёнными данными с помощью умных кастов, например:

```kotlin
// ...
if (update !is MessageUpdate) {
    message { "Only messages are allowed" }.send(user, bot)
    return
}
// Further on, ProcessedUpdate will be perceived as MessageUpdate.
```

Также существует интерфейс [`UserReference`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-user-reference/index.html), который позволяет определить, есть ли ссылка на пользователя внутри, пример использования:

```kotlin
val user = if(update is UserReference) update.user else null

```

При необходимости внутри всегда доступен оригинальный [`update`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types/-update/index.html) в параметре обновления.


### Dependency injection

Библиотека использует простой механизм инициализации классов, где ваши методы обработки обновлений помечены предоставленными аннотациями.

[`ClassManagerImpl`](https://github.com/vendelieu/telegram-bot/blob/master/telegram-bot/src/commonMain/kotlin/eu/vendeli/tgbot/implementations/ClassManagerImpl.kt) используется по умолчанию для вызова аннотированных методов.

Но если вы хотите использовать какие‑то другие библиотеки для этого, вы можете переопределить интерфейс [`ClassManager`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-manager/index.html), <br/>используя предпочтительный механизм и передать его при инициализации бота.

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.controllers") {
        classManager = ClassManagerImpl()
    }

    bot.handleUpdates()
}
```

### Filtering updates

Если нет сложных условий, вы можете просто отфильтровать некоторые обновления от дальнейшей обработки:

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

для включения фильтрации в сопоставление команд или исключения процесса посмотрите на guards или `@CommonHandler`.

### Generalize options for different methods

Если вам часто нужно применять одинаковые необязательные параметры, вы можете написать похожую функцию, которая вам подходит, и уменьшить объем шаблонного кода :)

Некоторые общие свойства вынесены в [разные интерфейсы](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.options/-options/index.html).

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


---