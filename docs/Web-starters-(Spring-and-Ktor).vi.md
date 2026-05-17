---
---
title: Web Starters (Spring And Ktor)
---

### Spring starter

Mô-đun Spring Starter cho thư viện là một mô-đun cấu hình tự động tích hợp các chức năng bot Telegram vào các ứng dụng Spring Boot. Nó tận dụng sức mạnh của việc tiêm phụ thuộc và các thuộc tính cấu hình của Spring Boot để tự động cấu hình bot Telegram dựa trên cấu hình đã cung cấp. Thư viện này đặc biệt hữu ích cho các nhà phát triển muốn xây dựng bot Telegram bằng Kotlin và Spring Boot, cung cấp một cách tiếp cận hợp lý cho việc phát triển và quản lý bot.

### Key Features

- **Auto-Configuration**: Thư viện tự động cấu hình bot Telegram dựa trên các thuộc tính cấu hình đã cung cấp, loại bỏ nhu cầu thiết lập thủ công.
- **Configuration Properties**: Hỗ trợ các thuộc tính cấu hình để dễ dàng tùy chỉnh cài đặt bot, như token bot, tên package và identifier.
- **Spring Integration**: Tích hợp liền mạch với hệ sinh thái Spring, sử dụng tiêm phụ thuộc và ApplicationContext của Spring để quản lý các thể hiện bot.
- **Coroutine Support**: Tận dụng coroutine của Kotlin cho các thao tác bot bất đồng bộ, đảm bảo thực thi hiệu quả và không chặn.

### Getting Started

Để sử dụng Spring Starter Library cho Telegram Bots, bạn cần đưa nó vào như một phụ thuộc trong dự án Spring Boot của mình. Thư viện được thiết kế để làm việc với các ứng dụng Spring Boot và yêu cầu framework Spring Boot để hoạt động.

#### Dependency

Thêm phụ thuộc sau vào file `build.gradle` hoặc `pom.xml` của bạn:

```gradle
dependencies {
    implementation 'eu.vendeli:spring-starter:<version>'
}
```

Thay `<version>` bằng phiên bản mới nhất của thư viện.

#### Configuration

Thư viện sử dụng `@ConfigurationProperties` của Spring Boot để liên kết các thuộc tính cấu hình. Bạn có thể định nghĩa cấu hình bot trong file `application.properties` hoặc `application.yml` của ứng dụng Spring Boot.

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

Khi thư viện đã được đưa vào và cấu hình, nó sẽ tự động tạo và cấu hình các thể hiện bot Telegram dựa trên cấu hình đã cung cấp.

Nó cũng hỗ trợ nhiều thể hiện bot, để khởi tạo nhiều bot chỉ cần khai báo chúng như mục mới trong phần bot:

```yaml
ktgram:
 bot:
    - token: YOUR_BOT_TOKEN
    - token: SECOND_BOT_TOKEN
```

### Advanced Configuration

Đối với các cấu hình nâng cao hơn, như tùy chỉnh hành vi bot hoặc tích hợp với các thành phần Spring khác, bạn có thể kế thừa lớp `BotConfiguration` và thay đổi cấu hình bot thông qua phương thức `applyCfg` của nó, xem ví dụ [ở đây](https://github.com/vendelieu/telegram-bot_template/blob/spring-bot/src/main/kotlin/com/example/springbot/configuration/BotConfig.kt).

> [!TIP]
> Để cấu hình mỗi thể hiện đã khởi tạo bằng một cấu hình tùy chỉnh, hãy phân biệt chúng bằng identifier (lớp BotConfiguration cũng có một identifier).

### Ktor

Mô-đun này được thiết kế để hỗ trợ việc tạo một server webhook cho bot Telegram. Nó cho phép các nhà phát triển cấu hình server, bao gồm các thiết lập SSL/TLS, và khai báo nhiều bot Telegram với các cấu hình tùy chỉnh. Quy trình thiết lập linh hoạt, cho phép các nhà phát triển tùy chỉnh server theo nhu cầu cụ thể.

### Installation

Để cài đặt ktor starter, thêm phụ thuộc phụ vào phụ thuộc chính:

```gradle
dependencies {
    implementation("eu.vendeli:ktor-starter:x.y.z") // there
    // change x.y.z to current library version
}
```

### Key Components

`serveWebhook` Function

Hàm `serveWebhook` là lõi của thư viện. Nó thiết lập và khởi động server webhook cho bot Telegram. Hàm nhận hai tham số:

- `wait`: Một boolean chỉ định liệu server có nên chờ ứng dụng dừng trước khi tắt hay không. Mặc định là true.
- `serverBuilder`: Một hàm lambda cấu hình server. Mặc định là một lambda rỗng.

### Configuration

* `WEBHOOK_PREFIX`: là tham số sẽ được dùng làm tiền tố địa chỉ cho route lắng nghe webhook. (mặc định là "/")

#### Server Setup

- `server`: Phương thức để đặt cấu hình server bằng EnvConfiguration hoặc ManualConfiguration.
- `engine`: Phương thức để cấu hình engine ứng dụng Netty.
- `ktorModule`: Phương thức để thêm các module Ktor vào ứng dụng.

Thư viện cung cấp nhiều tham số cấu hình cho server, bao gồm host, port, thiết lập SSL, và hơn nữa. Có hai tùy chọn cụ thể để cấu hình:

* `EnvConfiguration`: Đọc giá trị cấu hình từ môi trường với tiền tố `KTGRAM_`.
* `ManualConfiguration`: Cho phép thiết lập thủ công các giá trị cấu hình, đặt các tham số của bạn trong hàm `server {}`.

Có danh sách các tham số có thể thiết lập:

- `HOST`: Tên máy hoặc địa chỉ IP của server.
- `PORT`: Số cổng cho server.
- `SSL_PORT`: Số cổng cho kết nối SSL/TLS.
- `PEM_PRIVATE_KEY_PATH`: Đường dẫn đến file khóa private PEM.
- `PEM_CHAIN_PATH`: Đường dẫn đến file chuỗi chứng chỉ PEM.
- `PEM_PRIVATE_KEY`: MẬT KHẨU của khóa private PEM dưới dạng mảng ký tự.
- `KEYSTORE_PATH`: Đường dẫn đến file Java KeyStore.
- `KEYSTORE_PASSWORD`: Mật khẩu cho KeyStore.
- `KEY_ALIAS`: Alias cho khóa trong KeyStore.
- `SSL_ON`: Boolean chỉ định liệu SSL/TLS có được bật hay không. Mặc định là true.

> [!TIP]
> Nếu có chứng chỉ pem, mô-đun sẽ tự tạo một kho lưu trữ jks từ chúng tại đường dẫn được chỉ định.

#### Bot Configuration:

Để cấu hình bot, gọi `declareBot {}` với các tham số sau:

- `token`: Token của bot.
- `pckg`: Tên package cho bot.
- `configuration`: Hàm lambda để cấu hình bot.
- `handlingBehaviour`: Hàm lambda để đặt hành vi xử lý của bot.
- `onInit`: Hàm lambda sẽ được thực thi khi bot được khởi tạo.

### Example Usage

Để sử dụng mô-đun này, gọi hàm `serveWebhook`, cấu hình nó với các thiết lập mong muốn, khai báo bot của bạn. Dưới đây là một ví dụ đơn giản:

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
> Đừng quên thiết lập webhook để mọi thứ hoạt động. :)

Mặc định mô-đun sẽ phục vụ các endpoint webhook dưới dạng `host/BOT_TOKEN`


---