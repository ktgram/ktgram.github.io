---
---
title: Update Parsing
---

### Text payload

Beberapa update mungkin memiliki payload teks yang dapat diparsing untuk pemrosesan lebih lanjut. Mari kita lihat mereka:

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

Dari update yang terdaftar, parameter tertentu dipilih dan diambil sebagai [`TextReference`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-text-reference/index.html), untuk parsing lebih lanjut.

### Parsing

Parameter yang dipilih diparsing dengan delimiter yang dikonfigurasi dengan tepat menjadi perintah dan parameter untuknya.

Lihat konfigurasi blok [`commandParsing`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.configuration/-bot-configuration/command-parsing.html).

Anda dapat melihat pada diagram di bawah komponen mana yang dipetakan ke bagian mana dari fungsi target.

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/7489099a-cca8-4049-a374-efaf6ce52128" alt="Text parsing diagram" />
</p>

### @ParamMapping

Ada juga anotasi yang disebut [`@ParamMapping`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-param-mapping/index.html) untuk kenyamanan atau untuk kasus khusus.

Ini memungkinkan Anda memetakan nama parameter dari teks masuk ke parameter apa pun.

Ini juga nyaman ketika data masuk Anda terbatas, misalnya, `CallbackData` (64 karakter).

Lihat contoh penggunaan:
`greeting?name=Adam`

```kotlin
@CommandHandler(["greeting"])
suspend fun greeting(@ParamMapping("name") anyParameterName: String, user: User, bot: TelegramBot) {
    message { "Hello, $anyParameterName" }.send(to = user, via = bot)
}
```

Dan juga dapat digunakan untuk menangkap parameter tak bernama, dalam kasus di mana parser diatur sedemikian rupa sehingga nama parameter dilewati atau bahkan tidak ada, yang dilewati dengan pola 'param_n', di mana `n` adalah ordinalnya.

Sebagai contoh teks seperti itu - `myCommand?p1=v1&v2&p3=&p4=v4&p5=`, akan diparsing menjadi:
* command - `myCommand`
* parameters
  * `p1` = `v1`
  * `param_2` = `v2`
  * `p3` = ``
  * `p4` = `v4`
  * `p5` = ``

Seperti yang Anda lihat karena parameter kedua tidak memiliki nama yang dideklarasikan, itu direpresentasikan sebagai `param_2`.

Jadi Anda dapat menyingkat nama variabel dalam callback itu sendiri dan menggunakan nama yang jelas dan mudah dibaca dalam kode.

### Deeplink

Mempertimbangkan informasi dari atas, jika Anda mengharapkan deeplink dalam perintah start Anda, Anda dapat menangkapnya dengan:

```kotlin
@CommandHandler(["/start"])
suspend fun start(@ParamMapping("param_1") deeplink: String?, user: User, bot: TelegramBot) {
    message { "deeplink is $deeplink" }.send(to = user, via = bot)
}
```

### Group commands

Dalam konfigurasi `commandParsing` kita memiliki parameter [`useIdentifierInGroupCommands`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.configuration/-command-parsing-configuration/use-identifier-in-group-commands.html) ketika diaktifkan, kita dapat menggunakan `TelegramBot.identifier` (jangan lupa untuk mengubahnya jika Anda menggunakan parameter yang dijelaskan) dalam proses pencocokan perintah, ini membantu memisahkan perintah serupa antara beberapa bot, jika tidak bagian `@MyBot` hanya akan dilewati.

### See also

* [Activity invocation](Activity-invocation.md)
* [Activities & Processors](Activites-and-Processors.md)
* [Actions](Actions.md)