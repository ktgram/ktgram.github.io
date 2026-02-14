---
---
title: Análise de Atualizações
---

### Payload de Texto

Determinadas atualizações podem ter payload de texto que pode ser analisado para processamento adicional. Vamos dar uma olhada nelas:

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

A partir das atualizações listadas, um determinado parâmetro é selecionado e tomado como [`TextReference`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-text-reference/index.html), para análise adicional.

### Análise

Os parâmetros selecionados são analisados com os delimitadores configurados apropriados em comando e parâmetros para ele.

Veja o bloco de configuração [`commandParsing`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.configuration/-bot-configuration/command-parsing.html).

Você pode ver no diagrama abaixo quais componentes são mapeados para quais partes da função alvo.

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/7489099a-cca8-4049-a374-efaf6ce52128" alt="Diagrama de análise de texto" />
</p>

### @ParamMapping

Há também uma anotação chamada [`@ParamMapping`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-param-mapping/index.html) para conveniência ou para qualquer caso especial.

Ela permite mapear o nome do parâmetro do texto de entrada para qualquer parâmetro.

Isto também é conveniente quando seus dados de entrada são limitados, por exemplo, `CallbackData` (64 caracteres).

Veja exemplo de uso:
`greeting?name=Adam`

```kotlin
@CommandHandler(["greeting"])
suspend fun greeting(@ParamMapping("name") anyParameterName: String, user: User, bot: TelegramBot) {
    message { "Hello, $anyParameterName" }.send(to = user, via = bot)
}
```

E também pode ser usado para capturar parâmetros não nomeados, em casos onde o analisador é configurado de forma que nomes de parâmetros são ignorados ou mesmo ausentes, o que passa pelo padrão 'param_n', onde `n` é seu ordinal.

Por exemplo, tal texto - `myCommand?p1=v1&v2&p3=&p4=v4&p5=`, será analisado como:
* comando - `myCommand`
* parâmetros
  * `p1` = `v1`
  * `param_2` = `v2`
  * `p3` = ``
  * `p4` = `v4`
  * `p5` = ``

Como você pode ver, desde o segundo parâmetro não tem nome declarado, ele é representado como `param_2`.

Assim você pode abreviaar os nomes de variáveis no callback em si e usar nomes claros e legíveis no código.

### Deeplink

Considerando as informações acima, se você espera um deeplink em seu comando start, você pode capturá-lo com:

```kotlin
@CommandHandler(["/start"])
suspend fun start(@ParamMapping("param_1") deeplink: String?, user: User, bot: TelegramBot) {
    message { "deeplink is $deeplink" }.send(to = user, via = bot)
}
```

### Comandos de Grupo

Na configuração `commandParsing` temos o parâmetro [`useIdentifierInGroupCommands`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.configuration/-command-parsing-configuration/use-identifier-in-group-commands.html) quando está ativado, podemos usar `TelegramBot.identifier` (não se esqueça de alterá-lo se você está usando o parâmetro descrito) no processo de correspondência de comando, isso ajuda a separar comandos similares entre vários bots, caso contrário a parte `@MyBot` será simplesmente ignorada.

### Veja também

* [Invocação de Atividade](Activity-invocation.md)
* [Atividades & Processadores](Activites-and-Processors.md)
* [Ações](Actions.md)