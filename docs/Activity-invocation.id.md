---
---
title: Activity Invocation
---

Selama invocation activity, adalah mungkin untuk melewatkan konteks bot, karena dinyatakan sebagai parameter dalam fungsi target.

Parameter yang dapat dilewatkan adalah:

* [`ProcessedUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processed-update/index.html) (dan semua subclass-nya) - update pemrosesan saat ini.
* [`ProcessingContext`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processing-context/index.html) - konteks level rendah dari penanganan activity.
* [`User`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types/-user/index.html) - jika ada.
* [`Chat`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.chat/-chat/index.html) - jika ada.
* [`TelegramBot`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot/-telegram-bot/index.html) - instance bot saat ini.

Juga dimungkinkan untuk menambahkan tipe kustom untuk dilewatkan.

Untuk melakukannya, tambahkan kelas yang mengimplementasikan [`Autowiring<T>`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.marker/-autowiring/index.html) dan tandai dengan anotasi [`@Injectable`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-injectable/index.html).

Setelah mengimplementasikan interface `Autowiring` - `T` akan tersedia untuk dilewatkan dalam fungsi target dan akan diperoleh melalui metode yang dijelaskan dalam interface.

```kotlin
@Injectable
object UserResolver : Autowiring<UserRecord> {
    override suspend fun get(update: ProcessedUpdate, bot: TelegramBot): UserRecord? {
        return userRepository.getUserByTgId(update.user.id)
    }
}
```


Parameter lain yang dinyatakan dalam fungsi akan **dicari** dalam parameter yang diparse.

Selain itu, parameter yang diparse selama dilewatkan dapat di-cast ke tipe tertentu, berikut daftarnya:

- `String`
- `Integer`
- `Long`
- `Short`
- `Float`
- `Double`

Selain itu, perhatikan bahwa jika parameter dinyatakan dan hilang (atau dalam parameter yang diparse atau misalnya `User` hilang dalam `Update`) atau tipe yang dinyatakan tidak sesuai dengan parameter yang diterima dalam fungsi, **`null`** akan dilewatkan jadi berhati-hatilah.

Meringkas semuanya, di bawah ini adalah contoh bagaimana parameter fungsi biasanya dibentuk:

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/3c1d7830-8e5d-45fb-82bb-ac63f08c3782" alt="Invokation process diagram" />
</p>

### Lihat juga

* [Update parsing](Update-parsing.md)
* [Activities & Processors](Activites-and-Processors.md)
---