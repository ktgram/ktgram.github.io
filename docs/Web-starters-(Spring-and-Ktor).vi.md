---
---
title: Web Starters (Spring And Ktor)
---

### Spring starter

Mô-đun Spring Starter cho thư viện là một mô-đun tự động cấu hình tích hợp các chức năng bot Telegram vào các ứng dụng Spring Boot. Nó tận dụng sức mạnh của dependency injection và configuration properties của Spring Boot để tự động cấu hình các bot Telegram dựa trên cấu hình được cung cấp. Thư viện này đặc biệt hữu ích cho các nhà phát triển muốn xây dựng các bot Telegram sử dụng Kotlin và Spring Boot, cung cấp cách tiếp cận được tối ưu hóa cho việc phát triển và quản lý bot.

### Tính năng chính

- **Tự động cấu hình**: Thư viện tự động cấu hình các bot Telegram dựa trên các properties cấu hình được cung cấp, loại bỏ nhu cầu thiết lập thủ công.
- **Properties cấu hình**: Nó hỗ trợ properties cấu hình để tùy chỉnh dễ dàng các cài đặt bot, chẳng hạn như bot tokens, tên gói và identifiers.
- **Tích hợp Spring**: Tích hợp liền mạch với hệ sinh thái Spring, sử dụng dependency injection và application context của Spring để quản lý các bot instances.
- **Hỗ trợ Coroutine**: Tận dụng Kotlin coroutines cho các hoạt động bot bất đồng bộ, đảm bảo thực thi hiệu quả và không bị chặn.

### Bắt đầu

Để sử dụng Spring Starter Library cho Telegram Bots, bạn cần thêm nó làm dependency vào dự án Spring Boot của bạn. Thư viện được thiết kế để hoạt động với các ứng dụng Spring Boot và yêu cầu framework Spring Boot để hoạt động.

#### Dependency

Thêm dependency sau vào tệp `build.gradle` hoặc `pom.xml` của bạn:

```gradle
dependencies {
    implementation 'eu.vendeli:spring-starter:<version>'
}
```

Thay thế `<version>` với phiên bản mới nhất của thư viện.

#### Cấu hình

Thư viện sử dụng `@ConfigurationProperties` của Spring Boot để liên kết properties cấu hình. Bạn có thể định nghĩa cấu hình bot của mình trong tệp `application.properties` hoặc `application.yml` của ứng dụng Spring Boot của bạn.

```yaml
ktgram:
 autoStartPolling: true
 shareHttpClient: true
 bot:
    - token: YOUR_BOT_TOKEN
      pckg: com.example.bot
      identifier: MyBot
```

#### Sử dụng

Sau khi thư viện được thêm và cấu hình, nó tự động tạo và cấu hình các bot instances của Telegram dựa trên cấu hình được cung cấp.

Nó cũng hỗ trợ nhiều bot instances, để khởi tạo nhiều bot chỉ cần khai báo nó như một entry mới trong phần bot:

```yaml
ktgram:
 bot:
    - token: YOUR_BOT_TOKEN
    - token: SECOND_BOT_TOKEN
```

### Cấu hình nâng cao

Đối với các cấu hình nâng cao hơn, chẳng hạn như tùy chỉnh hành vi bot hoặc tích hợp với các thành phần Spring khác, bạn có thể mở rộng lớp `BotConfiguration` và thay đổi cấu hình bot thông qua phương thức `applyCfg` của nó, bạn có thể xem ví dụ [ở đó](https://github.com/vendelieu/telegram-bot_template/blob/spring-bot/src/main/kotlin/com/example/springbot/configuration/BotConfig.kt).

> [!TIP]
> Để cấu hình từng instance đã khởi tạo với cấu hình tùy chỉnh, phân biệt chúng bằng identifier của chúng (lớp BotConfiguration cũng có identifier).

### Ktor

Mô-đun được thiết kế để tạo điều kiện thuận lợi cho việc tạo webhook server cho các bot Telegram. Nó cho phép các nhà phát triển cấu hình server, bao gồm cả cài đặt SSL/TLS, và khai báo nhiều bot Telegram với cấu hình tùy chỉnh. Quá trình thiết lập linh hoạt, cho phép các nhà phát triển điều chỉnh server theo nhu cầu cụ thể của họ.

### Cài đặt

Để cài đặt ktor starter thêm bổ sung vào dependency chính:

```gradle
dependencies {
    implementation("eu.vendeli:ktor-starter:x.y.z") // ở đó
    // thay đổi x.y.z thành phiên bản thư viện hiện tại
}
```

### Thành phần chính

Hàm `serveWebhook`

Hàm serveWebhook là lõi của thư viện. Nó thiết lập và bắt đầu webhook server cho các bot Telegram. Nó chấp nhận hai tham số:

- `wait`: Một boolean chỉ ra liệu server có nên đợi ứng dụng dừng lại trước khi tắt hay không. Mặc định là true.
- `serverBuilder`: Một lambda function cấu hình server. Mặc định là lambda rỗng.

### Cấu hình

* `WEBHOOK_PREFIX`: đó là tham số sẽ được sử dụng cho tiền tố địa chỉ cho webhook listener route. (mặc định là "/")

#### Thiết lập server

- `server`: Một phương thức để đặt cấu hình server sử dụng hoặc EnvConfiguration hoặc ManualConfiguration.
- `engine`: Một phương thức để cấu hình Netty application engine.
- `ktorModule`: Một phương thức để thêm Ktor modules vào ứng dụng.

Thư viện cung cấp phạm vi rộng các tham số có thể cấu hình cho server, bao gồm host, port, SSL settings, và hơn nữa. Có hai tùy chọn cụ thể cho việc cấu hình nó:

* `EnvConfiguration`: Đọc các giá trị cấu hình từ environment với tiền tố `KTGRAM_`.
* `ManualConfiguration`: Cho phép thiết lập thủ công các giá trị cấu hình, đặt các tham số của bạn trong hàm `server {}`.

Đây là danh sách các tham số có thể được đặt:

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
> Nếu có pem certificates, mô-đun tự nó sẽ tạo jks storage từ chúng tại đường dẫn được chỉ định.

#### Cấu hình Bot:

Để cấu hình bot gọi `declareBot {}` có các tham số như:

- `token`: Bot token.
- `pckg`: Tên gói cho bot.
- `configuration`: Một lambda function để cấu hình bot.
- `handlingBehaviour`: Một lambda function để đặt hành vi xử lý của bot.
- `onInit`: Một lambda function được thực thi khi bot được khởi tạo.

### Ví dụ sử dụng

Để sử dụng mô-đun này, gọi hàm `serveWebhook`, cấu hình nó với các cài đặt mong muốn của bạn, khai báo các bot của bạn. Đây là một ví dụ đơn giản:

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
            // Đặt các tham số cấu hình khác theo cần
        }
        declareBot {
            token = "YOUR_BOT_TOKEN"
            // Cấu hình các cài đặt bot khác
        }
        // Thêm nhiều bot hoặc đặt các tham số khác nếu cần
    }
}
```

> [!CAUTION]
> Đừng quên đặt webhook để mọi thứ hoạt động. :)

Mặc định mô-đun sẽ phục vụ webhook listening endpoints là `host/BOT_TOKEN`


---