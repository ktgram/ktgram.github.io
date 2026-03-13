---
---
title: Cập nhật phân tích
---

### Tải trọng văn bản

Một số cập nhật có thể có tải trọng văn bản có thể được phân tích để xử lý tiếp theo. Hãy xem xét chúng:

* `MessageUpdate` -> `message.text`
* `EditedMessageUpdate` -> `editedMessage.text`
* `ChannelPostUpdate` -> `channelPost.text`
* `EditedChannelPostUpdate` -> `editedChannelPost.text`
* `InlineQueryUpdate` -> `inlineQuery.query`
* `ChosenInlineResultUpdate` -> `chosenInlineResult.query`
* `CallbackQueryUpdate` -> `callbackQuery.data`
* `ShippingQueryUpdate` -> `shippingQuery.invoicePayload`
* `PreCheckoutQueryUpdate` -> `preCheckoutQuery.invoicePayload`
* `PollUpdate` -> `poll.question`
* `PurchasedPaidMediaUpdate` -> `purchasedPaidMedia.paidMediaPayload`

Từ các cập nhật được liệt kê, một tham số nhất định được chọn và lấy làm [`TextReference`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-text-reference/index.html) để phân tích tiếp theo.

### Phân tích

Các tham số được chọn được phân tích với các phân cách được cấu hình phù hợp thành lệnh và các tham số cho nó.

Xem khối cấu hình [`commandParsing`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.configuration/-bot-configuration/command-parsing.html).

Bạn có thể thấy trong sơ đồ bên dưới các thành phần nào được ánh xạ vào phần nào của hàm mục tiêu.

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/7489099a-cca8-4049-a374-efaf6ce52128" alt="Sơ đồ phân tích văn bản" />
</p>

### @ParamMapping

Cũng có một chú thích gọi là [`@ParamMapping`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-param-mapping/index.html) để thuận tiện hoặc cho bất kỳ trường hợp đặc biệt nào.

Nó cho phép bạn ánh xạ tên tham số từ văn bản đến bất kỳ tham số nào.

Điều này cũng thuận tiện khi dữ liệu đến của bạn bị giới hạn, ví dụ `CallbackData` (64 ký tự).

Xem ví dụ sử dụng:
`greeting?name=Adam`

```kotlin
@CommandHandler(["greeting"])
suspend fun greeting(@ParamMapping("name") anyParameterName: String, user: User, bot: TelegramBot) {
    message { "Hello, $anyParameterName" }.send(to = user, via = bot)
}
```

Và nó cũng có thể được sử dụng để bắt các tham số chưa đặt tên, trong các trường hợp nơi bộ phân tích được thiết lập để bỏ qua tên tham số hoặc thậm chí chúng vắng mặt, được truyền theo mẫu 'param_n', trong đó `n` là thứ tự của nó.

Ví dụ văn bản như vậy - `myCommand?p1=v1&v2&p3=&p4=v4&p5=`, sẽ được phân tích thành:
* lệnh - `myCommand`
* tham số
  * `p1` = `v1`
  * `param_2` = `v2`
  * `p3` = ``
  * `p4` = `v4`
  * `p5` = ``

Như bạn có thể thấy, vì tham số thứ hai không có tên được khai báo nên nó được biểu diễn là `param_2`.

Vì vậy bạn có thể viết tắt tên biến trong callback và sử dụng tên rõ ràng, dễ đọc trong code.

### Deeplink

Xét thông tin từ trên, nếu bạn mong đợi deeplink trong lệnh start của mình, bạn có thể bắt nó với:

```kotlin
@CommandHandler(["/start"])
suspend fun start(@ParamMapping("param_1") deeplink: String?, user: User, bot: TelegramBot) {
    message { "deeplink is $deeplink" }.send(to = user, via = bot)
}
```

### Lệnh nhóm

Trong cấu hình `commandParsing` chúng ta có tham số [`useIdentifierInGroupCommands`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.configuration/-command-parsing-configuration/use-identifier-in-group-commands.html) khi nó được bật, chúng ta có thể sử dụng `TelegramBot.identifier` (đừng quên thay đổi nó nếu bạn đang sử dụng tham số được mô tả) trong quá trình khớp lệnh, nó giúp tách các lệnh tương tự giữa nhiều bot, nếu không phần `@MyBot` sẽ chỉ bị bỏ qua.

### Xem thêm

* [Hoạt động gọi](Activity-invocation.md)
* [Hoạt động & Bộ xử lý](Activites-and-Processors.md)
* [Hành động](Actions.md)