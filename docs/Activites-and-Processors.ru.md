---
---
title: Activites And Processors
---

### Introduction

`Activity` в терминах этой библиотеки — это абстрактная сущность, обобщающая такие сущности, как `@CommandHandler`, `@InputHandler`, `@UnprocessedHandler`, `@CommonHandler`, `@UpdateHandler` и `@WizardHandler`.

Также посмотрите статью о [handlers](Handlers.md).

### Collecting activities

Activities обнаруживаются и связываются **во время компиляции** процессором **ktnip** KSP. Исключением является [Functional DSL](Handlers#functional-dsl.md) — обработчики, определённые через `bot.setFunctionality { ... }`, регистрируются во время выполнения.

Если вы хотите ограничить область, в которой будет происходить поиск пакетов, вы можете передать параметр плагину:

```gradle
ktGram {
    packages = listOf("com.example.mybot")
}
```

или без плагина через ksp:

```gradle
ksp {
    arg("package", "com.example.mybot")
}
```

обратите внимание, что в таком случае, чтобы собранные действия корректно обрабатывались, вы также должны указать пакет в самом экземпляре.

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.mybot")

    bot.handleUpdates()
    // start long-polling listener
}
```

эта опция добавлена, чтобы можно было запускать несколько экземпляров бота:

```gradle
ktGram {
    packages = listOf("com.example.mybot", "com.example.mybot2")
}
```


или, если вы не используете плагин, для указания разных пакетов необходимо перечислить их через разделитель `;`:

```gradle
ksp {
    arg("package", "com.example.mybot;com.example.mybot2")
}
```

### Processing

#### Webhooks

В вашем контроллере (или другом месте, где обрабатывается `webhook`) вы вызываете: [`bot.update.parseAndHandle(webhookString)`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.core/-tg-update-handler/index.html#706360827%2FFunctions%2F-880831646)

#### Long polling

Вызовите: `bot.handleUpdates()` или через `bot.update.setListener { handle(it) }`


### See also

* [Update parsing](Update-parsing.md)
* [Activity invocation](Activity-invocation.md)
* [Actions](Actions.md)

---