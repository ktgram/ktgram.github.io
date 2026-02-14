---
---
title: Xử Lý FSM Và Hội Thoại
---

Thư viện cũng hỗ trợ cơ chế FSM, đây là cơ chế xử lý tiến bộ đầu vào của người dùng với việc xử lý đầu vào không chính xác.

> [!NOTE]
> TL;DR: Xem ví dụ [ở đó](https://github.com/vendelieu/telegram-bot_template/tree/conversation).

### Về mặt lý thuyết

Hãy tưởng tượng một tình huống bạn cần thu thập khảo sát người dùng, bạn có thể hỏi tất cả dữ liệu của một người trong một bước, nhưng với đầu vào không chính xác của một trong các tham số, nó sẽ khó khăn cả cho người dùng và cho chúng ta, và mỗi bước có thể khác nhau tùy thuộc vào một số dữ liệu đầu vào nhất định.

Bây giờ hãy tưởng tượng đầu vào từng bước của dữ liệu, nơi bot đi vào chế độ hội thoại với người dùng.

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/2e84fa00-e59c-4352-8665-83be3b971e7b" alt="Sơ đồ quá trình xử lý" />
</p>

Mũi tên màu xanh lá cây chỉ quá trình chuyển tiếp qua các bước không có lỗi, mũi tên màu xanh dương có nghĩa là lưu trạng thái hiện tại và chờ nhập lại (ví dụ: nếu người dùng chỉ ra rằng anh ta -100 tuổi, nó nên hỏi lại tuổi), và mũi tên màu đỏ hiển thị thoát khỏi toàn bộ quá trình do bất kỳ lệnh nào hoặc bất kỳ ý nghĩa hủy bỏ nào khác.

### Trong thực tế

Hệ thống Wizard cho phép tương tác nhiều bước với người dùng trong các bot Telegram. Nó hướng dẫn người dùng qua một chuỗi các bước, xác thực đầu vào, lưu trạng thái và chuyển tiếp giữa các bước.

**Lợi ích chính:**
- **An toàn kiểu**: Kiểm tra kiểu tại thời gian biên dịch cho truy cập trạng thái
- **Khai báo**: Định nghĩa các bước dưới dạng lớp/nhóm lồng nhau
- **Linh hoạt**: Hỗ trợ chuyển tiếp có điều kiện, nhảy và thử lại
- **Có trạng thái**: Tự động lưu trữ trạng thái với backend lưu trữ có thể cắm được
- **Tích hợp**: Hoạt động với hệ thống Activity hiện có

### Các Khái Niệm Cốt Lõi

#### WizardStep

`WizardStep` đại diện cho một bước đơn trong luồng wizard. Mỗi bước phải triển khai:

- **`onEntry(ctx: WizardContext)`**: Được gọi khi người dùng vào bước này. Sử dụng để nhắc người dùng.
- **`onRetry(ctx: WizardContext)`**: Được gọi khi xác thực thất bại và bước nên thử lại. Sử dụng để hiển thị thông báo lỗi.
- **`validate(ctx: WizardContext): Transition`**: Xác thực đầu vào hiện tại và trả về `Transition` chỉ ra điều gì xảy ra tiếp theo.
- **`store(ctx: WizardContext): Any?`** (tùy chọn): Trả về giá trị để lưu trữ cho bước này. Trả về `null` nếu bước không lưu trữ trạng thái.

```kotlin
object NameStep : WizardStep(isInitial = true) {
    override suspend fun onEntry(ctx: WizardContext) {
        message { "What is your name?" }.send(ctx.user, ctx.bot)
    }
    
    override suspend fun onRetry(ctx: WizardContext) {
        message { "Name cannot be empty. Please try again." }.send(ctx.user, ctx.bot)
    }
    
    override suspend fun validate(ctx: WizardContext): Transition {
        return if (ctx.update.text.isNullOrBlank()) {
            Transition.Retry
        } else {
            Transition.Next
        }
    }
    
    override suspend fun store(ctx: WizardContext): String {
        return ctx.update.text!!
    }
}
```

> [!NOTE]
> Nếu một số bước không được đánh dấu là ban đầu -> bước được khai báo đầu tiên được coi là.

#### Transition

`Transition` xác định điều gì xảy ra sau khi xác thực:

- **`Transition.Next`**: Chuyển sang bước tiếp theo trong chuỗi
- **`Transition.JumpTo(step: KClass<out WizardStep>)`**: Nhảy đến một bước cụ thể
- **`Transition.Retry`**: Thử lại bước hiện tại (xác thực thất bại)
- **`Transition.Finish`**: Kết thúc wizard

```kotlin
// Nhảy có điều kiện dựa trên đầu vào
override suspend fun validate(ctx: WizardContext): Transition {
    val age = ctx.update.text?.toIntOrNull()
    return when {
        age == null -> Transition.Retry
        age < 18 -> Transition.JumpTo(UnderageStep::class)
        else -> Transition.Next
    }
}
```

#### WizardContext

`WizardContext` cung cấp quyền truy cập vào:
- **`user: User`**: Người dùng hiện tại
- **`update: ProcessedUpdate`**: Cập nhật hiện tại
- **`bot: TelegramBot`**: Thể hiện bot
- **`userReference: UserChatReference`**: Tham chiếu ID người dùng và chat cho lưu trữ trạng thái

Cộng với các phương thức truy cập trạng thái an toàn kiểu (được tạo bởi KSP).

---

### Định Nghĩa Một Wizard

#### Cấu Trúc Cơ Bản

Một wizard được định nghĩa là một lớp hoặc đối tượng được chú thích với `@WizardHandler`:

```kotlin
@WizardHandler(trigger = ["/survey"])
object SurveyWizard {
    object NameStep : WizardStep(isInitial = true) {
        // ... triển khai bước
    }
    
    object AgeStep : WizardStep {
        // ... triển khai bước
    }
    
    object FinishStep : WizardStep {
        // ... triển khai bước
    }
}
```

#### Tham Số Chú Thích

**`@WizardHandler`** chấp nhận:
- **`trigger: Array<String>`**: Lệnh bắt đầu wizard (ví dụ: `["/start", "/survey"]`)
- **`scope: Array<UpdateType>`**: Các loại cập nhật để lắng nghe (mặc định: `[UpdateType.MESSAGE]`)
- **`stateManagers: Array<KClass<out WizardStateManager<*>>>`**: Các lớp quản lý trạng thái cho lưu trữ dữ liệu bước

---

### Quản Lý Trạng Thái

#### WizardStateManager

Trạng thái được lưu trữ sử dụng các triển khai `WizardStateManager<T>`. Mỗi trình quản lý xử lý một kiểu cụ thể:

```kotlin
interface WizardStateManager<T : Any> {
    suspend fun get(key: KClass<out WizardStep>, reference: UserChatReference): T?
    suspend fun set(key: KClass<out WizardStep>, reference: UserChatReference, value: T)
    suspend fun del(key: KClass<out WizardStep>, reference: UserChatReference)
}
```

Xem thêm: [MapStateManager<T>](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-state-manager/index.html), [MapStringStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-string-state-manager/index.html), [MapIntStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-int-state-manager/index.html), [MapLongStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-long-state-manager/index.html).

#### Ghép Đôi Tự Động

KSP ghép các bước với trình quản lý trạng thái dựa trên kiểu trả về của `store()`:

```kotlin
@WizardHandler(
    trigger = ["/survey"],
    stateManagers = [StringStateManager::class, IntStateManager::class]
)
object SurveyWizard {
    object NameStep : WizardStep(isInitial = true) {
        override suspend fun store(ctx: WizardContext): String {
            return ctx.update.text!! // Khớp với StringStateManager
        }
    }
    
    object AgeStep : WizardStep {
        override suspend fun store(ctx: WizardContext): Int {
            return ctx.update.text!!.toInt() // Khớp với IntStateManager
        }
    }
}
```

#### Ghi Đè Theo Bước

Ghi đè trình quản lý trạng thái cho một bước cụ thể sử dụng `@WizardHandler.StateManager`:

```kotlin
@WizardHandler(
    trigger = ["/survey"],
    stateManagers = [DefaultStateManager::class]
)
object SurveyWizard {
    object NameStep : WizardStep(isInitial = true) {
        // Sử dụng DefaultStateManager
    }
    
    @WizardHandler.StateManager(CustomStateManager::class)
    object AgeStep : WizardStep {
        // Sử dụng CustomStateManager thay thế
    }
}
```

---

### Truy Cập Trạng Thái An Toàn Kiểu

KSP tạo các hàm mở rộng an toàn kiểu trên `WizardContext` cho mỗi bước lưu trữ trạng thái.

#### Hàm Được Tạo

Đối với một bước lưu trữ `String`:

```kotlin
// Được tạo tự động bởi KSP
suspend inline fun <reified S : WizardStep> WizardContext.getState(): String?
suspend inline fun <reified S : WizardStep> WizardContext.setState(value: String)
suspend inline fun <reified S : WizardStep> WizardContext.delState()
```

#### Cách Sử Dụng

```kotlin
object FinishStep : WizardStep {
    override suspend fun onEntry(ctx: WizardContext) {
        // Truy cập an toàn kiểu - trả về String? (nullable)
        val name: String? = ctx.getState<NameStep>()
        
        // Truy cập an toàn kiểu - trả về Int? (nullable)
        val age: Int? = ctx.getState<AgeStep>()
        
        val summary = buildString {
            appendLine("Name: $name")
            appendLine("Age: $age")
        }
        
        message { summary }.send(ctx.user, ctx.bot)
    }
    
    override suspend fun onRetry(ctx: WizardContext) = Unit
    
    override suspend fun validate(ctx: WizardContext): Transition {
        return Transition.Finish
    }
}
```

#### Phương Thức Dự Phòng

Nếu các phương thức an toàn kiểu không khả dụng, sử dụng các phương thức dự phòng:

```kotlin
// Dự phòng - trả về Any?
val name = ctx.getState(NameStep::class)

// Dự phòng - chấp nhận Any?
ctx.setState(NameStep::class, "John")
ctx.delState(NameStep::class)
```

---

### Ví Dụ Hoàn Chỉnh

#### Wizard Đăng Ký Người Dùng

```kotlin
@WizardHandler(
    trigger = ["/register"],
    stateManagers = [StringStateManager::class, IntStateManager::class]
)
object RegistrationWizard {
    object NameStep : WizardStep(isInitial = true) {
        override suspend fun onEntry(ctx: WizardContext) {
            message { "What is your name?" }.send(ctx.user, ctx.bot)
        }
        
        override suspend fun onRetry(ctx: WizardContext) {
            message { "Please enter a valid name." }.send(ctx.user, ctx.bot)
        }
        
        override suspend fun validate(ctx: WizardContext): Transition {
            val name = ctx.update.text?.trim()
            return if (name.isNullOrBlank() || name.length < 2) {
                Transition.Retry
            } else {
                Transition.Next
            }
        }
        
        override suspend fun store(ctx: WizardContext): String {
            return ctx.update.text!!.trim()
        }
    }
    
    object AgeStep : WizardStep {
        override suspend fun onEntry(ctx: WizardContext) {
            message { "How old are you?" }.send(ctx.user, ctx.bot)
        }
        
        override suspend fun onRetry(ctx: WizardContext) {
            message { "Please enter a valid age (must be a number)." }.send(ctx.user, ctx.bot)
        }
        
        override suspend fun validate(ctx: WizardContext): Transition {
            val age = ctx.update.text?.toIntOrNull()
            return when {
                age == null -> Transition.Retry
                age < 0 || age > 150 -> Transition.Retry
                age < 18 -> Transition.JumpTo(UnderageStep::class)
                else -> Transition.Next
            }
        }
        
        override suspend fun store(ctx: WizardContext): Int {
            return ctx.update.text!!.toInt()
        }
    }
    
    object UnderageStep : WizardStep {
        override suspend fun onEntry(ctx: WizardContext) {
            message { 
                "Sorry, you must be 18 or older to register." 
            }.send(ctx.user, ctx.bot)
        }
        
        override suspend fun onRetry(ctx: WizardContext) = Unit
        
        override suspend fun validate(ctx: WizardContext): Transition {
            return Transition.Finish
        }
    }
    
    object ConfirmationStep : WizardStep {
        override suspend fun onEntry(ctx: WizardContext) {
            // Truy cập trạng thái an toàn kiểu
            val name: String? = ctx.getState<NameStep>()
            val age: Int? = ctx.getState<AgeStep>()
            
            val confirmation = buildString {
                appendLine("Please confirm your information:")
                appendLine("Name: $name")
                appendLine("Age: $age")
                appendLine()
                appendLine("Reply 'yes' to confirm or 'no' to start over.")
            }
            
            message { confirmation }.send(ctx.user, ctx.bot)
        }
        
        override suspend fun onRetry(ctx: WizardContext) {
            message { "Please reply 'yes' or 'no'." }.send(ctx.user, ctx.bot)
        }
        
        override suspend fun validate(ctx: WizardContext): Transition {
            val response = ctx.update.text?.lowercase()?.trim()
            return when (response) {
                "yes" -> Transition.Finish
                "no" -> Transition.JumpTo(NameStep::class) // Bắt đầu lại
                else -> Transition.Retry
            }
        }
    }
    
    object FinishStep : WizardStep {
        override suspend fun onEntry(ctx: WizardContext) {
            val name: String? = ctx.getState<NameStep>()
            val age: Int? = ctx.getState<AgeStep>()
            
            // Lưu vào cơ sở dữ liệu, gửi xác nhận, v.v.
            message { 
                "Registration complete! Welcome, $name (age $age)." 
            }.send(ctx.user, ctx.bot)
        }
        
        override suspend fun onRetry(ctx: WizardContext) = Unit
        
        override suspend fun validate(ctx: WizardContext): Transition {
            return Transition.Finish
        }
    }
}
```

---

### Tính Năng Nâng Cao

#### Chuyển Tiếp Có Điều Kiện

Sử dụng `Transition.JumpTo` cho luồng có điều kiện:

```kotlin
override suspend fun validate(ctx: WizardContext): Transition {
    val choice = ctx.update.text?.lowercase()
    return when (choice) {
        "premium" -> Transition.JumpTo(PremiumStep::class)
        "basic" -> Transition.JumpTo(BasicStep::class)
        else -> Transition.Retry
    }
}
```

#### Các Bước Không Có Trạng Thái

Các bước không cần lưu trữ trạng thái. Đơn giản trả về `null` từ `store()` (hoặc giữ nguyên):

```kotlin
object ConfirmationStep : WizardStep {
    override suspend fun store(ctx: WizardContext): Any? = null
    // ... phần còn lại của triển khai
}
```

#### Trình Quản Lý Trạng Thái Tùy Chỉnh

Triển khai `WizardStateManager<T>` cho lưu trữ tùy chỉnh (cơ sở dữ liệu, Redis, v.v.):

```kotlin
class DatabaseStateManager : WizardStateManager<String> {
    override suspend fun get(
        key: KClass<out WizardStep>,
        reference: UserChatReference
    ): String? {
        // Tải từ cơ sở dữ liệu
        return database.getWizardState(reference.userId, key.qualifiedName)
    }
    
    override suspend fun set(
        key: KClass<out WizardStep>,
        reference: UserChatReference,
        value: String
    ) {
        // Lưu vào cơ sở dữ liệu
        database.saveWizardState(reference.userId, key.qualifiedName, value)
    }
    
    override suspend fun del(
        key: KClass<out WizardStep>,
        reference: UserChatReference
    ) {
        // Xóa khỏi cơ sở dữ liệu
        database.deleteWizardState(reference.userId, key.qualifiedName)
    }
}
```

---

### Cách Nó Hoạt Động Bên Trong

#### Tạo Mã

KSP tạo:

1. **WizardActivity**: Một triển khai cụ thể mở rộng `WizardActivity` với các bước được mã hóa cứng
2. **Start Activity**: Xử lý trình kích hoạt lệnh và bắt đầu wizard
3. **Input Activity**: Xử lý đầu vào người dùng trong luồng wizard
4. **State Accessors**: Các hàm mở rộng an toàn kiểu cho truy cập trạng thái

#### Luồng

1. Người dùng gửi `/register` → Start Activity được gọi
2. Start Activity tạo `WizardContext` và gọi `wizardActivity.start(ctx)`
3. `start()` vào bước ban đầu và thiết lập `inputListener` để theo dõi bước hiện tại
4. Người dùng gửi tin nhắn → Input Activity được gọi
5. Input Activity gọi `wizardActivity.handleInput(ctx)`
6. `handleInput()` xác thực đầu vào, lưu trữ trạng thái và chuyển tiếp sang bước tiếp theo
7. Quá trình lặp lại cho đến khi `Transition.Finish` được trả về

#### Lưu Trữ Trạng Thái

- Trạng thái được lưu trữ sau khi xác thực thành công (trước khi chuyển tiếp)
- Giá trị trả về của `store()` cho mỗi bước được lưu trữ sử dụng `WizardStateManager` khớp
- Trạng thái được giới hạn theo người dùng và chat (`UserChatReference`)

---

### Thực Hành Tốt Nhất

#### 1. Luôn Cung Cấp Lời Nhắc Rõ Ràng

```kotlin
override suspend fun onEntry(ctx: WizardContext) {
    message { 
        "Please enter your email address:\n" +
        "(Format: user@example.com)" 
    }.send(ctx.user, ctx.bot)
}
```

#### 2. Xử Lý Lỗi Xác Thực Một Cách Lịch Sự

```kotlin
override suspend fun onRetry(ctx: WizardContext) {
    message { 
        "Invalid email format. Please try again.\n" +
        "Example: user@example.com" 
    }.send(ctx.user, ctx.bot)
}
```

#### 3. Sử Dụng Truy Cập Trạng Thái An Toàn Kiểu

Thích các phương thức an toàn kiểu được tạo:

```kotlin
// ✅ Tốt - an toàn kiểu
val name: String? = ctx.getState<NameStep>()

// ❌ Tránh - mất an toàn kiểu
val name = ctx.getState(NameStep::class) as? String
```

#### 4. Giữ Các Bước Tập Trung

Mỗi bước nên có một trách nhiệm duy nhất:

```kotlin
// ✅ Tốt - bước tập trung
object EmailStep : WizardStep {
    // Chỉ xử lý thu thập email
}

// ❌ Tránh - quá nhiều logic
object PersonalInfoStep : WizardStep {
    // Xử lý tên, email, điện thoại, địa chỉ...
}
```

#### 5. Sử Dụng Tên Bước Có Ý Nghĩa

```kotlin
// ✅ Tốt
object EmailVerificationStep : WizardStep

// ❌ Tránh
object Step2 : WizardStep
```

#### 6. Dọn Dẹp Trạng Thái Khi Cần

Nếu bạn cần xóa trạng thái thủ công:

```kotlin
object CancelStep : WizardStep {
    override suspend fun onEntry(ctx: WizardContext) {
        // Xóa tất cả trạng thái wizard
        ctx.delState<NameStep>()
        ctx.delState<AgeStep>()
        
        message { "Registration cancelled." }.send(ctx.user, ctx.bot)
    }
}
```

---

### Tóm Tắt

Hệ thống Wizard cung cấp:
- ✅ **An toàn kiểu** quản lý trạng thái với kiểm tra tại thời gian biên dịch
- ✅ **Khai báo** định nghĩa bước dưới dạng lớp lồng nhau
- ✅ **Linh hoạt** chuyển tiếp với logic có điều kiện
- ✅ **Tự động** tạo mã qua KSP
- ✅ **Tích hợp** với hệ thống Activity hiện có
- ✅ **Có thể cắm được** backend lưu trữ trạng thái

Bắt đầu xây dựng wizard bằng cách chú thích một lớp với `@WizardHandler` và định nghĩa các bước của bạn dưới dạng các đối tượng `WizardStep` lồng nhau!
nếu bạn có bất kỳ câu hỏi nào liên hệ với chúng tôi trong chat, chúng tôi sẽ rất vui được giúp đỡ :)
---