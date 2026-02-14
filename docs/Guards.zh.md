---
---
title: Guards
---

### 介绍
Guards 是开发者创建机器人时的一项重要功能。这些 guards 作为执行前检查，用于确定是否应该调用特定命令。通过实施这些检查，开发者可以增强机器人的功能性、安全性和用户体验。

### Activity Guards 的目的
Activity Guards 的主要目的是确保只有授权用户或特定条件才能触发活动。

这可以防止滥用，维护机器人的完整性，并简化交互。

### 常见用例
1. 认证和授权：确保只有特定用户可以访问特定命令。
2. 前置条件检查：在执行活动之前验证是否满足某些条件（例如，确保用户处于特定状态或上下文中）。
3. 上下文 Guards：根据当前聊天或用户状态进行决策。

### 实现策略
实现 Telegram Command Guards 通常涉及编写封装每个 guard 逻辑的函数或方法。以下是常见策略：

1. 用户角色检查：
   - 确保用户具有执行命令所需的角色（例如，管理员、版主）之前执行命令。
      ```kotlin
       override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // 检查用户是否为给定聊天中的管理员
       }
      ```

2. 状态验证：
   - 在允许命令执行之前检查用户状态。
     ```kotlin
     override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        return bot.userData[user.id, "data"] == requiredState
     }
     ```

3. 自定义 Guards：
   - 根据特定需求创建自定义逻辑。
     ```kotlin
     override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // 自定义逻辑来确定是否应该执行命令
     }
     ```

### 将 Guards 与 Activities 集成
要将这些 Guards 与机器人命令集成，您可以创建一个 guard 来检查这些条件，然后再调用命令处理程序。

### 实现示例

```kotlin
// 在某个地方定义实现 Guard 接口的 guard 类
object YourGuard : Guard {
    override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // 在此处编写条件
    }
}

// ...

@CommandHandler(["yourCommand"])
@Guard(YourGuard::class) // 也支持 InputHandler
fun command(bot: TelegramBot) {
   // 命令主体
}
```

### 最佳实践

- 模块化：保持 guard 逻辑模块化并与 activities 分离。
- 可重用性：编写可重用的 guard 函数，可以轻松应用于不同的命令/输入。
- 效率：优化 guard 检查以最小化性能开销。
- 用户反馈：当命令被 guard 阻止时，向用户提供清晰的反馈。

### 结论

Activity Guards 是管理机器人命令/输入执行的强大工具。

通过实施强大的 guard 机制，开发者可以确保他们的机器人安全高效地运行，提供更好的用户体验。

### 另请参阅

* [Activities and Proccessors](Activites-and-Processors.md)
* [Update parsing](Update-parsing.md)
* [Actions](Actions.md)
* [Activity invocation](Activity-invocation.md)