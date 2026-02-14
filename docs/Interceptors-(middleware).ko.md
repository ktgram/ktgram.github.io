---
---
title: 인터셉터 (미들웨어)
---

### 인터셉터: 봇을 위한 횡단 관심사

Telegram 봇을 구축할 때 핸들러 전반에 걸쳐 설정, 검사 또는 정리 작업을 반복하는 경우가 많습니다. 인터셉터를 사용하면 핸들러 주위에 공유 로직을 연결하여 핸들러를 집중적이고 유지보수가 용이하게 만들 수 있습니다.

*telegram-bot*에서 인터셉터가 작동하는 방식과 사용하는 방법은 다음과 같습니다.

### 인터셉터란? (간단한 설명)

인터셉터는 업데이트 처리 파이프라인의 특정 시점에서 실행되는 함수입니다. 다음을 할 수 있습니다:
- 처리 컨텍스트를 검사하고 수정
- 횡단 관심사 로직 추가 (로깅, 인증, 메트릭)
- 필요한 경우 처리를 일찍 중단
- 처리 후 리소스 정리

인터셉터를 모든 업데이트가 핸들러 실행 전, 중, 후에 통과하는 체크포인트로 생각해보세요.


### 처리 파이프라인

봇은 7단계 파이프라인을 통해 업데이트를 처리합니다:

| 단계 | 실행 시점 | 용도 |
|-------|--------------|-------------------------|
| **설정** | 처리 전, 업데이트가 도착하자마자 | ✔ 전역 속도 제한<br>✔ 스팸 또는 잘못된 업데이트 필터링<br>✔ 초기 로깅<br>✔ 공유 컨텍스트 설정 |
| **파싱** | 설정 후, 명령과 매개변수 추출 | ✔ 사용자 정의 명령 파싱<br>✔ 파싱된 데이터로 컨텍스트 보강<br>✔ 업데이트 구조 유효성 검사 |
| **매칭** | 적절한 핸들러 찾기 (명령/입력/일반) | ✔ 핸들러 선택 재정의<br>✔ 사용자 정의 입력 처리 로직<br>✔ 일치된 핸들러 로깅 |
| **검증** | 핸들러를 찾은 후, 호출 전 | ✔ 핸들러별 권한<br>✔ 핸들러별 속도 제한<br>✔ 가드 검사<br>✔ 조건이 충족되지 않으면 처리 취소 |
| **호출 전** | 핸들러가 실행되기 직전 | ✔ 마지막 순간 검사<br>✔ 타이머/메트릭 시작<br>✔ 핸들러를 위한 컨텍스트 보강<br>✔ 핸들러 동작 수정 |
| **호출** | 핸들러가 여기서 실행됨 | ✔ 핸들러 실행 감싸기<br>✔ 오류 처리<br>✔ 핸들러 결과 로깅 |
| **호출 후** | 핸들러 완료 후 (성공 또는 실패) | ✔ 리소스 정리<br>✔ 결과 로깅<br>✔ 오류 시 폴백 메시지 전송<br>✔ 반환 전 결과 수정 |


### 인터셉터 생성

인터셉터는 `ProcessingContext`를 받는 간단한 함수입니다:

```kotlin
import eu.vendeli.tgbot.core.PipelineInterceptor
import eu.vendeli.tgbot.types.component.ProcessingContext

val myInterceptor: PipelineInterceptor = { context ->
    // 여기에 로직 작성
    println("Processing update: ${context.update.updateId}")
}
```

또는 람다를 사용합니다:

```kotlin
val loggingInterceptor = PipelineInterceptor { context ->
    val logger = context.bot.config.loggerFactory.get("MyInterceptor")
    logger.info("Processing update #${context.update.updateId}")
}
```


### 인터셉터 등록

처리 파이프라인에 인터셉터를 등록합니다:

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")
    
    // 설정 단계에 인터셉터 등록
    bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
        // 사용자가 차단되었는지 확인
        val user = context.update.userOrNull
        if (user != null && isBanned(user.id)) {
            context.finish() // 처리 중단
            return@intercept
        }
    }
    
    // 호출 전 단계에 인터셉터 등록
    bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
        val startTime = System.currentTimeMillis()
        // 시작 시간 저장
    }
    
    // 호출 후 단계에 인터셉터 등록
    bot.update.pipeline.intercept(ProcessingPipePhase.PostInvoke) { context ->
        val startTime = // 시작 시간 가져오기
        if (startTime != null) {
            val duration = System.currentTimeMillis() - startTime
            println("Handler took ${duration}ms")
        }
    }
    
    bot.handleUpdates()
}
```

### 실제 사례: 인증 및 메트릭

예제: 특정 명령에 인증이 필요한 봇, 핸들러 실행 시간 측정, 모든 명령 로깅:

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")
    
    // 설정 단계: 사용자 인증 여부 확인
    bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
        val user = context.update.userOrNull ?: return@intercept
        
        if (!isAuthenticated(user.id)) {
            message { "Please authenticate first using /login" }
                .send(user, context.bot)
            context.finish()
        }
    }
    
    // 호출 전 단계: 타이머 시작 및 권한 확인
    bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
        val activity = context.activity ?: return@intercept
        val user = context.update.userOrNull ?: return@intercept
        
        // 이 핸들러에 대한 사용자 권한 확인
        if (!hasPermission(user.id, activity)) {
            message { "You don't have permission to use this command." }
                .send(user, context.bot)
            context.finish()
            return@intercept
        }
        
        // 타이머 시작
        // 시작 시간 저장
    }
    
    // 호출 후 단계: 로깅 및 정리
    bot.update.pipeline.intercept(ProcessingPipePhase.PostInvoke) { context ->
        val activity = context.activity ?: return@intercept
        val startTime = // 시작 시간 가져오기
        
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

`ProcessingContext`는 다음에 대한 액세스를 제공합니다:

- **`update: ProcessedUpdate`** - 현재 처리 중인 업데이트
- **`bot: TelegramBot`** - 봇 인스턴스
- **`registry: ActivityRegistry`** - 액티비티 레지스트리
- **`parsedInput: String`** - 파싱된 명령/입력 텍스트
- **`parameters: Map<String, String>`** - 파싱된 명령 매개변수
- **`activity: Activity?`** - 확인된 핸들러 (매칭 단계까지 null)
- **`shouldProceed: Boolean`** - 처리를 계속해야 하는지 여부
- **`additionalContext: AdditionalContext`** - 추가 컨텍스트 데이터
- **`finish()`** - 처리를 일찍 중단

#### 처리 일찍 중단

`context.finish()`를 호출하여 처리를 중단합니다:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.Validation) { context ->
    if (someCondition) {
        context.finish() // 더 이상 단계가 실행되지 않음
    }
}
```

#### 사용자 데이터 저장

인터셉터 간에 데이터를 전달하려면 `additionalContext`를 사용합니다:

```kotlin
// 호출 전에
context.additionalContext["userId"] = context.update.userOrNull?.id

// 호출 후에
val userId = context.additionalContext["userId"] as? Long
```


### 여러 인터셉터

같은 단계에 여러 인터셉터를 등록할 수 있습니다. 등록 순서대로 실행됩니다:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    println("First interceptor")
}

bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    println("Second interceptor")
}

// 업데이트가 처리될 때:
// 출력: "First interceptor"
// 출력: "Second interceptor"
```

인터셉터가 `context.finish()`를 호출하면 해당 단계의 후속 인터셉터가 건너뛰어지고 이후 단계는 실행되지 않습니다.


### 모범 사례

#### 1. 적절한 단계 사용

- 설정: 전역 검사, 필터링, 초기 설정
- 파싱: 사용자 정의 파싱 로직
- 매칭: 핸들러 선택 로직
- 검증: 권한, 속도 제한, 가드
- 호출 전: 핸들러별 준비
- 호출: 기본적으로 기본 인터셉터가 처리
- 호출 후: 정리, 로깅, 오류 처리

#### 2. 인터셉터 집중 유지

각 인터셉터는 한 가지 일만 해야 합니다:

```kotlin
// ✅ 좋음 - 집중된 인터셉터
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    if (isBanned(context.update.userOrNull?.id)) {
        context.finish()
    }
}

// ❌ 피해야 함 - 너무 많은 일을 함
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    // 인증
    // 로깅
    // 메트릭
    // 속도 제한
    // ... 너무 많음!
}
```

#### 3. 오류를 우아하게 처리

인터셉터는 봇을 중단시키면 안 됩니다:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
    try {
        // 로직
    } catch (e: Exception) {
        val logger = context.bot.config.loggerFactory.get("Interceptor")
        logger.error("Interceptor error", e)
        // 처리를 중단하려는 경우가 아니면 context.finish() 호출 안 함
    }
}
```

#### 4. 리소스 정리

`PreInvoke`에서 리소스를 열면 `PostInvoke`에서 정리합니다:

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

#### 5. 순서가 중요함

원하는 순서대로 인터셉터를 등록합니다:

```kotlin
// 더 일반적인 검사를 먼저
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { 
    // 전역 차단 확인
}

// 더 구체적인 검사를 나중에
bot.update.pipeline.intercept(ProcessingPipePhase.Validation) { 
    // 핸들러별 권한 확인
}
```

#### 6. 횡단 관심사에 인터셉터 사용

인터셉터는 다음에 적합합니다:
- ✅ 인증/인가
- ✅ 로깅
- ✅ 메트릭/성능 모니터링
- ✅ 속도 제한
- ✅ 오류 처리
- ✅ 요청/응답 변환

핸들러별 로직은 핸들러에 유지합니다.


### 기본 인터셉터

프레임워크에는 핵심 기능을 위한 기본 인터셉터가 포함되어 있습니다:

- **DefaultSetupInterceptor**: 전역 속도 제한
- **DefaultParsingInterceptor**: 명령 파싱
- **DefaultMatchInterceptor**: 핸들러 매칭 (명령, 입력, 일반 매처)
- **DefaultValidationInterceptor**: 가드 검사 및 핸들러별 속도 제한
- **DefaultInvokeInterceptor**: 핸들러 실행 및 오류 처리

사용자 정의 인터셉터는 이 기본값과 함께 실행됩니다. 기본값 전후에 로직을 추가할 수 있지만 기본 인터셉터를 제거할 수는 없습니다.

---

### 고급: 조건부 인터셉터

인터셉터를 조건부로 만들 수 있습니다:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
    val activity = context.activity ?: return@intercept
    
    // 특정 핸들러에만 적용
    if (activity::class.simpleName?.contains("Admin") == true) {
        // 관리자 전용 로직
        checkAdminPermissions(context)
    }
}
```


### 요약

인터셉터는 봇에 횡단 관심사 로직을 추가하는 깔끔한 방법을 제공합니다:

- ✅ **7단계** 처리의 다른 단계를 위한
- ✅ **간단한 API**: `PipelineInterceptor` 구현만 하면 됨
- ✅ **유연함**: 단계별 여러 인터셉터 등록 가능
- ✅ **강력함**: 전체 처리 컨텍스트에 액세스
- ✅ **안전함**: `context.finish()`로 처리를 일찍 중단할 수 있음

인터셉터를 사용하여 핸들러를 비즈니스 로직에 집중시키고 인증, 로깅, 메트릭 같은 공유 관심사를 중앙 집중식으로 처리하세요.

---

### 참고

* [Functional Handling DSL](Functional-handling-DSL.md) - 함수형 업데이트 처리
* [Guards](Guards.md) - 핸들러 수준 권한 확인
---