---
---
title: Cấu hình Bot
---

Thư viện cung cấp rất nhiều tùy chọn cấu hình, bạn có thể xem tham chiếu API trong mô tả lớp [`BotConfiguration`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.configuration/-bot-configuration/index.html).

Có hai cách tiếp cận để cấu hình bot:

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

Cũng có khả năng cấu hình thông qua một interface [`ConfigLoader`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.helper/-config-loader/index.html) đặc biệt,<br/> mà bạn có thể sử dụng để tải cài đặt từ các nguồn bên ngoài (`properties`, `command line args`, v.v.).

Việc triển khai interface này có thể được truyền qua constructor thứ cấp và instance sẽ được cấu hình tương ứng.

```kotlin
val bot = TelegramBot(ConfigLoaderImpl)
```

Hiện tại có một số module được cung cấp triển khai interface này như `ktgram-config-env`, `ktgram-config-toml`.

### Tổng quan về BotConfiguration

#### BotConfiguration

Lớp `BotConfiguration` là trung tâm để cấu hình một bot. Nó bao gồm các properties để nhận dạng bot, thiết lập host API, xác định xem bot có hoạt động trong môi trường test hay không, xử lý input, quản lý classes, và kiểm soát tự động xóa input. Ngoài ra, nó cung cấp các properties nội bộ cho giới hạn tỷ lệ, cấu hình HTTP client, logging, listener cập nhật, và parsing command.

##### Properties

- `identifier`: Nhận dạng các instance bot khác nhau trong quá trình xử lý multi-bot.
- `apiHost`: Host của Telegram API.
- `isTestEnv`: Cờ chỉ ra bot có hoạt động trong môi trường test hay không.
- `inputListener`: Instance của class xử lý input.
- `classManager`: Manager được sử dụng để lấy classes.
- `inputAutoRemoval`: Cờ điều chỉnh việc tự động xóa điểm input trong quá trình xử lý.
- `exceptionHandlingStrategy`: Định nghĩa chiến lược xử lý ngoại lệ.
    * `CollectToChannel` - Thu thập vào `TgUpdateHandler.caughtExceptions`.
    * `Throw` - Throw lại được bọc với `TgException`.
    * `DoNothing` - Không làm gì :)
    * `Handle` - Thiết lập custom handler.
- `throwExOnActionsFailure`: Throw exception khi bất kỳ request bot nào thất bại.

##### Configuration Blocks

`BotConfiguration` cũng cung cấp các hàm để cấu hình các thành phần nội bộ của nó:

- `httpClient(block: HttpConfiguration.() -> Unit)`: Cấu hình HTTP client.
- `logging(block: LoggingConfiguration.() -> Unit)`: Cấu hình logging.
- `rateLimiter(block: RateLimiterConfiguration.() -> Unit)`: Cấu hình giới hạn request.
- `updatesListener(block: UpdatesListenerConfiguration.() -> Unit)`: Cấu hình listener cập nhật.
- `commandParsing(block: CommandParsingConfiguration.() -> Unit)`: Xác định pattern parsing command.

### Các Classes Cấu hình Liên quan

#### RateLimiterConfiguration

Cấu hình giới hạn tỷ lệ toàn cục.

- `limits`: Giới hạn tỷ lệ toàn cục.
- `mechanism`: Cơ chế được sử dụng cho giới hạn tỷ lệ, mặc định là thuật toán TokenBucket.
- `exceededAction`: Action được áp dụng khi vượt quá giới hạn.

#### HttpConfiguration

Chứa cấu hình cho HTTP client của bot.

- `requestTimeoutMillis`: Request timeout tính bằng milliseconds.
- `connectTimeoutMillis`: Connection timeout tính bằng milliseconds.
- `socketTimeoutMillis`: Socket timeout tính bằng milliseconds.
- `maxRequestRetry`: Maximum retry cho HTTP requests.
- `retryStrategy`: Strategy cho retries, có thể tùy chỉnh.
- `retryDelay`: Multiplier cho timeout tại mỗi retry.
- `proxy`: Proxy settings cho HTTP calls.
- `additionalHeaders`: Headers được áp dụng cho mọi request.

#### LoggingConfiguration

Quản lý các mức logging cho bot actions và HTTP requests.

- `botLogLevel`: Mức logging cho bot actions.
- `httpLogLevel`: Mức logging cho HTTP requests.

#### UpdatesListenerConfiguration

Cấu hình các tham số liên quan đến pulling updates.

- `dispatcher`: Dispatcher để thu thập incoming updates.
- `processingDispatcher`: Dispatcher để xử lý updates.
- `pullingDelay`: Delay sau mỗi pulling request.
- `updatesPollingTimeout`: Timeout option cho cơ chế long-polling.

#### CommandParsingConfiguration

Xác định các tham số cho command parsing.

- `commandDelimiter`: Separator giữa command và parameters.
- `parametersDelimiter`: Separator giữa parameters.
- `parameterValueDelimiter`: Separator giữa key và value của parameter.
- `restrictSpacesInCommands`: Cờ chỉ ra nếu spaces trong commands có nên được xem là kết thúc command.
- `useIdentifierInGroupCommands`: Sử dụng identifier của bot để match commands chứa @.

### Ví dụ Cấu hình

Đây là ví dụ về cách cấu hình một bot sử dụng các classes này:

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

Cấu hình này thiết lập một bot với các identifiers cụ thể, bật chế độ test environment, cấu hình rate limiting, HTTP client settings, logging levels, update listener parameters, và command parsing rules.

Bằng cách tận dụng các tùy chọn cấu hình này, các nhà phát triển có thể tinh chỉnh bots của họ để đáp ứng các yêu cầu cụ thể và tối ưu hiệu năng trên nhiều tình huống hoạt động khác nhau.
---