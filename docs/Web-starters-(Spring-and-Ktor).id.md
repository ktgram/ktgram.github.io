---
---
title: Web Starters (Spring And Ktor)
---

### Spring starter

Modul Spring Starter untuk library adalah modul auto‑configuration yang mengintegrasikan fungsionalitas bot Telegram ke dalam aplikasi Spring Boot. Modul ini memanfaatkan kekuatan dependency injection dan properti konfigurasi Spring Boot untuk secara otomatis mengonfigurasi bot Telegram berdasarkan konfigurasi yang diberikan. Library ini sangat berguna bagi pengembang yang ingin membangun bot Telegram menggunakan Kotlin dan Spring Boot, menawarkan pendekatan yang terstruktur untuk pengembangan dan manajemen bot.

### Key Features

- **Auto-Configuration**: Library secara otomatis mengonfigurasi bot Telegram berdasarkan properti konfigurasi yang diberikan, menghilangkan kebutuhan penyiapan manual.
- **Configuration Properties**: Mendukung properti konfigurasi untuk memudahkan kustomisasi pengaturan bot, seperti token bot, nama paket, dan identifier.
- **Spring Integration**: Terintegrasi mulus dengan ekosistem Spring, memanfaatkan dependency injection dan konteks aplikasi Spring untuk mengelola instance bot.
- **Coroutine Support**: Memanfaatkan coroutine Kotlin untuk operasi bot asynchronous, memastikan eksekusi yang efisien dan non‑blocking.

### Getting Started

Untuk menggunakan Spring Starter Library untuk Telegram Bots, Anda perlu menambahkannya sebagai dependensi dalam proyek Spring Boot Anda. Library ini dirancang untuk bekerja dengan aplikasi Spring Boot dan memerlukan kerangka kerja Spring Boot untuk berfungsi.

#### Dependency

Tambahkan dependensi berikut ke file `build.gradle` atau `pom.xml` Anda:

```gradle
dependencies {
    implementation 'eu.vendeli:spring-starter:<version>'
}
```

Ganti `<version>` dengan versi terbaru library.

#### Configuration

Library menggunakan `@ConfigurationProperties` Spring Boot untuk mengikat properti konfigurasi. Anda dapat mendefinisikan konfigurasi bot Anda dalam file `application.properties` atau `application.yml` aplikasi Spring Boot Anda.

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

Setelah library termasuk dan dikonfigurasi, ia secara otomatis membuat dan mengonfigurasi instance bot Telegram berdasarkan konfigurasi yang diberikan.

Ia juga mendukung banyak instance bot; untuk menginisialisasi beberapa bot cukup deklarasikan sebagai entri baru di bagian bot:

```yaml
ktgram:
 bot:
    - token: YOUR_BOT_TOKEN
    - token: SECOND_BOT_TOKEN
```

### Advanced Configuration

Untuk konfigurasi lebih lanjut, seperti menyesuaikan perilaku bot atau mengintegrasikan dengan komponen Spring lainnya, Anda dapat memperluas kelas `BotConfiguration` dan mengubah konfigurasi bot melalui metode `applyCfg`, contoh dapat dilihat [di sana](https://github.com/vendelieu/telegram-bot_template/blob/spring-bot/src/main/kotlin/com/example/springbot/configuration/BotConfig.kt).

> [!TIP]
> Untuk mengkonfigurasi setiap instance yang diinisialisasi dengan konfigurasi khusus, bedakan mereka berdasarkan identifier‑nya (kelas BotConfiguration juga memiliki identifier).

### Ktor

Modul ini dirancang untuk memfasilitasi pembuatan server webhook untuk bot Telegram. Ia memungkinkan pengembang mengkonfigurasi server, termasuk pengaturan SSL/TLS, dan mendeklarasikan banyak bot Telegram dengan konfigurasi khusus. Proses penyiapan fleksibel, memungkinkan pengembang menyesuaikan server sesuai kebutuhan mereka.

### Installation

Untuk menginstal ktor starter tambahkan tambahan ke dependensi utama:

```gradle
dependencies {
    implementation("eu.vendeli:ktor-starter:x.y.z") // there
    // change x.y.z to current library version
}
```

### Key Components

`serveWebhook` Function

Fungsi `serveWebhook` adalah inti dari library. Ia menyiapkan dan memulai server webhook untuk bot Telegram. Fungsi ini menerima dua parameter:

- `wait`: Boolean yang menunjukkan apakah server harus menunggu aplikasi berhenti sebelum dimatikan. Nilai default true.
- `serverBuilder`: Lambda yang mengkonfigurasi server. Nilai default lambda kosong.

### Configuration

* `WEBHOOK_PREFIX`: parameter yang akan digunakan sebagai prefiks alamat untuk rute listener webhook. (defaultnya "/")

#### Server Setup

- `server`: Metode untuk mengatur konfigurasi server menggunakan `EnvConfiguration` atau `ManualConfiguration`.
- `engine`: Metode untuk mengkonfigurasi engine aplikasi Netty.
- `ktorModule`: Metode untuk menambahkan modul Ktor ke aplikasi.

Library menyediakan beragam parameter yang dapat dikonfigurasi untuk server, termasuk host, port, pengaturan SSL, dan lainnya. Ada dua opsi konkret untuk konfigurasi:

* `EnvConfiguration`: Membaca nilai konfigurasi dari environment dengan prefiks `KTGRAM_`.
* `ManualConfiguration`: Memungkinkan penetapan nilai konfigurasi secara manual, atur parameter Anda dalam fungsi `server {}`.

Berikut daftar parameter yang dapat diatur:

- `HOST`: Nama host atau alamat IP server.
- `PORT`: Nomor port server.
- `SSL_PORT`: Nomor port untuk koneksi SSL/TLS.
- `PEM_PRIVATE_KEY_PATH`: Path ke file kunci pribadi PEM.
- `PEM_CHAIN_PATH`: Path ke file rantai sertifikat PEM.
- `PEM_PRIVATE_KEY`: PASSWORD kunci pribadi PEM sebagai array karakter.
- `KEYSTORE_PATH`: Path ke file Java KeyStore.
- `KEYSTORE_PASSWORD`: Password untuk KeyStore.
- `KEY_ALIAS`: Alias untuk kunci dalam KeyStore.
- `SSL_ON`: Boolean yang menunjukkan apakah SSL/TLS harus diaktifkan. Default true.

> [!TIP]
> Jika sertifikat pem ada, modul itu sendiri akan membuat penyimpanan jks dari mereka pada path yang ditentukan.

#### Bot Configuration:

Untuk mengkonfigurasi bot panggil `declareBot {}` yang memiliki parameter berikut:

- `token`: Token bot.
- `pckg`: Nama paket bot.
- `configuration`: Lambda untuk mengkonfigurasi bot.
- `handlingBehaviour`: Lambda untuk mengatur perilaku penanganan bot.
- `onInit`: Lambda yang dijalankan saat bot diinisialisasi.

### Example Usage

Untuk menggunakan modul ini, panggil fungsi `serveWebhook`, konfigurasikan dengan pengaturan yang diinginkan, deklarasikan bot Anda. Berikut contoh sederhana:

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
> Jangan lupa mengatur webhook agar semuanya berfungsi. :)

Secara default modul akan menyajikan endpoint webhook sebagai `host/BOT_TOKEN`


---