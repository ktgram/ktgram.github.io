---
---
title: Utilitas dan Tips Berguna
---


### Operasi dengan ProcessedUpdate

[`ProcessedUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processed-update/index.html) adalah kelas generik untuk pembaruan yang, tergantung pada data asli, dapat disediakan dalam berbagai tipe ([`MessageUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-message-update/index.html), [`CallbackQueryUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-callback-query-update/index.html), dll.)

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

Jika diperlukan di dalamnya selalu ada [`update`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types/-update/index.html) asli dalam parameter update.


### Injeksi dependensi

Pustaka menggunakan mekanisme sederhana untuk menginisialisasi kelas di mana metode pemrosesan pembaruan Anda dianotasi dengan anotasi yang disediakan.

[`ClassManagerImpl`](https://github.com/vendelieu/telegram-bot/blob/master/telegram-bot/src/commonMain/kotlin/eu/vendeli/tgbot/implementations/ClassManagerImpl.kt) digunakan secara default untuk memanggil metode yang dianotasi.

Tetapi jika Anda ingin menggunakan beberapa pustaka lain untuk itu Anda dapat mendefinisikan ulang antarmuka [`ClassManager`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-manager/index.html), <br/>menggunakan mekanisme pilihan Anda dan meneruskannya saat menginisialisasi bot.

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.controllers") {
        classManager = ClassManagerImpl()
    }

    bot.handleUpdates()
}
```

### Memfilter pembaruan

Jika tidak ada kondisi kompleks Anda dapat dengan mudah memfilter beberapa pembaruan untuk diproses:

```kotlin
// fungsi di mana kondisi penyaringan pembaruan didefinisikan
fun filteringFun(update: Update): Boolean = update.message?.text.isNullOrBlank()

fun main() = runBlocking {
  val bot = TelegramBot("BOT_TOKEN")

  // menetapkan alur pemrosesan yang lebih spesifik untuk pembaruan
  bot.update.setListener {
    if(filteringFun(it)) return@setListener

    // jadi sederhana, jika listener meninggalkan scope sebelum mencapai fungsi handler, itu adalah penyaringan.
    // sebenarnya Anda bahkan bisa langsung menulis if-condition di sana dengan return@setListener atau memperluas penyaringan ke kelas terpisah.

    handle(it) // atau cara penanganan manual dengan block
  }
}
```

untuk menyertakan penyaringan dalam proses pencocokan atau pengecualian perintah Anda lihat guards atau `@CommonHandler`.

### Opsi generalisasi untuk metode berbeda

Jika Anda harus menerapkan parameter opsional yang sama sering, Anda dapat menulis fungsi serupa yang sesuai dengan Anda dan meringankan kode boilerplate :)

Beberapa properti umum dipisahkan ke [antarmuka berbeda](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.options/-options/index.html).

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


// ... dan di kode Anda

message { "test" }.markdownMode().send(to, via)

```