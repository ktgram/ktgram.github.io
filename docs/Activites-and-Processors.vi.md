---
---
title: Activites And Processors
---

### Giới thiệu

`Activity` trong thuật ngữ của thư viện này là thực thể trừu tượng là tổng quát hóa của các thực thể như `@CommandHandler`, `@InputHandler`, `@UnprocessedHandler`, và `@CommonHandler`.

Bạn cũng có thể xem [bài viết về handlers](Handlers.md).

### Thu thập activities

Activities được thu thập và chuẩn bị tất cả ngữ cảnh trong thời gian biên dịch (trừ những cái được định nghĩa thông qua functional dsl).

Nếu bạn muốn giới hạn vùng mà package sẽ được tìm kiếm, bạn có thể truyền tham số vào plugin:

```gradle
ktGram {
    packages = listOf("com.example.mybot")
}
```

hoặc không dùng plugin thông qua ksp:

```gradle
ksp {
    arg("package", "com.example.mybot")
}
```

lưu ý trong trường hợp như vậy, để các actions được thu thập được xử lý chính xác, bạn cũng phải chỉ định package trong bản thân instance.

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.mybot")

    bot.handleUpdates()
    // bắt đầu long-polling listener
}
```

tùy chọn này được thêm vào để có thể chạy nhiều instance bot:

```gradle
ktGram {
    packages = listOf("com.example.mybot", "com.example.mybot2")
}
```

hoặc nếu bạn không dùng plugin để chỉ định các package khác nhau, bạn cần chỉ định chúng với `;` làm separator:

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

* [Update parsing](Update-parsing.md)
* [Activity invocation](Activity-invocation.md)
* [Actions](Actions.md)

---