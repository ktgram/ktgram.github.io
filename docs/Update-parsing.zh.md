---
title: 更新解析
---

### 文本负载

某些更新可能具有可以解析以进行进一步处理的文本负载。让我们来看一下它们：

* `MessageUpdate` -> `message.text`
* `EditedMessageUpdate` -> `editedMessage.text`
* `ChannelPostUpdate` -> `channelPost.text`
* `EditedChannelPostUpdate` -> `editedChannelPost.text`
* `InlineQueryUpdate` -> `inlineQuery.query`
* `ChosenInlineResultUpdate` -> `chosenInlineResult.query`
* `CallbackQueryUpdate` -> `callbackQuery.data`
* `ShippingQueryUpdate` -> `shippingQuery.invoicePayload`
* `PreCheckoutQueryUpdate` -> `preCheckoutQuery.invoicePayload`
* `PollUpdate` -> `poll.question`
* `PurchasedPaidMediaUpdate` -> `purchasedPaidMedia.paidMediaPayload`

从列出的更新中，选择某个参数并作为 [`TextReference`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.internal/-text-reference/index.html) 进行进一步解析。

### 解析

所选参数使用适当配置的分隔符解析为命令及其参数。

请参见配置 [`commandParsing`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.internal.configuration/-command-parsing-configuration/index.html) 块。

您可以在下面的图表中看到哪些组件映射到目标函数的哪些部分。

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/7489099a-cca8-4049-a374-efaf6ce52128" alt="文本解析图" />
</p>

### @ParamMapping

还有一个名为 [`@ParamMapping`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-param-mapping/index.html) 的注解，用于方便或特殊情况。

它允许您将传入文本中的参数名称映射到任何参数。

当您的传入数据有限时，例如 `CallbackData`（64 个字符），这也很方便。

使用示例：
`greeting?name=Adam`

```kotlin
@CommandHandler(["greeting"])
suspend fun greeting(@ParamMapping("name") anyParameterName: String, user: User, bot: TelegramBot) {
    message { "你好，$anyParameterName" }.send(to = user, via = bot)
}
```

它也可以用于捕获未命名的参数，在解析器设置为跳过参数名称或甚至缺少参数名称的情况下，这些参数将以 'param_n' 模式传递，其中 `n` 是其序号。

例如，以下文本 - `myCommand?p1=v1&v2&p3=&p4=v4&p5=`，将被解析为：
* 命令 - `myCommand`
* 参数
  * `p1` = `v1`
  * `param_2` = `v2`
  * `p3` = ``
  * `p4` = `v4`
  * `p5` = ``

如您所见，由于第二个参数没有声明名称，因此表示为 `param_2`。

因此，您可以在回调中缩写变量名称，并在代码中使用清晰可读的名称。

### 深度链接

考虑到上述信息，如果您期望在启动命令中使用深度链接，可以通过以下方式捕获它：

```kotlin
@CommandHandler(["/start"])
suspend fun start(@ParamMapping("param_1") deeplink: String?, user: User, bot: TelegramBot) {
    message { "深度链接是 $deeplink" }.send(to = user, via = bot)
}
```

### 群组命令

在 `commandParsing` 配置中，我们有参数 [`useIdentifierInGroupCommands`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.internal.configuration/-command-parsing-configuration/use-identifier-in-group-commands.html)，当它开启时，我们可以在命令匹配过程中使用 `TelegramBot.identifier`（如果您使用了描述的参数，请不要忘记更改它），这有助于在多个机器人之间区分相似的命令，否则 `@MyBot` 部分将被跳过。

### 另请参见

* [活动调用](/Activity-invocation)
* [活动与处理器](/Activites-and-Processors)
* [动作](/Actions)