---
---
title: Действия и Процессоры
---

### Введение

`Activity` в терминах этой библиотеки - это абстрактная сущность, которая является обобщением таких сущностей, как `@CommandHandler`, `@InputHandler`, `@UnprocessedHandler` и `@CommonHandler`.

Также взгляните на [статью о хэндлерах](Handlers.md).

### Сбор действий

Действия собираются и подготавливают весь контекст во время компиляции (за исключением тех, которые определены через функциональный dsl).

Если вы хотите ограничить область, в которой будет производиться поиск пакета, вы можете передать параметр в плагин:

```gradle
ktGram {
    packages = listOf("com.example.mybot")
}
```

или без плагина через ksp:

```kotlin
ksp {
    arg("package", "com.example.mybot")
}
```

обратите внимание, что в таком случае, для того чтобы собранные действия обрабатывались корректно, вы также должны указать пакет в самом экземпляре.

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.mybot")

    bot.handleUpdates()
    // запуск long-polling слушателя
}
```

эта опция добавлена для возможности запуска множественных экземпляров бота:

```gradle
ktGram {
    packages = listOf("com.example.mybot", "com.example.mybot2")
}
```

или если вы не используете плагин для указания разных пакетов, вам нужно указать их через разделитель `;`:

```gradle
ksp {
    arg("package", "com.example.mybot;com.example.mybot2")
}
```

### Обработка

#### Вебхуки

В вашем контроллере (или другом месте, где обрабатывается `webhook`), вы вызываете: [`bot.update.parseAndHandle(webhookString)`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.core/-tg-update-handler/index.html#706360827%2FFunctions%2F-880831646)

#### Long polling

Вызывайте: `bot.handleUpdates()` или через `bot.update.setListener { handle(it) }`


### См. также

* [Парсинг обновлений](Update-parsing.md)
* [Вызов действия](Activity-invocation.md)
* [Действия](Actions.md)