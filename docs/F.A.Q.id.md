---
---
title: F.A.Q
---

### `AbstractMethodError` exception

Jika Anda mendapatkan pengecualian seperti ini saat startup aplikasi Anda:

```kotlin
Exception in thread "DefaultDispatcher-worker-1" java.lang.AbstractMethodError: 'kotlinx.serialization.KSerializer[] kotlinx.serialization.internal.GeneratedSerializer.typeParametersSerializers()'
	at eu.vendeli.tgbot.types.options.GetUpdatesOptions$$serializer.typeParametersSerializers(GetUpdatesOptions.kt:6)
```

Hal ini terjadi karena sistem build Anda menggunakan library serialisasi lama yang mekanisme internalnya berbeda.
Untuk mengatasinya, Anda harus membuatnya menggunakan versi yang lebih baru, misalnya dengan menambahkan ini ke buildscript Anda:

```kotlin
configurations.all {
    resolutionStrategy.eachDependency {
        val serdeVer = "x.x.x" // should be >= 1.8.0
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

(Jika ini sudah dijelaskan dengan baik di changelog, saya tidak akan pernah memutakhirkannya karena saya mendapat banyak laporan tentang masalah ini)

### Bagaimana cara mendapatkan respons dari method?

Untuk mendapatkan respons dan dapat mengoperasikannya, Anda perlu menggunakan `sendReturning` di akhir method sebagai ganti `send`.

Dalam hal ini, class `Response` dikembalikan, yang berisi respons, keberhasilan atau kegagalan, selanjutnya Anda perlu menangani kegagalan atau cukup panggil `getOrNull()`.

Ada bagian tentang: [Processing responses](https://github.com/vendelieu/telegram-bot#processing-responses).

### Saya mendapatkan error saat menggunakan `spring-boot-devtools`

Hal ini terjadi karena `spring-boot-devtools` memiliki `classloader` sendiri dan tidak menemukan method.

Anda perlu menambahkan ke `resources/META-INF/spring-devtools.properties`:

```properties
restart.include.generated=/eu.vendeli
```

### Bagaimana cara mengubah engine ktor

Jika Anda ingin mengubah engine yang digunakan oleh client, Anda dapat dengan mudah mengubah [parameter](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/ktor-jvm-engine.html) di [plugin settings](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/index.html).

### Bagaimana cara menggunakan logging provider favorit saya

Library menggunakan `slf4j-api` dan untuk menggunakan provider, Anda hanya perlu menambahkannya ke dependencies.

Plugin library secara otomatis mendeteksi penggunaan provider, jika provider tidak ada, `logback` akan digunakan secara default.

### Menangkap network exceptions dalam long-polling handler

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

---