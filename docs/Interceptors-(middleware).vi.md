---
---
title: Interceptors (Middleware)
---

### Interceptors: Logic Cross-Cutting cho Bot của bạn

Khi xây dựng một bot Telegram, bạn thường lặp lại việc thiết lập, kiểm tra, hoặc dọn dẹp trên các handler. Interceptors cho phép bạn chèn logic chia sẻ xung quanh các handler, giữ cho các handler tập trung và dễ bảo trì.

Đây là cách interceptors hoạt động trong *telegram-bot* và cách sử dụng chúng.

### Interceptors là gì? (Giải thích đơn giản)

Interceptors là các hàm chạy tại các điểm cụ thể trong pipeline xử lý cập nhật. Chúng cho phép bạn:
- Kiểm tra và sửa đổi context xử lý
- Thêm logic cross-cutting (logging, auth, metrics)
- Dừng xử lý sớm nếu cần
- Dọn dẹp tài nguyên sau khi xử lý

Hãy nghĩ về interceptors như các checkpoint mà mọi cập nhật đều đi qua trước, trong và sau khi thực thi handler.

### Pipeline Xử lý

Bot xử lý cập nhật thông qua một pipeline với bảy giai đoạn:

| Giai đoạn | Khi nào chạy | Bạn có thể dùng để làm gì |
|-----------|--------------|--------------------------|
| **Setup** | Ngay khi cập nhật đến, trước mọi xử lý | ✔ Giới hạn tốc độ toàn cục<br>✔ Lọc spam hoặc cập nhật bị lỗi<br>✔ Logging ban đầu<br>✔ Thiết lập context chia sẻ |
| **Parsing** | Sau Setup, trích xuất lệnh và tham số | ✔ Custom command parsing<br>✔ Bổ sung context với dữ liệu đã parsed<br>✔ Validate cấu trúc cập nhật |
| **Match** | Tìm handler phù hợp (Command/Input/Common) | ✔ Ghi đè selection handler<br>✔ Custom input handling logic<br>✔ Log matched handlers |
| **Validation** | Sau khi tìm thấy handler, trước khi gọi | ✔ Permissions riêng cho handler<br>✔ Giới hạn tốc độ theo handler<br>✔ Guard checks<br>✔ Cancel processing nếu điều kiện không được đáp ứng |
| **PreInvoke** | Ngay trước khi handler chạy | ✔ Checks phút cuối<br>✔ Start timers/metrics<br>✔ Bổ sung context cho handler<br>✔ Sửa đổi hành vi handler |
| **Invoke** | Handler được thực thi ở đây | ✔ Wrap handler execution<br>✔ Error handling<br>✔ Logging handler results |
| **PostInvoke** | Sau khi handler hoàn thành (thành công hoặc thất bại) | ✔ Dọn dẹp tài nguyên<br>✔ Log results<br>✔ Send fallback messages khi lỗi<br>✔ Sửa đổi kết quả trước khi trả về |

### Tạo một Interceptor

Một interceptor là một hàm đơn giản nhận một `ProcessingContext`:

```kotlin
import eu.vendeli.tgbot.core.PipelineInterceptor
import eu.vendeli.tgbot.types.component.ProcessingContext

val myInterceptor: PipelineInterceptor = { context ->
    // Logic của bạn ở đây
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

### Đăng ký Interceptors

Đăng ký interceptors trên pipeline xử lý:

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

    // Đăng ký interceptor cho giai đoạn Setup
    bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
        // Kiểm tra nếu user bị banned
        val user = context.update.userOrNull
        if (user != null && isBanned(user.id)) {
            context.finish() // Dừng xử lý
            return@intercept
        }
    }

    // Đăng ký interceptor cho giai đoạn PreInvoke
    bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
        val startTime = System.currentTimeMillis()
        // store start time
    }

    // Đăng ký interceptor cho giai đoạn PostInvoke
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

### Ví dụ thực tế: Authentication & Metrics

Ví dụ: một bot yêu cầu authentication cho một số lệnh, đo thời gian thực thi handler, và log tất cả các lệnh.

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

    // Giai đoạn Setup: Kiểm tra nếu user đã được authenticated
    bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
        val user = context.update.userOrNull ?: return@intercept

        if (!isAuthenticated(user.id)) {
            message { "Please authenticate first using /login" }
                .send(user, context.bot)
            context.finish()
        }
    }

    // Giai đoạn PreInvoke: Start timer và check permissions
    bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
        val activity = context.activity ?: return@intercept
        val user = context.update.userOrNull ?: return@intercept

        // Kiểm tra nếu user có permission cho handler cụ thể này
        if (!hasPermission(user.id, activity)) {
            message { "You don't have permission to use this command." }
                .send(user, context.bot)
            context.finish()
            return@intercept
        }

        // Start timer
        // store start time
    }

    // Giai đoạn PostInvoke: Log và cleanup
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

`ProcessingContext` cung cấp truy cập đến:

- **`update: ProcessedUpdate`** - Cập nhật hiện tại đang được xử lý
- **`bot: TelegramBot`** - Bot instance
- **`registry: ActivityRegistry`** - Activity registry
- **`parsedInput: String`** - Command/input text đã parsed
- **`parameters: Map<String, String>`** - Command parameters đã parsed
- **`activity: Activity?`** - Handler đã resolved (null cho đến giai đoạn Match)
- **`shouldProceed: Boolean`** - Liệu xử lý có nên tiếp tục
- **`additionalContext: AdditionalContext`** - Dữ liệu context bổ sung
- **`finish()`** - Dừng xử lý sớm

#### Dừng Xử lý Sớm

Gọi `context.finish()` để dừng xử lý:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.Validation) { context ->
    if (someCondition) {
        context.finish() // Không có giai đoạn tiếp theo nào sẽ thực thi
    }
}
```

#### Lưu trữ Dữ liệu Tùy chỉnh

Sử dụng `additionalContext` để truyền dữ liệu giữa các interceptors:

```kotlin
// Trong PreInvoke
context.additionalContext["userId"] = context.update.userOrNull?.id

// Trong PostInvoke
val userId = context.additionalContext["userId"] as? Long
```

### Multiple Interceptors

Bạn có thể đăng ký multiple interceptors cho cùng một giai đoạn. Chúng thực thi theo thứ tự đăng ký:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    println("First interceptor")
}

bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    println("Second interceptor")
}

// Khi một cập nhật được xử lý:
// Output: "First interceptor"
// Output: "Second interceptor"
```

Nếu một interceptor gọi `context.finish()`, các interceptors tiếp theo trong giai đoạn đó sẽ bị bỏ qua, và các giai đoạn sau sẽ không thực thi.

### Best Practices

#### 1. Dùng đúng Giai đoạn

- Setup: Global checks, filtering, initial setup
- Parsing: Custom parsing logic
- Match: Handler selection logic
- Validation: Permissions, rate limits, guards
- PreInvoke: Handler-specific preparation
- Invoke: Thường được xử lý bởi interceptor mặc định
- PostInvoke: Cleanup, logging, error handling

#### 2. Giữ Interceptors Tập trung

Mỗi interceptor nên làm một việc:

```kotlin
// ✅ Good - interceptor tập trung
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    if (isBanned(context.update.userOrNull?.id)) {
        context.finish()
    }
}

// ❌ Avoid - làm quá nhiều
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    // Authentication
    // Logging
    // Metrics
    // Rate limiting
    // ... quá nhiều!
}
```

#### 3. Xử lý Errors Gracefully

Interceptors không nên crash bot:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
    try {
        // Logic của bạn
    } catch (e: Exception) {
        val logger = context.bot.config.loggerFactory.get("Interceptor")
        logger.error("Interceptor error", e)
        // Đừng gọi context.finish() trừ khi bạn muốn dừng xử lý
    }
}
```

#### 4. Dọn dẹp Tài nguyên

Nếu bạn mở tài nguyên trong `PreInvoke`, dọn dẹp chúng trong `PostInvoke`:

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

#### 5. Thứ tự Quan trọng

Đăng ký interceptors theo thứ tự bạn muốn chúng chạy:

```kotlin
// Checks chung trước
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) {
    // Global ban check
}

// Checks cụ thể sau
bot.update.pipeline.intercept(ProcessingPipePhase.Validation) {
    // Handler-specific permission check
}
```

#### 6. Dùng Interceptors cho Cross-Cutting Concerns

Interceptors lý tưởng cho:
- ✅ Authentication/authorization
- ✅ Logging
- ✅ Metrics/performance monitoring
- ✅ Rate limiting
- ✅ Error handling
- ✅ Request/response transformation

Với handler-specific logic, giữ nó trong handler.

### Default Interceptors

Framework bao gồm default interceptors cho core functionality:

- **DefaultSetupInterceptor**: Global rate limiting
- **DefaultParsingInterceptor**: Command parsing
- **DefaultMatchInterceptor**: Handler matching (commands, inputs, common matchers)
- **DefaultValidationInterceptor**: Guard checks và per-handler rate limiting
- **DefaultInvokeInterceptor**: Handler execution và error handling

Custom interceptors của bạn chạy cùng với defaults. Bạn có thể thêm logic trước hoặc sau defaults, nhưng bạn không thể xóa default interceptors.

---

### Advanced: Conditional Interceptors

Bạn có thể làm interceptors conditional:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
    val activity = context.activity ?: return@intercept

    // Chỉ áp dụng cho các handler cụ thể
    if (activity::class.simpleName?.contains("Admin") == true) {
        // Admin-specific logic
        checkAdminPermissions(context)
    }
}
```

### Summary

Interceptors cung cấp cách sạch sẽ để thêm cross-cutting logic cho bot của bạn:

- ✅ **Bảy giai đoạn** cho các stages khác nhau của xử lý
- ✅ **API đơn giản**: Chỉ implement `PipelineInterceptor`
- ✅ **Flexible**: Đăng ký multiple interceptors mỗi giai đoạn
- ✅ **Powerful**: Truy cập đầy đủ processing context
- ✅ **Safe**: Có thể dừng xử lý sớm với `context.finish()`

Dùng interceptors để giữ handlers tập trung vào business logic trong khi xử lý shared concerns như authentication, logging, và metrics một cách centralized.

---

### See also

* [Functional Handling DSL](Functional-handling-DSL.md) - Functional update processing
* [Guards](Guards.md) - Handler-level permission checks
---