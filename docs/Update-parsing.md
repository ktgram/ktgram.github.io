---
title: Update Parsing
---

### Text payload

Certain updates may have text payload that can be parsed for further processing. Let's take a look at them:

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

From the listed updates, a certain parameter is selected and taken as [`TextReference`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.internal/-text-reference/index.html), for further parsing.

### Parsing

The selected parameters are parsed with the appropriate configured delimiters into the command and parameters to it.

See configuration [`commandParsing`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.internal.configuration/-command-parsing-configuration/index.html) block.

You can see in the diagram below which components are mapped to which parts of the target function.

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/7489099a-cca8-4049-a374-efaf6ce52128" alt="Text parsing diagram" />
</p>

### @ParamMapping

There is also an annotation called [`@ParamMapping`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-param-mapping/index.html) for convenience or for any special case. 

It allows you to map the name of the parameter from the incoming text to any parameter. 

This is also convenient when your incoming data is limited, for example, `CallbackData` (64 characters).

See example of usage:
`greeting?name=Adam`

```kotlin
@CommandHandler(["greeting"])
suspend fun greeting(@ParamMapping("name") anyParameterName: String, user: User, bot: TelegramBot) {
    message { "Hello, $anyParameterName" }.send(to = user, via = bot)
}
```

And also it can be used for catching unnamed parameters, in cases where the parser is set up such that parameter names are skipped or even they absent, which passes by 'param_n' pattern, where `n` is its ordinal.

For example such text - `myCommand?p1=v1&v2&p3=&p4=v4&p5=`, will be parsed to:
* command - `myCommand`
* parameters
  * `p1` = `v1`
  * `param_2` = `v2`
  * `p3` = ``
  * `p4` = `v4`
  * `p5` = ``

As you can see since second parameter don't have declared name it represented as `param_2`.

So you can abbreviate the variable names in the callback itself and use clear readable names in the code.

### Deeplink

Considering the information from above if you expect deeplink in your start command you can catch it with:

```kotlin
@CommandHandler(["/start"])
suspend fun start(@ParamMapping("param_1") deeplink: String?, user: User, bot: TelegramBot) {
    message { "deeplink is $deeplink" }.send(to = user, via = bot)
}
```

### Group commands

In `commandParsing` configuration we have parameter [`useIdentifierInGroupCommands`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.internal.configuration/-command-parsing-configuration/use-identifier-in-group-commands.html) when it turned on, we can use `TelegramBot.identifier` (don't forget to change it if you are using described parameter) in the command matching process, it helps to separate similar commands between several bots, otherwise the `@MyBot` part will just be skipped. 

### See also

* [Activity invocation](/Activity-invocation)
* [Activities & Processors](/Activites-and-Processors)
* [Actions](/Actions)
