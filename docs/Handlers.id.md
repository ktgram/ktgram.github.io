---
---
title: Handlers
---


### Variety of Handlers

Dalam pengembangan bot, terutama pada sistem yang melibatkan interaksi pengguna, penting untuk mengelola dan memproses perintah serta peristiwa secara efisien.

Anotasi‑an ini menandai fungsi yang dirancang untuk memproses perintah, masukan, atau pembaruan tertentu dan menyediakan metadata seperti kata kunci perintah, ruang lingkup, dan guard.

### Annotations Overview

#### CommandHandler

Anotasi `CommandHandler` digunakan untuk menandai fungsi yang memproses perintah tertentu. Anotasi ini mencakup properti yang mendefinisikan kata kunci dan ruang lingkup perintah.

-   **value**: Menentukan kata kunci yang terkait dengan perintah.
-   **scope**: Menentukan konteks atau ruang lingkup di mana perintah akan diperiksa.

```kotlin
@CommandHandler(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommandHandler.CallbackQuery

Versi khusus dari anotasi `CommandHandler` yang dirancang khusus untuk menangani callback query. Ini mencakup properti serupa dengan `CommandHandler`, dengan fokus pada perintah yang terkait dengan callback.

_Ini sebenarnya sama dengan `@CommandHandler` dengan ruang lingkup `UpdateType.CALLBACK_QUERY` yang telah ditetapkan sebelumnya_.

-   **value**: Menentukan kata kunci yang terkait dengan perintah.
-   **autoAnswer**: Membalas `callbackQuery` secara otomatis (memanggil `answerCallbackQuery` sebelum penanganan).

```kotlin
@CommandHandler.CallbackQuery(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### CommonHandler

Anotasi `CommonHandler` ditujukan untuk fungsi yang memproses perintah dengan prioritas lebih rendah dibandingkan `CommandHandler` dan `InputHandler`. Anotasi ini digunakan pada level sumber dan menyediakan cara fleksibel untuk mendefinisikan handler perintah umum.

**Perhatikan, prioritas bekerja hanya di dalam `@CommonHandler` sendiri (yaitu tidak memengaruhi handler lain).**

##### CommonHandler.Text

Anotasi ini menentukan pencocokan teks terhadap pembaruan. Ini mencakup properti untuk mendefinisikan teks yang dicocokkan, kondisi penyaringan, prioritas, dan ruang lingkup.

-   **value**: Teks yang akan dicocokkan dengan pembaruan yang masuk.
-   **filter**: Kelas yang mendefinisikan kondisi yang digunakan dalam proses pencocokan.
-   **priority**: Tingkat prioritas handler, di mana 0 adalah prioritas tertinggi.
-   **scope**: Konteks atau ruang lingkup di mana pencocokan teks akan diperiksa.

```kotlin
@CommonHandler.Text(["text"], filter = isNewUserFilter::class, priority = 10)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommonHandler.Regex

Mirip dengan `CommonHandler.Text`, anotasi ini digunakan untuk mencocokkan pembaruan berdasarkan ekspresi reguler. Ini mencakup properti untuk mendefinisikan pola regex, opsi, kondisi penyaringan, prioritas, dan ruang lingkup.

-   **value**: Pola regex yang digunakan untuk pencocokan.
-   **options**: Opsi regex yang mengubah perilaku pola regex.
-   **filter**: Kelas yang mendefinisikan kondisi yang digunakan dalam proses pencocokan.
-   **priority**: Tingkat prioritas handler, di mana 0 adalah prioritas tertinggi.
-   **scope**: Konteks atau ruang lingkup di mana pencocokan regex akan diperiksa.

```kotlin
@CommonHandler.Regex("^\d+$", scope = [UpdateType.EDITED_MESSAGE])
suspend fun test(update: EditedMessageUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### InputHandler

Anotasi `InputHandler` menandai fungsi yang memproses peristiwa masukan tertentu. Anotasi ini ditujukan untuk fungsi yang menangani masukan pada waktu berjalan dan mencakup properti untuk mendefinisikan kata kunci masukan serta ruang lingkup.

-   **value**: Menentukan kata kunci yang terkait dengan peristiwa masukan.

```kotlin
@InputHandler("text")
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UnprocessedHandler

Anotasi `UnprocessedHandler` digunakan untuk menandai fungsi yang menangani pembaruan yang tidak diproses oleh handler lain. Anotasi ini memastikan bahwa setiap pembaruan yang tidak diproses dikelola secara tepat, dengan hanya satu titik pemrosesan yang memungkinkan untuk tipe handler ini.

```kotlin
@UnprocessedHandler
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UpdateHandler

Anotasi `UpdateHandler` menandai fungsi yang menangani jenis pembaruan masuk tertentu. Ini menyediakan cara untuk mengkategorikan dan memproses berbagai tipe pembaruan secara sistematis.

-   **type**: Menentukan jenis pembaruan yang akan diproses oleh fungsi handler.
-   **messageKind** *(added in 9.5)*: Set opsional dari [`MessageKind`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-message-kind/index.html)s yang mempersempit dispatch ke pembaruan yang mengandung pesan dengan jenis yang terdeteksi cocok. Kosong (default) berarti semua jenis cocok.

```kotlin
@UpdateHandler([UpdateType.PRE_CHECKOUT_QUERY])
suspend fun test(update: PreCheckoutQueryUpdate, user: User, bot: TelegramBot) {
    //...
}
```

##### Filtering by `MessageKind`

Gunakan parameter `messageKind` untuk bereaksi hanya pada subset tertentu dari pembaruan pesan (foto, teks, peristiwa layanan, …) alih‑alih memeriksa bidang nullable secara manual:

```kotlin
@UpdateHandler(type = [UpdateType.MESSAGE], messageKind = [MessageKind.PHOTO])
suspend fun onPhoto(update: MessageUpdate, bot: TelegramBot) {
    //...
}
```
### Handler Companion Annotations

Ada juga anotasi tambahan yang opsional untuk handler, melengkapi perilaku opsional dari handler itu sendiri.

Mereka dapat ditempatkan baik pada fungsi yang diterapkan handler maupun pada kelas; pada kasus kelas, mereka akan secara otomatis diterapkan ke semua handler dalam kelas tersebut, namun bila diperlukan dapat memiliki perilaku terpisah untuk beberapa fungsi.

Misalnya, penerapan memiliki prioritas seperti ini, `Function` > `Class`, di mana fungsi memiliki prioritas lebih tinggi.

#### Rate Limiting

Selain itu, mari juga mengungkap mekanisme rate limiting yang dijelaskan dalam anotasi‑an.

Anda dapat mengatur batas umum untuk setiap pengguna:

```kotlin
// ...
val bot = TelegramBot("BOT_TOKEN") {
    rateLimiter { // general limits
        limits = RateLimits(period = 10000, rate = 5)
    }
}
```

###### Handler specific

Batas pada aksi tertentu dapat didefinisikan menggunakan anotasi `RateLimits`, didukung oleh `@CommandHandler`, `@CommandHandler.CallbackQuery`, `@InputHandler`, `@CommonHandler`.

```kotlin
@CommandHandler(["/start"])
@RateLimits(period = 1000L, rate = 1L)
suspend fun start(user: User, bot: TelegramBot) {
    // ...
}
```

#### Guard

Anda dapat mendefinisikan guard secara terpisah untuk mengontrol akses ke handler, didukung oleh `@CommandHandler`, `@CommandHandler.CallbackQuery`, `@InputHandler` :

```kotlin
@CommandHandler(["text"])
@Guard(isAdminGuard::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### ArgParser

Anda dapat mendefinisikan parser argumen khusus secara terpisah untuk mengubah perilaku parsing parameter bagi handler, didukung oleh `@CommandHandler`, `@CommandHandler.CallbackQuery`, `@CommonHandler`:

```kotlin
@CommandHandler(["text"])
@ArgParser(SpaceArgParser::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

**see also [`defaultArgParser`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.common/default-arg-parser.html)**

### Functional DSL

Setiap anotasi di atas memiliki pasangan dalam **Functional DSL**, cara alternatif untuk mendeklarasikan handler pada waktu berjalan via `bot.setFunctionality { … }`. Kedua pendekatan berbagi `ActivityRegistry` yang sama dan dapat digabungkan secara bebas dalam bot yang sama.

| Annotation | DSL counterpart |
|------------|-----------------|
| `@CommandHandler` | `onCommand(...)` |
| `@CommandHandler.CallbackQuery` | `onCommand(..., scope = [UpdateType.CALLBACK_QUERY])` |
| `@InputHandler` / input chains | `onInput(...)` / `inputChain(...)` |
| `@CommonHandler` | `common(...)` |
| `@UpdateHandler` | `onUpdate(...)` |
| `@UnprocessedHandler` | `whenNotHandled { ... }` |

Contoh minimal:

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

    bot.setFunctionality {
        onChosenInlineResult {
            println("got a result ${update.chosenInlineResult.resultId} from ${update.user}")
        }
    }
}
```

### Commands

```kotlin
bot.setFunctionality {
    // Regular command
    onCommand("/start") {
        message { "Hello" }.send(user, bot)
    }

    // Regex-based command matching
    onCommand("""(red|green|blue)""".toRegex()) {
        message { "you typed ${update.text} color" }.send(user, bot)
    }
}
```

Di dalam blok `onCommand`, parameter yang diparsing tersedia sebagai `Map<String, String>` yang dibentuk oleh konfigurasi `commandParsing` yang aktif.

### Inputs

```kotlin
bot.setFunctionality {
    onCommand("/start") {
        message { "Hello, what's your name?" }.send(user, bot)
        bot.inputListener[user] = "testInput"
    }

    onInput("testInput") {
        message { "Hey, nice to meet you, ${update.text}" }.send(user, bot)
    }
}
```

Lihat [`bot.inputListener`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot/-telegram-bot/input-listener.html) untuk API penyimpanan.

#### Input chains

Untuk alur masukan multi‑langkah gunakan `inputChain`:

```kotlin
bot.setFunctionality {
    inputChain("conversation") {
        message { "Nice to meet you, ${update.text}" }.send(user, bot)
        message { "What is your favorite food?" }.send(user, bot)
    }.breakIf({ update.text == "peanut butter" }) {     // chain break condition
        message { "Oh, too bad, I'm allergic to it." }.send(user, bot)
    }.andThen {
        // next step when the break condition didn't match
        message { "Great choice!" }.send(user, bot)
    }
}
```

Rantai secara otomatis melanjutkan kecuali kondisi break terpenuhi; ketika `repeat = true` (default), break yang cocok akan menjaga pengguna pada langkah saat ini.

> Untuk alur multi‑langkah yang lebih kaya dengan status bertipe dan validasi, sebaiknya gunakan [`@WizardHandler`](FSM-and-Conversation-handling.md) sebagai gantinya.

### Update type handlers

```kotlin
bot.setFunctionality {
    onUpdate(UpdateType.MESSAGE, UpdateType.CALLBACK_QUERY) {
        println("Received update: ${update.type}")
    }
}
```

### Common matchers

```kotlin
bot.setFunctionality {
    common("hello") {
        message { "Hi there!" }.send(user, bot)
    }

    common("""\d+""".toRegex()) {
        message { "You sent a number!" }.send(user, bot)
    }
}
```

### Fallback handler

```kotlin
bot.setFunctionality {
    whenNotHandled {
        message { "I didn't understand that." }.send(user, bot)
    }
}
```

### Companion options

Rate limits, guard, dan parser argumen diteruskan langsung sebagai parameter bernama alih‑alih anotasi terpisah:

```kotlin
bot.setFunctionality {
    onCommand("/expensive", rateLimits = RateLimits(rate = 5, period = 60_000)) {
        message { "Processing..." }.send(user, bot)
    }

    onCommand("/admin", guard = AdminGuard::class) {
        message { "Admin command executed" }.send(user, bot)
    }

    onCommand("/custom", argParser = CustomArgParser::class) {
        message { "Parameters: $parameters" }.send(user, bot)
    }
}
```

### Combining DSL and annotations

Kedua gaya dapat hidup berdampingan — didaftarkan dengan cara yang sama, didispatch dengan cara yang sama:

```kotlin
@CommandHandler(["/register"])
suspend fun register(user: User, bot: TelegramBot) {
    message { "Registration started" }.send(user, bot)
}

bot.setFunctionality {
    onCommand("/help") {
        message { "Available commands: /register, /help" }.send(user, bot)
    }
}
```

### Conclusion

Anotasi‑an ini menyediakan alat yang kuat dan fleksibel untuk menangani perintah, masukan, dan peristiwa, sambil memungkinkan konfigurasi terpisah untuk rate limits dan guard, meningkatkan struktur keseluruhan serta pemeliharaan pengembangan bot.

### See also

* [Activities & Processors](Activites-and-Processors.md)
* [Activity invocation](Activity-invocation.md)
* [FSM and Conversation handling](FSM-and-Conversation-handling.md)
* [Sessions](Sessions.md)
* [Update parsing](Update-parsing.md)

---