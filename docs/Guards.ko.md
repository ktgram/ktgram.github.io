---
---
title: Guards
---

### 소개
가드는 봇을 개발하는 개발자들을 위한 필수적인 기능입니다. 이 가드는 특정 명령이 실행되어야 하는지 여부를 결정하는 사전 실행 검사로 작동합니다. 이러한 검사를 구현함으로써 개발자들은 봇의 기능, 보안 및 사용자 경험을 향상시킬 수 있습니다.

### 액티비티 가드의 목적
액티비티 가드의 주요 목적은 오직 권한이 있는 사용자나 특정 조건만이 액티비티를 트리거하도록 보장하는 것입니다.

이는 오용을 방지하고, 봇의 무결성을 유지하며, 상호작용을 간소화할 수 있습니다.

### 일반적인 사용 사례
1. 인증 및 인가: 특정 사용자만 특정 명령에 접근할 수 있도록 보장합니다.
2. 사전 조건 검사: 명령을 실행하기 전에 특정 조건이 충족되는지 확인합니다(예: 사용자가 특정 상태나 컨텍스트에 있는지 확인).
3. 컨텍스트 가드: 현재 채팅이나 사용자 상태에 기반한 결정을 내립니다.

### 구현 전략
Telegram 명령 가드를 구현하는 것은 일반적으로 각 가드에 대한 로직을 캡슐화하는 함수를 작성하거나 메서드를 작성하는 것을 포함합니다. 아래는 일반적인 전략입니다:

1. 사용자 역할 확인:
   - 명령을 실행하기 전에 사용자가 필요한 역할(예: 관리자, 중재자)을 가지고 있는지 확인합니다.
      ```kotlin
       override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // 주어진 채팅에서 사용자가 관리자인지 확인
       }
      ```

2. 상태 확인:
   - 명령 실행을 허용하기 전에 사용자의 상태를 확인합니다.
     ```kotlin
     override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        return bot.userData[user.id, "data"] == requiredState
     }
     ```

3. 사용자 정의 가드:
   - 특정 요구사항에 기반한 사용자 정의 로직을 생성합니다.
     ```kotlin
     override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // 명령을 실행해야 하는지 여부를 결정하는 사용자 정의 로직
     }
     ```

### 액티비티와 가드 통합
이러한 가드를 봇 명령과 통합하려면 명령 핸들러가 호출되기 전에 이러한 조건을 확인하는 가드를 생성할 수 있습니다.

### 구현 예제

```kotlin
// 어딘가에 Guard 인터페이스를 구현하는 가드 클래스를 정의합니다
object YourGuard : Guard {
    override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // 여기에 조건을 작성합니다
    }
}

// ...

@CommandHandler(["yourCommand"])
@Guard(YourGuard::class) // InputHandler도 지원됩니다
fun command(bot: TelegramBot) {
   // 명령 본문
}
```

### 모범 사례

- 모듈성: 가드 로직을 모듈화하고 액티비티와 분리합니다.
- 재사용성: 다양한 명령/입력에 쉽게 적용할 수 있는 재사용 가능한 가드 함수를 작성합니다.
- 효율성: 성능 오버헤드를 최소화하기 위해 가드 검사를 최적화합니다.
- 사용자 피드백: 가드에 의해 명령이 차단될 때 사용자에게 명확한 피드백을 제공합니다.

### 결론

액티비티 가드는 봇 명령/입력 실행을 관리하기 위한 강력한 도구입니다.

견고한 가드 메커니즘을 구현함으로써 개발자들은 봇이 안전하고 효율적으로 작동하도록 보장할 수 있으며, 더 나은 사용자 경험을 제공할 수 있습니다.

### 참조

* [액티비티 및 프로세서](Activites-and-Processors.md)
* [업데이트 파싱](Update-parsing.md)
* [액션](Actions.md)
* [액티비티 호출](Activity-invocation.md)