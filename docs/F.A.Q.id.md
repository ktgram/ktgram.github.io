---
---
title: F.A.Q
---

### `AbstractMethodError` exception

Jika Anda mendapatkan pengecualian seperti itu saat memulai aplikasi Anda:

```kotlin
Exception in thread "DefaultDispatcher-worker-1" java.lang.AbstractMethodError: 'kotlinx.serialization.KSerializer[] kotlinx.serialization.internal.GeneratedSerializer.typeParametersSerializers()'
	at eu.vendeli.tgbot.types.options.GetUpdatesOptions$$serializer.typeParametersSerializers(GetUpdatesOptions.kt:6)
```

Hal ini terjadi karena sistem build Anda menyelesaikan (resolve) pustaka serialisasi lama yang mekanisme internalnya berbeda.  
Untuk mengatasinya, Anda harus membuatnya menggunakan versi yang lebih baru, misalnya dengan menambahkan ini ke skrip build Anda:

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

(Jika hal ini sudah dijelaskan dengan baik di changelog, saya tidak akan memperbaruinya karena saya mendapatkan begitu banyak laporan tentang masalah ini)

### How do I get the method's response?

Untuk mendapatkan respons dan dapat mengoperasikannya, Anda perlu menggunakan `sendReturning` di akhir metode alih-alih `send`.

Dalam kasus ini kelas `Response` yang dikembalikan, yang berisi respons, keberhasilan atau kegagalan; selanjutnya Anda harus menangani kegagalan atau cukup memanggil `getOrNull()`.

Ada bagian tentang: [Processing responses](https://github.com/vendelieu/telegram-bot#processing-responses).

### I'm getting error while using `spring-boot-devtools`

Hal ini terjadi karena `spring-boot-devtools` memiliki `classloader` sendiri dan tidak menemukan metode.

Anda perlu menambahkan ke `resources/META-INF/spring-devtools.properties`:

```properties
restart.include.generated=/eu.vendeli
```

### How to change ktor engine

Jika Anda ingin mengubah engine yang digunakan oleh klien, Anda cukup mengubah [parameter](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/ktor-jvm-engine.html) di [pengaturan plugin](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/index.html).

### How to use my favorite logging provider

Pustaka ini menggunakan `slf4j-api` dan untuk menggunakan penyedia Anda cukup menambahkannya ke dependensi.

Plugin pustaka secara otomatis mendeteksi penggunaan penyedia; jika penyedia tidak ada, `logback` akan digunakan secara default.

### Catch network exceptions within long-polling handler

Misalnya Anda memiliki koneksi yang tidak stabil dan perlu menangkap kesalahan karena hal tersebut, pendekatan berikut mungkin membantu Anda:

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

Anda juga dapat melihat cara melakukannya di [spring-starter](https://github.com/vendelieu/telegram-bot/blob/1584d40f9a94a8c31bba9e7614c0070155630a52/spring-ktgram-starter/src/jvmMain/kotlin/eu/vendeli/spring/starter/TelegramAutoConfiguration.kt#L53).

---