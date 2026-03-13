---
---
title: Actions
---

### 所有请求都是 Actions
所有 Telegram API 请求都是各种类型的 [`TgAction`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.action/-tg-action/index.html) 接口，它们实现了不同的方法，例如 [`SendMessageAction`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.api.message/-send-message-action/index.html)，<br/>这些方法以 [`message()`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.api.message/message.html) 等类型函数的形式包装，以方便库接口的使用。

<p align="center">
    <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/2d097d60-1907-4ca1-8ad3-3ee8d223f8eb" alt="Actions diagram" />
</p>

每个 `Action` 可能具有自己的可用方法，取决于可用的 [`Feature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-feature/index.html)。

### 特性

不同的 actions 可能具有不同的 [`Features`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-feature/index.html)，取决于 Telegram Bot API，例如：
[`OptionsFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-options-feature/index.html),
[`MarkupFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-markup-feature/index.html),
[`EntitiesFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-entities-feature/index.html),
[`CaptionFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-caption-feature/index.html)。

让我们更仔细地了解它们：

### 选项
例如，[`OptionsFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-options-feature/index.html) 用于传递可选参数。

每个 action 都有自己的选项类型，对应的可以在 `Action` 本身的 `options` 参数中看到，在属性部分。<br/>例如，`sendMessage` 包含一个 [`MessageOptions`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.options/-message-options/index.html) 数据类，带有不同的参数作为选项。

使用示例：

```kotlin
message{ "*Test*" }.options {
    parseMode = ParseMode.Markdown
}.send(user, bot)
```
### 标记

还有一种发送标记的方法，支持所有类型的 [keyboards](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.marker/-keyboard/index.html)：<br/>[`ReplyKeyboardMarkup`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-reply-keyboard-markup/index.html), [`InlineKeyboardMarkup`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-inline-keyboard-markup/index.html), [`ForceReply`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-force-reply/index.html), [`ReplyKeyboardRemove`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-reply-keyboard-remove/index.html)。

#### 内联键盘标记

这个构建器允许您构建内联按钮，可以组合任何参数。

```kotlin
message{ "Test" }.inlineKeyboardMarkup {
    "name" callback "callbackData"         //
    "buttonName" url "https://google.com"  //--- 这两个按钮将在同一行。
    newLine() // 或 br()
    "otherButton" webAppInfo "data"       // 这将位于其他行

    // 您还可以在构建器中使用不同的风格：
    callbackData("buttonName") { "callbackData" }
}.send(user, bot)

```

更多详细信息可以在构建器[文档](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.builders/-inline-keyboard-markup-builder/index.html)中看到。

#### 回复键盘标记

这个构建器允许您构建菜单按钮。

```kotlin
message{ "Test" }.replyKeyboardMarkup {
  + "Menu button"     // 您可以使用一元加运算符添加按钮
  + "Menu button 2"
  br() // 转到第二行
  "Send polls 👀" requestPoll true   // 带参数的按钮

  options {
    resizeKeyboard = true
  }
}.send(user, bot)
```

适用于键盘的其他选项可以在 [`ReplyKeyboardMarkupOptions`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.options/-reply-keyboard-markup-options/index.html) 中看到。

有关方法的更多详细信息，请参阅构建器[文档](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.builders/-reply-keyboard-markup-builder/index.html)。

使用 DSL 收集键盘标记通常很方便，但如果需要，您也可以手动添加标记。

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

### 实体
还有一种发送 [`MessageEntity`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.msg/-message-entity/index.html) 的方法。

使用示例：

```kotlin
message{ "Test \$hello" }.replyKeyboardMarkup {
    +"Test menu button"
}.entities {
    5 to 15 url "https://google.com" // 添加 TextLink
    entity(EntityType.Bold, 0, 4)
    entity(EntityType.Cashtag, 5, 5) // 反斜杠不计入（因为编译器使用）
}.send(user, bot)
```

#### 上下文实体

实体也可以通过某些构造的上下文添加，它们标记为特定的 [EntitiesContextBuilder](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.builders/-entities-ctx-builder/index.html) 接口，它也存在于标题特性中。

使用示例：

```kotlin
message { "usual text " - bold { "this is bold text" } - " continue usual" }.send(user, bot)
```

支持所有类型的 [entity types](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.msg/-entity-type/index.html)。

### 标题
此外，`caption` 方法可以用于为媒体文件添加标题。

使用示例：

```kotlin
photo { "FILE_ID" }.caption { "Test caption" }.send(user, bot)
```


### 另请参阅

* [Bot context](Bot-Context.md)
* [FSM | Conversation handling](FSM-and-Conversation-handling.md)