---
---
title: Web Starters (Spring And Ktor)
---

### Spring starter

Mô-đun Spring Starter cho thư viện là một mô-đun tự động cấu hình tích hợp các chức năng bot Telegram vào ứng dụng Spring Boot. Nó tận dụng sức mạnh của Spring Boot's dependency injection và configuration properties để tự động cấu hình các bot Telegram dựa trên cấu hình được cung cấp. Thư viện này đặc biệt hữu ích cho các nhà phát triển muốn xây dựng các bot Telegram bằng Kotlin và Spring Boot, cung cấp một cách tiếp cận đơn giản hóa cho việc phát triển và quản lý bot.

### Tính năng chính

- **Tự động cấu hình**: Thư viện tự động cấu hình các bot Telegram dựa trên các properties cấu hình được cung cấp, loại bỏ nhu cầu thiết lập thủ công.
- **Configuration Properties**: Hỗ trợ configuration properties để dễ dàng tùy chỉnh các cài đặt bot, chẳng hạn như bot tokens, package names và identifiers.
- **Spring Integration**: Tích hợp liền mạch với hệ sinh thái Spring, sử dụng Spring's dependency injection và application context để quản lý các bot instances.
- **Coroutine Support**: Tận dụng Kotlin coroutines cho các hoạt động bot bất đồng bộ, đảm bảo thực thi hiệu quả và không chặn.

### Bắt đầu

Để sử dụng Spring Starter Library cho Telegram Bots, bạn cần thêm nó làm dependency trong dự án Spring Boot của bạn. Thư viện được thiết kế để hoạt động với các ứng dụng Spring Boot và yêu cầu framework Spring Boot để hoạt động.

#### Dependency

Thêm dependency sau vào file `build.gradle` hoặc `pom.xml` của bạn:

```gradle
dependencies {
    implementation 'eu.vendeli:spring-starter:<version>'
}
```

Thay thế `<version>` với phiên bản mới nhất của thư viện.

#### Configuration

Thư viện sử dụng Spring Boot's `@ConfigurationProperties` để bind configuration properties. Bạn có thể định nghĩa các cấu hình bot của mình trong file `application.properties` hoặc `application.yml` của ứng dụng Spring Boot.

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

Khi thư viện được bao gồm và cấu hình, nó tự động tạo và cấu hình các Telegram bot instances dựa trên cấu hình được cung cấp.

Nó cũng hỗ trợ nhiều bot instances, để khởi tạo nhiều instance chỉ cần khai báo nó như một entry mới trong bot section:

```yaml
ktgram:
 bot:
    - token: YOUR_BOT_TOKEN
    - token: SECOND_BOT_TOKEN
```

### Cấu hình nâng cao

Đối với các cấu hình nâng cao hơn, chẳng hạn như tùy chỉnh hành vi bot hoặc tích hợp với các Spring components khác, bạn có thể mở rộng class `BotConfiguration` và thay đổi cấu hình bot thông qua method `applyCfg` của nó, bạn có thể xem ví dụ [ở đó](https://github.com/vendelieu/telegram-bot_template/blob/spring-bot/src/main/kotlin/com/example/springbot/configuration/BotConfig.kt).

> [!TIP]
> Để cấu hình từng instance được khởi tạo với cấu hình tùy chỉnh, phân biệt chúng bằng identifier của chúng (class BotConfiguration cũng có một identifier).

### Ktor

Mô-đun được thiết kế để tạo điều kiện cho việc tạo webhook server cho Telegram bots. Nó cho phép các nhà phát triển cấu hình server, bao gồm cả SSL/TLS settings, và khai báo nhiều Telegram bots với cấu hình tùy chỉnh. Quá trình thiết lập linh hoạt, cho phép các nhà phát triển điều chỉnh server theo nhu cầu cụ thể của họ.

### Installation

Để cài đặt ktor starter thêm bổ sung vào main dependency:

```gradle
dependencies {
    implementation("eu.vendeli:ktor-starter:x.y.z") // there
    // change x.y.z to current library version
}
```

### Key Components

`serveWebhook` Function

Function serveWebhook là core của thư viện. Nó thiết lập và bắt đầu webhook server cho Telegram bots. Nó chấp nhận hai tham số:

- `wait`: Một boolean chỉ ra liệu server có nên chờ cho ứng dụng dừng lại trước khi tắt hay không. Mặc định là true.
- `serverBuilder`: Một lambda function cấu hình server. Mặc định là một lambda rỗng.

### Configuration

* `WEBHOOK_PREFIX`: Đây là parameter sẽ được sử dụng cho address prefix cho webhook listener route. (mặc định là "/")

#### Server Setup

- `server`: Một method để thiết lập cấu hình server sử dụng hoặc EnvConfiguration hoặc ManualConfiguration.
- `engine`: Một method để cấu hình Netty application engine.
- `ktorModule`: Một method để thêm Ktor modules vào application.

Thư viện cung cấp wide range của các configurable parameters cho server, bao gồm host, port, SSL settings và nhiều hơn nữa. Có hai tùy chọn cụ thể để cấu hình nó:

* `EnvConfiguration`: Đọc configuration values từ environment với prefix `KTGRAM_`.
* `ManualConfiguration`: Cho phép thiết lập thủ công các configuration values, đặt parameters của bạn trong function `server {}`.

Có danh sách các parameters có thể được thiết lập:

- `HOST`: Hostname hoặc IP address của server.
- `PORT`: Port number cho server.
- `SSL_PORT`: Port number cho SSL/TLS connections.
- `PEM_PRIVATE_KEY_PATH`: Đường dẫn đến PEM private key file.
- `PEM_CHAIN_PATH`: Đường dẫn đến PEM certificate chain file.
- `PEM_PRIVATE_KEY`: PEM private key PASSWORD dưới dạng character array.
- `KEYSTORE_PATH`: Đường dẫn đến Java KeyStore file.
- `KEYSTORE_PASSWORD`: Password cho KeyStore.
- `KEY_ALIAS`: Alias cho key trong KeyStore.
- `SSL_ON`: Một boolean chỉ ra liệu SSL/TLS có nên được bật hay không. Mặc định là true.

> [!TIP]
> Nếu có pem certificates, mô-đun tự nó sẽ tạo một jks storage từ chúng tại đường dẫn được chỉ định.

#### Bot Configuration:

Để cấu hình bot gọi `declareBot {}` có các parameters như:

- `token`: Bot token.
- `pckg`: Package name cho bot.
- `configuration`: Một lambda function để cấu hình bot.
- `handlingBehaviour`: Một lambda function để thiết lập bot's handling behavior.
- `onInit`: Một lambda function để được thực thi khi bot được khởi tạo.

### Example Usage

Để sử dụng mô-đun này, gọi function `serveWebhook`, cấu hình nó với các settings mong muốn của bạn, khai báo các bots của bạn. Đây là một ví dụ đơn giản hóa:

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
> Đừng quên set webhook để mọi thứ hoạt động. :)

Theo mặc định module sẽ serve webhook listenening endpoints là `host/BOT_TOKEN`