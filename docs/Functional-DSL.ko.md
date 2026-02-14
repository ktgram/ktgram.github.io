---
---
title: 함수형 DSL
---

### ~~무한대~~ 함수형 DSL와 그 너머로!

봇은 어노테이션 기반과 함수형 DSL 컨텍스트 설정 모두를 지원합니다. 두 접근 방식을 결합할 수 있습니다.

### 함수형 DSL

함수형 DSL은 봇 컨텍스트를 정의하는 다른 방법일 뿐입니다.

예제:

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

    bot.setFunctionality {
        onChosenInlineResult {
            println("got a result ${update.chosenInlineResult.resultId} from ${update.user}")
        }
    }
}
```

### 명령어와 입력

함수형 DSL을 사용하여 `명령어`와 `입력`을 모두 처리할 수 있습니다.

#### 명령어

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

    bot.setFunctionality {
        // 일반 명령어
        onCommand("/start") {
            message { "Hello" }.send(user, bot)
        }
        
        // 정규식 기반 명령어 매칭
        onCommand("""(red|green|blue)""".toRegex()) {
            message { "you typed ${update.text} color" }.send(user, bot)
        }
    }
}
```

`onCommand`에서 파싱된 매개변수는 구성에 따라 `Map<String, String>`으로 사용할 수 있습니다.

#### 입력

[`bot.inputListener`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot/-telegram-bot/input-listener.html)를 통해 입력을 사용할 수 있습니다.

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

    bot.setFunctionality {
        onCommand("/start") {
            message { "Hello, what's your name?" }.send(user, bot)
            bot.inputListener[user] = "testInput"
        }
        
        onInput("testInput") {
            message { "Hey, nice to meet you, ${update.text}" }.send(user, bot)
        }
    }
}
```

#### 입력 체인

다단계 입력 흐름의 경우 `inputChain`을 사용하세요:

```kotlin
bot.setFunctionality {
    inputChain("conversation") {
        message { "Nice to meet you, ${update.text}" }.send(user, bot)
        message { "What is your favorite food?" }.send(user, bot)
    }.breakIf({ update.text == "peanut butter" }) { // 체인 중단 조건
        message { "Oh, too bad, I'm allergic to it." }.send(user, bot)
        // 조건이 일치할 때 적용될 작업
    }.andThen {
        // 중단 조건이 일치하지 않으면 다음 입력 지점
        message { "Great choice!" }.send(user, bot)
    }
}
```

체인은 중단 조건이 충족되지 않는 한 자동으로 다음 단계로 진행됩니다. 중단 조건이 일치하고 `repeat`이 `true`(기본값)이면 사용자는 현재 단계에 머무릅니다.

#### 업데이트 타입 핸들러

특정 업데이트 타입을 직접 처리합니다:

```kotlin
bot.setFunctionality {
    onUpdate(UpdateType.MESSAGE, UpdateType.CALLBACK_QUERY) {
        // 메시지와 콜백 쿼리 업데이트 모두 처리
        println("Received update: ${update.type}")
    }
}
```

#### 일반 매처

`common`을 사용하여 텍스트 내용(명령어뿐만 아니라)을 매칭합니다:

```kotlin
bot.setFunctionality {
    // 문자열 매칭
    common("hello") {
        message { "Hi there!" }.send(user, bot)
    }
    
    // 정규식 매칭
    common("""\d+""".toRegex()) {
        message { "You sent a number!" }.send(user, bot)
    }
}
```

#### 폴백 핸들러

어떤 핸들러에서도 처리되지 않은 업데이트를 처리합니다:

```kotlin
bot.setFunctionality {
    whenNotHandled {
        message { "I didn't understand that." }.send(user, bot)
    }
}
```

### 고급 설정

#### 속도 제한

어떤 핸들러에도 속도 제한을 적용합니다:

```kotlin
bot.setFunctionality {
    onCommand("/expensive", rateLimits = RateLimits(5, 60)) {
        // 이 명령어는 60초당 최대 5회만 호출할 수 있습니다
        message { "Processing..." }.send(user, bot)
    }
}
```

#### 가드

가드를 사용하여 커스텀 유효성 검사 로직을 추가합니다:

```kotlin
bot.setFunctionality {
    onCommand("/admin", guard = AdminGuard::class) {
        message { "Admin command executed" }.send(user, bot)
    }
}
```

#### 인수 파싱

명령어 인수를 파싱하는 방법을 커스터마이즈합니다:

```kotlin
bot.setFunctionality {
    onCommand("/custom", argParser = CustomArgParser::class) {
        // 매개변수는 CustomArgParser를 사용하여 파싱됩니다
        message { "Parameters: $parameters" }.send(user, bot)
    }
}
```

### 함수형과 어노테이션 기반 설정 결합

두 접근 방식을 같은 봇에서 사용할 수 있습니다:

```kotlin
// 어노테이션 기반 핸들러
@CommandHandler(["/register"])
suspend fun register(ctx: CommandContext) {
    message { "Registration started" }.send(ctx.user, ctx.bot)
}

// 함수형 핸들러
bot.setFunctionality {
    onCommand("/help") {
        message { "Available commands: /register, /help" }.send(user, bot)
    }
}
```

두 핸들러 모두 같은 `ActivityRegistry`에 등록되며 원활하게 함께 작동합니다.

### 참고

* [Action](Actions.md)
* [유용한 유틸리티](Useful-utilities-and-tips.md)
---