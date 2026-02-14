---
---
title: Hoạt động và Bộ xử lý
---

### Giới thiệu

`Activity` trong thư viện này là thực thể trừu tượng tổng quát hóa các thực thể như `@CommandHandler`, `@InputHandler`, `@UnprocessedHandler`, và `@CommonHandler`.

Cũng xem thêm bài viết về [handlers](Handlers.md).

### Thu thập hoạt động

Các hoạt động được thu thập và chuẩn bị tất cả ngữ cảnh trong thời gian biên dịch (trừ những hoạt động được định nghĩa thông qua DSL chức năng).

Nếu bạn muốn giới hạn khu vực mà gói sẽ được tìm kiếm, bạn có thể truyền tham số cho plugin:

```gradle
ktGram {
    packages = listOf("com.example.mybot")
}
```

hoặc không sử dụng plugin thông qua ksp:

```gradle
ksp {
    arg("package", "com.example.mybot")
}
```

lưu ý rằng trong trường hợp này, để các hành động được thu thập được xử lý chính xác, bạn cũng phải chỉ định gói trong chính thể hiện đó.

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.mybot")

    bot.handleUpdates()
    // bắt đầu trình lắng nghe long-polling
}
```

tùy chọn này được thêm vào để có thể chạy nhiều thể hiện bot:

```gradle
ktGram {
    packages = listOf("com.example.mybot", "com.example.mybot2")
}
```


hoặc nếu bạn không sử dụng plugin để chỉ định các gói khác nhau, bạn cần chỉ định chúng với dấu phân cách `;`:

```gradle
ksp {
    arg("package", "com.example.mybot;com.example.mybot2")
}
```

### Xử lý

#### Webhooks

Trong controller của bạn (hoặc một nơi khác nơi `webhook` được xử lý), bạn gọi: [`bot.update.parseAndHandle(webhookString)`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.core/-tg-update-handler/index.html#706360827%2FFunctions%2F-880831646)

#### Long polling

Gọi: `bot.handleUpdates()` hoặc thông qua `bot.update.setListener { handle(it) }`


### Xem thêm

* [Cập nhật phân tích](Update-parsing.md)
* [Gọi hoạt động](Activity-invocation.md)
* [Hành động](Actions.md)