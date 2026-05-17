---
---
title: Activites And Processors
---

### Introduction

`Activity` dalam istilah perpustakaan ini adalah entitas abstrak yang merupakan generalisasi dari entitas seperti `@CommandHandler`, `@InputHandler`, `@UnprocessedHandler`, `@CommonHandler`, `@UpdateHandler`, dan `@WizardHandler`.

Juga lihat artikel [handlers article](Handlers.md).

### Collecting activities

Activities ditemukan dan di‑wire pada **waktu kompilasi** oleh prosesor KSP **ktnip**. [Functional DSL](Handlers#functional-dsl.md) adalah satu satu‑satunya pengecualian — handler yang didefinisikan melalui `bot.setFunctionality { ... }` didaftarkan pada runtime.

Jika Anda ingin membatasi area di mana paket akan dicari, Anda dapat memberikan parameter ke plugin:

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

catatan dalam kasus seperti itu, agar aksi yang dikumpulkan diproses dengan benar, Anda juga harus menentukan paket dalam instance itu sendiri.

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.mybot")

    bot.handleUpdates()
    // start long-polling listener
}
```

opsi ini ditambahkan agar dapat menjalankan banyak instance bot:

```gradle
ktGram {
    packages = listOf("com.example.mybot", "com.example.mybot2")
}
```


atau jika Anda tidak menggunakan plugin untuk menentukan paket yang berbeda, Anda harus menyebutkannya dengan pemisah `;`:

```gradle
ksp {
    arg("package", "com.example.mybot;com.example.mybot2")
}
```

### Processing

#### Webhooks

Di dalam controller Anda (atau tempat lain dimana `webhook` diproses), Anda memanggil: [`bot.update.parseAndHandle(webhookString)`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.core/-tg-update-handler/index.html#706360827%2FFunctions%2F-880831646)

#### Long polling

Panggil: `bot.handleUpdates()` atau melalui `bot.update.setListener { handle(it) }`


### See also

* [Update parsing](Update-parsing.md)
* [Activity invocation](Activity-invocation.md)
* [Actions](Actions.md)

---