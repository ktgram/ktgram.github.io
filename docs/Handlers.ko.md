---
---
title: 핸들러
---


### 핸들러의 다양성

봇 개발, 특히 사용자 상호작용이 포함된 시스템에서 명령과 이벤트를 효율적으로 관리하고 처리하는 것은 매우 중요합니다.

이러한 어노테이션은 특정 명령, 입력 또는 업데이트를 처리하도록 설계된 함수를 표시하고 명령 키워드, 범위 및 가드와 같은 메타데이터를 제공합니다.

### 어노테이션 개요

#### CommandHandler

`CommandHandler` 어노테이션은 특정 명령을 처리하는 함수를 표시하는 데 사용됩니다. 이 어노테이션에는 명령의 키워드와 범위를 정의하는 속성이 포함되어 있습니다.

-   **value**: 명령과 관련된 키워드를 지정합니다.
-   **scope**: 명령이 확인될 컨텍스트 또는 범위를 결정합니다.

```kotlin
@CommandHandler(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommandHandler.CallbackQuery

`CommandHandler` 어노테이션의 특수한 버전으로, 콜백 쿼리를 처리하기 위해 특별히 설계되었습니다. 콜백 관련 명령에 초점을 맞춘 `CommandHandler`와 유사한 속성을 포함합니다.

_실제로는 미리 설정된 `UpdateType.CALLBACK_QUERY` 범위를 가진 단순한 `@CommandHandler`와 동일합니다_.

-   **value**: 명령과 관련된 키워드를 지정합니다.
-   **autoAnswer**: `callbackQuery`에 자동으로 응답합니다 (`answerCallbackQuery`를 처리하기 전에 호출합니다).


```kotlin
@CommandHandler.CallbackQuery(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### CommonHandler

`CommonHandler` 어노테이션은 `CommandHandler` 및 `InputHandler`에 비해 우선순위가 낮은 명령을 처리하는 함수에 사용됩니다. 소스 수준에서 사용되며 일반 명령 핸들러를 정의하는 유연한 방법을 제공합니다.

**`@CommonHandler` 자체 내에서만 우선순위가 작동한다는 점에 유의하세요(즉, 다른 핸들러에 영향을 주지 않습니다).**

##### CommonHandler.Text

이 어노테이션은 업데이트에 대한 텍스트 일치를 지정합니다. 일치하는 텍스트, 필터링 조건, 우선순위 및 범위를 정의하는 속성을 포함합니다.

-   **value**: 들어오는 업데이트와 일치할 텍스트입니다.
-   **filter**: 일치 프로세스에서 사용되는 조건을 정의하는 클래스입니다.
-   **priority**: 핸들러의 우선순위 수준으로, 0이 가장 높은 우선순위입니다.
-   **scope**: 텍스트 일치가 확인될 컨텍스트 또는 범위입니다.

```kotlin
@CommonHandler.Text(["text"], filter = isNewUserFilter::class, priority = 10)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommonHandler.Regex

`CommonHandler.Text`와 유사하게, 이 어노테이션은 정규표현식을 기반으로 업데이트를 일치시키는 데 사용됩니다. 정규표현식 패턴, 옵션, 필터링 조건, 우선순위 및 범위를 정의하는 속성을 포함합니다.

-   **value**: 일치에 사용되는 정규표현식 패턴입니다.
-   **options**: 정규표현식 패턴의 동작을 수정하는 정규표현식 옵션입니다.
-   **filter**: 일치 프로세스에서 사용되는 조건을 정의하는 클래스입니다.
-   **priority**: 핸들러의 우선순위 수준으로, 0이 가장 높은 우선순위입니다.
-   **scope**: 정규표현식 일치가 확인될 컨텍스트 또는 범위입니다.

```kotlin
@CommonHandler.Regex("^\d+$", scope = [UpdateType.EDITED_MESSAGE])
suspend fun test(update: EditedMessageUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### InputHandler

`InputHandler` 어노테이션은 특정 입력 이벤트를 처리하는 함수를 표시합니다. 런타임에 입력을 처리하는 함수에 사용되며 입력 키워드와 범위를 정의하는 속성을 포함합니다.

-   **value**: 입력 이벤트와 관련된 키워드를 지정합니다.

```kotlin
@InputHandler("text")
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UnprocessedHandler

`UnprocessedHandler` 어노테이션은 다른 핸들러에서 처리되지 않은 업데이트를 처리하는 함수를 표시하는 데 사용됩니다. 처리되지 않은 업데이트가 적절하게 관리되도록 하며, 이 핸들러 유형에 대해 하나의 처리 지점만 가능합니다.

```kotlin
@UnprocessedHandler
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UpdateHandler

`UpdateHandler` 어노테이션은 특정 유형의 들어오는 업데이트를 처리하는 함수를 표시합니다. 다양한 업데이트 유형을 체계적으로 분류하고 처리하는 방법을 제공합니다.

-   **type**: 핸들러 함수가 처리할 업데이트 유형을 지정합니다.

```kotlin
@UpdateHandler([UpdateType.PRE_CHECKOUT_QUERY])
suspend fun test(update: PreCheckoutQueryUpdate, user: User, bot: TelegramBot) {
    //...
}
```
### 핸들러 동반 어노테이션

핸들러 자체의 선택적 동작을 보완하는 추가 어노테이션도 있습니다.

이 어노테이션은 핸들러가 적용되는 함수와 클래스 모두에 배치할 수 있으며, 후자의 경우 해당 클래스의 모든 핸들러에 자동으로 적용되지만, 필요에 따라 일부 함수에 대해 별도의 동작을 가질 수 있습니다.

즉, 적용 우선순위는 `함수` > `클래스`이며, 함수가 더 높은 우선순위를 가집니다.

#### 속도 제한

또한 어노테이션에 설명된 속도 제한 메커니즘에 대해서도 설명하겠습니다.

각 사용자에 대한 일반적인 제한을 설정할 수 있습니다:

```kotlin
// ...
val bot = TelegramBot("BOT_TOKEN") {
    rateLimiter { // 일반 제한
        limits = RateLimits(period = 10000, rate = 5)
    }
}
```

###### 핸들러별 제한

특정 작업에 대한 제한은 `RateLimits` 어노테이션을 사용하여 정의할 수 있으며, `@CommandHandler`, `@CommandHandler.CallbackQuery`, `@InputHandler`, `@CommonHandler`에서 지원됩니다.

```kotlin
@CommandHandler(["/start"])
@RateLimits(period = 1000L, rate = 1L)
suspend fun start(user: User, bot: TelegramBot) {
    // ...
}
```

#### Guard

핸들러에 대한 액세스를 제어하기 위해 가드를 별도로 정의할 수 있으며, `@CommandHandler`, `@CommandHandler.CallbackQuery`, `@InputHandler`에서 지원됩니다:

```kotlin
@CommandHandler(["text"])
@Guard(isAdminGuard::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### ArgParser

핸들러에 대한 매개변수 구문 분석 동작을 변경하기 위해 사용자 정의 인수 파서를 별도로 정의할 수 있으며, `@CommandHandler`, `@CommandHandler.CallbackQuery`, `@CommonHandler`에서 지원됩니다:

```kotlin
@CommandHandler(["text"])
@ArgParser(SpaceArgParser::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

**[`defaultArgParser`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.common/default-arg-parser.html)도 참조하세요**

### 결론

이러한 어노테이션은 명령, 입력 및 이벤트를 처리하기 위한 강력하고 유연한 도구를 제공하며, 속도 제한 및 가드의 별도 구성을 허용하여 봇 개발의 전체적인 구조와 유지보수성을 향상시킵니다.

### 참고 자료

* [Activities & Processors](Activites-and-Processors.md)
* [Activity invocation](Activity-invocation.md)
* [FSM and Conversation handling](FSM-and-Conversation-handling.md)
* [Update parsing](Update-parsing.md)
* [Aide](Aide.md)

---