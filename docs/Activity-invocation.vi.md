---
---
title: Activity Invocation
---

Trong quá trình gọi hoạt động, có thể truyền ngữ cảnh bot, vì nó được khai báo là tham số trong các hàm đích.

Các tham số có thể truyền là:

* [`ProcessedUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processed-update/index.html) (và tất cả lớp con của nó) - cập nhật đang xử lý hiện tại.
* [`ProcessingContext`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processing-context/index.html) - ngữ cảnh cấp thấp của việc xử lý hoạt động.
* [`User`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types/-user/index.html) - nếu có.
* [`Chat`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.chat/-chat/index.html) - nếu có.
* [`TelegramBot`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot/-telegram-bot/index.html) - thể hiện bot hiện tại.

Cũng có thể thêm một kiểu tùy chỉnh để truyền.

Để làm điều này, thêm một lớp implements [`Autowiring<T>`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.marker/-autowiring/index.html) và đánh dấu nó với annotation [`@Injectable`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-injectable/index.html).

Sau khi implements interface `Autowiring` - `T` sẽ có sẵn để truyền trong các hàm đích và sẽ được lấy thông qua phương thức được mô tả trong interface.

```kotlin
@Injectable
object UserResolver : Autowiring<UserRecord> {
    override suspend fun get(update: ProcessedUpdate, bot: TelegramBot): UserRecord? {
        return userRepository.getUserByTgId(update.user.id)
    }
}
```

Các tham số khác được khai báo trong hàm sẽ được **tìm kiếm** trong các tham số đã được parse.

Ngoài ra, các tham số đã được parse trong quá trình truyền có thể được ép kiểu thành một số kiểu nhất định, đây là danh sách của chúng:

- `String`
- `Integer`
- `Long`
- `Short`
- `Float`
- `Double`

Hơn nữa, lưu ý rằng nếu các tham số được khai báo và bị thiếu (hoặc trong các tham số đã được parse hoặc ví dụ `User` bị thiếu trong `Update`) hoặc kiểu được khai báo không phù hợp với tham số nhận được trong hàm, **`null`** sẽ được truyền nên hãy cẩn thận.

Tóm tắt tất cả, dưới đây là một ví dụ về cách các tham số hàm thường được hình thành:

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/3c1d7830-8e5d-45fb-82bb-ac63f08c3782" alt="Invokation process diagram" />
</p>

### Xem thêm

* [Update parsing](Update-parsing.md)
* [Activities & Processors](Activites-and-Processors.md)
---