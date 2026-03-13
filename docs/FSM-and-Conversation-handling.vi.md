---
---
title: Xử lý FSM và Hội thoại
---

Thư viện cũng hỗ trợ cơ chế FSM, đây là cơ chế xử lý tiến bộ đầu vào của người dùng với xử lý đầu vào không chính xác.

> [!NOTE]
> TL;DR: Xem ví dụ [tại đây](https://github.com/vendelieu/telegram-bot_template/tree/conversation).

### Về mặt lý thuyết

Hãy tưởng tượng một tình huống nơi bạn cần thu thập khảo sát người dùng, bạn có thể yêu cầu tất cả dữ liệu của một người trong một bước, nhưng với đầu vào không chính xác của một trong các tham số, nó sẽ khó khăn cả cho người dùng và cho chúng ta, và mỗi bước có thể khác nhau tùy thuộc vào dữ liệu đầu vào nhất định.

Bây giờ hãy tưởng tượng đầu vào từng bước của dữ liệu, nơi bot bước vào chế độ hội thoại với người dùng.

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/2e84fa00-e59c-4352-8665-83be3b971e7b" alt="Sơ đồ xử lý quá trình" />
</p>

Mũi tên màu xanh lá cây chỉ ra quá trình chuyển qua các bước không có lỗi, mũi tên màu xanh dương có nghĩa là lưu trạng thái hiện tại và chờ nhập lại (ví dụ: nếu người dùng chỉ ra rằng anh ta -100 tuổi, nó nên yêu cầu tuổi lại), và mũi tên màu đỏ hiển thị thoát khỏi toàn bộ quá trình do bất kỳ lệnh nào hoặc bất kỳ hủy bỏ có ý nghĩa nào khác.

### Trong thực tế

Hệ thống Wizard cho phép tương tác nhiều bước với người dùng trong các bot Telegram. Nó hướng dẫn người dùng qua một chuỗi các bước, xác thực đầu vào, lưu trữ trạng thái, và chuyển đổi giữa các bước.

**Lợi ích chính:**
- **An toàn kiểu**: Kiểm tra kiểu ở thời gian biên dịch cho truy cập trạng thái
- **Khai báo**: Định nghĩa các bước dưới dạng lớp/nhóm lồng nhau
- **Linh hoạt**: Hỗ trợ chuyển đổi có điều kiện, nhảy và thử lại
- **Có trạng thái**: Tự động lưu trữ trạng thái với bộ lưu trữ backend có thể cắm ghép
- **Tích hợp**: Hoạt động với hệ thống Activity hiện có

### Các khái niệm cốt lõi

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

- **`Transition.Next`**: Chuyển đến bước tiếp theo trong thứ tự
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

`WizardContext` cung cấp truy cập đến:
- **`user: User`**: Người dùng hiện tại
- **`update: ProcessedUpdate`**: Cập nhật hiện tại
- **`bot: TelegramBot`**: Bot instance
- **`userReference: UserChatReference`**: Tham chiếu ID người dùng và chat cho lưu trữ trạng thái

Cộng với các phương thức truy cập trạng thái an toàn kiểu (được tạo bởi KSP).

---

### Định nghĩa một Wizard

#### Cấu trúc cơ bản

Một wizard được định nghĩa dưới dạng lớp hoặc đối tượng được chú thích với `@WizardHandler`:

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

#### Tham số chú thích

**`@WizardHandler`** chấp nhận:
- **`trigger: Array<String>`**: Lệnh bắt đầu wizard (ví dụ: `["/start", "/survey"]`)
- **`scope: Array<UpdateType>`**: Loại cập nhật để lắng nghe (mặc định: `[UpdateType.MESSAGE]`)
- **`stateManagers: Array<KClass<out WizardStateManager<*>>>`**: Các lớp quản lý trạng thái cho lưu trữ dữ liệu bước

---

### Quản lý trạng thái

#### WizardStateManager

Trạng thái được lưu trữ bằng cách sử dụng các triển khai `WizardStateManager<T>`. Mỗi trình quản lý xử lý một kiểu cụ thể:

```kotlin
interface WizardStateManager<T : Any> {
    suspend fun get(key: KClass<out WizardStep>, reference: UserChatReference): T?
    suspend fun set(key: KClass<out WizardStep>, reference: UserChatReference, value: T)
    suspend fun del(key: KClass<out WizardStep>, reference: UserChatReference)
}
```

Xem thêm: [MapStateManager<T>](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-state-manager/index.html), [MapStringStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-string-state-manager/index.html), [MapIntStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-int-state-manager/index.html), [MapLongStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-long-state-manager/index.html).

#### Ghép đôi tự động

KSP ghép đôi các bước với trình quản lý trạng thái dựa trên kiểu trả về của `store()`:

```kotlin
@WizardHandler(
    trigger = ["/survey"],
    stateManagers = [StringStateManager::class, IntStateManager::class]
)
object SurveyWizard {
    object NameStep : WizardStep(isInitial = true) {
        override suspend fun store(ctx: WizardContext): String {
            return ctx.update.text!! // Trùng với StringStateManager
        }
    }
    
    object AgeStep : WizardStep {
        override suspend fun store(ctx: WizardContext): Int {
            return ctx.update.text!!.toInt() // Trùng với IntStateManager
        }
    }
}
```

#### Ghi đè từng bước

Ghi đè trình quản lý trạng thái cho một bước cụ thể bằng cách sử dụng `@WizardHandler.StateManager`:

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

### Truy cập trạng thái an toàn kiểu

KSP tạo các hàm mở rộng an toàn kiểu trên `WizardContext` cho mỗi bước lưu trữ trạng thái.

#### Các hàm được tạo

Đối với một bước lưu trữ `String`:

```kotlin
// Được tạo tự động bởi KSP
suspend inline fun <reified S : WizardStep> WizardContext.getState(): String?
suspend inline fun <reified S : WizardStep> WizardContext.setState(value: String)
suspend inline fun <reified S : WizardStep> WizardContext.delState()
```

#### Sử dụng

```kotlin
object FinishStep : WizardStep {
    override suspend fun onEntry(ctx: WizardContext) {
        // Truy cập an toàn kiểu - trả về String? (có thể null)
        val name: String? = ctx.getState<NameStep>()
        
        // Truy cập an toàn kiểu - trả về Int? (có thể null)
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

#### Phương thức dự phòng

Nếu các phương thức an toàn kiểu không có sẵn, sử dụng các phương thức dự phòng:

```kotlin
// Dự phòng - trả về Any?
val name = ctx.getState(NameStep::class)

// Dự phòng - chấp nhận Any?
ctx.setState(NameStep::class, "John")
ctx.delState(NameStep::class)
```

---

### Ví dụ hoàn chỉnh

#### Wizard đăng ký người dùng

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

### Tính năng nâng cao

#### Chuyển đổi có điều kiện

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

#### Các bước không trạng thái

Các bước không cần lưu trữ trạng thái. Đơn giản trả về `null` từ `store()` (hoặc giữ nguyên):

```kotlin
object ConfirmationStep : WizardStep {
    override suspend fun store(ctx: WizardContext): Any? = null
    // ... phần còn lại của triển khai
}
```

#### Trình quản lý trạng thái tùy chỉnh

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

### Cách nó hoạt động bên trong

#### Tạo mã

KSP tạo:

1. **WizardActivity**: Một triển khai cụ thể mở rộng `WizardActivity` với các bước được mã hóa cứng
2. **Start Activity**: Xử lý lệnh trigger và bắt đầu wizard
3. **Input Activity**: Xử lý đầu vào người dùng trong luồng wizard
4. **State Accessors**: Các hàm mở rộng truy cập trạng thái an toàn kiểu

#### Luồng

1. Người dùng gửi `/register` → Start Activity được gọi
2. Start Activity tạo `WizardContext` và gọi `wizardActivity.start(ctx)`
3. `start()` vào bước ban đầu và đặt `inputListener` để theo dõi bước hiện tại
4. Người dùng gửi tin nhắn → Input Activity được gọi
5. Input Activity gọi `wizardActivity.handleInput(ctx)`
6. `handleInput()` xác thực đầu vào, lưu trữ trạng thái, và chuyển đến bước tiếp theo
7. Quá trình lặp lại cho đến khi `Transition.Finish` được trả về

#### Lưu trữ trạng thái

- Trạng thái được lưu trữ sau khi xác thực thành công (trước khi chuyển đổi)
- Giá trị trả về `store()` của mỗi bước được lưu trữ bằng `WizardStateManager` trùng khớp
- Trạng thái được giới hạn cho mỗi người dùng và chat (`UserChatReference`)

---

### Các thực hành tốt nhất

#### 1. Luôn cung cấp lời nhắc rõ ràng

```kotlin
override suspend fun onEntry(ctx: WizardContext) {
    message { 
        "Please enter your email address:\n" +
        "(Format: user@example.com)" 
    }.send(ctx.user, ctx.bot)
}
```

#### 2. Xử lý lỗi xác thực một cách lịch sự

```kotlin
override suspend fun onRetry(ctx: WizardContext) {
    message { 
        "Invalid email format. Please try again.\n" +
        "Example: user@example.com" 
    }.send(ctx.user, ctx.bot)
}
```

#### 3. Sử dụng truy cập trạng thái an toàn kiểu

Ưu tiên các phương thức an toàn kiểu được tạo:

```kotlin
// ✅ Tốt - an toàn kiểu
val name: String? = ctx.getState<NameStep>()

// ❌ Tránh - mất an toàn kiểu
val name = ctx.getState(NameStep::class) as? String
```

#### 4. Giữ các bước tập trung

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

#### 5. Sử dụng tên bước có ý nghĩa

```kotlin
// ✅ Tốt
object EmailVerificationStep : WizardStep

// ❌ Tránh
object Step2 : WizardStep
```

#### 6. Dọn dẹp trạng thái khi cần

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

### Tóm tắt

Hệ thống Wizard cung cấp:
- ✅ **Quản lý trạng thái an toàn kiểu** với kiểm tra thời gian biên dịch
- ✅ **Định nghĩa khai báo** các bước dưới dạng lớp lồng nhau
- ✅ **Chuyển đổi linh hoạt** với logic có điều kiện
- ✅ **Tạo mã tự động** qua KSP
- ✅ **Tích hợp** với hệ thống Activity hiện có
- ✅ **Lưu trữ trạng thái có thể cắm ghép** backend

Bắt đầu xây dựng wizards bằng cách chú thích một lớp với `@WizardHandler` và định nghĩa các bước của bạn dưới dạng các đối tượng `WizardStep` lồng nhau!
nếu bạn có bất kỳ câu hỏi nào liên hệ chúng tôi trong chat, chúng tôi sẽ rất vui được giúp đỡ :)
---