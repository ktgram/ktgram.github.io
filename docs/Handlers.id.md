---
---
title: Handlers
---


### Variety of Handlers

Dalam pengembangan bot, khususnya dalam sistem yang melibatkan interaksi pengguna, sangat penting untuk mengelola dan memproses perintah dan peristiwa secara efisien.

Anotasi ini menandai fungsi yang dirancang untuk memproses perintah, input, atau pembaruan tertentu dan memberikan metadata seperti kata kunci perintah, cakupan, dan penjaga.

### Annotations Overview

#### CommandHandler

Anotasi `CommandHandler` digunakan untuk menandai fungsi yang memproses perintah tertentu. Anotasi ini mencakup properti yang mendefinisikan kata kunci dan cakupan perintah.

-   **value**: Menentukan kata kunci yang terkait dengan perintah.
-   **scope**: Menentukan konteks atau cakupan di mana perintah akan diperiksa.

```kotlin
@CommandHandler(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommandHandler.CallbackQuery

Versi khusus dari anotasi `CommandHandler` yang dirancang khusus untuk menangani callback query. Ini mencakup properti serupa dengan `CommandHandler`, dengan fokus pada perintah terkait callback.

_Sebenarnya sama saja dengan hanya `@CommandHandler` dengan preset `UpdateType.CALLBACK_QUERY` scope_.

-   **value**: Menentukan kata kunci yang terkait dengan perintah.
-   **autoAnswer**: Membalas `callbackQuery` secara otomatis (panggil `answerCallbackQuery` sebelum penanganan).


```kotlin
@CommandHandler.CallbackQuery(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### CommonHandler

Anotasi `CommonHandler` ditujukan untuk fungsi yang memproses perintah dengan prioritas lebih rendah dibandingkan `CommandHandler` dan `InputHandler`. Ini digunakan pada level sumber dan memberikan cara fleksibel untuk mendefinisikan penangan perintah umum.

**Perhatikan, prioritas bekerja hanya dalam `@CommonHandler` sendiri (yaitu tidak mempengaruhi penangan lain).**

##### CommonHandler.Text

Anotasi ini menentukan pencocokan teks terhadap pembaruan. Ini mencakup properti untuk mendefinisikan teks pencocokan, kondisi penyaringan, prioritas, dan cakupan.

-   **value**: Teks yang akan dicocokkan dengan pembaruan masuk.
-   **filter**: Kelas yang mendefinisikan kondisi yang digunakan dalam proses pencocokan.
-   **priority**: Tingkat prioritas penangan, di mana 0 adalah prioritas tertinggi.
-   **scope**: Konteks atau cakupan di mana pencocokan teks akan diperiksa.

```kotlin
@CommonHandler.Text(["text"], filter = isNewUserFilter::class, priority = 10)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommonHandler.Regex

Mirip dengan `CommonHandler.Text`, anotasi ini digunakan untuk pencocokan pembaruan berdasarkan ekspresi reguler. Ini mencakup properti untuk mendefinisikan pola regex, opsi, kondisi penyaringan, prioritas, dan cakupan.

-   **value**: Pola regex yang digunakan untuk pencocokan.
-   **options**: Opsi regex yang memodifikasi perilaku pola regex.
-   **filter**: Kelas yang mendefinisikan kondisi yang digunakan dalam proses pencocokan.
-   **priority**: Tingkat prioritas penangan, di mana 0 adalah prioritas tertinggi.
-   **scope**: Konteks atau cakupan di mana pencocokan regex akan diperiksa.

```kotlin
@CommonHandler.Regex("^\d+$", scope = [UpdateType.EDITED_MESSAGE])
suspend fun test(update: EditedMessageUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### InputHandler

Anotasi `InputHandler` menandai fungsi yang memproses peristiwa input tertentu. Ini ditujukan untuk fungsi yang menangani input saat runtime dan mencakup properti untuk mendefinisikan kata kunci input dan cakupan.

-   **value**: Menentukan kata kunci yang terkait dengan peristiwa input.

```kotlin
@InputHandler("text")
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UnprocessedHandler

Anotasi `UnprocessedHandler` digunakan untuk menandai fungsi yang menangani pembaruan yang tidak diproses oleh penangan lain. Ini memastikan bahwa setiap pembaruan yang tidak diproses ditangani dengan tepat, dengan hanya satu titik pemrosesan yang mungkin untuk tipe penangan ini.

```kotlin
@UnprocessedHandler
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UpdateHandler

Anotasi `UpdateHandler` menandai fungsi yang menangani jenis pembaruan masuk tertentu. Ini memberikan cara untuk mengkategorikan dan memproses berbagai tipe pembaruan secara sistematis.

-   **type**: Menentukan tipe-tipe pembaruan yang akan diproses oleh fungsi penangan.

```kotlin
@UpdateHandler([UpdateType.PRE_CHECKOUT_QUERY])
suspend fun test(update: PreCheckoutQueryUpdate, user: User, bot: TelegramBot) {
    //...
}
```
### Handler Companion Annotations

Ada juga anotasi tambahan yang opsional untuk penangan, melengkapi perilaku opsional dari penangan itu sendiri.

Mereka dapat ditempatkan baik pada fungsi maupun kelas, di mana pada kasus terakhir mereka akan diterapkan secara otomatis ke semua penangan dalam kelas tersebut, tetapi jika diperlukan dimungkinkan untuk memiliki perilaku terpisah untuk beberapa fungsi.

Artinya penerapan memiliki prioritas seperti ini, `Function` > `Class`, dimana fungsi memiliki prioritas lebih tinggi.

#### Rate Limiting

Selain itu, mari juga mengungkap mekanisme rate limiting yang dijelaskan dalam anotasi.

Anda dapat menetapkan batasan umum untuk setiap pengguna:

```kotlin
// ...
val bot = TelegramBot("BOT_TOKEN") {
    rateLimiter { // general limits
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

Anda dapat mendefinisikan penjaga secara terpisah untuk mengontrol akses ke penangan, didukung `@CommandHandler`, `@CommandHandler.CallbackQuery`, `@InputHandler` :

```kotlin
@CommandHandler(["text"])
@Guard(isAdminGuard::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### ArgParser

Anda dapat mendefinisikan parser argumen kustom secara terpisah untuk mengubah perilaku parsing parameter untuk penangan, didukung `@CommandHandler`, `@CommandHandler.CallbackQuery`, `@CommonHandler`:

```kotlin
@CommandHandler(["text"])
@ArgParser(SpaceArgParser::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

**lihat juga [`defaultArgParser`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.common/default-arg-parser.html)**

### Conclusion

Anotasi-anotasi ini memberikan alat yang tangguh dan fleksibel untuk menangani perintah, input, dan peristiwa, sambil memungkinkan konfigurasi terpisah untuk batasan laju dan penjaga, meningkatkan struktur dan pemeliharaan pengembangan bot secara keseluruhan.

### See also

* [Activities & Processors](Activites-and-Processors.md)
* [Activity invocation](Activity-invocation.md)
* [FSM and Conversation handling](FSM-and-Conversation-handling.md)
* [Update parsing](Update-parsing.md)

---