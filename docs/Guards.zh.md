---
---
title: Guards
---

### Introduction
Guards 是开发者创建机器人时的一个重要特性。这些 guard 充当执行前的检查，决定是否应调用特定命令。通过实现这些检查，开发者可以提升机器人功能、安全性和用户体验。

### Purpose of Activity Guards
活动 guard 的主要目的是确保只有授权用户或满足特定条件时才会触发活动。

这可以防止滥用，维护机器人的完整性，并简化交互流程。

### Common Use Cases
1. 身份验证与授权：确保只有特定用户能够访问特定命令。  
2. 前置条件检查：在执行活动之前验证某些条件是否满足（例如，确保用户处于特定状态或上下文）。  
3. 上下文 guard：根据当前聊天或用户状态作出决策。

### Implementation Strategies
实现 Telegram 命令 guard 通常涉及编写函数或方法来封装每个 guard 的逻辑。以下是常见策略：

1. User Role Check:
   - 在执行命令之前确保用户拥有所需角色（例如，admin、moderator）。
      ```kotlin
       override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // Check if the user is an admin in the given chat
       }
      ```
   
2. State Verification:
   - 在允许命令执行之前检查用户的状态。
     ```kotlin
     override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        return bot.userData[user.id, "data"] == requiredState
     }
     ```
   
3. Custom Guards:
   - 根据具体需求创建自定义逻辑。
     ```kotlin
     override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // Custom logic to determine if the command should be executed
     }
     ```
   
### Integrating Guards with Activities
要将这些 guard 与机器人命令集成，可以创建一个在命令处理器被调用前检查这些条件的 guard。

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

- Modularity: 将 guard 逻辑保持模块化并与活动分离。  
- Reusability: 编写可在不同命令/输入之间轻松复用的 guard 函数。  
- Efficiency: 优化 guard 检查以最小化性能开销。  
- User Feedback: 当命令被 guard 阻止时，向用户提供明确的反馈。

### Conclusion

Activity Guards 是管理机器人命令/输入执行的强大工具。

通过实现健壮的 guard 机制，开发者可以确保机器人安全高效运行，提供更好的用户体验。

### See also

* [Activities and Proccessors](Activites-and-Processors.md)
* [Update parsing](Update-parsing.md)
* [Actions](Actions.md)
* [Activity invocation](Activity-invocation.md)

---