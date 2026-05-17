---
---
title: Guards
---

### Introduction
Guards는 봇을 개발하는 개발자에게 필수적인 기능입니다. 이러한 가드는 사전 실행 검사로 작동하여 특정 명령을 호출해야 하는지를 결정합니다. 이러한 검사를 구현함으로써 개발자는 봇의 기능, 보안 및 사용자 경험을 향상시킬 수 있습니다.

### Purpose of Activity Guards
활동 가드의 주요 목적은 권한이 있는 사용자 또는 특정 조건이 충족될 때만 활동이 트리거되도록 보장하는 것입니다.  

이를 통해 오용을 방지하고, 봇의 무결성을 유지하며, 상호 작용을 간소화할 수 있습니다.

### Common Use Cases
1. 인증 및 인가: 특정 사용자만 특정 명령에 접근하도록 보장합니다.  
2. 사전 조건 검사: 활동을 실행하기 전에 특정 조건이 만족되는지 확인합니다(예: 사용자가 특정 상태 또는 컨텍스트에 있는지 확인).  
3. 컨텍스트 가드: 현재 채팅 또는 사용자 상태에 기반하여 결정을 내립니다.

### Implementation Strategies
Telegram Command Guard를 구현하려면 일반적으로 각 가드의 논리를 캡슐화하는 함수 또는 메서드를 작성합니다. 아래는 일반적인 전략입니다.

1. User Role Check:
   - 명령을 실행하기 전에 사용자가 필요한 역할(예: admin, moderator)을 가지고 있는지 확인합니다.
      ```kotlin
       override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // Check if the user is an admin in the given chat
       }
      ```
   
2. State Verification:
   - 명령 실행을 허용하기 전에 사용자의 상태를 확인합니다.
     ```kotlin
     override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        return bot.userData[user.id, "data"] == requiredState
     }
     ```
   
3. Custom Guards:
   - 특정 요구 사항에 기반한 사용자 정의 논리를 작성합니다.
     ```kotlin
     override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // Custom logic to determine if the command should be executed
     }
     ```
   
### Integrating Guards with Activities
이러한 가드를 봇 명령에 통합하려면, 명령 핸들러가 호출되기 전에 조건을 확인하는 가드를 생성하면 됩니다.

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

- Modularity: 가드 로직을 모듈화하고 활동과 분리하십시오.
- Reusability: 다양한 명령/입력에 쉽게 적용할 수 있도록 재사용 가능한 가드 함수를 작성하십시오.
- Efficiency: 성능 오버헤드를 최소화하도록 가드 검사를 최적화하십시오.
- User Feedback: 가드에 의해 명령이 차단될 경우 사용자에게 명확한 피드백을 제공하십시오.

### Conclusion

Activity Guards는 봇 명령/입력 실행을 관리하는 강력한 도구입니다.  

견고한 가드 메커니즘을 구현함으로써 개발자는 봇이 안전하고 효율적으로 작동하도록 보장하고, 더 나은 사용자 경험을 제공할 수 있습니다.

### See also

* [Activities and Proccessors](Activites-and-Processors.md)
* [Update parsing](Update-parsing.md)
* [Actions](Actions.md)
* [Activity invocation](Activity-invocation.md)

---