---
---
title: Bot Configuration
---

Library menyediakan banyak opsi konfigurasi, Anda dapat melihat referensi API di kelas [`BotConfiguration`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.configuration/-bot-configuration/index.html).

Ada juga dua pendekatan untuk mengonfigurasi bot:

### Configurator lambda

```kotlin
// ...
val bot = TelegramBot("BOT_TOKEN") {
  inputListener = RedisInputListenerImpl()
  classManager = KoinClassManagerImpl()
  logging {
      botLogLevel = LogLvl.DEBUG
  }
}
// ...
```

### ConfigLoader interface

Ada juga kemampuan untuk mengonfigurasi melalui interface [`ConfigLoader`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.helper/-config-loader/index.html) khusus,<br/> yang dapat Anda gunakan untuk memuat pengaturan dari sumber eksternal (`properties`, `command line args`, dll.).

Implementasi dari interface ini dapat dilewatkan melalui constructor sekunder dan instance akan dikonfigurasi sesuai.

```kotlin
val bot = TelegramBot(ConfigLoaderImpl)
```

Saat ini ada beberapa modul yang disediakan yang mengimplementasikan interface ini seperti `ktgram-config-env`, `ktgram-config-toml`.

### BotConfiguration Overview

#### BotConfiguration

Kelas `BotConfiguration` adalah hub sentral untuk mengonfigurasi bot. Ini termasuk properti untuk mengidentifikasi bot, mengatur host API, menentukan apakah bot beroperasi dalam lingkungan uji, menangani input, mengelola kelas, dan mengontrol penghapusan input otomatis. Selain itu, ini menyediakan properti internal untuk pembatasan laju, konfigurasi klien HTTP, logging, pendengar pembaruan, dan parsing perintah.

##### Properties

- `identifier`: Mengidentifikasi instans bot yang berbeda selama pemrosesan multi-bot.
- `apiHost`: Host dari API Telegram.
- `isTestEnv`: Flag yang menunjukkan apakah bot beroperasi dalam lingkungan uji.
- `inputListener`: Instance dari kelas penanganan input.
- `classManager`: Manager yang digunakan untuk mendapatkan kelas.
- `inputAutoRemoval`: Flag yang mengatur penghapusan otomatis titik input selama pemrosesan.
- `exceptionHandlingStrategy`: Menentukan strategi untuk menangani exception.
    * `CollectToChannel` - Kumpulkan ke `TgUpdateHandler.caughtExceptions`.
    * `Throw` - Lempar lagi dibungkus dengan `TgException`.
    * `DoNothing` - Lakukan tidak apa-apa :)
    * `Handle` - Setel handler kustom.
- `throwExOnActionsFailure`: Melempar exception ketika ada permintaan bot yang gagal.

##### Configuration Blocks

`BotConfiguration` juga menawarkan fungsi untuk mengonfigurasi komponen internalnya:

- `httpClient(block: HttpConfiguration.() -> Unit)`: Mengonfigurasi klien HTTP.
- `logging(block: LoggingConfiguration.() -> Unit)`: Mengonfigurasi logging.
- `rateLimiter(block: RateLimiterConfiguration.() -> Unit)`: Mengonfigurasi pembatasan permintaan.
- `updatesListener(block: UpdatesListenerConfiguration.() -> Unit)`: Mengonfigurasi pendengar pembaruan.
- `commandParsing(block: CommandParsingConfiguration.() -> Unit)`: Menentukan pola parsing perintah.

### Associated Configuration Classes

#### RateLimiterConfiguration

Mengonfigurasi pembatasan laju global.

- `limits`: Pembatasan laju global.
- `mechanism`: Mekanisme yang digunakan untuk pembatasan laju, default adalah algoritma TokenBucket.
- `exceededAction`: Aksi yang diterapkan ketika batas terlewati.

#### HttpConfiguration

Berisi konfigurasi untuk klien HTTP bot.

- `requestTimeoutMillis`: Request timeout dalam milidetik.
- `connectTimeoutMillis`: Connection timeout dalam milidetik.
- `socketTimeoutMillis`: Socket timeout dalam milidetik.
- `maxRequestRetry`: Maximum retry untuk HTTP requests.
- `retryStrategy`: Strategy untuk retry, dapat dikustomisasi.
- `retryDelay`: Multiplier untuk timeout pada setiap retry.
- `proxy`: Proxy settings untuk HTTP calls.
- `additionalHeaders`: Headers yang diterapkan ke setiap request.

#### LoggingConfiguration

Mengelola level logging untuk aksi bot dan HTTP requests.

- `botLogLevel`: Level logs untuk aksi bot.
- `httpLogLevel`: Level logs untuk HTTP requests.

#### UpdatesListenerConfiguration

Mengonfigurasi parameter terkait penarikan pembaruan.

- `dispatcher`: Dispatcher untuk mengumpulkan pembaruan masuk.
- `processingDispatcher`: Dispatcher untuk memproses pembaruan.
- `pullingDelay`: Delay setelah setiap pulling request.
- `updatesPollingTimeout`: Timeout option untuk mekanisme long-polling.

#### CommandParsingConfiguration

Menentukan parameter untuk parsing perintah.

- `commandDelimiter`: Separator antara perintah dan parameter.
- `parametersDelimiter`: Separator antara parameter.
- `parameterValueDelimiter`: Separator antara key dan value dari parameter.
- `restrictSpacesInCommands`: Flag yang menunjukkan apakah spasi dalam perintah harus dianggap sebagai akhir dari perintah.
- `useIdentifierInGroupCommands`: Menggunakan identifier bot untuk mencocokkan perintah yang mengandung @.

### Example Configuration

Berikut adalah contoh cara mengonfigurasi bot menggunakan kelas-kelas ini:

```kotlin
val bot = TelegramBot("TOKEN") {
    identifier = "MyBot",
    apiHost = "https://api.telegram.org",
    isTestEnv = true,
    inputListener = InputListenerMapImpl(),
    classManager = ClassManagerImpl(),

    httpClient {
        requestTimeoutMillis = 5000L
        connectTimeoutMillis = 3000L
        socketTimeoutMillis = 2000L
    }
    logging {
        botLogLevel = LogLvl.DEBUG
        httpLogLevel = HttpLogLevel.BODY
    }
    updatesListener {
        dispatcher = Dispatchers.IO
        processingDispatcher = Dispatchers.Unconfined
        pullingDelay = 1000L
    }
    commandParsing {
        commandDelimiter = '*'
        parametersDelimiter = '&'
        restrictSpacesInCommands = true
    }
}
```

Konfigurasi ini menyiapkan bot dengan identifier spesifik, mengaktifkan mode lingkungan uji, mengonfigurasi pembatasan laju, pengaturan klien HTTP, level logging, parameter pendengar pembaruan, dan aturan parsing perintah.

Dengan memanfaatkan opsi konfigurasi ini, developer dapat menyempurnakan bot mereka untuk memenuhi persyaratan spesifik dan mengoptimalkan performa di berbagai skenario operasional.
---