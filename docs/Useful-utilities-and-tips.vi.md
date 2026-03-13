---
---
title: Tiện ích và Mẹo hữu ích
---


### Vận hành với ProcessedUpdate

[`ProcessedUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processed-update/index.html) là một lớp generic cho các bản cập nhật, tùy thuộc vào dữ liệu gốc, có thể được cung cấp ở các kiểu khác nhau ([`MessageUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-message-update/index.html), [`CallbackQueryUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-callback-query-update/index.html), v.v.)

Vì vậy bạn có thể kiểm tra kiểu dữ liệu đến và tiếp tục thao tác với dữ liệu cụ thể bằng smartcasts, ví dụ:

```kotlin
// ...
if (update !is MessageUpdate) {
    message { "Only messages are allowed" }.send(user, bot)
    return
}
// Tiếp theo, ProcessedUpdate sẽ được hiểu là MessageUpdate.
```

Cũng có một interface [`UserReference`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-user-reference/index.html) bên trong cho phép bạn xác định xem có tham chiếu người dùng bên trong không, ví dụ sử dụng:

```kotlin
val user = if(update is UserReference) update.user else null

```

Nếu cần bên trong luôn có bản gốc [`update`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types/-update/index.html) trong tham số update.


### Tiêm phụ thuộc

Thư viện sử dụng cơ chế đơn giản để khởi tạo các lớp nơi các phương thức xử lý bản cập nhật của bạn được chú thích với các chú thích được cung cấp.

[`ClassManagerImpl`](https://github.com/vendelieu/telegram-bot/blob/master/telegram-bot/src/commonMain/kotlin/eu/vendeli/tgbot/implementations/ClassManagerImpl.kt) được sử dụng mặc định để gọi các phương thức được chú thích.

Nhưng nếu bạn muốn sử dụng một số thư viện khác cho việc đó bạn có thể định nghĩa lại interface [`ClassManager`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-manager/index.html), <br/>sử dụng cơ chế ưa thích của bạn và truyền vào khi khởi tạo bot.

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.controllers") {
        classManager = ClassManagerImpl()
    }

    bot.handleUpdates()
}
```

### Lọc bản cập nhật

Nếu không có điều kiện phức tạp bạn có thể đơn giản lọc một số bản cập nhật để xử lý:

```kotlin
// hàm nơi định nghĩa điều kiện lọc bản cập nhật
fun filteringFun(update: Update): Boolean = update.message?.text.isNullOrBlank()

fun main() = runBlocking {
  val bot = TelegramBot("BOT_TOKEN")

  // thiết lập luồng xử lý cụ thể hơn cho bản cập nhật
  bot.update.setListener {
    if(filteringFun(it)) return@setListener

    // vậy đơn giản, nếu listener rời khỏi phạm vi trước khi đạt tới hàm handler, đó là đang lọc.
    // thực ra bạn thậm chí có thể viết trực tiếp if-condition ở đó với return@setListener hoặc mở rộng lọc ra lớp riêng.

    handle(it) // hoặc cách xử lý thủ công với block
  }
}
```

để bao gồm lọc trong quá trình so khớp hoặc loại trừ lệnh của bạn hãy xem guards hoặc `@CommonHandler`.

### Tổng quát hóa tùy chọn cho các phương thức khác nhau

Nếu bạn phải áp dụng thường xuyên các tham số tùy chọn giống nhau, bạn có thể viết một hàm tương tự phù hợp với bạn và giảm bớt code boilerplate :)

Một số thuộc tính chung được tách ra thành [các interface khác nhau](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.options/-options/index.html).

```kotlin
@Suppress("NOTHING_TO_INLINE")
inline fun <T, R, O> T.markdownMode(crossinline block: O.() -> Unit = {}): T
        where               T : TgAction<R>,
                            T : OptionsFeature<T, O>,
                            O : Options,
                            O : OptionsParseMode =
    options {
        parseMode = ParseMode.Markdown
        block()
    }


// ... và trong code của bạn

message { "test" }.markdownMode().send(to, via)

```