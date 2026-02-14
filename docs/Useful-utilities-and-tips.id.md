---
---
title: Utilities dan Tips Berguna
---


### Beroperasi dengan ProcessedUpdate

[`ProcessedUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processed-update/index.html) adalah kelas generik untuk pembaruan yang, tergantung pada data asli, dapat disediakan dalam tipe berbeda ([`MessageUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-message-update/index.html), [`CallbackQueryUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-callback-query-update/index.html), dll.)

Jadi Anda dapat memeriksa tipe data masuk dan lebih lanjut memanipulasi data tertentu dengan smartcasts, misalnya:

```kotlin
// ...
if (update !is MessageUpdate) {
    message { "Only messages are allowed" }.send(user, bot)
    return
}
// Selanjutnya, ProcessedUpdate akan dianggap sebagai MessageUpdate.
```

Ada juga antarmuka [`UserReference`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-user-reference/index.html) di dalamnya yang memungkinkan Anda menentukan apakah ada referensi pengguna di dalamnya, contoh penggunaan:

```kotlin
val user = if(update is UserReference) update.user else null

```

Jika diperlukan di dalamnya selalu ada [`update`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types/-update/index.html) asli di parameter update.


### Dependency injection

Pustaka menggunakan mekanisme sederhana untuk menginisialisasi kelas di mana metode pemrosesan pembaruan Anda diannotasi dengan anotasi yang disediakan.

[`ClassManagerImpl`](https://github.com/vendelieu/telegram-bot/blob/master/telegram-bot/src/commonMain/kotlin/eu/vendeli/tgbot/implementations/ClassManagerImpl.kt) digunakan secara default untuk memanggil metode yang diannotasi.

Tetapi jika Anda ingin menggunakan beberapa pustaka lain untuk itu Anda dapat mendefinisikan ulang antarmuka [`ClassManager`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-manager/index.html), <br/>menggunakan mekanisme pilihan Anda dan meneruskannya saat menginisialisasi bot.

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.controllers") {
        classManager = ClassManagerImpl()
    }

    bot.handleUpdates()
}
```

### Filtering updates

Jika tidak ada kondisi kompleks Anda dapat dengan sederhana memfilter beberapa pembaruan untuk diproses:

```kotlin
// fungsi di mana kondisi filtering pembaruan didefinisikan
fun filteringFun(update: Update): Boolean = update.message?.text.isNullOrBlank()

fun main() = runBlocking {
  val bot = TelegramBot("BOT_TOKEN")

  // menetapkan aliran pemrosesan yang lebih spesifik untuk pembaruan
  bot.update.setListener {
    if(filteringFun(it)) return@setListener

    // jadi sederhana, jika listener keluar dari scope sebelum mencapai fungsi handler, itu adalah filtering.
    // sebenarnya Anda bahkan bisa langsung menulis if-condition di sana dengan return@setListener atau memperluas filtering ke kelas terpisah.

    handle(it) // atau cara penanganan manual dengan block
  }
}
```

untuk menyertakan filtering dalam proses pencocokan atau pengecualian perintah Anda lihat guards atau `@CommonHandler`.

### Generalize options untuk metode yang berbeda

Jika Anda harus menerapkan parameter opsional yang sama sering, Anda dapat menulis fungsi serupa yang sesuai untuk Anda dan meringankan kode boilerplate :)

Beberapa properti umum dipisahkan ke [antarmuka yang berbeda](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.options/-options/index.html).

```kotlin
@Suppress("NOTHING_TO_INLINE")
inline fun <T, R, O> T.markdownMode(crossinline block: O.() -> Unit = {}): T
        where               T : TgAction<R>,
                            T : OptionsFeature<T, O>,
                            O : Options,
                            O : OptionsParseMode =
    options {
        parseMode = ParseMode.Markdown
        block()
    }


// ... dan dalam kode Anda

message { "test" }.markdownMode().send(to, via)

```