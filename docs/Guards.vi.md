---
---
title: Guards
---

### Giới thiệu
Guards là một tính năng thiết yếu cho các nhà phát triển tạo bot. Những guards này hoạt động như các kiểm tra trước khi thực thi để xác định xem một lệnh cụ thể có nên được gọi hay không. Bằng cách triển khai các kiểm tra này, các nhà phát triển có thể nâng cao chức năng, bảo mật và trải nghiệm người dùng của bot.

### Mục đích của Activity Guards
Mục đích chính của activity guards là đảm bảo chỉ những người dùng được ủy quyền hoặc điều kiện cụ thể mới có thể kích hoạt một activity.

Điều này có thể ngăn chặn lạm dụng, duy trì tính toàn vẹn của bot và tối ưu hóa tương tác.

### Các trường hợp sử dụng phổ biến
1. Xác thực và Ủy quyền: Đảm bảo chỉ một số người dùng nhất định có thể truy cập các lệnh cụ thể.
2. Kiểm tra điều kiện tiên quyết: Xác minh rằng một số điều kiện được đáp ứng trước khi thực thi một activity (ví dụ: đảm bảo người dùng ở trong trạng thái hoặc ngữ cảnh cụ thể).
3. Guards ngữ cảnh: Đưa ra quyết định dựa trên trạng thái chat hoặc người dùng hiện tại.

### Chiến lược triển khai
Việc triển khai Telegram Command Guards thường liên quan đến việc viết các hàm hoặc phương thức đóng gói logic cho mỗi guard. Dưới đây là các chiến lược phổ biến:

1. Kiểm tra vai trò người dùng:
   - Đảm bảo người dùng có vai trò yêu cầu (ví dụ: admin, moderator) trước khi thực thi lệnh.
      ```kotlin
       override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // Check if the user is an admin in the given chat
       }
      ```

2. Xác minh trạng thái:
   - Kiểm tra trạng thái của người dùng trước khi cho phép thực thi lệnh.
     ```kotlin
     override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        return bot.userData[user.id, "data"] == requiredState
     }
     ```

3. Guards tùy chỉnh:
   - Tạo logic tùy chỉnh dựa trên yêu cầu cụ thể.
     ```kotlin
     override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // Custom logic to determine if the command should be executed
     }
     ```

### Tích hợp Guards với Activities
Để tích hợp các guards này với các lệnh bot của bạn, bạn có thể tạo một guard kiểm tra các điều kiện này trước khi trình xử lý lệnh được gọi.

### Ví dụ triển khai

```kotlin
// define somewhere your guard class that implements Guard interface
object YourGuard : Guard {
    override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // write your condition here
    }
}

// ...

@CommandHandler(["yourCommand"])
@Guard(YourGuard::class) // InputHandler also is supported
fun command(bot: TelegramBot) {
   // command body
}
```

### Các phương pháp tốt nhất

- Mô-đun hóa: Giữ logic guard mô-đun và tách biệt khỏi activities.
- Tái sử dụng: Viết các hàm guard có thể tái sử dụng và dễ dàng áp dụng cho các lệnh/inputs khác nhau.
- Hiệu quả: Tối ưu hóa các kiểm tra guard để giảm thiểu overhead về hiệu năng.
- Phản hồi người dùng: Cung cấp phản hồi rõ ràng cho người dùng khi một lệnh bị block bởi guard.

### Kết luận

Activity Guards là một công cụ mạnh mẽ để quản lý việc thực thi lệnh/input của bot.

Bằng cách triển khai các cơ chế guard mạnh mẽ, các nhà phát triển có thể đảm bảo bot của họ hoạt động an toàn và hiệu quả, cung cấp trải nghiệm người dùng tốt hơn.

### Xem thêm

* [Activities and Proccessors](Activites-and-Processors.md)
* [Update parsing](Update-parsing.md)
* [Actions](Actions.md)
* [Activity invocation](Activity-invocation.md)

---