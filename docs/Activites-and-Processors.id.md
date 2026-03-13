---
---
title: Activites And Processors
---

### Introduction

`Activity` dalam konteks library ini adalah entitas abstrak yang merupakan generalisasi dari entitas seperti `@CommandHandler`, `@InputHandler`, `@UnprocessedHandler`, dan `@CommonHandler`.

Juga lihat [artikel handlers](Handlers.md).

### Mengumpulkan activities

Activities dikumpulkan dan dipersiapkan semua konteks pada waktu kompilasi (kecuali yang didefinisikan melalui functional dsl).

Jika Anda ingin membatasi area di mana package akan dicari, Anda dapat memberikan parameter ke plugin:

```gradle
ktGram {
    packages = listOf("com.example.mybot")
}
```

atau tanpa plugin melalui ksp:

```gradle
ksp {
    arg("package", "com.example.mybot")
}
```

catatan dalam kasus seperti itu, agar actions yang dikumpulkan dapat diproses dengan benar, Anda juga harus menentukan package pada instansinya sendiri.

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.mybot")

    bot.handleUpdates()
    // start long-polling listener
}
```

opsi ini ditambahkan untuk dapat menjalankan beberapa instans bot:

```gradle
ktGram {
    packages = listOf("com.example.mybot", "com.example.mybot2")
}
```


atau jika Anda tidak menggunakan plugin untuk menentukan package yang berbeda, Anda perlu menentukannya dengan pemisah `;`:

```gradle
ksp {
    arg("package", "com.example.mybot;com.example.mybot2")
}
```

### Processing

#### Webhooks

Di controller Anda (atau tempat lain di mana `webhook` diproses), Anda panggil: [`bot.update.parseAndHandle(webhookString)`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.core/-tg-update-handler/index.html#706360827%2FFunctions%2F-880831646)

#### Long polling

Panggil: `bot.handleUpdates()` atau melalui `bot.update.setListener { handle(it) }`


### Lihat juga

* [Update parsing](Update-parsing.md)
* [Activity invocation](Activity-invocation.md)
* [Actions](Actions.md)

---