---
---
title: FSM 및 대화 처리
---

라이브러리는 또한 FSM(유한 상태 기계) 메커니즘을 지원합니다. 이는 잘못된 입력 처리를 통해 사용자 입력을 점진적으로 처리하는 메커니즘입니다.

> [!NOTE]
> TL;DR: 예제는 [여기](https://github.com/vendelieu/telegram-bot_template/tree/conversation)에서 확인하세요.

### 이론상

사용자 설문 조사를 수집해야 하는 상황을 상상해 보세요. 한 단계에서 사람의 모든 데이터를 요청할 수 있지만, 매개변수 중 하나의 입력이 잘못되면 사용자와 우리 모두에게 어려울 것이며, 특정 입력 데이터에 따라 각 단계가 다를 수 있습니다.

이제 단계별로 데이터를 입력하는 상황을 상상해 보세요. 봇이 사용자와 대화 모드로 들어갑니다.

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/2e84fa00-e59c-4352-8665-83be3b971e7b" alt="처리 과정 다이어그램" />
</p>

녹색 화살표는 오류 없이 단계를 전환하는 과정을 나타내고, 파란색 화살표는 현재 상태를 저장하고 재입력을 기다리는 것을 의미합니다(예: 사용자가 -100세라고 입력하면 다시 나이를 묻습니다), 빨간색 화살표는 모든 명령 또는 기타 의미 있는 취소로 인해 전체 프로세스를 종료하는 것을 보여줍니다.

### 실제 적용

Wizard 시스템은 Telegram 봇에서 다단계 사용자 상호작용을 가능하게 합니다. 사용자를 일련의 단계를 통해 안내하고, 입력을 검증하며, 상태를 저장하고, 단계 간에 전환합니다.

**주요 이점:**
- **타입 안전**: 상태 접근을 위한 컴파일 타임 타입 검사
- **선언적**: 중첩 클래스/객체로 단계 정의
- **유연성**: 조건부 전환, 점프 및 재시도 지원
- **상태 유지**: 플러그 가능한 저장소 백엔드를 통한 자동 상태 지속성
- **통합**: 기존 Activity 시스템과 통합

### 핵심 개념

#### WizardStep

`WizardStep`은 Wizard 흐름의 단일 단계를 나타냅니다. 각 단계는 다음을 구현해야 합니다:

- **`onEntry(ctx: WizardContext)`**: 사용자가 이 단계에 들어올 때 호출됩니다. 사용자에게 프롬프트를 표시하는 데 사용합니다.
- **`onRetry(ctx: WizardContext)`**: 검증이 실패하고 단계를 재시도해야 할 때 호출됩니다. 오류 메시지를 표시하는 데 사용합니다.
- **`validate(ctx: WizardContext): Transition`**: 현재 입력을 검증하고 다음에 무엇이 발생할지 나타내는 `Transition`을 반환합니다.
- **`store(ctx: WizardContext): Any?`** (선택 사항): 이 단계에 대해 지속할 값을 반환합니다. 단계가 상태를 저장하지 않으면 `null`을 반환합니다.

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
> 어떤 단계가 초기 단계로 표시되지 않으면 -> 첫 번째로 선언된 단계가 고려됩니다.

#### Transition

`Transition`은 검증 후 무엇이 발생할지 결정합니다:

- **`Transition.Next`**: 순서상 다음 단계로 이동
- **`Transition.JumpTo(step: KClass<out WizardStep>)`**: 특정 단계로 점프
- **`Transition.Retry`**: 현재 단계를 재시도(검증 실패)
- **`Transition.Finish`**: Wizard 완료

```kotlin
// 입력에 따른 조건부 점프
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

`WizardContext`는 다음에 대한 접근을 제공합니다:
- **`user: User`**: 현재 사용자
- **`update: ProcessedUpdate`**: 현재 업데이트
- **`bot: TelegramBot`**: 봇 인스턴스
- **`userReference: UserChatReference`**: 상태 저장을 위한 사용자 및 채팅 ID 참조

KSP에 의해 생성된 타입 안전 상태 접근 메서드가 추가됩니다.

---

### Wizard 정의

#### 기본 구조

Wizard는 `@WizardHandler` 어노테이션이 달린 클래스 또는 객체로 정의됩니다:

```kotlin
@WizardHandler(trigger = ["/survey"])
object SurveyWizard {
    object NameStep : WizardStep(isInitial = true) {
        // ... 단계 구현
    }
    
    object AgeStep : WizardStep {
        // ... 단계 구현
    }
    
    object FinishStep : WizardStep {
        // ... 단계 구현
    }
}
```

#### 어노테이션 매개변수

**`@WizardHandler`**는 다음을 허용합니다:
- **`trigger: Array<String>`**: Wizard를 시작하는 명령(예: `["/start", "/survey"]`)
- **`scope: Array<UpdateType>`**: 수신할 업데이트 유형(기본값: `[UpdateType.MESSAGE]`)
- **`stateManagers: Array<KClass<out WizardStateManager<*>>>`**: 단계 데이터를 저장하기 위한 상태 관리자 클래스

---

### 상태 관리

#### WizardStateManager

상태는 `WizardStateManager<T>` 구현을 사용하여 저장됩니다. 각 관리자는 특정 타입을 처리합니다:

```kotlin
interface WizardStateManager<T : Any> {
    suspend fun get(key: KClass<out WizardStep>, reference: UserChatReference): T?
    suspend fun set(key: KClass<out WizardStep>, reference: UserChatReference, value: T)
    suspend fun del(key: KClass<out WizardStep>, reference: UserChatReference)
}
```

다음도 참조하세요: [MapStateManager<T>](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-state-manager/index.html), [MapStringStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-string-state-manager/index.html), [MapIntStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-int-state-manager/index.html), [MapLongStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-long-state-manager/index.html).

#### 자동 매칭

KSP는 `store()` 반환 타입에 따라 단계를 상태 관리자와 매칭합니다:

```kotlin
@WizardHandler(
    trigger = ["/survey"],
    stateManagers = [StringStateManager::class, IntStateManager::class]
)
object SurveyWizard {
    object NameStep : WizardStep(isInitial = true) {
        override suspend fun store(ctx: WizardContext): String {
            return ctx.update.text!! // StringStateManager와 매칭
        }
    }
    
    object AgeStep : WizardStep {
        override suspend fun store(ctx: WizardContext): Int {
            return ctx.update.text!!.toInt() // IntStateManager와 매칭
        }
    }
}
```

#### 단계별 재정의

`@WizardHandler.StateManager`를 사용하여 특정 단계의 상태 관리자를 재정의합니다:

```kotlin
@WizardHandler(
    trigger = ["/survey"],
    stateManagers = [DefaultStateManager::class]
)
object SurveyWizard {
    object NameStep : WizardStep(isInitial = true) {
        // DefaultStateManager 사용
    }
    
    @WizardHandler.StateManager(CustomStateManager::class)
    object AgeStep : WizardStep {
        // CustomStateManager 사용
    }
}
```

---

### 타입 안전 상태 접근

KSP는 상태를 저장하는 각 단계에 대해 `WizardContext`에서 타입 안전 확장 함수를 생성합니다.

#### 생성된 함수

`String`을 저장하는 단계의 경우:

```kotlin
// KSP에 의해 자동으로 생성됨
suspend inline fun <reified S : WizardStep> WizardContext.getState(): String?
suspend inline fun <reified S : WizardStep> WizardContext.setState(value: String)
suspend inline fun <reified S : WizardStep> WizardContext.delState()
```

#### 사용법

```kotlin
object FinishStep : WizardStep {
    override suspend fun onEntry(ctx: WizardContext) {
        // 타입 안전 접근 - String? (nullable) 반환
        val name: String? = ctx.getState<NameStep>()
        
        // 타입 안전 접근 - Int? (nullable) 반환
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

#### 폴백 메서드

타입 안전 메서드를 사용할 수 없는 경우 폴백 메서드를 사용하세요:

```kotlin
// 폴백 - Any? 반환
val name = ctx.getState(NameStep::class)

// 폴백 - Any 허용
ctx.setState(NameStep::class, "John")
ctx.delState(NameStep::class)
```

---

### 전체 예제

#### 사용자 등록 Wizard

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
            // 타입 안전 상태 접근
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
                "no" -> Transition.JumpTo(NameStep::class) // 처음부터 다시 시작
                else -> Transition.Retry
            }
        }
    }
    
    object FinishStep : WizardStep {
        override suspend fun onEntry(ctx: WizardContext) {
            val name: String? = ctx.getState<NameStep>()
            val age: Int? = ctx.getState<AgeStep>()
            
            // 데이터베이스에 저장, 확인 메시지 전송 등
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

### 고급 기능

#### 조건부 전환

조건부 흐름에 `Transition.JumpTo`를 사용하세요:

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

#### 상태 없는 단계

단계는 상태를 저장할 필요가 없습니다. 단순히 `store()`에서 `null`을 반환하세요(또는 그대로 유지):

```kotlin
object ConfirmationStep : WizardStep {
    override suspend fun store(ctx: WizardContext): Any? = null
    // ... 나머지 구현
}
```

#### 사용자 정의 상태 관리자

사용자 정의 저장소(데이터베이스, Redis 등)를 위해 `WizardStateManager<T>`를 구현하세요:

```kotlin
class DatabaseStateManager : WizardStateManager<String> {
    override suspend fun get(
        key: KClass<out WizardStep>,
        reference: UserChatReference
    ): String? {
        // 데이터베이스에서 로드
        return database.getWizardState(reference.userId, key.qualifiedName)
    }
    
    override suspend fun set(
        key: KClass<out WizardStep>,
        reference: UserChatReference,
        value: String
    ) {
        // 데이터베이스에 저장
        database.saveWizardState(reference.userId, key.qualifiedName, value)
    }
    
    override suspend fun del(
        key: KClass<out WizardStep>,
        reference: UserChatReference
    ) {
        // 데이터베이스에서 삭제
        database.deleteWizardState(reference.userId, key.qualifiedName)
    }
}
```

---

### 내부 동작 방식

#### 코드 생성

KSP는 다음을 생성합니다:

1. **WizardActivity**: `WizardActivity`를 확장하는 구체적인 구현과 하드코딩된 단계
2. **시작 Activity**: 명령 트리거를 처리하고 Wizard를 시작
3. **입력 Activity**: Wizard 흐름 중 사용자 입력 처리
4. **상태 접근자**: 상태 접근을 위한 타입 안전 확장 함수

#### 흐름

1. 사용자가 `/register` 전송 → 시작 Activity가 호출됨
2. 시작 Activity가 `WizardContext`를 생성하고 `wizardActivity.start(ctx)` 호출
3. `start()`가 초기 단계에 진입하고 현재 단계를 추적하기 위해 `inputListener` 설정
4. 사용자가 메시지 전송 → 입력 Activity가 호출됨
5. 입력 Activity가 `wizardActivity.handleInput(ctx)` 호출
6. `handleInput()`이 입력을 검증하고 상태를 지속하며 다음 단계로 전환
7. `Transition.Finish`가 반환될 때까지 프로세스 반복

#### 상태 지속성

- 검증 성공 후 상태가 지속됨(전환 전)
- 각 단계의 `store()` 반환 값이 일치하는 `WizardStateManager`를 사용하여 저장됨
- 상태는 사용자 및 채팅별로 범위가 지정됨(`UserChatReference`)

---

### 모범 사례

#### 1. 항상 명확한 프롬프트 제공

```kotlin
override suspend fun onEntry(ctx: WizardContext) {
    message { 
        "Please enter your email address:\n" +
        "(Format: user@example.com)" 
    }.send(ctx.user, ctx.bot)
}
```

#### 2. 검증 오류를 우아하게 처리

```kotlin
override suspend fun onRetry(ctx: WizardContext) {
    message { 
        "Invalid email format. Please try again.\n" +
        "Example: user@example.com" 
    }.send(ctx.user, ctx.bot)
}
```

#### 3. 타입 안전 상태 접근 사용

생성된 타입 안전 메서드를 선호하세요:

```kotlin
// ✅ 좋음 - 타입 안전
val name: String? = ctx.getState<NameStep>()

// ❌ 피하세요 - 타입 안전성 상실
val name = ctx.getState(NameStep::class) as? String
```

#### 4. 단계를 집중적으로 유지

각 단계는 단일 책임을 가져야 합니다:

```kotlin
// ✅ 좋음 - 집중된 단계
object EmailStep : WizardStep {
    // 이메일 수집만 처리
}

// ❌ 피하세요 - 너무 많은 로직
object PersonalInfoStep : WizardStep {
    // 이름, 이메일, 전화번호, 주소 등 처리...
}
```

#### 5. 의미 있는 단계 이름 사용

```kotlin
// ✅ 좋음
object EmailVerificationStep : WizardStep

// ❌ 피하세요
object Step2 : WizardStep
```

#### 6. 필요할 때 상태 정리

상태를 수동으로 지워야 할 경우:

```kotlin
object CancelStep : WizardStep {
    override suspend fun onEntry(ctx: WizardContext) {
        // 모든 Wizard 상태 지우기
        ctx.delState<NameStep>()
        ctx.delState<AgeStep>()
        
        message { "Registration cancelled." }.send(ctx.user, ctx.bot)
    }
}
```

---

### 요약

Wizard 시스템은 다음을 제공합니다:
- ✅ **타입 안전** 상태 관리와 컴파일 타임 검사
- ✅ **선언적** 중첩 클래스로 단계 정의
- ✅ **유연한** 조건부 논리로 전환
- ✅ **자동** KSP를 통한 코드 생성
- ✅ **통합된** 기존 Activity 시스템
- ✅ **플러그 가능한** 상태 저장소 백엔드

`@WizardHandler`로 클래스에 어노테이션을 추가하고 중첩된 `WizardStep` 객체로 단계를 정의하여 Wizard 구축을 시작하세요!
질문이 있으면 채팅에서 문의하세요. 도와드리겠습니다 :)
---