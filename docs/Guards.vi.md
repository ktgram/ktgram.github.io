---
---
title: Guards
---

### Introduction
Guards là một tính năng thiết yếu cho các nhà phát triển tạo bot. Các guard này hoạt động như các kiểm tra trước khi thực thi để xác định liệu một lệnh cụ thể có nên được gọi hay không. Bằng cách triển khai các kiểm tra này, các nhà phát triển có thể nâng cao chức năng, bảo mật và trải nghiệm người dùng của bot.

### Purpose of Activity Guards
Mục đích chính của activity guards là đảm bảo chỉ có người dùng được ủy quyền hoặc các điều kiện cụ thể mới kích hoạt một activity.

Điều này có thể ngăn ngừa việc lạm dụng, duy trì tính toàn vẹn của bot và tối ưu hoá các tương tác.

### Common Use Cases
1. Authentication and Authorization: Đảm bảo chỉ một số người dùng nhất định có thể truy cập các lệnh cụ thể.  
2. Pre-condition Checks: Xác nhận rằng các điều kiện nhất định đã được đáp ứng trước khi thực thi một activity (ví dụ: đảm bảo người dùng đang ở trong một trạng thái hoặc ngữ cảnh cụ thể).  
3. Contextual Guards: Đưa ra quyết định dựa trên trạng thái chat hoặc người dùng hiện tại.

### Implementation Strategies
Triển khai Telegram Command Guards thường bao gồm việc viết các hàm hoặc phương thức bao gói logic cho từng guard. Dưới đây là các chiến lược thường dùng:

1. User Role Check:
   - Đảm bảo người dùng có vai trò yêu cầu (ví dụ: admin, moderator) trước khi thực thi lệnh.
      ```kotlin
       override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // Check if the user is an admin in the given chat
       }
      ```
   
2. State Verification:
   - Kiểm tra trạng thái của người dùng trước khi cho phép thực thi lệnh.
     ```kotlin
     override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        return bot.userData[user.id, "data"] == requiredState
     }
     ```
   
3. Custom Guards:
   - Tạo logic tùy chỉnh dựa trên các yêu cầu cụ thể.
     ```kotlin
     override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // Custom logic to determine if the command should be executed
     }
     ```
   
### Integrating Guards with Activities
Để tích hợp các guard này với các lệnh bot của bạn, bạn có thể tạo một guard kiểm tra các điều kiện trước khi trình xử lý lệnh được gọi.

### Implementing Example

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

### Best Practices

- Modularity: Giữ logic guard dạng mô-đun và tách rời khỏi activities.  
- Reusability: Viết các hàm guard có thể tái sử dụng dễ dàng cho nhiều lệnh/input khác nhau.  
- Efficiency: Tối ưu hóa các kiểm tra guard để giảm thiểu chi phí hiệu năng.  
- User Feedback: Cung cấp phản hồi rõ ràng cho người dùng khi một lệnh bị chặn bởi guard.

### Conclusion

Activity Guards là một công cụ mạnh mẽ để quản lý việc thực thi lệnh/input của bot.

Bằng cách triển khai các cơ chế guard vững chắc, các nhà phát triển có thể đảm bảo bot của họ hoạt động an toàn và hiệu quả, mang lại trải nghiệm người dùng tốt hơn.

### See also

* [Activities and Proccessors](Activites-and-Processors.md)
* [Update parsing](Update-parsing.md)
* [Actions](Actions.md)
* [Activity invocation](Activity-invocation.md)

---