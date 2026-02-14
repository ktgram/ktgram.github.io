---
---
title: Actions
---

### All requests is Actions
Tất cả các yêu cầu API của telegram là các kiểu khác nhau của giao diện [`TgAction`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.action/-tg-action/index.html) triển khai các phương thức khác nhau như [`SendMessageAction`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.api.message/-send-message-action/index.html), <br/>được đóng gói dưới dạng các hàm kiểu [`message()`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.api.message/message.html) để thuận tiện cho giao diện thư viện.

<p align="center">
    <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/2d097d60-1907-4ca1-8ad3-3ee8d223f8eb" alt="Actions diagram" />
</p>

Mỗi `Action` có thể có các phương thức riêng của nó, tùy thuộc vào các [`Feature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-feature/index.html) có sẵn.

### Features

Các actions khác nhau có thể có các [`Features`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-feature/index.html) khác nhau tùy thuộc vào Telegram Bot Api, chẳng hạn như:
[`OptionsFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-options-feature/index.html),
[`MarkupFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-markup-feature/index.html)
[`EntitiesFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-entities-feature/index.html)
[`CaptionFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-caption-feature/index.html).

Hãy xem kỹ hơn về chúng:

### Options
Ví dụ, [`OptionsFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-options-feature/index.html) được sử dụng để truyền các tham số tùy chọn.

Mỗi action có loại options riêng của nó, bạn có thể thấy tương ứng trong chính `Action` trong tham số `options`, trong phần properties. <br/>Ví dụ, `sendMessage` chứa một dữ liệu [`MessageOptions`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.options/-message-options/index.html) với các tham số khác nhau như options.

Ví dụ sử dụng:

```kotlin
message{ "*Test*" }.options {
    parseMode = ParseMode.Markdown
}.send(user, bot)
```
### Markup

Cũng có một phương thức để gửi markups hỗ trợ tất cả các loại [keyboards](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.marker/-keyboard/index.html): <br/>[`ReplyKeyboardMarkup`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-reply-keyboard-markup/index.html), [`InlineKeyboardMarkup`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-inline-keyboard-markup/index.html), [`ForceReply`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-force-reply/index.html), [`ReplyKeyboardRemove`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-reply-keyboard-remove/index.html).

#### Inline Keyboard Markup

Trình xây dựng này cho phép bạn xây dựng các nút inline với bất kỳ kết hợp tham số nào.

```kotlin
message{ "Test" }.inlineKeyboardMarkup {
    "name" callback "callbackData"         //
    "buttonName" url "https://google.com"  //--- hai nút này sẽ ở cùng một hàng.
    newLine() // or br()
    "otherButton" webAppInfo "data"       // điều này sẽ ở hàng khác

    // bạn cũng có thể sử dụng phong cách khác trong trình xây dựng:
    callbackData("buttonName") { "callbackData" }
}.send(user, bot)

```

Chi tiết hơn có thể được xem trong tài liệu trình xây dựng [documentation](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.builders/-inline-keyboard-markup-builder/index.html).

#### Reply Keyboard Markup

Trình xây dựng này cho phép bạn xây dựng các nút menu.

```kotlin
message{ "Test" }.replyKeyboardMarkup {
  + "Menu button"     // bạn có thể thêm nút bằng cách sử dụng toán tử cộng một ngôi
  + "Menu button 2"
  br() // chuyển sang hàng thứ hai
  "Send polls 👀" requestPoll true   // nút có tham số

  options {
    resizeKeyboard = true
  }
}.send(user, bot)
```

Các tùy chọn bổ sung áp dụng cho bàn phím có thể được xem trong [`ReplyKeyboardMarkupOptions`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.options/-reply-keyboard-markup-options/index.html).

Xem tài liệu trình xây dựng [documentation](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.builders/-reply-keyboard-markup-builder/index.html) để biết thêm chi tiết về các phương thức.

Nhìn chung, sử dụng DSL để thu thập bàn phím markup rất tiện lợi, nhưng nếu cần, bạn cũng có thể thêm markup theo cách thủ công.

```kotlin
message{ "*Test*" }.markup {
    InlineKeyboardMarkup(
        InlineKeyboardButton("test", callbackData = "testCallback")
    )
}.send(user, bot)

```

```kotlin
message{ "*Test*" }.markup {
    ReplyKeyboardMarkup(
        KeyboardButton("Test menu button")
    )
}.send(user, bot)
```

### Entities
Cũng có một phương thức để gửi [`MessageEntity`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.msg/-message-entity/index.html).

Ví dụ sử dụng:

```kotlin
message{ "Test \$hello" }.replyKeyboardMarkup {
    +"Test menu button"
}.entities {
    5 to 15 url "https://google.com" // thêm TextLink
    entity(EntityType.Bold, 0, 4)
    entity(EntityType.Cashtag, 5, 5) // dấu gạch chéo ngược không được tính (vì nó được sử dụng cho trình biên dịch)
}.send(user, bot)
```

#### Contextual entities.

Các entities cũng có thể được thêm thông qua ngữ cảnh của một số cấu trúc, chúng được gắn nhãn với một giao diện [EntitiesContextBuilder](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.builders/-entities-ctx-builder/index.html) cụ thể, nó cũng có mặt trong feature caption.

Ví dụ sử dụng:

```kotlin
message { "usual text " - bold { "this is bold text" } - " continue usual" }.send(user, bot)
```

Tất cả các loại [entity types](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.msg/-entity-type/index.html) đều được hỗ trợ.

### Caption
Ngoài ra, phương thức `caption` có thể được sử dụng để thêm chú thích cho các tệp media.

Ví dụ sử dụng:

```kotlin
photo { "FILE_ID" }.caption { "Test caption" }.send(user, bot)
```


### See also

* [Bot context](Bot-Context.md)
* [FSM | Conversation handling](FSM-and-Conversation-handling.md)