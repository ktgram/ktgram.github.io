---
---
title: Web Starters (Spring Dan Ktor)
---

### Spring starter

Modul Spring Starter untuk library adalah modul auto-configuration yang mengintegrasikan fungsionalitas bot Telegram ke dalam aplikasi Spring Boot. Ini memanfaatkan kekuatan dependency injection dan properties konfigurasi Spring Boot untuk secara otomatis mengonfigurasi bot Telegram berdasarkan konfigurasi yang diberikan. Library ini sangat berguna untuk developer yang ingin membangun bot Telegram menggunakan Kotlin dan Spring Boot, menawarkan pendekatan yang terstruktur untuk pengembangan dan manajemen bot.

### Fitur Utama

- **Auto-Configuration**: Library secara otomatis mengonfigurasi bot Telegram berdasarkan properties konfigurasi yang diberikan, menghilangkan kebutuhan untuk setup manual.
- **Properties Konfigurasi**: Mendukung properties konfigurasi untuk kustomisasi mudah dari pengaturan bot, seperti token bot, nama paket, dan identifier.
- **Spring Integration**: Terintegrasi secara mulus dengan ekosistem Spring, memanfaatkan dependency injection dan application context Spring untuk mengelola instance bot.
- **Coroutine Support**: Memanfaatkan Kotlin coroutines untuk operasi bot asynchronous, memastikan eksekusi yang efisien dan non-blocking.

### Getting Started

Untuk menggunakan Library Spring Starter untuk Telegram Bots, Anda perlu menyertakannya sebagai dependency di proyek Spring Boot Anda. Library dirancang untuk bekerja dengan aplikasi Spring Boot dan memerlukan framework Spring Boot untuk berfungsi.

#### Dependency

Tambahkan dependency berikut ke file `build.gradle` atau `pom.xml` Anda:

```gradle
dependencies {
    implementation 'eu.vendeli:spring-starter:<version>'
}
```

Ganti `<version>` dengan versi terbaru dari library.

#### Configuration

Library menggunakan Spring Boot's `@ConfigurationProperties` untuk mengikat properties konfigurasi. Anda dapat mendefinisikan konfigurasi bot Anda di file `application.properties` atau `application.yml` dari aplikasi Spring Boot Anda.

```yaml
ktgram:
 autoStartPolling: true
 shareHttpClient: true
 bot:
    - token: YOUR_BOT_TOKEN
      pckg: com.example.bot
      identifier: MyBot
```

#### Usage

Setelah library disertakan dan dikonfigurasi, secara otomatis membuat dan mengonfigurasi instance bot Telegram berdasarkan konfigurasi yang diberikan.

Ini juga mendukung multiple bot instances, untuk menginisialisasi beberapa instance cukup deklarasikan sebagai entry baru di section bot:

```yaml
ktgram:
 bot:
    - token: YOUR_BOT_TOKEN
    - token: SECOND_BOT_TOKEN
```

### Advanced Configuration

Untuk konfigurasi yang lebih advance, seperti menyesuaikan perilaku bot atau mengintegrasikan dengan komponen Spring lainnya, Anda dapat memperluas kelas `BotConfiguration` dan mengubah konfigurasi bot melalui method `applyCfg`, Anda dapat melihat contoh [di sana](https://github.com/vendelieu/telegram-bot_template/blob/spring-bot/src/main/kotlin/com/example/springbot/configuration/BotConfig.kt).

> [!TIP]
> Untuk mengonfigurasi setiap instance yang diinisialisasi dengan konfigurasi custom, bedakan mereka dengan identifier mereka (kelas BotConfiguration juga memiliki identifier).

### Ktor

Modul ini dirancang untuk memfasilitasi pembuatan webhook server untuk Telegram bots. Ini memungkinkan developer untuk mengonfigurasi server, termasuk pengaturan SSL/TLS, dan mendeklarasikan multiple Telegram bots dengan konfigurasi custom. Proses setup fleksibel, memungkinkan developer untuk menyesuaikan server sesuai kebutuhan spesifik mereka.

### Installation

Untuk menginstal ktor starter tambahkan additional ke main dependency:

```gradle
dependencies {
    implementation("eu.vendeli:ktor-starter:x.y.z") // there
    // change x.y.z to current library version
}
```

### Key Components

`serveWebhook` Function

Fungsi serveWebhook adalah inti dari library. Ini mengatur dan memulai webhook server untuk Telegram bots. Ini menerima dua parameter:

- `wait`: Boolean yang menunjukkan apakah server harus menunggu aplikasi berhenti sebelum shutdown. Defaults to true.
- `serverBuilder`: Fungsi lambda yang mengonfigurasi server. Defaults to an empty lambda.

### Configuration

* `WEBHOOK_PREFIX`: itu adalah parameter yang akan digunakan untuk address prefix untuk webhook listener route. (defaults to "/")

#### Server Setup

- `server`: Method untuk mengatur konfigurasi server menggunakan EnvConfiguration atau ManualConfiguration.
- `engine`: Method untuk mengonfigurasi Netty application engine.
- `ktorModule`: Method untuk menambahkan Ktor modules ke aplikasi.

Library menyediakan wide range dari configurable parameters untuk server, termasuk host, port, SSL settings, dan lainnya. Ada dua concrete options untuk configuringnya:

* `EnvConfiguration`: Membaca configuration values dari environment dengan prefix `KTGRAM_`.
* `ManualConfiguration`: Memungkinkan untuk manual setting dari configuration values, set parameters Anda di function `server {}`.

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
- `SSL_ON`: Boolean yang menunjukkan apakah SSL/TLS harus di-enable. Defaults to true.

> [!TIP]
> Jika pem certificates ada, module sendiri akan membuat jks storage dari mereka di path yang ditentukan.

#### Bot Configuration:

Untuk mengonfigurasi bot panggil `declareBot {}` yang memiliki parameters seperti:

- `token`: Bot token.
- `pckg`: Package name untuk bot.
- `configuration`: Fungsi lambda untuk mengonfigurasi bot.
- `handlingBehaviour`: Fungsi lambda untuk mengatur handling behavior bot.
- `onInit`: Fungsi lambda untuk dieksekusi saat bot diinisialisasi.

### Example Usage

Untuk menggunakan module ini, panggil function `serveWebhook`, konfigurasikan dengan settings yang diinginkan, deklarasikan bots Anda. Berikut contoh sederhananya:

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
> Jangan lupa untuk set webhook agar semuanya berfungsi. :)

Secara default module akan serve webhook listenening endpoints sebagai `host/BOT_TOKEN`


---