---
---
title: Web Starters (Spring Dan Ktor)
---

### Spring starter

Modul Spring Starter untuk library adalah modul auto-configuration yang mengintegrasikan fungsionalitas bot Telegram ke dalam aplikasi Spring Boot. Modul ini memanfaatkan kekuatan dependency injection dan configuration properties dari Spring Boot untuk mengonfigurasi bot Telegram secara otomatis berdasarkan konfigurasi yang diberikan. Library ini sangat berguna bagi developer yang ingin membangun bot Telegram menggunakan Kotlin dan Spring Boot, menawarkan pendekatan yang terstruktur untuk pengembangan dan manajemen bot.

### Fitur Utama

- **Auto-Configuration**: Library secara otomatis mengonfigurasi bot Telegram berdasarkan configuration properties yang diberikan, menghilangkan kebutuhan setup manual.
- **Configuration Properties**: Mendukung configuration properties untuk kustomisasi mudah pengaturan bot, seperti bot tokens, package names, dan identifiers.
- **Spring Integration**: Terintegrasi secara mulus dengan ekosistem Spring, memanfaatkan dependency injection dan application context dari Spring untuk mengelola bot instances.
- **Coroutine Support**: Memanfaatkan Kotlin coroutines untuk operasi bot asynchronous, memastikan eksekusi yang efisien dan non-blocking.

### Memulai

Untuk menggunakan Spring Starter Library untuk Telegram Bots, Anda perlu menyertakannya sebagai dependency di proyek Spring Boot Anda. Library didesain untuk bekerja dengan aplikasi Spring Boot dan memerlukan framework Spring Boot untuk berfungsi.

#### Dependency

Tambahkan dependency berikut ke file `build.gradle` atau `pom.xml` Anda:

```gradle
dependencies {
    implementation 'eu.vendeli:spring-starter:<version>'
}
```

Ganti `<version>` dengan versi terbaru dari library.

#### Configuration

Library menggunakan `@ConfigurationProperties` dari Spring Boot untuk binding configuration properties. Anda dapat mendefinisikan konfigurasi bot Anda di file `application.properties` atau `application.yml` dari aplikasi Spring Boot Anda.

```yaml
ktgram:
 autoStartPolling: true
 shareHttpClient: true
 bot:
    - token: YOUR_BOT_TOKEN
      pckg: com.example.bot
      identifier: MyBot
```

#### Penggunaan

Setelah library disertakan dan dikonfigurasi, library secara otomatis membuat dan mengonfigurasi instances bot Telegram berdasarkan konfigurasi yang diberikan.

Library juga mendukung multiple bot instances, untuk menginisialisasi beberapa instance cukup deklarasikan sebagai entry baru di bagian bot:

```yaml
ktgram:
 bot:
    - token: YOUR_BOT_TOKEN
    - token: SECOND_BOT_TOKEN
```

### Advanced Configuration

Untuk konfigurasi yang lebih advanced, seperti menyesuaikan perilaku bot atau integrasi dengan komponen Spring lainnya, Anda dapat memperluas kelas `BotConfiguration` dan mengubah konfigurasi bot melalui method `applyCfg` nya, Anda dapat melihat contoh [di sana](https://github.com/vendelieu/telegram-bot_template/blob/spring-bot/src/main/kotlin/com/example/springbot/configuration/BotConfig.kt).

> [!TIP]
> Untuk mengonfigurasi setiap instance yang diinisialisasi dengan custom configuration, bedakan mereka dengan identifier mereka (kelas BotConfiguration juga memiliki identifier).

### Ktor

Modul ini didesain untuk memfasilitasi pembuatan webhook server untuk Telegram bots. Modul ini memungkinkan developer untuk mengonfigurasi server, termasuk SSL/TLS settings, dan mendeklarasikan multiple Telegram bots dengan custom configurations. Proses setup fleksibel, memungkinkan developer untuk menyesuaikan server sesuai kebutuhan spesifik mereka.

### Installation

Untuk menginstall ktor starter tambahkan tambahan ke main dependency:

```gradle
dependencies {
    implementation("eu.vendeli:ktor-starter:x.y.z") // there
    // change x.y.z to current library version
}
```

### Komponen Utama

Fungsi `serveWebhook`

Fungsi serveWebhook adalah inti dari library. Fungsi ini men-setup dan memulai webhook server untuk Telegram bots. Fungsi ini menerima dua parameter:

- `wait`: Sebuah boolean yang menunjukkan apakah server harus menunggu aplikasi berhenti sebelum shutdown. Defaults ke true.
- `serverBuilder`: Sebuah lambda function yang mengonfigurasi server. Defaults ke empty lambda.

### Configuration

* `WEBHOOK_PREFIX`: ini adalah parameter yang akan digunakan untuk address prefix untuk webhook listener route. (defaults ke "/")

#### Server Setup

- `server`: Sebuah method untuk mengatur server configuration menggunakan EnvConfiguration atau ManualConfiguration.
- `engine`: Sebuah method untuk mengonfigurasi Netty application engine.
- `ktorModule`: Sebuah method untuk menambahkan Ktor modules ke aplikasi.

Library menyediakan wide range dari configurable parameters untuk server, termasuk host, port, SSL settings, dan lainnya. Ada dua concrete options untuk mengonfigurasi:

* `EnvConfiguration`: Membaca configuration values dari environment dengan prefix `KTGRAM_`.
* `ManualConfiguration`: Memungkinkan manual setting dari configuration values, set parameter Anda di dalam function `server {}`.

Ada list dari parameters yang dapat di-set:

- `HOST`: Hostname atau IP address dari server.
- `PORT`: Port number untuk server.
- `SSL_PORT`: Port number untuk SSL/TLS connections.
- `PEM_PRIVATE_KEY_PATH`: Path ke PEM private key file.
- `PEM_CHAIN_PATH`: Path ke PEM certificate chain file.
- `PEM_PRIVATE_KEY`: PEM private key PASSWORD sebagai character array.
- `KEYSTORE_PATH`: Path ke Java KeyStore file.
- `KEYSTORE_PASSWORD`: Password untuk KeyStore.
- `KEY_ALIAS`: Alias untuk key di KeyStore.
- `SSL_ON`: Sebuah boolean yang menunjukkan apakah SSL/TLS harus di-enable. Defaults ke true.

> [!TIP]
> Jika pem certificates ada, modul itu sendiri akan membuat jks storage dari mereka di path yang ditentukan.

#### Bot Configuration:

Untuk mengonfigurasi bot panggil `declareBot {}` yang memiliki parameter sebagai berikut:

- `token`: Bot token.
- `pckg`: Package name untuk bot.
- `configuration`: Sebuah lambda function untuk mengonfigurasi bot.
- `handlingBehaviour`: Sebuah lambda function untuk mengatur handling behavior dari bot.
- `onInit`: Sebuah lambda function yang dieksekusi ketika bot diinisialisasi.

### Example Usage

Untuk menggunakan modul ini, panggil fungsi `serveWebhook`, konfigurasikan dengan settings yang Anda inginkan, deklarasikan bot Anda. Berikut adalah contoh simplified:

```kotlin
fun main() = runBlocking {
    serveWebhook {
        server {
            HOST = "0.0.0.0"
            PORT = 8080
            SSL_PORT = 8443

            PEM_PRIVATE_KEY_PATH = "/etc/letsencrypt/live/example.com/privkey.pem"
            PEM_CHAIN_PATH = "/etc/letsencrypt/live/example.com/fullchain.pem"
            PEM_PRIVATE_KEY = "pem_changeit".toCharArray()

            KEYSTORE_PATH = "/etc/ssl/certs/java/cacerts/bot_keystore.jks"
            KEYSTORE_PASSWORD = "changeit".toCharArray()
            // Set other configuration parameters as needed
        }
        declareBot {
            token = "YOUR_BOT_TOKEN"
            // Configure other bot settings
        }
        // Add more bots or set other parameters if needed
    }
}
```

> [!CAUTION]
> Jangan lupa untuk set webhook untuk membuat semuanya bekerja. :)

Secara default modul akan serve webhook listenening endpoints sebagai `host/BOT_TOKEN`


---