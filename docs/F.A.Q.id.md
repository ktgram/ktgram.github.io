---
---
title: F.A.Q
---

### Pengecualian `AbstractMethodError`

Jika Anda mendapatkan pengecualian seperti ini saat startup aplikasi Anda:

```kotlin
Exception in thread "DefaultDispatcher-worker-1" java.lang.AbstractMethodError: 'kotlinx.serialization.KSerializer[] kotlinx.serialization.internal.GeneratedSerializer.typeParametersSerializers()'
	at eu.vendeli.tgbot.types.options.GetUpdatesOptions$$serializer.typeParametersSerializers(GetUpdatesOptions.kt:6)
```

Ini terjadi karena sistem build Anda menggunakan library serialisasi lama yang mekanisme internalnya berbeda.
Untuk mengatasinya, Anda harus membuatnya menggunakan versi yang lebih baru, misalnya dengan menambahkan ini ke buildscript Anda:

```kotlin
configurations.all {
    resolutionStrategy.eachDependency {
        val serdeVer = "x.x.x" // harus >= 1.8.0
        when(requested.module.toString()) {
            // json serialiazaton
            "org.jetbrains.kotlinx:kotlinx-serialization-json" -> useVersion(serdeVer)
            "org.jetbrains.kotlinx:kotlinx-serialization-json-jvm" -> useVersion(serdeVer)
            "org.jetbrains.kotlinx:kotlinx-serialization-core" -> useVersion(serdeVer)
            "org.jetbrains.kotlinx:kotlinx-serialization-core-jvm" -> useVersion(serdeVer)
            "org.jetbrains.kotlinx:kotlinx-serialization-bom" -> useVersion(serdeVer)
        }
    }
}
```

(Jika ini dijelaskan dengan baik di changelog, saya tidak akan pernah memutakhirkannya karena saya mendapat begitu banyak laporan tentang masalah ini)

### Bagaimana cara mendapatkan respons dari metode?

Untuk mendapatkan respons dan dapat mengoperasikannya, Anda perlu menggunakan `sendReturning` di akhir metode sebagai ganti `send`.

Dalam hal ini, kelas `Response` dikembalikan, yang berisi respons, sukses atau gagal, selanjutnya Anda perlu menangani kegagalan atau cukup memanggil `getOrNull()`.

Ada bagian tentang: [Memproses respons](https://github.com/vendelieu/telegram-bot#processing-responses).

### Saya mendapatkan error saat menggunakan `spring-boot-devtools`

Ini terjadi karena `spring-boot-devtools` memiliki `classloader` sendiri dan tidak menemukan metode.

Anda perlu menambahkan ke `resources/META-INF/spring-devtools.properties`:

```properties
restart.include.generated=/eu.vendeli
```

### Cara mengubah engine ktor

Jika Anda ingin mengubah engine yang digunakan oleh klien, Anda dapat dengan mudah mengubah [parameter](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/ktor-jvm-engine.html) di [pengaturan plugin](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/index.html).

### Cara menggunakan logging provider favorit saya

Library menggunakan `slf4j-api` dan untuk menggunakan provider, Anda hanya perlu menambahkannya ke dependensi.

Plugin library secara otomatis mendeteksi penggunaan provider, jika provider tidak ada, `logback` akan digunakan secara default.

### Menangkap exception jaringan dalam handler long-polling

Misalnya jika Anda memiliki koneksi yang tidak stabil dan perlu menangkap error karena ini, mungkin pendekatan ini akan membantu Anda:

```kotlin
fun main() {
    val bot = TelegramBot("TOKEN")

    try {
        bot.handleUpdates()
    } catch (e: Exception) {
        // handle if needed
        
        bot.update.stopListener()
        bot.handleUpdates()
    }
}
```

Anda juga dapat melihat bagaimana ini dilakukan di [spring-starter](https://github.com/vendelieu/telegram-bot/blob/1584d40f9a94a8c31bba9e7614c0070155630a52/spring-ktgram-starter/src/jvmMain/kotlin/eu/vendeli/spring/starter/TelegramAutoConfiguration.kt#L53).