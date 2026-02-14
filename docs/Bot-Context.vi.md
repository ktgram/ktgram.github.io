---
---
title: Ngữ cảnh Bot
---

<p align="center">
  <img src="https://github.com/user-attachments/assets/60bb58ae-1806-4b8d-8550-833b09c2b606" alt="Bot context diagram" />
</p>

Bot cũng có thể cung cấp khả năng ghi nhớ một số dữ liệu thông qua các giao diện `UserData` và `ClassData`.

- [`userData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-user-data/index.html) là dữ liệu ở cấp độ người dùng.
- [`classData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-data/index.html) là dữ liệu ở cấp độ lớp, tức là dữ liệu sẽ được lưu trữ cho đến khi người dùng chuyển sang lệnh hoặc đầu vào nằm trong
  một lớp khác. (Ở chế độ hàm nó sẽ hoạt động giống như dữ liệu người dùng)

Mặc định, việc triển khai được cung cấp thông qua [`ConcurrentHashMap`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.collections/java.util.concurrent.-concurrent-map/) nhưng có thể thay đổi thành của riêng bạn thông qua các giao diện [`UserData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-user-data/index.html) và [`ClassData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-data/index.html) sử dụng
các công cụ lưu trữ dữ liệu bạn chọn.


> [!CAUTION]
> Đừng quên chạy gradle `kspKotlin`/hoặc bất kỳ tác vụ ksp liên quan nào để làm cho các ràng buộc sinh mã cần thiết có sẵn.


Để thay đổi, tất cả những gì bạn cần làm là đặt annotation `@CtxProvider` dưới lớp triển khai của bạn và chạy tác vụ gradle ksp (hoặc build).

```kotlin
@CtxProvider
class MyRedis : UserData<String> {
    // ...
}
```

### Xem thêm

* [Trang chủ](https://github.com/vendelieu/telegram-bot/wiki)
* [Cập nhật phân tích](Update-parsing.md)
---