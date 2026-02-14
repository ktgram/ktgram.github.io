---
---
title: FSM 与会话处理
---

库还支持 FSM 机制，这是一种用于处理用户输入和错误输入处理的渐进式处理机制。

> [!NOTE]
> TL;DR: 查看示例 [那里](https://github.com/vendelieu/telegram-bot_template/tree/conversation)。

### 理论

让我们想象一个需要收集用户调查的情况，你可以在一个步骤中询问一个人的所有数据，但对于某个参数的错误输入，对于用户和我们来说都会很困难，并且每个步骤可能根据某些输入数据而有所不同。

现在让我们想象逐步输入数据，其中机器人进入与用户的对话模式。

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/2e84fa00-e59c-4352-8665-83be3b971e7b" alt="处理过程图" />
</p>

绿色箭头表示无错误地通过步骤的转换过程，蓝色箭头表示保存当前状态并等待重新输入（例如，如果用户表示他 -100 岁，应该重新询问年龄），红色箭头表示由于任何命令或任何其他有意义的取消而退出整个过程。

### 实践

Wizard 系统在 Telegram 机器人中启用多步骤用户交互。它引导用户完成一系列步骤，验证输入，存储状态，并在步骤之间转换。

**主要优点:**
- **类型安全**: 编译时类型检查用于状态访问
- **声明式**: 将步骤定义为嵌套类/对象
- **灵活**: 支持条件转换、跳转和重试
- **有状态**: 自动状态持久化，支持可插拔的存储后端
- **集成**: 与现有的 Activity 系统配合工作

### 核心概念

#### WizardStep

`WizardStep` 表示向导流程中的单个步骤。每个步骤必须实现:

- **`onEntry(ctx: WizardContext)`**: 当用户进入此步骤时调用。用于提示用户。
- **`onRetry(ctx: WizardContext)`**: 当验证失败且步骤应该重试时调用。用于显示错误消息。
- **`validate(ctx: WizardContext): Transition`**: 验证当前输入并返回 `Transition` 以指示接下来发生什么。
- **`store(ctx: WizardContext): Any?`** (可选): 返回要为此步骤持久化的返回值。如果步骤不存储状态，则返回 `null`。

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
> 如果某个步骤未标记为初始 -> 第一个声明的步骤被视为初始。

#### Transition

`Transition` 确定验证后发生什么:

- **`Transition.Next`**: 移动到序列中的下一个步骤
- **`Transition.JumpTo(step: KClass<out WizardStep>)`**: 跳转到特定步骤
- **`Transition.Retry`**: 重试当前步骤（验证失败）
- **`Transition.Finish`**: 完成向导

```kotlin
// 基于输入的条件跳转
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

`WizardContext` 提供对以下内容的访问:
- **`user: User`**: 当前用户
- **`update: ProcessedUpdate`**: 当前更新
- **`bot: TelegramBot`**: 机器人实例
- **`userReference: UserChatReference`**: 用于状态存储的用户和聊天 ID 引用

以及类型安全的状态访问方法（由 KSP 生成）。

---

### 定义向导

#### 基本结构

向导被定义为使用 `@WizardHandler` 注解的类或对象:

```kotlin
@WizardHandler(trigger = ["/survey"])
object SurveyWizard {
    object NameStep : WizardStep(isInitial = true) {
        // ... 步骤实现
    }
    
    object AgeStep : WizardStep {
        // ... 步骤实现
    }
    
    object FinishStep : WizardStep {
        // ... 步骤实现
    }
}
```

#### 注解参数

**`@WizardHandler`** 接受:
- **`trigger: Array<String>`**: 启动向导的命令（例如: `["/start", "/survey"]`）
- **`scope: Array<UpdateType>`**: 要监听的更新类型（默认: `[UpdateType.MESSAGE]`）
- **`stateManagers: Array<KClass<out WizardStateManager<*>>>`**: 用于存储步骤数据的状态管理器类

---

### 状态管理

#### WizardStateManager

状态使用 `WizardStateManager<T>` 实现存储。每个管理器处理特定类型:

```kotlin
interface WizardStateManager<T : Any> {
    suspend fun get(key: KClass<out WizardStep>, reference: UserChatReference): T?
    suspend fun set(key: KClass<out WizardStep>, reference: UserChatReference, value: T)
    suspend fun del(key: KClass<out WizardStep>, reference: UserChatReference)
}
```

另请参阅: [MapStateManager<T>](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-state-manager/index.html), [MapStringStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-string-state-manager/index.html), [MapIntStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-int-state-manager/index.html), [MapLongStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-long-state-manager/index.html)。

#### 自动匹配

KSP 根据 `store()` 返回类型将步骤匹配到状态管理器:

```kotlin
@WizardHandler(
    trigger = ["/survey"],
    stateManagers = [StringStateManager::class, IntStateManager::class]
)
object SurveyWizard {
    object NameStep : WizardStep(isInitial = true) {
        override suspend fun store(ctx: WizardContext): String {
            return ctx.update.text!! // 匹配 StringStateManager
        }
    }
    
    object AgeStep : WizardStep {
        override suspend fun store(ctx: WizardContext): Int {
            return ctx.update.text!!.toInt() // 匹配 IntStateManager
        }
    }
}
```

#### 每步覆盖

使用 `@WizardHandler.StateManager` 为特定步骤覆盖状态管理器:

```kotlin
@WizardHandler(
    trigger = ["/survey"],
    stateManagers = [DefaultStateManager::class]
)
object SurveyWizard {
    object NameStep : WizardStep(isInitial = true) {
        // 使用 DefaultStateManager
    }
    
    @WizardHandler.StateManager(CustomStateManager::class)
    object AgeStep : WizardStep {
        // 使用 CustomStateManager 代替
    }
}
```

---

### 类型安全的状态访问

KSP 为每个存储状态的步骤生成类型安全的扩展函数到 `WizardContext`。

#### 生成的函数

对于存储 `String` 的步骤:

```kotlin
// 由 KSP 自动生成
suspend inline fun <reified S : WizardStep> WizardContext.getState(): String?
suspend inline fun <reified S : WizardStep> WizardContext.setState(value: String)
suspend inline fun <reified S : WizardStep> WizardContext.delState()
```

#### 用法

```kotlin
object FinishStep : WizardStep {
    override suspend fun onEntry(ctx: WizardContext) {
        // 类型安全访问 - 返回 String? (可空)
        val name: String? = ctx.getState<NameStep>()
        
        // 类型安全访问 - 返回 Int? (可空)
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

#### 回退方法

如果类型安全方法不可用，请使用回退方法:

```kotlin
// 回退 - 返回 Any?
val name = ctx.getState(NameStep::class)

// 回退 - 接受 Any?
ctx.setState(NameStep::class, "John")
ctx.delState(NameStep::class)
```

---

### 完整示例

#### 用户注册向导

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
            // 类型安全状态访问
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
                "no" -> Transition.JumpTo(NameStep::class) // 重新开始
                else -> Transition.Retry
            }
        }
    }
    
    object FinishStep : WizardStep {
        override suspend fun onEntry(ctx: WizardContext) {
            val name: String? = ctx.getState<NameStep>()
            val age: Int? = ctx.getState<AgeStep>()
            
            // 保存到数据库、发送确认等
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

### 高级功能

#### 条件转换

使用 `Transition.JumpTo` 实现条件流程:

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

#### 无状态步骤

步骤不需要存储状态。只需从 `store()` 返回 `null` (或保持原样):

```kotlin
object ConfirmationStep : WizardStep {
    override suspend fun store(ctx: WizardContext): Any? = null
    // ... 其余实现
}
```

#### 自定义状态管理器

为自定义存储（数据库、Redis 等）实现 `WizardStateManager<T>`:

```kotlin
class DatabaseStateManager : WizardStateManager<String> {
    override suspend fun get(
        key: KClass<out WizardStep>,
        reference: UserChatReference
    ): String? {
        // 从数据库加载
        return database.getWizardState(reference.userId, key.qualifiedName)
    }
    
    override suspend fun set(
        key: KClass<out WizardStep>,
        reference: UserChatReference,
        value: String
    ) {
        // 保存到数据库
        database.saveWizardState(reference.userId, key.qualifiedName, value)
    }
    
    override suspend fun del(
        key: KClass<out WizardStep>,
        reference: UserChatReference
    ) {
        // 从数据库删除
        database.deleteWizardState(reference.userId, key.qualifiedName)
    }
}
```

---

### 内部工作原理

#### 代码生成

KSP 生成:

1. **WizardActivity**: 扩展 `WizardActivity` 的具体实现，包含硬编码步骤
2. **Start Activity**: 处理命令触发并启动向导
3. **Input Activity**: 在向导流程中处理用户输入
4. **State Accessors**: 用于状态访问的类型安全扩展函数

#### 流程

1. 用户发送 `/register` → Start Activity 被调用
2. Start Activity 创建 `WizardContext` 并调用 `wizardActivity.start(ctx)`
3. `start()` 进入初始步骤并设置 `inputListener` 以跟踪当前步骤
4. 用户发送消息 → Input Activity 被调用
5. Input Activity 调用 `wizardActivity.handleInput(ctx)`
6. `handleInput()` 验证输入、持久化状态并转换到下一步
7. 过程重复直到返回 `Transition.Finish`

#### 状态持久化

- 状态在成功验证后持久化（转换之前）
- 每个步骤的 `store()` 返回值使用匹配的 `WizardStateManager` 保存
- 状态按用户和聊天作用域 (`UserChatReference`)

---

### 最佳实践

#### 1. 始终提供清晰的提示

```kotlin
override suspend fun onEntry(ctx: WizardContext) {
    message { 
        "Please enter your email address:\n" +
        "(Format: user@example.com)" 
    }.send(ctx.user, ctx.bot)
}
```

#### 2. 优雅地处理验证错误

```kotlin
override suspend fun onRetry(ctx: WizardContext) {
    message { 
        "Invalid email format. Please try again.\n" +
        "Example: user@example.com" 
    }.send(ctx.user, ctx.bot)
}
```

#### 3. 使用类型安全的状态访问

优先使用生成的类型安全方法:

```kotlin
// ✅ 好 - 类型安全
val name: String? = ctx.getState<NameStep>()

// ❌ 避免 - 失去类型安全
val name = ctx.getState(NameStep::class) as? String
```

#### 4. 保持步骤专注

每个步骤应该有单一职责:

```kotlin
// ✅ 好 - 专注的步骤
object EmailStep : WizardStep {
    // 只处理电子邮件收集
}

// ❌ 避免 - 逻辑过多
object PersonalInfoStep : WizardStep {
    // 处理姓名、电子邮件、电话、地址...
}
```

#### 5. 使用有意义的步骤名称

```kotlin
// ✅ 好
object EmailVerificationStep : WizardStep

// ❌ 避免
object Step2 : WizardStep
```

#### 6. 在需要时清理状态

如果需要手动清除状态:

```kotlin
object CancelStep : WizardStep {
    override suspend fun onEntry(ctx: WizardContext) {
        // 清除所有向导状态
        ctx.delState<NameStep>()
        ctx.delState<AgeStep>()
        
        message { "Registration cancelled." }.send(ctx.user, ctx.bot)
    }
}
```

---

### 总结

Wizard 系统提供:
- ✅ **类型安全** 的状态管理，编译时检查
- ✅ **声明式** 的步骤定义作为嵌套类
- ✅ **灵活** 的转换，支持条件逻辑
- ✅ **自动** 的代码生成，通过 KSP
- ✅ **集成** 到现有的 Activity 系统
- ✅ **可插拔** 的状态存储后端

开始构建向导，通过使用 `@WizardHandler` 注解类并定义步骤作为嵌套 `WizardStep` 对象!