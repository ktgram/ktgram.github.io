---
---
title: Functional Dsl
---

### Đến ~~vô cực~~ functional dsl và xa hơn!

Bot hỗ trợ cả hai cách tiếp cận dựa trên chú thích và functional dsl để thiết lập ngữ cảnh. Bạn có thể kết hợp cả hai cách tiếp cận.

### Functional DSL

Functional DSL chỉ là một cách khác để định nghĩa ngữ cảnh bot.

Ví dụ:

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

    bot.setFunctionality {
        onChosenInlineResult {
            println("nhận được kết quả ${update.chosenInlineResult.resultId} từ ${update.user}")
        }
    }
}
```

### Lệnh và Đầu vào

Bạn có thể xử lý cả `lệnh` và `đầu vào` bằng functional DSL.

#### Lệnh

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

    bot.setFunctionality {
        // Lệnh thông thường
        onCommand("/start") {
            message { "Hello" }.send(user, bot)
        }
        
        // Khớp lệnh dựa trên regex
        onCommand("""(red|green|blue)""".toRegex()) {
            message { "bạn đã nhập màu ${update.text}" }.send(user, bot)
        }
    }
}
```

Trong `onCommand`, các tham số đã được phân tích có sẵn dưới dạng `Map<String, String>` dựa trên cấu hình của bạn.

#### Đầu vào

Bạn có thể sử dụng đầu vào qua [`bot.inputListener`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot/-telegram-bot/input-listener.html).

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

    bot.setFunctionality {
        onCommand("/start") {
            message { "Hello, tên bạn là gì?" }.send(user, bot)
            bot.inputListener[user] = "testInput"
        }
        
        onInput("testInput") {
            message { "Xin chào, rất vui được gặp bạn, ${update.text}" }.send(user, bot)
        }
    }
}
```

#### Chuỗi Đầu vào

Đối với luồng đầu vào nhiều bước, sử dụng `inputChain`:

```kotlin
bot.setFunctionality {
    inputChain("conversation") {
        message { "Rất vui được gặp bạn, ${update.text}" }.send(user, bot)
        message { "Món ăn yêu thích của bạn là gì?" }.send(user, bot)
    }.breakIf({ update.text == "peanut butter" }) { // điều kiện dừng chuỗi
        message { "Ồ, tiếc quá, tôi bị dị ứng với nó." }.send(user, bot)
        // hành động sẽ được áp dụng khi điều kiện khớp
    }.andThen {
        // điểm đầu vào tiếp theo nếu điều kiện dừng không khớp
        message { "Lựa chọn tuyệt vời!" }.send(user, bot)
    }
}
```

Chuỗi tự động chuyển sang bước tiếp theo trừ khi gặp điều kiện dừng. Nếu điều kiện dừng khớp và `repeat` là `true` (mặc định), người dùng sẽ ở lại bước hiện tại.

#### Trình xử lý Loại Cập nhật

Xử lý trực tiếp các loại cập nhật cụ thể:

```kotlin
bot.setFunctionality {
    onUpdate(UpdateType.MESSAGE, UpdateType.CALLBACK_QUERY) {
        // Xử lý cả cập nhật message và callback query
        println("Đã nhận cập nhật: ${update.type}")
    }
}
```

#### Trình so khớp Chung

So khớp nội dung văn bản (không chỉ lệnh) bằng `common`:

```kotlin
bot.setFunctionality {
    // So khớp chuỗi
    common("hello") {
        message { "Xin chào!" }.send(user, bot)
    }
    
    // So khớp regex
    common("""\d+""".toRegex()) {
        message { "Bạn đã gửi một số!" }.send(user, bot)
    }
}
```

#### Trình xử lý Dự phòng

Xử lý các cập nhật không được xử lý bởi bất kỳ trình xử lý nào:

```kotlin
bot.setFunctionality {
    whenNotHandled {
        message { "Tôi không hiểu điều đó." }.send(user, bot)
    }
}
```

### Cấu hình Nâng cao

#### Giới hạn Tốc độ

Áp dụng giới hạn tốc độ cho bất kỳ trình xử lý nào:

```kotlin
bot.setFunctionality {
    onCommand("/expensive", rateLimits = RateLimits(5, 60)) {
        // Lệnh này chỉ có thể được gọi 5 lần mỗi 60 giây
        message { "Đang xử lý..." }.send(user, bot)
    }
}
```

#### Guards

Sử dụng guards để thêm logic xác thực tùy chỉnh:

```kotlin
bot.setFunctionality {
    onCommand("/admin", guard = AdminGuard::class) {
        message { "Đã thực thi lệnh admin" }.send(user, bot)
    }
}
```

#### Phân tích Tham số

Tùy chỉnh cách phân tích tham số lệnh:

```kotlin
bot.setFunctionality {
    onCommand("/custom", argParser = CustomArgParser::class) {
        // tham số sẽ được phân tích bằng CustomArgParser
        message { "Tham số: $parameters" }.send(user, bot)
    }
}
```

### Kết hợp Functional và Annotation-Based setting

Bạn có thể sử dụng cả hai cách tiếp cận trong cùng một bot:

```kotlin
// Trình xử lý dựa trên chú thích
@CommandHandler(["/register"])
suspend fun register(ctx: CommandContext) {
    message { "Đã bắt đầu đăng ký" }.send(ctx.user, ctx.bot)
}

// Trình xử lý functional
bot.setFunctionality {
    onCommand("/help") {
        message { "Các lệnh khả dụng: /register, /help" }.send(user, bot)
    }
}
```

Cả hai trình xử lý đều được đăng ký trong cùng một `ActivityRegistry` và hoạt động liền mạch với nhau.

### Xem thêm

* [Action](Actions.md)
* [Tiện ích hữu ích](Useful-utilities-and-tips.md)
---