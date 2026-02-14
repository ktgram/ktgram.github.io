---
---
title: Actions
---

### Все запросы - это Actions
Все запросы Telegram API являются различными видами интерфейсов [`TgAction`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.action/-tg-action/index.html), реализующих различные методы, такие как [`SendMessageAction`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.api.message/-send-message-action/index.html), <br/>которые обернуты в виде функций типа [`message()`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.api.message/message.html) для удобства интерфейса библиотеки.

<p align="center">
    <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/2d097d60-1907-4ca1-8ad3-3ee8d223f8eb" alt="Actions diagram" />
</p>

Каждый `Action` может иметь свои собственные возможные методы, в зависимости от доступных [`Feature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-feature/index.html).

### Features

Различные действия могут иметь различные [`Features`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-feature/index.html) в зависимости от Telegram Bot Api, такие как:
[`OptionsFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-options-feature/index.html),
[`MarkupFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-markup-feature/index.html)
[`EntitiesFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-entities-feature/index.html)
[`CaptionFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-caption-feature/index.html).

Давайте рассмотрим их подробнее:

### Options
Например, [`OptionsFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-options-feature/index.html) используется для передачи дополнительных параметров.

У каждого действия свой тип опций, соответствующий можно увидеть в самом `Action` в параметре `options`, в разделе свойств. <br/>Например, `sendMessage` содержит data class [`MessageOptions`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.options/-message-options/index.html) с различными параметрами в качестве опций.

Пример использования:

```kotlin
message{ "*Test*" }.options {
    parseMode = ParseMode.Markdown
}.send(user, bot)
```
### Markup

Также существует метод для отправки разметки, который поддерживает все виды [клавиатур](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.marker/-keyboard/index.html): <br/>[`ReplyKeyboardMarkup`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-reply-keyboard-markup/index.html), [`InlineKeyboardMarkup`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-inline-keyboard-markup/index.html), [`ForceReply`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-force-reply/index.html), [`ReplyKeyboardRemove`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-reply-keyboard-remove/index.html).

#### Inline Keyboard Markup

Этот билдер позволяет создавать inline кнопки с любой комбинацией параметров.

```kotlin
message{ "Test" }.inlineKeyboardMarkup {
    "name" callback "callbackData"         //
    "buttonName" url "https://google.com"  //--- эти две кнопки будут в одной строке.
    newLine() // или br()
    "otherButton" webAppInfo "data"       // это будет в другой строке

    // вы также можете использовать другой стиль внутри билдера:
    callbackData("buttonName") { "callbackData" }
}.send(user, bot)

```

Более подробную информацию можно найти в документации билдера [documentation](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.builders/-inline-keyboard-markup-builder/index.html).

#### Reply Keyboard Markup

Этот билдер позволяет создавать кнопки меню.

```kotlin
message{ "Test" }.replyKeyboardMarkup {
  + "Menu button"     // вы можете добавлять кнопки с помощью унарного оператора плюс
  + "Menu button 2"
  br() // переход на вторую строку
  "Send polls 👀" requestPoll true   // кнопка с параметром

  options {
    resizeKeyboard = true
  }
}.send(user, bot)
```

Дополнительные опции, применимые к клавиатуре, можно найти в [`ReplyKeyboardMarkupOptions`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.options/-reply-keyboard-markup-options/index.html).

Более подробную информацию о методах можно найти в [документации](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.builders/-reply-keyboard-markup-builder/index.html).

В основном удобно использовать DSL для сбора разметки клавиатуры, но при необходимости вы также можете добавить разметку вручную.

```kotlin
message{ "*Test*" }.markup {
    InlineKeyboardMarkup(
        InlineKeyboardButton("test", callbackData = "testCallback")
    )
}.send(user, bot)

```

```kotlin
message{ "*Test*" }.markup {
    ReplyKeyboardMarkup(
        KeyboardButton("Test menu button")
    )
}.send(user, bot)
```

### Entities
Также существует метод для отправки [`MessageEntity`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.msg/-message-entity/index.html).

Пример использования:

```kotlin
message{ "Test \$hello" }.replyKeyboardMarkup {
    +"Test menu button"
}.entities {
    5 to 15 url "https://google.com" // добавить TextLink
    entity(EntityType.Bold, 0, 4)
    entity(EntityType.Cashtag, 5, 5) // обратный слеш не считается (потому что используется для компилятора)
}.send(user, bot)
```

#### Контекстные entities.

Entities также могут быть добавлены через контекст некоторых конструкций, они помечены специальным интерфейсом [EntitiesContextBuilder](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.builders/-entities-ctx-builder/index.html), который также присутствует в feature caption.

Пример использования:

```kotlin
message { "usual text " - bold { "this is bold text" } - " continue usual" }.send(user, bot)
```

Поддерживаются все виды [entity types](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.msg/-entity-type/index.html).

### Caption
Также метод `caption` может использоваться для добавления подписей к медиафайлам.

Пример использования:

```kotlin
photo { "FILE_ID" }.caption { "Test caption" }.send(user, bot)
```


### См. также

* [Bot context](Bot-Context.md)
* [FSM | Conversation handling](FSM-and-Conversation-handling.md)