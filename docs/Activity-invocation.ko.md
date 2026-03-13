---
---
title: Activity Invocation
---

활동 호출 시, 대상 함수의 매개변수로 선언되어 있기 때문에 봇 컨텍스트를 전달할 수 있습니다.

전달할 수 있는 매개변수는 다음과 같습니다:

* [`ProcessedUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processed-update/index.html) (및 모든 하위 클래스) - 현재 처리 중인 업데이트.
* [`ProcessingContext`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processing-context/index.html) - 활동 처리의 저수준 컨텍스트.
* [`User`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types/-user/index.html) - 존재하는 경우.
* [`Chat`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.chat/-chat/index.html) - 존재하는 경우.
* [`TelegramBot`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot/-telegram-bot/index.html) - 현재 봇 인스턴스.

커스텀 타입을 전달하기 위해 추가하는 것도 가능합니다.

이렇게 하려면 [`Autowiring<T>`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.marker/-autowiring/index.html)를 구현하는 클래스를 추가하고 [`@Injectable`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-injectable/index.html) 어노테이션으로 표시하세요.

`Autowiring` 인터페이스를 구현한 후 - `T`는 대상 함수에서 전달할 수 있게 되고 인터페이스에 설명된 메서드를 통해 얻어집니다.

```kotlin
@Injectable
object UserResolver : Autowiring<UserRecord> {
    override suspend fun get(update: ProcessedUpdate, bot: TelegramBot): UserRecord? {
        return userRepository.getUserByTgId(update.user.id)
    }
}
```

함수에 선언된 다른 매개변수는 파싱된 매개변수에서 **검색**됩니다.

또한 전달되는 동안 파싱된 매개변수는 특정 타입으로 캐스팅될 수 있으며, 여기 그 목록이 있습니다:

- `String`
- `Integer`
- `Long`
- `Short`
- `Float`
- `Double`

또한, 매개변수가 선언되었지만 누락된 경우(또는 파싱된 매개변수에서 누락된 경우, 또는 예를 들어 `Update`에서 `User`가 누락된 경우) 또는 선언된 타입이 함수에서 받은 매개변수에 맞지 않는 경우 **`null`**이 전달되므로 주의하세요.

모든 것을 요약하면, 아래에는 함수 매개변수가 일반적으로 어떻게 형성되는지에 대한 예시가 있습니다:

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/3c1d7830-8e5d-45fb-82bb-ac63f08c3782" alt="Invokation process diagram" />
</p>

### See also

* [Update parsing](Update-parsing.md)
* [Activities & Processors](Activites-and-Processors.md)
---