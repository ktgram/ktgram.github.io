---
---
title: Handlers
---


### Variety of Handlers

Trong việc phát triển bot, đặc biệt là trong các hệ thống liên quan đến tương tác người dùng, việc quản lý và xử lý lệnh cũng như sự kiện một cách hiệu quả là rất quan trọng.

Các annotation này đánh dấu các hàm được thiết kế để xử lý các lệnh, đầu vào hoặc cập nhật cụ thể và cung cấp siêu dữ liệu như từ khóa lệnh, phạm vi và guard.

### Annotations Overview

#### CommandHandler

Annotation `CommandHandler` được sử dụng để đánh dấu các hàm xử lý các lệnh cụ thể. Annotation này bao gồm các thuộc tính định nghĩa từ khóa và phạm vi của lệnh.

-   **value**: Xác định các từ khóa liên quan tới lệnh.
-   **scope**: Xác định ngữ cảnh hoặc phạm vi mà lệnh sẽ được kiểm tra.

```kotlin
@CommandHandler(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommandHandler.CallbackQuery

Một phiên bản đặc biệt của annotation `CommandHandler` được thiết kế riêng cho việc xử lý callback query. Nó bao gồm các thuộc tính tương tự như `CommandHandler`, tập trung vào các lệnh liên quan tới callback.

_Thực tế nó giống như chỉ `@CommandHandler` với phạm vi `UpdateType.CALLBACK_QUERY` được đặt trước sẵn_.

-   **value**: Xác định các từ khóa liên quan tới lệnh.
-   **autoAnswer**: Tự động trả lời `callbackQuery` (gọi `answerCallbackQuery` trước khi xử lý).

```kotlin
@CommandHandler.CallbackQuery(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### CommonHandler

Annotation `CommonHandler` nhằm vào các hàm xử lý lệnh có mức độ ưu tiên thấp hơn so với `CommandHandler` và `InputHandler`. Nó được sử dụng ở mức nguồn và cung cấp cách linh hoạt để định nghĩa các handler lệnh chung.

**Lưu ý, mức ưu tiên chỉ hoạt động trong chính `@CommonHandler` (không ảnh hưởng tới các handler khác).**

##### CommonHandler.Text

Annotation này chỉ định việc khớp văn bản với các cập nhật. Nó bao gồm các thuộc tính để định nghĩa văn bản khớp, điều kiện lọc, mức ưu tiên và phạm vi.

-   **value**: Văn bản sẽ được so sánh với các cập nhật đến.
-   **filter**: Lớp định nghĩa các điều kiện được sử dụng trong quá trình khớp.
-   **priority**: Cấp độ ưu tiên của handler, trong đó 0 là mức cao nhất.
-   **scope**: Ngữ cảnh hoặc phạm vi mà việc khớp văn bản sẽ được kiểm tra.

```kotlin
@CommonHandler.Text(["text"], filter = isNewUserFilter::class, priority = 10)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommonHandler.Regex

Tương tự như `CommonHandler.Text`, annotation này được dùng để khớp các cập nhật dựa trên biểu thức chính quy. Nó bao gồm các thuộc tính để định nghĩa mẫu regex, tùy chọn, điều kiện lọc, mức ưu tiên và phạm vi.

-   **value**: Mẫu regex dùng để khớp.
-   **options**: Các tùy chọn regex ảnh hưởng đến hành vi của mẫu.
-   **filter**: Lớp định nghĩa các điều kiện được sử dụng trong quá trình khớp.
-   **priority**: Cấp độ ưu tiên của handler, trong đó 0 là mức cao nhất.
-   **scope**: Ngữ cảnh hoặc phạm vi mà việc khớp regex sẽ được kiểm tra.

```kotlin
@CommonHandler.Regex("^\d+$", scope = [UpdateType.EDITED_MESSAGE])
suspend fun test(update: EditedMessageUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### InputHandler

Annotation `InputHandler` đánh dấu các hàm xử lý các sự kiện đầu vào cụ thể. Nó dành cho các hàm xử lý đầu vào tại thời gian chạy và bao gồm các thuộc tính để định nghĩa từ khóa và phạm vi đầu vào.

-   **value**: Xác định các từ khóa liên quan tới sự kiện đầu vào.

```kotlin
@InputHandler("text")
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UnprocessedHandler

Annotation `UnprocessedHandler` được dùng để đánh dấu các hàm xử lý các cập nhật mà không được các handler khác xử lý. Nó đảm bảo bất kỳ cập nhật nào không được xử lý sẽ được quản lý thích hợp, với chỉ một điểm xử lý duy nhất có thể cho loại handler này.

```kotlin
@UnprocessedHandler
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UpdateHandler

Annotation `UpdateHandler` đánh dấu các hàm xử lý các loại cập nhật đến cụ thể. Nó cung cấp cách phân loại và xử lý các loại cập nhật một cách có hệ thống.

-   **type**: Xác định các loại cập nhật mà hàm handler sẽ xử lý.
-   **messageKind** *(added in 9.5)*: Tập tùy chọn của [`MessageKind`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-message-kind/index.html) dùng để thu hẹp việc phân phối tới các cập nhật mang tin nhắn mà loại được phát hiện khớp. Trống (mặc định) nghĩa là bất kỳ loại nào cũng khớp.

```kotlin
@UpdateHandler([UpdateType.PRE_CHECKOUT_QUERY])
suspend fun test(update: PreCheckoutQueryUpdate, user: User, bot: TelegramBot) {
    //...
}
```

##### Filtering by `MessageKind`

Sử dụng tham số `messageKind` để phản hồi chỉ một tập hợp con cụ thể của các cập nhật tin nhắn (ảnh, văn bản, sự kiện dịch vụ, …) thay vì tự kiểm tra các trường nullable:

```kotlin
@UpdateHandler(type = [UpdateType.MESSAGE], messageKind = [MessageKind.PHOTO])
suspend fun onPhoto(update: MessageUpdate, bot: TelegramBot) {
    //...
}
```
### Handler Companion Annotations

Ngoài ra còn có các annotation bổ trợ, không bắt buộc, để bổ sung hành vi tùy chọn cho các handler.

Chúng có thể được đặt cả trên các hàm mà một handler được áp dụng và trên các lớp; trong trường hợp lớp, chúng sẽ tự động được áp dụng cho tất cả các handler trong lớp đó, nhưng nếu cần có thể có hành vi riêng cho một số hàm.

Nghĩa là việc áp dụng có mức ưu tiên như sau, `Function` > `Class`, trong đó hàm có ưu tiên cao hơn.

#### Rate Limiting

Thêm vào đó, chúng tôi cũng công bố cơ chế giới hạn tốc độ được mô tả trong các annotation.

Bạn có thể đặt giới hạn chung cho từng người dùng:

```kotlin
// ...
val bot = TelegramBot("BOT_TOKEN") {
    rateLimiter { // general limits
        limits = RateLimits(period = 10000, rate = 5)
    }
}
```

###### Handler specific

Giới hạn cho một số hành động nhất định có thể được định nghĩa bằng annotation `RateLimits`, hỗ trợ `@CommandHandler`, `@CommandHandler.CallbackQuery`, `@InputHandler`, `@CommonHandler`.

```kotlin
@CommandHandler(["/start"])
@RateLimits(period = 1000L, rate = 1L)
suspend fun start(user: User, bot: TelegramBot) {
    // ...
}
```

#### Guard

Bạn có thể định nghĩa guard riêng để kiểm soát quyền truy cập vào các handler, hỗ trợ `@CommandHandler`, `@CommandHandler.CallbackQuery`, `@InputHandler` :

```kotlin
@CommandHandler(["text"])
@Guard(isAdminGuard::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### ArgParser

Bạn có thể định nghĩa parser đối số tùy chỉnh để thay đổi cách phân tích tham số cho các handler, hỗ trợ `@CommandHandler`, `@CommandHandler.CallbackQuery`, `@CommonHandler`:

```kotlin
@CommandHandler(["text"])
@ArgParser(SpaceArgParser::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

**see also [`defaultArgParser`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.common/default-arg-parser.html)**

### Functional DSL

Mỗi annotation ở trên đều có một đối tác trong **Functional DSL**, một cách thay thế để khai báo các handler tại thời gian chạy qua `bot.setFunctionality { … }`. Cả hai cách đều chia sẻ cùng một `ActivityRegistry` và có thể được kết hợp tự do trong cùng một bot.

| Annotation | DSL counterpart |
|------------|-----------------|
| `@CommandHandler` | `onCommand(...)` |
| `@CommandHandler.CallbackQuery` | `onCommand(..., scope = [UpdateType.CALLBACK_QUERY])` |
| `@InputHandler` / input chains | `onInput(...)` / `inputChain(...)` |
| `@CommonHandler` | `common(...)` |
| `@UpdateHandler` | `onUpdate(...)` |
| `@UnprocessedHandler` | `whenNotHandled { ... }` |

Ví dụ tối thiểu:

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

    bot.setFunctionality {
        onChosenInlineResult {
            println("got a result ${update.chosenInlineResult.resultId} from ${update.user}")
        }
    }
}
```

### Commands

```kotlin
bot.setFunctionality {
    // Regular command
    onCommand("/start") {
        message { "Hello" }.send(user, bot)
    }

    // Regex-based command matching
    onCommand("""(red|green|blue)""".toRegex()) {
        message { "you typed ${update.text} color" }.send(user, bot)
    }
}
```

Trong một khối `onCommand`, các tham số đã phân tích sẵn có sẵn dưới dạng `Map<String, String>` được định hình bởi cấu hình `commandParsing` hiện hành.

### Inputs

```kotlin
bot.setFunctionality {
    onCommand("/start") {
        message { "Hello, what's your name?" }.send(user, bot)
        bot.inputListener[user] = "testInput"
    }

    onInput("testInput") {
        message { "Hey, nice to meet you, ${update.text}" }.send(user, bot)
    }
}
```

Xem [`bot.inputListener`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot/-telegram-bot/input-listener.html) để biết API lưu trữ.

#### Input chains

Đối với luồng nhập đa bước, sử dụng `inputChain`:

```kotlin
bot.setFunctionality {
    inputChain("conversation") {
        message { "Nice to meet you, ${update.text}" }.send(user, bot)
        message { "What is your favorite food?" }.send(user, bot)
    }.breakIf({ update.text == "peanut butter" }) {     // chain break condition
        message { "Oh, too bad, I'm allergic to it." }.send(user, bot)
    }.andThen {
        // next step when the break condition didn't match
        message { "Great choice!" }.send(user, bot)
    }
}
```

Chuỗi sẽ tự động chuyển sang bước tiếp theo trừ khi một điều kiện break khớp; khi `repeat = true` (mặc định), một break khớp sẽ giữ người dùng ở bước hiện tại.

> Đối với các luồng đa bước phong phú hơn với trạng thái đã gõ và xác thực, nên ưu tiên sử dụng [`@WizardHandler`](FSM-and-Conversation-handling.md) thay vì.

### Update type handlers

```kotlin
bot.setFunctionality {
    onUpdate(UpdateType.MESSAGE, UpdateType.CALLBACK_QUERY) {
        println("Received update: ${update.type}")
    }
}
```

### Common matchers

```kotlin
bot.setFunctionality {
    common("hello") {
        message { "Hi there!" }.send(user, bot)
    }

    common("""\d+""".toRegex()) {
        message { "You sent a number!" }.send(user, bot)
    }
}
```

### Fallback handler

```kotlin
bot.setFunctionality {
    whenNotHandled {
        message { "I didn't understand that." }.send(user, bot)
    }
}
```

### Companion options

Giới hạn tốc độ, guard và parser đối số được truyền trực tiếp như các tham số tên thay vì các annotation riêng:

```kotlin
bot.setFunctionality {
    onCommand("/expensive", rateLimits = RateLimits(rate = 5, period = 60_000)) {
        message { "Processing..." }.send(user, bot)
    }

    onCommand("/admin", guard = AdminGuard::class) {
        message { "Admin command executed" }.send(user, bot)
    }

    onCommand("/custom", argParser = CustomArgParser::class) {
        message { "Parameters: $parameters" }.send(user, bot)
    }
}
```

### Combining DSL and annotations

Hai phong cách này cùng tồn tại — đăng ký cùng cách, phân phối cùng cách:

```kotlin
@CommandHandler(["/register"])
suspend fun register(user: User, bot: TelegramBot) {
    message { "Registration started" }.send(user, bot)
}

bot.setFunctionality {
    onCommand("/help") {
        message { "Available commands: /register, /help" }.send(user, bot)
    }
}
```

### Conclusion

Những annotation này cung cấp các công cụ mạnh mẽ và linh hoạt để xử lý lệnh, đầu vào và sự kiện, đồng thời cho phép cấu hình riêng biệt cho giới hạn tốc độ và guard, nâng cao cấu trúc và khả năng bảo trì chung của việc phát triển bot.

### See also

* [Activities & Processors](Activites-and-Processors.md)
* [Activity invocation](Activity-invocation.md)
* [FSM and Conversation handling](FSM-and-Conversation-handling.md)
* [Sessions](Sessions.md)
* [Update parsing](Update-parsing.md)

---