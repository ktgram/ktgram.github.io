---
---
title: Interceptors (Middleware)
---

### Interceptors: Cross-Cutting Logic for Your Bot

当构建 Telegram 机器人时，您常常会在多个处理器之间重复进行设置、检查或清理工作。拦截器让您可以在处理器周围插入共享逻辑，使处理器保持专注且易于维护。

下面介绍 *telegram-bot* 中拦截器的工作原理以及如何使用它们。

### What Are Interceptors? (Simple Explanation)

拦截器是运行在更新处理管道特定节点的函数。它们可以让您：
- 检查并修改处理上下文
- 添加横切逻辑（日志、认证、指标）
- 在需要时提前结束处理
- 在处理完成后清理资源

可以把拦截器看作每个更新在处理器执行前、执行中和执行后必须通过的检查点。


### The Processing Pipeline

机器人通过一个包含七个阶段的管道来处理更新：

| Phase | When It Runs | What You Can Use It For |
|-------|--------------|-------------------------|
| **Setup** | 当更新到达时，任何处理之前 | ✔ 全局速率限制<br>✔ 过滤垃圾或格式错误的更新<br>✔ 初始日志记录<br>✔ 设置共享上下文 |
| **Parsing** | Setup 之后，提取命令和参数 | ✔ 自定义命令解析<br>✔ 用解析后的数据丰富上下文<br>✔ 验证更新结构 |
| **Match** | 找到合适的处理器（Command/Input/Common） | ✔ 覆盖处理器选择<br>✔ 自定义输入处理逻辑<br>✔ 记录匹配的处理器 |
| **Validation** | 找到处理器后，调用前 | ✔ 针对处理器的权限检查<br>✔ 每个处理器的速率限制<br>✔ 守卫检查<br>✔ 条件不满足时取消处理 |
| **PreInvoke** | 在处理器运行之前立即执行 | ✔ 最后检查<br>✔ 启动计时器/指标<br>✔ 为处理器丰富上下文<br>✔ 修改处理器行为 |
| **Invoke** | 处理器在此执行 | ✔ 包装处理器执行<br>✔ 错误处理<br>✔ 记录处理器结果 |
| **PostInvoke** | 处理器完成后（成功或失败） | ✔ 清理资源<br>✔ 记录结果<br>✔ 错误时发送回退消息<br>✔ 在返回前修改结果 |


### Creating an Interceptor

拦截器是一个接收 `ProcessingContext` 的简单函数：

```kotlin
import eu.vendeli.tgbot.core.PipelineInterceptor
import eu.vendeli.tgbot.types.component.ProcessingContext

val myInterceptor: PipelineInterceptor = { context ->
    // Your logic here
    println("Processing update: ${context.update.updateId}")
}
```

或者使用 lambda：

```kotlin
val loggingInterceptor = PipelineInterceptor { context ->
    val logger = context.bot.config.loggerFactory.get("MyInterceptor")
    logger.info("Processing update #${context.update.updateId}")
}
```


### Registering Interceptors

在处理管道上注册拦截器：

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

示例：一个需要对特定命令进行身份验证、测量处理器执行时间并记录所有命令的机器人。

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

`ProcessingContext` 提供以下访问入口：

- **`update: ProcessedUpdate`** - 当前正在处理的更新
- **`bot: TelegramBot`** - 机器人实例
- **`registry: ActivityRegistry`** - 活动注册表
- **`parsedInput: String`** - 解析后的命令/输入文本
- **`parameters: Map<String, String>`** - 解析得到的命令参数
- **`activity: Activity?`** - 已解析的处理器（在 Match 阶段之前为 null）
- **`shouldProceed: Boolean`** - 是否应继续处理
- **`additionalContext: AdditionalContext`** - 额外上下文数据
- **`finish()`** - 提前结束处理

#### Stopping Processing Early

调用 `context.finish()` 可提前结束处理：

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.Validation) { context ->
    if (someCondition) {
        context.finish() // No further phases will execute
    }
}
```

#### Storing Custom Data

使用 `additionalContext` 在拦截器之间传递数据：

```kotlin
// In PreInvoke
context.additionalContext["userId"] = context.update.userOrNull?.id

// In PostInvoke
val userId = context.additionalContext["userId"] as? Long
```


### Multiple Interceptors

同一阶段可以注册多个拦截器。它们按注册顺序执行：

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

如果某个拦截器调用 `context.finish()`，该阶段后续的拦截器将被跳过，后续阶段也不会执行。


### Best Practices

#### 1. Use the Right Phase

- Setup: 全局检查、过滤、初始设置
- Parsing: 自定义解析逻辑
- Match: 处理器选择逻辑
- Validation: 权限、速率限制、守卫
- PreInvoke: 处理器特定的准备工作
- Invoke: 通常由默认拦截器处理
- PostInvoke: 清理、日志、错误处理

#### 2. Keep Interceptors Focused

每个拦截器应只做一件事：

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

拦截器不应导致机器人崩溃：

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

如果在 `PreInvoke` 中打开资源，需要在 `PostInvoke` 中清理：

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

按希望的执行顺序注册拦截器：

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

拦截器非常适合处理：
- ✅ 身份验证/授权
- ✅ 日志记录
- ✅ 指标/性能监控
- ✅ 速率限制
- ✅ 错误处理
- ✅ 请求/响应转换

对于处理器特定的逻辑，请保留在处理器内部。


### Default Interceptors

框架提供了以下默认拦截器以实现核心功能：

- **DefaultSetupInterceptor**: 全局速率限制
- **DefaultParsingInterceptor**: 命令解析
- **DefaultMatchInterceptor**: 处理器匹配（命令、输入、通用匹配器）
- **DefaultValidationInterceptor**: 守卫检查和每个处理器的速率限制
- **DefaultInvokeInterceptor**: 处理器执行和错误处理

您的自定义拦截器会与这些默认拦截器一起运行。您可以在默认拦截器之前或之后添加逻辑，但不能移除默认拦截器。

---

### Advanced: Conditional Interceptors

可以让拦截器有条件地执行：

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

拦截器为您的机器人提供了一种简洁的方式来添加横切逻辑：

- ✅ **七个阶段** 覆盖处理的不同阶段
- ✅ **简易 API**：实现 `PipelineInterceptor` 即可
- ✅ **灵活**：每个阶段可注册多个拦截器
- ✅ **强大**：可访问完整的处理上下文
- ✅ **安全**：可使用 `context.finish()` 提前结束处理

使用拦截器将共享关注点（如身份验证、日志、指标）集中管理，使处理器专注于业务逻辑。

---

### See also

* [Handlers (incl. Functional DSL)](Handlers.md) - Annotation- and DSL-based handler definition
* [Sessions](Sessions.md) - Per-chat / per-user state &amp; message tracking
* [Guards](Guards.md) - Handler-level permission checks
---