---
---
title: Actions
---

### Semua Permintaan adalah Actions
Semua permintaan api telegram adalah berbagai jenis antarmuka [`TgAction`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.action/-tg-action/index.html) yang mengimplementasikan metode berbeda seperti [`SendMessageAction`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.api.message/-send-message-action/index.html), <br/>yang dibungkus dalam bentuk fungsi bertipe [`message()`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.api.message/message.html) untuk kenyamanan antarmuka library.

<p align="center">
    <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/2d097d60-1907-4ca1-8ad3-3ee8d223f8eb" alt="Actions diagram" />
</p>

Setiap `Action` mungkin memiliki metode yang berbeda-beda, tergantung pada [`Feature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-feature/index.html) yang tersedia.

### Features

Action yang berbeda mungkin memiliki [`Features`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-feature/index.html) yang berbeda tergantung pada Telegram Bot Api, seperti:
[`OptionsFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-options-feature/index.html),
[`MarkupFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-markup-feature/index.html)
[`EntitiesFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-entities-feature/index.html)
[`CaptionFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-caption-feature/index.html).

Mari kita lihat lebih dekat:

### Options
Sebagai contoh, [`OptionsFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-options-feature/index.html) digunakan untuk meneruskan parameter opsional.

Setiap action memiliki jenis opsi sendiri, yang sesuai dapat Anda lihat di `Action` itu sendiri dalam parameter `options`, di bagian properties. <br/>Sebagai contoh, `sendMessage` yang berisi data class [`MessageOptions`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.options/-message-options/index.html) dengan parameter berbeda sebagai opsi.

Contoh penggunaan:

```kotlin
message{ "*Test*" }.options {
    parseMode = ParseMode.Markdown
}.send(user, bot)
```
### Markup

Ada juga metode untuk mengirim markups yang mendukung semua jenis [keyboards](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.marker/-keyboard/index.html): <br/>[`ReplyKeyboardMarkup`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-reply-keyboard-markup/index.html), [`InlineKeyboardMarkup`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-inline-keyboard-markup/index.html), [`ForceReply`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-force-reply/index.html), [`ReplyKeyboardRemove`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-reply-keyboard-remove/index.html).

#### Inline Keyboard Markup

Builder ini memungkinkan Anda membuat tombol inline dengan kombinasi parameter apa pun.

```kotlin
message{ "Test" }.inlineKeyboardMarkup {
    "name" callback "callbackData"         //
    "buttonName" url "https://google.com"  //--- kedua tombol ini akan berada di baris yang sama.
    newLine() // atau br()
    "otherButton" webAppInfo "data"       // ini akan berada di baris lain

    // Anda juga dapat menggunakan gaya berbeda dalam builder:
    callbackData("buttonName") { "callbackData" }
}.send(user, bot)

```

Detail lebih lanjut dapat dilihat di dokumentasi builder [documentation](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.builders/-inline-keyboard-markup-builder/index.html).

#### Reply Keyboard Markup

Builder ini memungkinkan Anda membuat tombol menu.

```kotlin
message{ "Test" }.replyKeyboardMarkup {
  + "Menu button"     // Anda dapat menambahkan tombol dengan menggunakan operator plus unary
  + "Menu button 2"
  br() // pindah ke baris kedua
  "Send polls 👀" requestPoll true   // tombol dengan parameter

  options {
    resizeKeyboard = true
  }
}.send(user, bot)
```

Opsi tambahan yang berlaku untuk keyboard dapat dilihat di [`ReplyKeyboardMarkupOptions`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.options/-reply-keyboard-markup-options/index.html).

Lihat dokumentasi builder [documentation](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.builders/-reply-keyboard-markup-builder/index.html) untuk detail lebih lanjut tentang metode-metode.

Biasanya nyaman menggunakan dsl untuk mengumpulkan keyboard markup, tetapi jika diperlukan, Anda juga dapat menambahkan markup secara manual.

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
Ada juga metode untuk mengirim [`MessageEntity`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.msg/-message-entity/index.html).

Contoh penggunaan:

```kotlin
message{ "Test \$hello" }.replyKeyboardMarkup {
    +"Test menu button"
}.entities {
    5 to 15 url "https://google.com" // tambahkan TextLink
    entity(EntityType.Bold, 0, 4)
    entity(EntityType.Cashtag, 5, 5) // backslash tidak dihitung (karena digunakan untuk compiler)
}.send(user, bot)
```

#### Contextual entities.

Entities juga dapat ditambahkan melalui konteks beberapa konstruksi, mereka diberi label dengan antarmuka [EntitiesContextBuilder](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.builders/-entities-ctx-builder/index.html) tertentu, yang juga hadir dalam fitur caption.

Contoh penggunaan:

```kotlin
message { "usual text " - bold { "this is bold text" } - " continue usual" }.send(user, bot)
```

Semua jenis [entity types](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.msg/-entity-type/index.html) didukung.

### Caption
Juga, metode `caption` dapat digunakan untuk menambahkan caption ke file media.

Contoh penggunaan:

```kotlin
photo { "FILE_ID" }.caption { "Test caption" }.send(user, bot)
```


### Lihat juga

* [Bot context](Bot-Context.md)
* [FSM | Conversation handling](FSM-and-Conversation-handling.md)