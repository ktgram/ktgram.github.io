---
---
title: Bot Context
---

<p align="center">
  <img src="https://github.com/user-attachments/assets/60bb58ae-1806-4b8d-8550-833b09c2b606" alt="Bot context diagram" />
</p>

Bot juga dapat memberikan kemampuan untuk mengingat beberapa data melalui antarmuka `UserData` dan `ClassData`.

- [`userData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-user-data/index.html) adalah data level pengguna.
- [`classData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-data/index.html) adalah data level kelas, yaitu data akan disimpan hingga pengguna berpindah ke perintah atau input yang berada di
  kelas yang berbeda. (dalam mode fungsi akan bekerja seperti data pengguna)

Secara default, implementasi disediakan melalui [`ConcurrentHashMap`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.collections/java.util.concurrent.-concurrent-map/) tetapi dapat diubah ke milik Anda sendiri melalui antarmuka [`UserData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-user-data/index.html) dan [`ClassData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-data/index.html) menggunakan
alat penyimpanan data pilihan Anda.


> [!CAUTION]
> Jangan lupa untuk menjalankan gradle `kspKotlin`/atau tugas ksp relevan lainnya untuk membuat binding codegen yang diperlukan tersedia.


Untuk mengubah, yang perlu Anda lakukan hanyalah menempatkan di bawah implementasi Anda anotasi `@CtxProvider` dan menjalankan tugas ksp gradle (atau build).

```kotlin
@CtxProvider
class MyRedis : UserData<String> {
    // ...
}
```

### Lihat juga

* [Beranda](https://github.com/vendelieu/telegram-bot/wiki)
* [Update parsing](Update-parsing.md)
---