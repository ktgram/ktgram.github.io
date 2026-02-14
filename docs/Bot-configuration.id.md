---
---
title: Konfigurasi Bot
---

Library menyediakan banyak opsi konfigurasi, Anda dapat melihat referensi API di kelas [`BotConfiguration`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.configuration/-bot-configuration/index.html).

Ada juga dua pendekatan untuk mengonfigurasi bot:

### Lambda Configurator

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

### Interface ConfigLoader

Ada juga kemampuan untuk mengonfigurasi melalui interface [`ConfigLoader`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.helper/-config-loader/index.html) khusus,<br/> yang dapat Anda gunakan untuk memuat pengaturan dari sumber eksternal (`properties`, `command line args`, dll).

Implementasi dari interface ini dapat dilewatkan melalui constructor sekunder dan instance akan dikonfigurasi sesuai.

```kotlin
val bot = TelegramBot(ConfigLoaderImpl)
```

Saat ini ada beberapa modul yang disediakan yang mengimplementasikan interface ini seperti `ktgram-config-env`, `ktgram-config-toml`.

### Ikhtisar BotConfiguration

#### BotConfiguration

Kelas `BotConfiguration` adalah pusat untuk mengonfigurasi bot. Ini termasuk properti untuk mengidentifikasi bot, mengatur host API, menentukan apakah bot beroperasi di lingkungan test, menangani input, mengelola kelas, dan mengontrol penghapusan input otomatis. Selain itu, ini menyediakan properti internal untuk rate limiting, konfigurasi HTTP client, logging, update listening, dan command parsing.

##### Properti

- `identifier`: Mengidentifikasi instance bot yang berbeda selama pemrosesan multi-bot.
- `apiHost`: Host dari Telegram API.
- `isTestEnv`: Flag yang menunjukkan apakah bot beroperasi di lingkungan test.
- `inputListener`: Instance dari kelas penanganan input.
- `classManager`: Manager yang digunakan untuk mendapatkan kelas.
- `inputAutoRemoval`: Flag yang mengatur penghapusan otomatis titik input selama pemrosesan.
- `exceptionHandlingStrategy`: Menentukan strategi untuk menangani exception.
    * `CollectToChannel` - Kumpulkan ke `TgUpdateHandler.caughtExceptions`.
    * `Throw` - Lempar lagi dibungkus dengan `TgException`.
    * `DoNothing` - Lakukan tidak ada :)
    * `Handle` - Setel handler kustom.
- `throwExOnActionsFailure`: Melempar exception ketika ada permintaan bot yang gagal.

##### Blok Konfigurasi

`BotConfiguration` juga menawarkan fungsi untuk mengonfigurasi komponen internalnya:

- `httpClient(block: HttpConfiguration.() -> Unit)`: Mengonfigurasi HTTP client.
- `logging(block: LoggingConfiguration.() -> Unit)`: Mengonfigurasi logging.
- `rateLimiter(block: RateLimiterConfiguration.() -> Unit)`: Mengonfigurasi request limiting.
- `updatesListener(block: UpdatesListenerConfiguration.() -> Unit)`: Mengonfigurasi updates listener.
- `commandParsing(block: CommandParsingConfiguration.() -> Unit)`: Menentukan pola command parsing.

### Kelas Konfigurasi Terkait

#### RateLimiterConfiguration

Mengonfigurasi global rate limiting.

- `limits`: Global rate limits.
- `mechanism`: Mekanisme yang digunakan untuk rate limiting, default adalah algoritma TokenBucket.
- `exceededAction`: Action yang diterapkan ketika limit terlewati.

#### HttpConfiguration

Berisi konfigurasi untuk HTTP client bot.

- `requestTimeoutMillis`: Request timeout dalam milidetik.
- `connectTimeoutMillis`: Connection timeout dalam milidetik.
- `socketTimeoutMillis`: Socket timeout dalam milidetik.
- `maxRequestRetry`: Maksimum retry untuk HTTP requests.
- `retryStrategy`: Strategi untuk retry, dapat disesuaikan.
- `retryDelay`: Multiplier untuk timeout pada setiap retry.
- `proxy`: Proxy settings untuk HTTP calls.
- `additionalHeaders`: Headers yang diterapkan ke setiap request.

#### LoggingConfiguration

Mengelola level logging untuk bot actions dan HTTP requests.

- `botLogLevel`: Level log untuk bot actions.
- `httpLogLevel`: Level log untuk HTTP requests.

#### UpdatesListenerConfiguration

Mengonfigurasi parameter terkait pulling updates.

- `dispatcher`: Dispatcher untuk mengumpulkan incoming updates.
- `processingDispatcher`: Dispatcher untuk memproses updates.
- `pullingDelay`: Delay setelah setiap pulling request.
- `updatesPollingTimeout`: Timeout option untuk long-polling mechanism.

#### CommandParsingConfiguration

Menentukan parameter untuk command parsing.

- `commandDelimiter`: Separator antara command dan parameters.
- `parametersDelimiter`: Separator antara parameters.
- `parameterValueDelimiter`: Separator antara key dan value dari parameter.
- `restrictSpacesInCommands`: Flag yang menunjukkan apakah spasi dalam commands harus dianggap sebagai akhir dari command.
- `useIdentifierInGroupCommands`: Menggunakan identifier bot untuk mencocokkan commands yang mengandung @.

### Contoh Konfigurasi

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

Konfigurasi ini menyiapkan bot dengan identifier khusus, mengaktifkan mode test environment, mengonfigurasi rate limiting, HTTP client settings, logging levels, update listener parameters, dan command parsing rules.

Dengan memanfaatkan opsi konfigurasi ini, developer dapat menyesuaikan bot mereka untuk memenuhi persyaratan spesifik dan mengoptimalkan kinerja di berbagai skenario operasional.
---