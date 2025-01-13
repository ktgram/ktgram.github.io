---
title: Actions
---

### All requests is Actions
All telegram api requests are various kinds of [`TgAction`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.action/-tg-action/index.html) interfaces that implementing different methods such as [`SendMessageAction`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.api.message/-send-message-action/index.html), <br/>which have wrapped in the form of [`message()`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.api.message/message.html) - type functions for the convenience of the library interface.

<p align="center">
    <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/2d097d60-1907-4ca1-8ad3-3ee8d223f8eb" alt="Actions diagram" />
</p>

Each `Action` may be able of having its own possible methods, depending on the available [`Feature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-feature/index.html).

### Features

Different actions may have different [`Features`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-feature/index.html) depending on the Telegram Bot Api, such as:
[`OptionsFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-options-feature/index.html),
[`MarkupFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-markup-feature/index.html)
[`EntitiesFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-entities-feature/index.html)
[`CaptionFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-caption-feature/index.html).

Let's take a closer look at them:

### Options
For example, [`OptionsFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-options-feature/index.html) is used to pass optional parameters.

Each action has its own type of options, the corresponding you can see in the `Action` itself in the `options` parameter, in properties section. <br/>For example, `sendMessage` which contains a [`MessageOptions`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.internal.options/-message-options/index.html) data class with different parameters as options.

Example usage:

```kotlin
message{ "*Test*" }.options {
    parseMode = ParseMode.Markdown
}.send(user, bot)
```
### Markup

There is also a method for sending markups that supports all kind of [keyboards](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.marker/-keyboard/index.html): <br/>[`ReplyKeyboardMarkup`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-reply-keyboard-markup/index.html), [`InlineKeyboardMarkup`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-inline-keyboard-markup/index.html), [`ForceReply`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-force-reply/index.html), [`ReplyKeyboardRemove`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-reply-keyboard-remove/index.html).

#### Inline Keyboard Markup

This builder allows you to construct inline buttons with any combination of parameters.

```kotlin
message{ "Test" }.inlineKeyboardMarkup {
    "name" callback "callbackData"         //
    "buttonName" url "https://google.com"  //--- these two buttons will be in the same row.
    newLine() // or br()
    "otherButton" webAppInfo "data"       // this will be in other row

    // you can also use a different style within the builder:
    callbackData("buttonName") { "callbackData" }
}.send(user, bot)

```

More details can be seen in the builder [documentation](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.builders/-inline-keyboard-markup-builder/index.html).

#### Reply Keyboard Markup

This builder allows you to construct menu buttons.

```kotlin
message{ "Test" }.replyKeyboardMarkup {
  + "Menu button"     // you can add buttons by using unary plus operator
  + "Menu button 2"
  br() // go to second row
  "Send polls 👀" requestPoll true   // button with parameter

  options {
    resizeKeyboard = true
  }
}.send(user, bot)
```

Additional options applicable to the keyboard can be seen in [`ReplyKeyboardMarkupOptions`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.internal.options/-reply-keyboard-markup-options/index.html).

See the builder [documentation](https://vendelieu.github.io/telegram-bot/-telegram%20-bot/eu.vendeli.tgbot.utils.builders/-reply-keyboard-markup-builder/index.html) for more details about the methods.

It's mostly convenient to use dsl for collecting keyboard markup, but if needed, you can also add markup manually.

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
There is also a method for sending [`MessageEntity`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.msg/-message-entity/index.html).

Example usage:

```kotlin
message{ "Test \$hello" }.replyKeyboardMarkup {
    +"Test menu button"
}.entities {
    5 to 15 url "https://google.com" // add TextLink
    entity(EntityType.Bold, 0, 4)
    entity(EntityType.Cashtag, 5, 5) // backslash doesn't count (because it's used for compiler)
}.send(user, bot)
```

#### Contextual entities.

Entities can also be added through the context of some constructs, they are labeled with a specific [EntitiesContextBuilder](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.builders/-entities-ctx-builder/index.html) interface, it is also present in the caption feature.

Example usage:

```kotlin
message { "usual text " - bold { "this is bold text" } - " continue usual" }.send(user, bot)
```

All kinds of [entity types](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.msg/-entity-type/index.html) are supported.

### Caption
Also, the `caption` method can be used to add captions to media files.

Example usage:

```kotlin
photo { "FILE_ID" }.caption { "Test caption" }.send(user, bot)
```


### See also

* [Bot context](./Bot-Context).md
* [FSM | Conversation handling](./FSM-and-Conversation-handling).md
