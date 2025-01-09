---
title: 动作
---

### 所有请求是动作
所有的 Telegram API 请求都是各种类型的 [`TgAction`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.action/-tg-action/index.html) 接口，实施不同的方法，如 [`SendMessageAction`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.api.message/-send-message-action/index.html)， <br/>
这些方法以 [`message()`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.api.message/message.html) - 类型函数的形式封装，以方便库接口的使用。

<p align="center">
    <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/2d097d60-1907-4ca1-8ad3-3ee8d223f8eb" alt="动作图" />
</p>

每个 `Action` 可能具有自己的可能方法，具体取决于可用的 [`Feature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-feature/index.html)。

### 特性

不同的动作可能具有不同的 [`Features`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-feature/index.html)，具体取决于 Telegram Bot API，例如：
[`OptionsFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-options-feature/index.html)，
[`MarkupFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-markup-feature/index.html)
[`EntitiesFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-entities-feature/index.html)
[`CaptionFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-caption-feature/index.html)。

让我们仔细看看它们：

### 选项
例如，[`OptionsFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-options-feature/index.html) 用于传递可选参数。

每个动作都有自己类型的选项，您可以在 `Action` 本身的 `options` 参数中看到相应的内容，在属性部分。 <br/>
例如，`sendMessage` 包含一个 [`MessageOptions`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.internal.options/-message-options/index.html) 数据类，具有不同的参数作为选项。

示例用法：

```kotlin
message{ "*测试*" }.options {
    parseMode = ParseMode.Markdown
}.send(user, bot)
```
### 标记

还有一种发送标记的方法，支持所有类型的 [键盘](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.marker/-keyboard/index.html)： <br/>
[`ReplyKeyboardMarkup`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-reply-keyboard-markup/index.html)， [`InlineKeyboardMarkup`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-inline-keyboard-markup/index.html)， [`ForceReply`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-force-reply/index.html)， [`ReplyKeyboardRemove`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-reply-keyboard-remove/index.html)。

#### 内联键盘标记

此构建器允许您构建具有任意参数组合的内联按钮。

```kotlin
message{ "测试" }.inlineKeyboardMarkup {
    "名称" callback "回调数据"         //
    "按钮名称" url "https://google.com"  //--- 这两个按钮将位于同一行。
    newLine() // 或 br()
    "其他按钮" webAppInfo "数据"       // 这将位于其他行

    // 您还可以在构建器中使用不同的样式：
    callbackData("按钮名称") { "回调数据" }
}.send(user, bot)

```

更多详细信息可以在构建器 [文档](https://vendelieu.github.io/telegram-bot/telegram -bot/eu.vendeli.tgbot.utils.builders/-inline-keyboard-markup-builder/index.html) 中查看。

#### 回复键盘标记

此构建器允许您构建菜单按钮。

```kotlin
message{ "测试" }.replyKeyboardMarkup {
  + "菜单按钮"     // 您可以使用一元加运算符添加按钮
  + "菜单按钮 2"
  br() // 转到第二行
  "发送投票 👀" requestPoll true   // 带参数的按钮

  options {
    resizeKeyboard = true
  }
}.send(user, bot)
```

适用于键盘的其他选项可以在 [`ReplyKeyboardMarkupOptions`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.internal.options/-reply-keyboard-markup-options/index.html) 中查看。

有关方法的更多详细信息，请参见构建器 [文档](https://vendelieu.github.io/telegram-bot/-telegram%20-bot/eu.vendeli.tgbot.utils.builders/-reply-keyboard-markup-builder/index.html)。

使用 DSL 收集键盘标记通常更方便，但如果需要，您也可以手动添加标记。

```kotlin
message{ "*测试*" }.markup {
    InlineKeyboardMarkup(
        InlineKeyboardButton("测试", callbackData = "testCallback")
    )
}.send(user, bot)

```

```kotlin
message{ "*测试*" }.markup {
    ReplyKeyboardMarkup(
        KeyboardButton("测试菜单按钮")
    )
}.send(user, bot)
```

### 实体
还有一种发送 [`MessageEntity`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.msg/-message-entity/index.html) 的方法。

示例用法：

```kotlin
message{ "测试 <br/>$hello" }.replyKeyboardMarkup {
    +"测试菜单按钮"
}.entities {
    5 to 15 url "https://google.com" // 添加文本链接
    entity(EntityType.Bold, 0, 4)
    entity(EntityType.Cashtag, 5, 5) // 反斜杠不计入（因为它用于编译器）
}.send(user, bot)
```

#### 上下文实体。

实体也可以通过某些构造的上下文添加，它们用特定的 [EntitiesContextBuilder](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.builders/-entities-ctx-builder/index.html) 接口标记，它也出现在标题特性中。

示例用法：

```kotlin
message { "普通文本 " - bold { "这是粗体文本" } - " 继续普通" }.send(user, bot)
```

所有类型的 [实体类型](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.msg/-entity-type/index.html) 都受支持。

### 标题
此外，`caption` 方法可用于为媒体文件添加标题。

示例用法：

```kotlin
photo { "FILE_ID" }.caption { "测试标题" }.send(user, bot)
```


### 另请参见

* [Bot 上下文](/Bot-Context)
* [FSM | 对话处理](/FSM-and-Conversation-handling)