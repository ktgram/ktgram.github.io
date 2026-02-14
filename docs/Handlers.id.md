---
---
title: Handlers
---


### Variety of Handlers

Dalam pengembangan bot, khususnya dalam sistem yang melibatkan interaksi pengguna, sangat penting untuk mengelola dan memproses perintah dan event secara efisien.

Anotasi-anotasi ini menandai fungsi yang dirancang untuk memproses perintah, input, atau update tertentu dan menyediakan metadata seperti kata kunci perintah, scope, dan guards.

### Annotations Overview

#### CommandHandler

Anotasi `CommandHandler` digunakan untuk menandai fungsi yang memproses perintah tertentu. Anotasi ini menyertakan properti yang mendefinisikan kata kunci dan scope perintah.

-   **value**: Menentukan kata kunci yang terkait dengan perintah.
-   **scope**: Menentukan konteks atau scope di mana perintah akan diperiksa.

```kotlin
@CommandHandler(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommandHandler.CallbackQuery

Versi khusus dari anotasi `CommandHandler` yang dirancang khusus untuk menangani callback queries. Ini menyertakan properti yang mirip dengan `CommandHandler`, dengan fokus pada perintah yang terkait callback.

_Sebenarnya sama saja dengan hanya `@CommandHandler` dengan preset `UpdateType.CALLBACK_QUERY` scope_.

-   **value**: Menentukan kata kunci yang terkait dengan perintah.
-   **autoAnswer**: Membalas `callbackQuery` secara otomatis (memanggil `answerCallbackQuery` sebelum penanganan).


```kotlin
@CommandHandler.CallbackQuery(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### CommonHandler

Anotasi `CommonHandler` ditujukan untuk fungsi yang memproses perintah dengan prioritas lebih rendah dibandingkan `CommandHandler` dan `InputHandler`. Ini digunakan pada level sumber dan menyediakan cara fleksibel untuk mendefinisikan common command handlers.

**Perhatikan, prioritas hanya berlaku dalam `@CommonHandler` itu sendiri (tidak mempengaruhi handler lain).**

##### CommonHandler.Text

Anotasi ini menentukan pencocokan teks terhadap update. Ini menyertakan properti untuk mendefinisikan teks yang dicocokkan, kondisi filtering, prioritas, dan scope.

-   **value**: Teks yang dicocokkan dengan update masuk.
-   **filter**: Kelas yang mendefinisikan kondisi yang digunakan dalam proses pencocokan.
-   **priority**: Tingkat prioritas handler, dimana 0 adalah prioritas tertinggi.
-   **scope**: Konteks atau scope di mana pencocokan teks akan diperiksa.

```kotlin
@CommonHandler.Text(["text"], filter = isNewUserFilter::class, priority = 10)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommonHandler.Regex

Mirip dengan `CommonHandler.Text`, anotasi ini digunakan untuk mencocokkan update berdasarkan regular expressions. Ini menyertakan properti untuk mendefinisikan pola regex, opsi, kondisi filtering, prioritas, dan scope.

-   **value**: Pola regex yang digunakan untuk pencocokan.
-   **options**: Opsi regex yang memodifikasi perilaku pola regex.
-   **filter**: Kelas yang mendefinisikan kondisi yang digunakan dalam proses pencocokan.
-   **priority**: Tingkat prioritas handler, dimana 0 adalah prioritas tertinggi.
-   **scope**: Konteks atau scope di mana pencocokan regex akan diperiksa.

```kotlin
@CommonHandler.Regex("^\d+$", scope = [UpdateType.EDITED_MESSAGE])
suspend fun test(update: EditedMessageUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### InputHandler

Anotasi `InputHandler` menandai fungsi yang memproses event input tertentu. Ini ditujukan untuk fungsi yang menangani input saat runtime dan menyertakan properti untuk mendefinisikan kata kunci input dan scope.

-   **value**: Menentukan kata kunci yang terkait dengan event input.

```kotlin
@InputHandler("text")
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UnprocessedHandler

Anotasi `UnprocessedHandler` digunakan untuk menandai fungsi yang menangani update yang tidak diproses oleh handler lain. Ini memastikan bahwa update yang tidak diproses dikelola dengan tepat, dengan hanya satu titik pemrosesan yang mungkin untuk tipe handler ini.

```kotlin
@UnprocessedHandler
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UpdateHandler

Anotasi `UpdateHandler` menandai fungsi yang menangani tipe update masuk tertentu. Ini menyediakan cara untuk mengkategorikan dan memproses berbagai tipe update secara sistematis.

-   **type**: Menentukan tipe update yang akan diproses oleh fungsi handler.

```kotlin
@UpdateHandler([UpdateType.PRE_CHECKOUT_QUERY])
suspend fun test(update: PreCheckoutQueryUpdate, user: User, bot: TelegramBot) {
    //...
}
```
### Handler Companion Annotations

Ada juga anotasi tambahan yang opsional untuk handler, melengkapi perilaku opsional dari handler itu sendiri.

Mereka dapat ditempatkan baik pada fungsi yang handler diterapkan maupun pada kelas, dalam kasus terakhir mereka akan diterapkan secara otomatis ke semua handler dalam kelas tersebut, tetapi jika diperlukan dimungkinkan untuk memiliki perilaku terpisah untuk beberapa fungsi.

Misalnya, penerapan memiliki prioritas seperti ini, `Function` > `Class`, dimana fungsi memiliki prioritas lebih tinggi.

#### Rate Limiting

Selain itu, mari juga bahas mekanisme rate limiting yang dijelaskan dalam anotasi.

Anda dapat mengatur batasan umum untuk setiap pengguna:

```kotlin
// ...
val bot = TelegramBot("BOT_TOKEN") {
    rateLimiter { // batasan umum
        limits = RateLimits(period = 10000, rate = 5)
    }
}
```

###### Handler specific

Batasan pada tindakan tertentu dapat didefinisikan menggunakan anotasi `RateLimits`, didukung `@CommandHandler`, `@CommandHandler.CallbackQuery`, `@InputHandler`, `@CommonHandler`.

```kotlin
@CommandHandler(["/start"])
@RateLimits(period = 1000L, rate = 1L)
suspend fun start(user: User, bot: TelegramBot) {
    // ...
}
```

#### Guard

Anda dapat mendefinisikan guards secara terpisah untuk mengontrol akses ke handler, didukung `@CommandHandler`, `@CommandHandler.CallbackQuery`, `@InputHandler` :

```kotlin
@CommandHandler(["text"])
@Guard(isAdminGuard::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### ArgParser

Anda dapat mendefinisikan custom argument parser secara terpisah untuk mengubah perilaku parsing parameter untuk handler, didukung `@CommandHandler`, `@CommandHandler.CallbackQuery`, `@CommonHandler`:

```kotlin
@CommandHandler(["text"])
@ArgParser(SpaceArgParser::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

**lihat juga [`defaultArgParser`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.common/default-arg-parser.html)**

### Conclusion

Anotasi-anotasi ini menyediakan alat yang robust dan fleksibel untuk menangani perintah, input, dan event, sambil memungkinkan konfigurasi terpisah untuk rate limits dan guards, meningkatkan struktur dan maintainability pengembangan bot secara keseluruhan.

### See also

* [Activities & Processors](Activites-and-Processors.md)
* [Activity invocation](Activity-invocation.md)
* [FSM and Conversation handling](FSM-and-Conversation-handling.md)
* [Update parsing](Update-parsing.md)
* [Aide](Aide.md)