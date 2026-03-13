---
---
title: Обновление парсинга
---

### Текстовая полезная нагрузка

Некоторые обновления могут иметь текстовую полезную нагрузку, которую можно распарсить для дальнейшей обработки. Рассмотрим их:

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

Из перечисленных обновлений выбирается определенный параметр и принимается как [`TextReference`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-text-reference/index.html) для дальнейшего парсинга.

### Парсинг

Выбранные параметры парсятся с помощью соответствующих настроенных разделителей в команду и параметры к ней.

См. конфигурацию блока [`commandParsing`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.configuration/-bot-configuration/command-parsing.html).

Вы можете увидеть на диаграмме ниже, какие компоненты сопоставлены с какими частями целевой функции.

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/7489099a-cca8-4049-a374-efaf6ce52128" alt="Диаграмма парсинга текста" />
</p>

### @ParamMapping

Также существует аннотация [`@ParamMapping`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-param-mapping/index.html) для удобства или для любого особого случая.

Она позволяет сопоставить имя параметра из входящего текста с любым параметром.

Это также удобно, когда ваши входящие данные ограничены, например, `CallbackData` (64 символа).

Пример использования:
`greeting?name=Adam`

```kotlin
@CommandHandler(["greeting"])
suspend fun greeting(@ParamMapping("name") anyParameterName: String, user: User, bot: TelegramBot) {
    message { "Hello, $anyParameterName" }.send(to = user, via = bot)
}
```

А также может использоваться для перехвата безымянных параметров в случаях, когда парсер настроен таким образом, что имена параметров пропускаются или даже отсутствуют, что проходит по шаблону 'param_n', где `n` - его порядковый номер.

Например, такой текст - `myCommand?p1=v1&v2&p3=&p4=v4&p5=`, будет распарсен как:
* команда - `myCommand`
* параметры
  * `p1` = `v1`
  * `param_2` = `v2`
  * `p3` = ``
  * `p4` = `v4`
  * `p5` = ``

Как видите, так как второй параметр не имеет объявленного имени, он представлен как `param_2`.

Таким образом вы можете сокращать имена переменных в обратном вызове и использовать понятные читаемые имена в коде.

### Deeplink

Учитывая информацию выше, если вы ожидаете deeplink в вашей стартовой команде, вы можете его перехватить с помощью:

```kotlin
@CommandHandler(["/start"])
suspend fun start(@ParamMapping("param_1") deeplink: String?, user: User, bot: TelegramBot) {
    message { "deeplink is $deeplink" }.send(to = user, via = bot)
}
```

### Групповые команды

В конфигурации `commandParsing` у нас есть параметр [`useIdentifierInGroupCommands`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.configuration/-command-parsing-configuration/use-identifier-in-group-commands.html). Когда он включен, мы можем использовать `TelegramBot.identifier` (не забудьте изменить его, если вы используете описанный параметр) в процессе сопоставления команд. Это помогает разделять похожие команды между несколькими ботами. В противном случае часть `@MyBot` просто будет пропущена.

### См. также

* [Вызов активности](Activity-invocation.md)
* [Активности и процессоры](Activites-and-Processors.md)
* [Действия](Actions.md)