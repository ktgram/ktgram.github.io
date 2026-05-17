---
---
title: Interceptors (Middleware)
---

### Interceptors: Cross-Cutting Logic for Your Bot

Khi xây dựng bot Telegram, bạn thường phải lặp lại việc thiết lập, kiểm tra hoặc dọn dẹp trên các handler. Interceptors cho phép bạn chèn logic chia sẻ quanh các handler, giúp các handler tập trung và dễ bảo trì hơn.

Dưới đây là cách interceptors hoạt động trong *telegram-bot* và cách sử dụng chúng.

### What Are Interceptors? (Simple Explanation)

Interceptors là các hàm chạy tại các điểm cụ thể trong pipeline xử lý update. Chúng cho phép bạn:
- Kiểm tra và sửa đổi ngữ cảnh xử lý
- Thêm logic xuyên suốt (logging, auth, metrics)
- Dừng xử lý sớm nếu cần
- Dọn dẹp tài nguyên sau khi xử lý

Hãy nghĩ interceptors như các checkpoint mà mọi update phải đi qua trước, trong và sau khi thực thi handler.


### The Processing Pipeline

Bot xử lý các update thông qua một pipeline với bảy giai đoạn:

| Phase | When It Runs | What You Can Use It For |
|-------|--------------|-------------------------|
| **Setup** | Ngay khi update đến, trước bất kỳ xử lý nào | ✔ Giới hạn tốc độ toàn cục<br>✔ Lọc spam hoặc update dạng sai<br>✔ Ghi nhật ký ban đầu<br>✔ Thiết lập ngữ cảnh chung |
| **Parsing** | Sau setup, trích xuất lệnh và tham số | ✔ Phân tích lệnh tùy chỉnh<br>✔ Bổ sung ngữ cảnh với dữ liệu đã phân tích<br>✔ Xác thực cấu trúc update |
| **Match** | Tìm handler phù hợp (Command/Input/Common) | ✔ Ghi đè lựa chọn handler<br>✔ Logic xử lý input tùy chỉnh<br>✔ Ghi nhật ký các handler đã khớp |
| **Validation** | Sau khi tìm được handler, trước khi gọi | ✔ Quyền hạn riêng của handler<br>✔ Giới hạn tốc độ per handler<br>✔ Kiểm tra guard<br>✔ Hủy xử lý nếu điều kiện không thỏa |
| **PreInvoke** | Ngay trước khi handler chạy | ✔ Kiểm tra lần cuối<br>✔ Bắt đầu timer/metrics<br>✔ Bổ sung ngữ cảnh cho handler<br>✔ Thay đổi hành vi handler |
| **Invoke** | Handler được thực thi ở đây | ✔ Bọc thực thi handler<br>✔ Xử lý lỗi<br>✔ Ghi nhật ký kết quả handler |
| **PostInvoke** | Sau khi handler hoàn thành (thành công hay thất bại) | ✔ Dọn dẹp tài nguyên<br>✔ Ghi nhật ký kết quả<br>✔ Gửi tin nhắn fallback khi có lỗi<br>✔ Thay đổi kết quả trước khi trả về |


### Creating an Interceptor

Một interceptor là một hàm đơn giản nhận vào `ProcessingContext`:

```kotlin
import eu.vendeli.tgbot.core.PipelineInterceptor
import eu.vendeli.tgbot.types.component.ProcessingContext

val myInterceptor: PipelineInterceptor = { context ->
    // Your logic here
    println("Processing update: ${context.update.updateId}")
}
```

Hoặc sử dụng lambda:

```kotlin
val loggingInterceptor = PipelineInterceptor { context ->
    val logger = context.bot.config.loggerFactory.get("MyInterceptor")
    logger.info("Processing update #${context.update.updateId}")
}
```


### Registering Interceptors

Đăng ký interceptor trên pipeline xử lý:

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")
    
    // Register an interceptor for the Setup phase
    bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
        // Check if user is banned
        val user = context.update.userOrNull
        if (user != null && isBanned(user.id)) {
            context.finish() // Stop processing
            return@intercept
        }
    }
    
    // Register an interceptor for the PreInvoke phase
    bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
        val startTime = System.currentTimeMillis()
        // store start time
    }
    
    // Register an interceptor for the PostInvoke phase
    bot.update.pipeline.intercept(ProcessingPipePhase.PostInvoke) { context ->
        val startTime = // get start time
        if (startTime != null) {
            val duration = System.currentTimeMillis() - startTime
            println("Handler took ${duration}ms")
        }
    }
    
    bot.handleUpdates()
}
```

### Real-World Example: Authentication & Metrics

Ví dụ: một bot yêu cầu xác thực cho một số lệnh, đo thời gian thực thi handler và ghi nhật ký tất cả các lệnh.

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")
    
    // Setup phase: Check if user is authenticated
    bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
        val user = context.update.userOrNull ?: return@intercept
        
        if (!isAuthenticated(user.id)) {
            message { "Please authenticate first using /login" }
                .send(user, context.bot)
            context.finish()
        }
    }
    
    // PreInvoke phase: Start timer and check permissions
    bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
        val activity = context.activity ?: return@intercept
        val user = context.update.userOrNull ?: return@intercept
        
        // Check if user has permission for this specific handler
        if (!hasPermission(user.id, activity)) {
            message { "You don't have permission to use this command." }
                .send(user, context.bot)
            context.finish()
            return@intercept
        }
        
        // Start timer
        // store start time
    }
    
    // PostInvoke phase: Log and cleanup
    bot.update.pipeline.intercept(ProcessingPipePhase.PostInvoke) { context ->
        val activity = context.activity ?: return@intercept
        val startTime = // get start time
        
        if (startTime != null) {
            val duration = System.currentTimeMillis() - startTime
            val logger = context.bot.config.loggerFactory.get("Metrics")
            logger.info(
                "Handler ${activity::class.simpleName} took ${duration}ms " +
                "for user ${context.update.userOrNull?.id}"
            )
        }
    }
    
    bot.handleUpdates()
}
```


### ProcessingContext

`ProcessingContext` cung cấp truy cập tới:

- **`update: ProcessedUpdate`** - Update hiện tại đang được xử lý
- **`bot: TelegramBot`** - Instance bot
- **`registry: ActivityRegistry`** - Registry activity
- **`parsedInput: String`** - Văn bản lệnh/input đã phân tích
- **`parameters: Map<String, String>`** - Tham số lệnh đã phân tích
- **`activity: Activity?`** - Handler đã giải quyết (null tới giai đoạn Match)
- **`shouldProceed: Boolean`** - Có nên tiếp tục xử lý hay không
- **`additionalContext: AdditionalContext`** - Dữ liệu ngữ cảnh bổ sung
- **`finish()`** - Dừng xử lý sớm

#### Stopping Processing Early

Gọi `context.finish()` để dừng xử lý:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.Validation) { context ->
    if (someCondition) {
        context.finish() // No further phases will execute
    }
}
```

#### Storing Custom Data

Sử dụng `additionalContext` để truyền dữ liệu giữa các interceptor:

```kotlin
// In PreInvoke
context.additionalContext["userId"] = context.update.userOrNull?.id

// In PostInvoke
val userId = context.additionalContext["userId"] as? Long
```


### Multiple Interceptors

Bạn có thể đăng ký nhiều interceptor cho cùng một phase. Chúng sẽ chạy theo thứ tự đăng ký:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    println("First interceptor")
}

bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    println("Second interceptor")
}

// When an update is processed:
// Output: "First interceptor"
// Output: "Second interceptor"
```

Nếu một interceptor gọi `context.finish()`, các interceptor còn lại trong phase đó sẽ bị bỏ qua, và các phase sau sẽ không được thực thi.


### Best Practices

#### 1. Use the Right Phase

- Setup: Kiểm tra toàn cục, lọc, thiết lập ban đầu
- Parsing: Logic phân tích tùy chỉnh
- Match: Logic lựa chọn handler
- Validation: Quyền hạn, giới hạn tốc độ, guard
- PreInvoke: Chuẩn bị riêng cho handler
- Invoke: Thường được xử lý bởi interceptor mặc định
- PostInvoke: Dọn dẹp, ghi nhật ký, xử lý lỗi

#### 2. Keep Interceptors Focused

Mỗi interceptor nên làm một việc:

```kotlin
// ✅ Good - focused interceptor
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    if (isBanned(context.update.userOrNull?.id)) {
        context.finish()
    }
}

// ❌ Avoid - doing too much
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    // Authentication
    // Logging
    // Metrics
    // Rate limiting
    // ... too much!
}
```

#### 3. Handle Errors Gracefully

Interceptor không nên làm bot bị crash:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
    try {
        // Your logic
    } catch (e: Exception) {
        val logger = context.bot.config.loggerFactory.get("Interceptor")
        logger.error("Interceptor error", e)
        // Don't call context.finish() unless you want to stop processing
    }
}
```

#### 4. Clean Up Resources

Nếu bạn mở tài nguyên trong `PreInvoke`, hãy dọn dẹp trong `PostInvoke`:

```kotlin
var timer: Timer? = null

bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
    timer = Timer()
    context.additionalContext["timer"] = timer
}

bot.update.pipeline.intercept(ProcessingPipePhase.PostInvoke) { context ->
    val timer = context.additionalContext["timer"] as? Timer
    timer?.stop()
}
```

#### 5. Order Matters

Đăng ký interceptor theo thứ tự bạn muốn chúng chạy:

```kotlin
// More general checks first
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { 
    // Global ban check
}

// More specific checks later
bot.update.pipeline.intercept(ProcessingPipePhase.Validation) { 
    // Handler-specific permission check
}
```

#### 6. Use Interceptors for Cross-Cutting Concerns

Interceptor là lựa chọn tuyệt vời cho:
- ✅ Xác thực/ủy quyền
- ✅ Ghi nhật ký
- ✅ Metrics/giám sát hiệu năng
- ✅ Giới hạn tốc độ
- ✅ Xử lý lỗi
- ✅ Biến đổi yêu cầu/đáp trả

Đối với logic riêng của handler, hãy để trong handler.

### Default Interceptors

Framework cung cấp các interceptor mặc định cho chức năng cốt lõi:

- **DefaultSetupInterceptor**: Giới hạn tốc độ toàn cục
- **DefaultParsingInterceptor**: Phân tích lệnh
- **DefaultMatchInterceptor**: Khớp handler (commands, inputs, common matchers)
- **DefaultValidationInterceptor**: Kiểm tra guard và giới hạn tốc độ per handler
- **DefaultInvokeInterceptor**: Thực thi handler và xử lý lỗi

Các interceptor tùy chỉnh của bạn chạy song song với các interceptor mặc định này. Bạn có thể thêm logic trước hoặc sau các interceptor mặc định, nhưng không thể xóa chúng.

---

### Advanced: Conditional Interceptors

Bạn có thể làm cho interceptor có điều kiện:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
    val activity = context.activity ?: return@intercept
    
    // Only apply to specific handlers
    if (activity::class.simpleName?.contains("Admin") == true) {
        // Admin-specific logic
        checkAdminPermissions(context)
    }
}
```


### Summary

Interceptors cung cấp cách sạch sẽ để thêm logic xuyên suốt vào bot của bạn:

- ✅ **Bảy phase** cho các bước xử lý khác nhau
- ✅ **API đơn giản**: Chỉ cần triển khai `PipelineInterceptor`
- ✅ **Linh hoạt**: Đăng ký nhiều interceptor cho mỗi phase
- ✅ **Mạnh mẽ**: Truy cập đầy đủ ngữ cảnh xử lý
- ✅ **An toàn**: Có thể dừng xử lý sớm bằng `context.finish()`

Hãy dùng interceptor để giữ cho các handler của bạn tập trung vào logic nghiệp vụ, trong khi các mối quan tâm chung như xác thực, ghi nhật ký và metrics được xử lý tập trung.

---

### See also

* [Handlers (incl. Functional DSL)](Handlers.md) - Annotation- và DSL-based handler definition
* [Sessions](Sessions.md) - Per-chat / per-user state &amp; message tracking
* [Guards](Guards.md) - Handler-level permission checks
---