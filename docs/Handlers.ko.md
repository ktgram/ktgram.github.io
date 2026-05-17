---
---
title: Handlers
---


### Variety of Handlers

봇 개발, 특히 사용자 상호 작용이 포함된 시스템에서는 명령과 이벤트를 효율적으로 관리하고 처리하는 것이 중요합니다.

이러한 어노테이션은 특정 명령, 입력 또는 업데이트를 처리하도록 설계된 함수를 표시하고, 명령 키워드, 스코프 및 가드와 같은 메타데이터를 제공합니다.

### Annotations Overview

#### CommandHandler

`CommandHandler` 어노테이션은 특정 명령을 처리하는 함수를 표시하는 데 사용됩니다. 이 어노테이션에는 명령의 키워드와 스코프를 정의하는 속성이 포함됩니다.

-   **value**: 명령과 연관된 키워드를 지정합니다.
-   **scope**: 명령이 검사될 컨텍스트 또는 스코프를 결정합니다.

```kotlin
@CommandHandler(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommandHandler.CallbackQuery

콜백 쿼리를 처리하기 위해 특별히 설계된 `CommandHandler` 어노테이션의 특수 버전입니다. `CommandHandler`와 유사한 속성을 가지고 있으며, 콜백 관련 명령에 초점을 맞춥니다.

_사실 `UpdateType.CALLBACK_QUERY` 스코프가 미리 설정된 `@CommandHandler`와 동일합니다_.

-   **value**: 명령과 연관된 키워드를 지정합니다.
-   **autoAnswer**: `callbackQuery`에 자동으로 응답합니다(`answerCallbackQuery`를 호출 후 처리).

```kotlin
@CommandHandler.CallbackQuery(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### CommonHandler

`CommonHandler` 어노테이션은 `CommandHandler` 및 `InputHandler`에 비해 우선순위가 낮은 명령을 처리하는 함수에 사용됩니다. 소스 레벨에서 사용되며, 일반 명령 핸들러를 유연하게 정의하는 방법을 제공합니다.

**주의, 우선순위는 `@CommonHandler` 내부에서만 작동합니다(다른 핸들러에는 영향을 주지 않음).**

##### CommonHandler.Text

업데이트와 텍스트 매칭을 지정하는 어노테이션입니다. 매칭 텍스트, 필터링 조건, 우선순위 및 스코프를 정의하는 속성을 포함합니다.

-   **value**: 들어오는 업데이트와 매칭할 텍스트.
-   **filter**: 매칭 과정에서 사용되는 조건을 정의하는 클래스.
-   **priority**: 핸들러의 우선순위 수준, 0이 가장 높은 우선순위.
-   **scope**: 텍스트 매칭이 검사될 컨텍스트 또는 스코프.

```kotlin
@CommonHandler.Text(["text"], filter = isNewUserFilter::class, priority = 10)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommonHandler.Regex

`CommonHandler.Text`와 유사하게 정규식을 기반으로 업데이트를 매칭하는 어노테이션입니다. 정규식 패턴, 옵션, 필터링 조건, 우선순위 및 스코프를 정의하는 속성을 포함합니다.

-   **value**: 매칭에 사용되는 정규식 패턴.
-   **options**: 정규식 패턴의 동작을 수정하는 옵션.
-   **filter**: 매칭 과정에서 사용되는 조건을 정의하는 클래스.
-   **priority**: 핸들러의 우선순위 수준, 0이 가장 높은 우선순위.
-   **scope**: 정규식 매칭이 검사될 컨텍스트 또는 스코프.

```kotlin
@CommonHandler.Regex("^\d+$", scope = [UpdateType.EDITED_MESSAGE])
suspend fun test(update: EditedMessageUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### InputHandler

`InputHandler` 어노테이션은 특정 입력 이벤트를 처리하는 함수를 표시합니다. 런타임에 입력을 처리하는 함수에 사용되며, 입력 키워드와 스코프를 정의하는 속성을 포함합니다.

-   **value**: 입력 이벤트와 연관된 키워드를 지정합니다.

```kotlin
@InputHandler("text")
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UnprocessedHandler

`UnprocessedHandler` 어노테이션은 다른 핸들러에 의해 처리되지 않은 업데이트를 처리하는 함수를 표시합니다. 이 핸들러 유형에 대해 하나의 처리 지점만 가능하도록 보장합니다.

```kotlin
@UnprocessedHandler
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UpdateHandler

`UpdateHandler` 어노테이션은 특정 유형의 들어오는 업데이트를 처리하는 함수를 표시합니다. 다양한 업데이트 유형을 체계적으로 분류하고 처리할 수 있는 방법을 제공합니다.

-   **type**: 핸들러 함수가 처리할 업데이트 유형을 지정합니다.
-   **messageKind** *(added in 9.5)*: [`MessageKind`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-message-kind/index.html) 중 선택적으로 지정하여, 감지된 종류와 일치하는 메시지 포함 업데이트만 디스패치합니다. 비어 있으면(기본) 모든 종류와 일치합니다.

```kotlin
@UpdateHandler([UpdateType.PRE_CHECKOUT_QUERY])
suspend fun test(update: PreCheckoutQueryUpdate, user: User, bot: TelegramBot) {
    //...
}
```

##### Filtering by `MessageKind`

`messageKind` 파라미터를 사용하여 특정 서브셋의 메시지 업데이트(사진, 텍스트, 서비스 이벤트 등)만 반응하도록 할 수 있습니다. 직접 nullable 필드를 검사할 필요가 없습니다:

```kotlin
@UpdateHandler(type = [UpdateType.MESSAGE], messageKind = [MessageKind.PHOTO])
suspend fun onPhoto(update: MessageUpdate, bot: TelegramBot) {
    //...
}
```
### Handler Companion Annotations

핸들러에 선택적으로 적용되는 추가 어노테이션이 있으며, 핸들러 자체의 선택적 동작을 보완합니다.

이들은 핸들러가 적용된 함수와 클래스 모두에 배치할 수 있으며, 클래스에 적용하면 해당 클래스의 모든 핸들러에 자동으로 적용됩니다. 필요에 따라 일부 함수에 대해 별도 동작을 지정할 수도 있습니다.

즉, 적용 우선순위는 `Function` > `Class`이며, 함수가 더 높은 우선순위를 가집니다.

#### Rate Limiting

또한 어노테이션에 설명된 속도 제한 메커니즘을 소개합니다.

사용자별 일반 제한을 설정할 수 있습니다:

```kotlin
// ...
val bot = TelegramBot("BOT_TOKEN") {
    rateLimiter { // general limits
        limits = RateLimits(period = 10000, rate = 5)
    }
}
```

###### Handler specific

특정 동작에 대한 제한은 `RateLimits` 어노테이션을 사용하여 정의할 수 있으며, `@CommandHandler`, `@CommandHandler.CallbackQuery`, `@InputHandler`, `@CommonHandler`를 지원합니다.

```kotlin
@CommandHandler(["/start"])
@RateLimits(period = 1000L, rate = 1L)
suspend fun start(user: User, bot: TelegramBot) {
    // ...
}
```

#### Guard

핸들러에 대한 접근을 제어하는 가드를 별도로 정의할 수 있으며, `@CommandHandler`, `@CommandHandler.CallbackQuery`, `@InputHandler`를 지원합니다:

```kotlin
@CommandHandler(["text"])
@Guard(isAdminGuard::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### ArgParser

핸들러에 대한 매개변수 파싱 동작을 변경하기 위해 커스텀 인자 파서를 별도로 정의할 수 있으며, `@CommandHandler`, `@CommandHandler.CallbackQuery`, `@CommonHandler`를 지원합니다:

```kotlin
@CommandHandler(["text"])
@ArgParser(SpaceArgParser::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

**see also [`defaultArgParser`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.common/default-arg-parser.html)**

### Functional DSL

위의 모든 어노테이션은 **Functional DSL**에서도 대응되는 형태를 가지며, `bot.setFunctionality { … }`를 통해 런타임에 핸들러를 선언하는 대안적인 방법을 제공합니다. 두 접근 방식은 동일한 `ActivityRegistry`를 공유하며, 같은 봇 안에서 자유롭게 혼합해 사용할 수 있습니다.

| Annotation | DSL counterpart |
|------------|-----------------|
| `@CommandHandler` | `onCommand(...)` |
| `@CommandHandler.CallbackQuery` | `onCommand(..., scope = [UpdateType.CALLBACK_QUERY])` |
| `@InputHandler` / input chains | `onInput(...)` / `inputChain(...)` |
| `@CommonHandler` | `common(...)` |
| `@UpdateHandler` | `onUpdate(...)` |
| `@UnprocessedHandler` | `whenNotHandled { ... }` |

Minimal example:

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

### Commands

```kotlin
bot.setFunctionality {
    // Regular command
    onCommand("/start") {
        message { "Hello" }.send(user, bot)
    }

    // Regex-based command matching
    onCommand("""(red|green|blue)""".toRegex()) {
        message { "you typed ${update.text} color" }.send(user, bot)
    }
}
```

`onCommand` 블록 내부에서는 파싱된 매개변수가 활성 `commandParsing` 설정에 의해 형태가 `Map<String, String>`인 형태로 제공됩니다.

### Inputs

```kotlin
bot.setFunctionality {
    onCommand("/start") {
        message { "Hello, what's your name?" }.send(user, bot)
        bot.inputListener[user] = "testInput"
    }

    onInput("testInput") {
        message { "Hey, nice to meet you, ${update.text}" }.send(user, bot)
    }
}
```

스토리지 API는 [`bot.inputListener`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot/-telegram-bot/input-listener.html)를 참고하세요.

#### Input chains

다단계 입력 흐름을 위해 `inputChain`을 사용합니다:

```kotlin
bot.setFunctionality {
    inputChain("conversation") {
        message { "Nice to meet you, ${update.text}" }.send(user, bot)
        message { "What is your favorite food?" }.send(user, bot)
    }.breakIf({ update.text == "peanut butter" }) {     // chain break condition
        message { "Oh, too bad, I'm allergic to it." }.send(user, bot)
    }.andThen {
        // next step when the break condition didn't match
        message { "Great choice!" }.send(user, bot)
    }
}
```

체인은 중단 조건이 일치하지 않는 한 자동으로 다음 단계로 진행됩니다; `repeat = true`(기본값)인 경우, 매칭되는 중단이 현재 단계에 머무르게 합니다.

> 보다 풍부한 다단계 흐름과 타입 상태 및 검증이 필요한 경우, [`@WizardHandler`](FSM-and-Conversation-handling.md)를 선호하십시오.

### Update type handlers

```kotlin
bot.setFunctionality {
    onUpdate(UpdateType.MESSAGE, UpdateType.CALLBACK_QUERY) {
        println("Received update: ${update.type}")
    }
}
```

### Common matchers

```kotlin
bot.setFunctionality {
    common("hello") {
        message { "Hi there!" }.send(user, bot)
    }

    common("""\d+""".toRegex()) {
        message { "You sent a number!" }.send(user, bot)
    }
}
```

### Fallback handler

```kotlin
bot.setFunctionality {
    whenNotHandled {
        message { "I didn't understand that." }.send(user, bot)
    }
}
```

### Companion options

Rate limits, guards, and argument parsers are passed directly as named parameters instead of separate annotations:

```kotlin
bot.setFunctionality {
    onCommand("/expensive", rateLimits = RateLimits(rate = 5, period = 60_000)) {
        message { "Processing..." }.send(user, bot)
    }

    onCommand("/admin", guard = AdminGuard::class) {
        message { "Admin command executed" }.send(user, bot)
    }

    onCommand("/custom", argParser = CustomArgParser::class) {
        message { "Parameters: $parameters" }.send(user, bot)
    }
}
```

### Combining DSL and annotations

두 스타일은 공존합니다 — 동일한 방식으로 등록하고, 동일한 방식으로 디스패치됩니다:

```kotlin
@CommandHandler(["/register"])
suspend fun register(user: User, bot: TelegramBot) {
    message { "Registration started" }.send(user, bot)
}

bot.setFunctionality {
    onCommand("/help") {
        message { "Available commands: /register, /help" }.send(user, bot)
    }
}
```

### Conclusion

이 어노테이션들은 명령, 입력 및 이벤트를 처리하기 위한 강력하고 유연한 도구를 제공하며, 속도 제한 및 가드와 같은 별도 구성을 허용하여 전체적인 구조와 유지 보수성을 향상시킵니다.

### See also

* [Activities & Processors](Activites-and-Processors.md)
* [Activity invocation](Activity-invocation.md)
* [FSM and Conversation handling](FSM-and-Conversation-handling.md)
* [Sessions](Sessions.md)
* [Update parsing](Update-parsing.md)

---