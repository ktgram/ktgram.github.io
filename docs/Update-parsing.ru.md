---
---
title: Разбор обновлений
---

### Текстовая полезная нагрузка

Некоторые обновления могут содержать текстовую полезную нагрузку, которую можно разобрать для дальнейшей обработки. Давайте рассмотрим их:

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

Из перечисленных обновлений выбирается определенный параметр и принимается в качестве [`TextReference`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-text-reference/index.html) для дальнейшего разбора.

### Разбор

Выбранные параметры разбираются с помощью соответствующих настроенных разделителей на команду и параметры к ней.

См. блок конфигурации [`commandParsing`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.configuration/-bot-configuration/command-parsing.html).

Вы можете увидеть на диаграмме ниже, какие компоненты сопоставляются с какими частями целевой функции.

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/7489099a-cca8-4049-a374-efaf6ce52128" alt="Диаграмма разбора текста" />
</p>

### @ParamMapping

Также существует аннотация под названием [`@ParamMapping`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-param-mapping/index.html) для удобства или для любого специального случая.

Она позволяет сопоставить имя параметра из входящего текста с любым параметром.

Это также удобно, когда ваши входящие данные ограничены, например, `CallbackData` (64 символа).

См. пример использования:
`greeting?name=Adam`

```kotlin
@CommandHandler(["greeting"])
suspend fun greeting(@ParamMapping("name") anyParameterName: String, user: User, bot: TelegramBot) {
    message { "Hello, $anyParameterName" }.send(to = user, via = bot)
}
```

А также она может использоваться для перехвата безымянных параметров в случаях, когда парсер настроен таким образом, что имена параметров пропускаются или даже отсутствуют, что передается по шаблону 'param_n', где `n` — его порядковый номер.

Например, такой текст - `myCommand?p1=v1&v2&p3=&p4=v4&p5=`, будет разобран на:
* команда - `myCommand`
* параметры
  * `p1` = `v1`
  * `param_2` = `v2`
  * `p3` = ``
  * `p4` = `v4`
  * `p5` = ``

Как вы можете видеть, поскольку у второго параметра нет объявленного имени, он представлен как `param_2`.

Таким образом, вы можете сократить имена переменных в обратном вызове и использовать понятные читаемые имена в коде.

### Глубокие ссылки

Учитывая информацию выше, если вы ожидаете глубокую ссылку в вашей команде start, вы можете перехватить ее с помощью:

```kotlin
@CommandHandler(["/start"])
suspend fun start(@ParamMapping("param_1") deeplink: String?, user: User, bot: TelegramBot) {
    message { "deeplink is $deeplink" }.send(to = user, via = bot)
}
```

### Команды в группах

В конфигурации `commandParsing` у нас есть параметр [`useIdentifierInGroupCommands`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.configuration/-command-parsing-configuration/use-identifier-in-group-commands.html). Когда он включен, мы можем использовать `TelegramBot.identifier` (не забудьте изменить его, если вы используете описанный параметр) в процессе сопоставления команд. Это помогает разделять похожие команды между несколькими ботами, в противном случае часть `@MyBot` просто будет пропущена.

### См. также

* [Вызов активности](Activity-invocation.md)
* [Активности и процессоры](Activites-and-Processors.md)
* [Действия](Actions.md)