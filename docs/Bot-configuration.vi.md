---
---
title: Cấu hình Bot
---

Thư viện cung cấp nhiều tùy chọn cấu hình, bạn có thể xem tham chiếu API trong mô tả lớp [`BotConfiguration`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.configuration/-bot-configuration/index.html).

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

Cũng có khả năng cấu hình thông qua interface [`ConfigLoader`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.helper/-config-loader/index.html) đặc biệt,<br/> mà bạn có thể sử dụng để tải cài đặt từ các nguồn bên ngoài (`properties`, `command line args`, etc.).

Việc triển khai interface này có thể được truyền qua constructor thứ cấp và instance sẽ được cấu hình tương ứng.

```kotlin
val bot = TelegramBot(ConfigLoaderImpl)
```

Hiện tại có một số module được cung cấp triển khai interface này như `ktgram-config-env`, `ktgram-config-toml`.

### Tổng quan về BotConfiguration

#### BotConfiguration

Lớp `BotConfiguration` là trung tâm để cấu hình bot. Nó bao gồm các thuộc tính để xác định bot, thiết lập host API, xác định bot có hoạt động trong môi trường thử nghiệm hay không, xử lý đầu vào, quản lý lớp, và kiểm soát tự động xóa đầu vào. Ngoài ra, nó cung cấp các thuộc tính nội bộ cho giới hạn tốc độ, cấu hình client HTTP, ghi log, lắng nghe cập nhật, và phân tích lệnh.

##### Thuộc tính

- `identifier`: Xác định các instance bot khác nhau trong quá trình xử lý multi-bot.
- `apiHost`: Host của Telegram API.
- `isTestEnv`: Cờ chỉ ra bot có hoạt động trong môi trường thử nghiệm hay không.
- `inputListener`: Instance của lớp xử lý đầu vào.
- `classManager`: Trình quản lý được sử dụng để lấy lớp.
- `inputAutoRemoval`: Cờ điều chỉnh tự động xóa điểm đầu vào trong quá trình xử lý.
- `exceptionHandlingStrategy`: Định nghĩa chiến lược xử lý ngoại lệ.
    * `CollectToChannel` - Thu thập vào `TgUpdateHandler.caughtExceptions`.
    * `Throw` - Ném lại được bọc với `TgException`.
    * `DoNothing` - Không làm gì :)
    * `Handle` - Đặt trình xử lý tùy chỉnh.
- `throwExOnActionsFailure`: Ném ngoại lệ khi bất kỳ request bot nào thất bại.

##### Khối Cấu hình

`BotConfiguration` cũng cung cấp các hàm để cấu hình các thành phần nội bộ của nó:

- `httpClient(block: HttpConfiguration.() -> Unit)`: Cấu hình client HTTP.
- `logging(block: LoggingConfiguration.() -> Unit)`: Cấu hình ghi log.
- `rateLimiter(block: RateLimiterConfiguration.() -> Unit)`: Cấu hình giới hạn request.
- `updatesListener(block: UpdatesListenerConfiguration.() -> Unit)`: Cấu hình trình lắng nghe cập nhật.
- `commandParsing(block: CommandParsingConfiguration.() -> Unit)`: Xác định pattern phân tích lệnh.

### Các Lớp Cấu hình Liên quan

#### RateLimiterConfiguration

Cấu hình giới hạn tốc độ toàn cục.

- `limits`: Giới hạn tốc độ toàn cục.
- `mechanism`: Cơ chế được sử dụng cho giới hạn tốc độ, mặc định là thuật toán TokenBucket.
- `exceededAction`: Hành động được áp dụng khi vượt quá giới hạn.

#### HttpConfiguration

Chứa cấu hình cho client HTTP của bot.

- `requestTimeoutMillis`: Thời gian chờ request tính bằng milliseconds.
- `connectTimeoutMillis`: Thời gian chờ kết nối tính bằng milliseconds.
- `socketTimeoutMillis`: Thời gian chờ socket tính bằng milliseconds.
- `maxRequestRetry`: Số lần thử lại tối đa cho HTTP requests.
- `retryStrategy`: Chiến lược cho retries, có thể tùy chỉnh.
- `retryDelay`: Nhân tử cho thời gian chờ ở mỗi lần thử lại.
- `proxy`: Cài đặt proxy cho HTTP calls.
- `additionalHeaders`: Headers được áp dụng cho mọi request.

#### LoggingConfiguration

Quản lý mức ghi log cho hành động bot và HTTP requests.

- `botLogLevel`: Mức log cho hành động bot.
- `httpLogLevel`: Mức log cho HTTP requests.

#### UpdatesListenerConfiguration

Cấu hình các tham số liên quan đến pulling updates.

- `dispatcher`: Dispatcher để thu thập incoming updates.
- `processingDispatcher`: Dispatcher để xử lý updates.
- `pullingDelay`: Độ trễ sau mỗi pulling request.
- `updatesPollingTimeout`: Tùy chọn timeout cho cơ chế long-polling.

#### CommandParsingConfiguration

Xác định các tham số cho phân tích lệnh.

- `commandDelimiter`: Phân tách giữa lệnh và tham số.
- `parametersDelimiter`: Phân tách giữa các tham số.
- `parameterValueDelimiter`: Phân tách giữa khóa và giá trị của tham số.
- `restrictSpacesInCommands`: Cờ chỉ ra liệu khoảng trắng trong lệnh có nên được coi là kết thúc lệnh hay không.
- `useIdentifierInGroupCommands`: Sử dụng identifier của bot để match lệnh chứa @.

### Ví dụ Cấu hình

Đây là ví dụ về cách cấu hình bot sử dụng các lớp này:

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

Cấu hình này thiết lập bot với các identifier cụ thể, bật chế độ test environment, cấu hình giới hạn tốc độ, cài đặt client HTTP, mức ghi log, các tham số listener cập nhật, và quy tắc phân tích lệnh.

Bằng cách tận dụng các tùy chọn cấu hình này, các nhà phát triển có thể tinh chỉnh bot của họ để đáp ứng các yêu cầu cụ thể và tối ưu hóa hiệu năng trên nhiều kịch bản hoạt động khác nhau.
---