---
---
title: Handlers
---


### Variety of Handlers

Trong phát triển bot, đặc biệt là trong các hệ thống liên quan đến tương tác người dùng, việc quản lý và xử lý lệnh và sự kiện một cách hiệu quả là rất quan trọng.

Những annotations này đánh dấu các hàm được thiết kế để xử lý các lệnh, đầu vào, hoặc cập nhật cụ thể và cung cấp metadata như các từ khóa lệnh, phạm vi, và guards.

### Annotations Overview

#### CommandHandler

Annotation `CommandHandler` được sử dụng để đánh dấu các hàm xử lý các lệnh cụ thể. Annotation này bao gồm các thuộc tính định nghĩa các từ khóa và phạm vi của lệnh.

-   **value**: Xác định các từ khóa liên kết với lệnh.
-   **scope**: Xác định ngữ cảnh hoặc phạm vi mà lệnh sẽ được kiểm tra.

```kotlin
@CommandHandler(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommandHandler.CallbackQuery

Một phiên bản chuyên biệt của annotation `CommandHandler` được thiết kế đặc biệt để xử lý callback queries. Nó bao gồm các thuộc tính tương tự như `CommandHandler`, với trọng tâm là các lệnh liên quan đến callback.

_Nó thực sự giống hệt như `@CommandHandler` với phạm vi `UpdateType.CALLBACK_QUERY` đã được preset_.

-   **value**: Xác định các từ khóa liên kết với lệnh.
-   **autoAnswer**: Tự động trả lời `callbackQuery` (gọi `answerCallbackQuery` trước khi xử lý).


```kotlin
@CommandHandler.CallbackQuery(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### CommonHandler

Annotation `CommonHandler` được sử dụng cho các hàm xử lý các lệnh với mức độ ưu tiên thấp hơn so với `CommandHandler` và `InputHandler`. Nó được sử dụng ở cấp độ nguồn và cung cấp cách linh hoạt để định nghĩa các common command handlers.

**Lưu ý, mức độ ưu tiên chỉ hoạt động trong phạm vi `@CommonHandler` (tức là không ảnh hưởng đến các handlers khác).**

##### CommonHandler.Text

Annotation này chỉ định việc so khớp văn bản với các cập nhật. Nó bao gồm các thuộc tính để định nghĩa văn bản so khớp, điều kiện lọc, mức độ ưu tiên, và phạm vi.

-   **value**: Văn bản để so khớp với các cập nhật đến.
-   **filter**: Một class định nghĩa các điều kiện được sử dụng trong quá trình so khớp.
-   **priority**: Mức độ ưu tiên của handler, trong đó 0 là mức độ ưu tiên cao nhất.
-   **scope**: Ngữ cảnh hoặc phạm vi mà việc so khớp văn bản sẽ được kiểm tra.

```kotlin
@CommonHandler.Text(["text"], filter = isNewUserFilter::class, priority = 10)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommonHandler.Regex

Tương tự như `CommonHandler.Text`, annotation này được sử dụng để so khớp các cập nhật dựa trên biểu thức chính quy. Nó bao gồm các thuộc tính để định nghĩa mẫu regex, tùy chọn, điều kiện lọc, mức độ ưu tiên, và phạm vi.

-   **value**: Mẫu regex được sử dụng để so khớp.
-   **options**: Các tùy chọn regex thay đổi hành vi của mẫu regex.
-   **filter**: Một class định nghĩa các điều kiện được sử dụng trong quá trình so khớp.
-   **priority**: Mức độ ưu tiên của handler, trong đó 0 là mức độ ưu tiên cao nhất.
-   **scope**: Ngữ cảnh hoặc phạm vi mà việc so khớp regex sẽ được kiểm tra.

```kotlin
@CommonHandler.Regex("^\d+$", scope = [UpdateType.EDITED_MESSAGE])
suspend fun test(update: EditedMessageUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### InputHandler

Annotation `InputHandler` đánh dấu các hàm xử lý các sự kiện đầu vào cụ thể. Nó được sử dụng cho các hàm xử lý đầu vào tại runtime và bao gồm các thuộc tính để định nghĩa các từ khóa đầu vào và phạm vi.

-   **value**: Xác định các từ khóa liên kết với sự kiện đầu vào.

```kotlin
@InputHandler("text")
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UnprocessedHandler

Annotation `UnprocessedHandler` được sử dụng để đánh dấu các hàm xử lý các cập nhật không được xử lý bởi các handlers khác. Nó đảm bảo rằng bất kỳ cập nhật nào chưa được xử lý đều được quản lý một cách thích hợp, với chỉ một điểm xử lý duy nhất có thể cho loại handler này.

```kotlin
@UnprocessedHandler
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UpdateHandler

Annotation `UpdateHandler` đánh dấu các hàm xử lý các loại cập nhật đến cụ thể. Nó cung cấp cách để phân loại và xử lý các loại cập nhật khác nhau một cách có hệ thống.

-   **type**: Xác định các loại cập nhật mà hàm handler sẽ xử lý.

```kotlin
@UpdateHandler([UpdateType.PRE_CHECKOUT_QUERY])
suspend fun test(update: PreCheckoutQueryUpdate, user: User, bot: TelegramBot) {
    //...
}
```
### Handler Companion Annotations

Cũng có các annotations bổ sung là tùy chọn cho các handlers, bổ sung cho hành vi tùy chọn của các handlers.

Chúng có thể được đặt cả trên các hàm mà handler được áp dụng và trên các class, trong trường hợp sau chúng sẽ được tự động áp dụng cho tất cả các handlers trong class đó, nhưng nếu cần thì có thể có hành vi riêng biệt cho một số hàm.

Tức là việc áp dụng có độ ưu tiên như sau, `Function` > `Class`, trong đó hàm có độ ưu tiên cao hơn.

#### Rate Limiting

Ngoài ra, hãy cũng tiết lộ cơ chế rate limiting được mô tả trong các annotations.

Bạn có thể đặt giới hạn chung cho mỗi người dùng:

```kotlin
// ...
val bot = TelegramBot("BOT_TOKEN") {
    rateLimiter { // giới hạn chung
        limits = RateLimits(period = 10000, rate = 5)
    }
}
```

###### Handler specific

Giới hạn cho một số hành động nhất định có thể được định nghĩa bằng annotation `RateLimits`, được hỗ trợ bởi `@CommandHandler`, `@CommandHandler.CallbackQuery`, `@InputHandler`, `@CommonHandler`.

```kotlin
@CommandHandler(["/start"])
@RateLimits(period = 1000L, rate = 1L)
suspend fun start(user: User, bot: TelegramBot) {
    // ...
}
```

#### Guard

Bạn có thể định nghĩa guards riêng biệt để kiểm soát truy cập vào các handlers, được hỗ trợ bởi `@CommandHandler`, `@CommandHandler.CallbackQuery`, `@InputHandler` :

```kotlin
@CommandHandler(["text"])
@Guard(isAdminGuard::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### ArgParser

Bạn có thể định nghĩa trình phân tích đối số tùy chỉnh riêng biệt để thay đổi hành vi phân tích tham số cho các handlers, được hỗ trợ bởi `@CommandHandler`, `@CommandHandler.CallbackQuery`, `@CommonHandler`:

```kotlin
@CommandHandler(["text"])
@ArgParser(SpaceArgParser::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

**xem thêm [`defaultArgParser`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.common/default-arg-parser.html)**

### Conclusion

Những annotations này cung cấp các công cụ mạnh mẽ và linh hoạt để xử lý các lệnh, đầu vào, và sự kiện, trong khi cho phép cấu hình riêng biệt các giới hạn tốc độ và guards, nâng cao cấu trúc tổng thể và khả năng bảo trì trong phát triển bot.

### See also

* [Activities & Processors](Activites-and-Processors.md)
* [Activity invocation](Activity-invocation.md)
* [FSM and Conversation handling](FSM-and-Conversation-handling.md)
* [Update parsing](Update-parsing.md)