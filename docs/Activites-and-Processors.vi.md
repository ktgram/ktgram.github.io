---
---
title: Activites And Processors
---

### Introduction

`Activity` trong thuật ngữ của thư viện này là thực thể trừu tượng là sự tổng quát hóa của các thực thể như `@CommandHandler`, `@InputHandler`, `@UnprocessedHandler`, `@CommonHandler`, `@UpdateHandler`, và `@WizardHandler`.

Cũng hãy xem bài viết về [handlers](Handlers.md).

### Collecting activities

Activities được phát hiện và nối lại vào **thời gian biên dịch** bởi bộ xử lý **ktnip** KSP. Ngoại lệ duy nhất là [Functional DSL](Handlers#functional-dsl.md) — các handler được định nghĩa thông qua `bot.setFunctionality { ... }` được đăng ký tại thời gian chạy.

Nếu bạn muốn giới hạn khu vực mà gói sẽ được tìm kiếm, bạn có thể truyền một tham số cho plugin:

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

lưu ý trong trường hợp như vậy, để các hành động đã thu thập được xử lý đúng, bạn cũng phải chỉ định gói trong chính instance.

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.mybot")

    bot.handleUpdates()
    // start long-polling listener
}
```

tùy chọn này được thêm vào để có thể chạy nhiều instance bot:

```gradle
ktGram {
    packages = listOf("com.example.mybot", "com.example.mybot2")
}
```


hoặc nếu bạn không sử dụng plugin để chỉ định các gói khác nhau, bạn cần chỉ định chúng bằng dấu phân cách `;`:

```gradle
ksp {
    arg("package", "com.example.mybot;com.example.mybot2")
}
```

### Processing

#### Webhooks

Trong controller của bạn (hoặc nơi khác nơi `webhook` được xử lý), bạn gọi: [`bot.update.parseAndHandle(webhookString)`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.core/-tg-update-handler/index.html#706360827%2FFunctions%2F-880831646)

#### Long polling

Gọi: `bot.handleUpdates()` hoặc thông qua `bot.update.setListener { handle(it) }`


### See also

* [Update parsing](Update-parsing.md)
* [Activity invocation](Activity-invocation.md)
* [Actions](Actions.md)

---