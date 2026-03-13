---
---
title: 拦截器 (中间件)
---

### 拦截器：机器人的横切逻辑

构建 Telegram 机器人时，您经常需要在处理程序之间重复设置、检查或清理。拦截器允许您插入共享逻辑到处理程序周围，让处理程序保持专注和可维护。

以下是拦截器在 *telegram-bot* 中的工作原理以及如何使用它们。

### 什么是拦截器？(简单解释)

拦截器是在更新处理管道的特定点运行的函数。它们允许您：
- 检查和修改处理上下文
- 添加横切逻辑 (日志记录、认证、指标)
- 如果需要，提前停止处理
- 处理完成后清理资源

将拦截器视为在处理程序执行之前、期间和之后通过的检查点。

### 处理管道

机器人通过包含七个阶段的管道处理更新：

| 阶段 | 何时运行 | 用途 |
|-------|--------------|-------------------------|
| **设置** | 更新到达后立即，在任何处理之前 | ✔ 全局速率限制<br>✔ 过滤垃圾邮件或格式错误的更新<br>✔ 初始日志记录<br>✔ 设置共享上下文 |
| **解析** | 设置后，提取命令和参数 | ✔ 自定义命令解析<br>✔ 使用解析数据丰富上下文<br>✔ 验证更新结构 |
| **匹配** | 找到适当的处理程序 (Command/Input/Common) | ✔ 覆盖处理程序选择<br>✔ 自定义输入处理逻辑<br>✔ 记录匹配的处理程序 |
| **验证** | 找到处理程序后，调用之前 | ✔ 处理程序特定权限<br>✔ 每个处理程序的速率限制<br>✔ 守卫检查<br>✔ 条件不满足时取消处理 |
| **预调用** | 处理程序运行前立即 | ✔ 最后检查<br>✔ 启动计时器/指标<br>✔ 为处理程序丰富上下文<br>✔ 修改处理程序行为 |
| **调用** | 这里执行处理程序 | ✔ 包装处理程序执行<br>✔ 错误处理<br>✔ 记录处理程序结果 |
| **后调用** | 处理程序完成后 (成功或失败) | ✔ 清理资源<br>✔ 记录结果<br>✔ 在错误时发送回退消息<br>✔ 修改返回结果 |

### 创建拦截器

拦截器是接收 `ProcessingContext` 的简单函数：

```kotlin
import eu.vendeli.tgbot.core.PipelineInterceptor
import eu.vendeli.tgbot.types.component.ProcessingContext

val myInterceptor: PipelineInterceptor = { context ->
    // 在这里编写逻辑
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

### 注册拦截器

在处理管道上注册拦截器：

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

    // 为设置阶段注册拦截器
    bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
        // 检查用户是否被禁止
        val user = context.update.userOrNull
        if (user != null && isBanned(user.id)) {
            context.finish() // 停止处理
            return@intercept
        }
    }

    // 为预调用阶段注册拦截器
    bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
        val startTime = System.currentTimeMillis()
        // 存储开始时间
    }

    // 为后调用阶段注册拦截器
    bot.update.pipeline.intercept(ProcessingPipePhase.PostInvoke) { context ->
        val startTime = // 获取开始时间
        if (startTime != null) {
            val duration = System.currentTimeMillis() - startTime
            println("Handler took ${duration}ms")
        }
    }

    bot.handleUpdates()
}
```

### 实际示例：认证与指标

示例：一个需要认证才能使用某些命令的机器人，测量处理程序执行时间，并记录所有命令。

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

    // 设置阶段：检查用户是否已认证
    bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
        val user = context.update.userOrNull ?: return@intercept

        if (!isAuthenticated(user.id)) {
            message { "Please authenticate first using /login" }
                .send(user, context.bot)
            context.finish()
        }
    }

    // 预调用阶段：启动计时器并检查权限
    bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
        val activity = context.activity ?: return@intercept
        val user = context.update.userOrNull ?: return@intercept

        // 检查用户是否有权使用此特定处理程序
        if (!hasPermission(user.id, activity)) {
            message { "You don't have permission to use this command." }
                .send(user, context.bot)
            context.finish()
            return@intercept
        }

        // 启动计时器
        // 存储开始时间
    }

    // 后调用阶段：记录和清理
    bot.update.pipeline.intercept(ProcessingPipePhase.PostInvoke) { context ->
        val activity = context.activity ?: return@intercept
        val startTime = // 获取开始时间

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

`ProcessingContext` 提供以下内容的访问权限：

- **`update: ProcessedUpdate`** - 当前正在处理的更新
- **`bot: TelegramBot`** - 机器人实例
- **`registry: ActivityRegistry`** - 活动注册表
- **`parsedInput: String`** - 解析的命令/输入文本
- **`parameters: Map<String, String>`** - 解析的命令参数
- **`activity: Activity?`** - 已解析的处理程序 (在匹配阶段之前为 null)
- **`shouldProceed: Boolean`** - 处理是否应继续
- **`additionalContext: AdditionalContext`** - 额外上下文数据
- **`finish()`** - 提前停止处理

#### 提前停止处理

调用 `context.finish()` 停止处理：

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.Validation) { context ->
    if (someCondition) {
        context.finish() // 不会执行后续阶段
    }
}
```

#### 存储自定义数据

使用 `additionalContext` 在拦截器之间传递数据：

```kotlin
// 在预调用阶段
context.additionalContext["userId"] = context.update.userOrNull?.id

// 在后调用阶段
val userId = context.additionalContext["userId"] as? Long
```

### 多个拦截器

可以为同一阶段注册多个拦截器。它们按注册顺序执行：

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    println("First interceptor")
}

bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    println("Second interceptor")
}

// 处理更新时：
// 输出: "First interceptor"
// 输出: "Second interceptor"
```

如果某个拦截器调用 `context.finish()`，该阶段的后续拦截器会被跳过，后续阶段也不会执行。

### 最佳实践

#### 1. 使用正确的阶段

- 设置：全局检查、过滤、初始设置
- 解析：自定义解析逻辑
- 匹配：处理程序选择逻辑
- 验证：权限、速率限制、守卫
- 预调用：处理程序特定准备
- 调用：通常由默认拦截器处理
- 后调用：清理、日志记录、错误处理

#### 2. 保持拦截器专注

每个拦截器应该只做一件事：

```kotlin
// ✅ 好的 - 专注的拦截器
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    if (isBanned(context.update.userOrNull?.id)) {
        context.finish()
    }
}

// ❌ 避免 - 做太多事
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    // 认证
    // 日志记录
    // 指标
    // 速率限制
    // ... 太多！
}
```

#### 3. 优雅处理错误

拦截器不应该让机器人崩溃：

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
    try {
        // 您的逻辑
    } catch (e: Exception) {
        val logger = context.bot.config.loggerFactory.get("Interceptor")
        logger.error("Interceptor error", e)
        // 除非您想停止处理，否则不要调用 context.finish()
    }
}
```

#### 4. 清理资源

如果在预调用阶段打开资源，在后调用阶段清理：

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

#### 5. 顺序很重要

按您希望它们运行的顺序注册拦截器：

```kotlin
// 更一般的检查先执行
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) {
    // 全局禁止检查
}

// 更具体的检查后执行
bot.update.pipeline.intercept(ProcessingPipePhase.Validation) {
    // 处理程序特定权限检查
}
```

#### 6. 将拦截器用于横切关注点

拦截器非常适合：
- ✅ 认证/授权
- ✅ 日志记录
- ✅ 指标/性能监控
- ✅ 速率限制
- ✅ 错误处理
- ✅ 请求/响应转换

对于处理程序特定的逻辑，保持在处理程序中。

### 默认拦截器

框架包含核心功能默认拦截器：

- **DefaultSetupInterceptor**：全局速率限制
- **DefaultParsingInterceptor**：命令解析
- **DefaultMatchInterceptor**：处理程序匹配 (命令、输入、通用匹配器)
- **DefaultValidationInterceptor**：守卫检查和每个处理程序的速率限制
- **DefaultInvokeInterceptor**：处理程序执行和错误处理

您的自定义拦截器与这些默认值并行运行。您可以添加逻辑在默认值之前或之后，但不能移除默认拦截器。

---

### 高级：条件拦截器

您可以使拦截器有条件：

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
    val activity = context.activity ?: return@intercept

    // 只对特定处理程序应用
    if (activity::class.simpleName?.contains("Admin") == true) {
        // 管理员特定逻辑
        checkAdminPermissions(context)
    }
}
```

### 总结

拦截器提供了一种向机器人添加横切逻辑的干净方式：

- ✅ **七个阶段** 处理不同处理阶段
- ✅ **简单 API**：只需实现 `PipelineInterceptor`
- ✅ **灵活**：每个阶段可注册多个拦截器
- ✅ **强大**：访问完整的处理上下文
- ✅ **安全**：可通过 `context.finish()` 提前停止处理

使用拦截器让处理程序专注于业务逻辑，同时集中处理认证、日志记录和指标等共享关注点。

---

### 另请参阅

* [Functional Handling DSL](Functional-handling-DSL.md) - 函数式更新处理
* [Guards](Guards.md) - 处理程序级别权限检查
---