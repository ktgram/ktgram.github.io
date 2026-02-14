---
---
title: 봇 컨텍스트
---

<p align="center">
  <img src="https://github.com/user-attachments/assets/60bb58ae-1806-4b8d-8550-833b09c2b606" alt="Bot context diagram" />
</p>

봇은 `UserData` 및 `ClassData` 인터페이스를 통해 일부 데이터를 기억할 수 있는 기능을 제공할 수 있습니다.

- [`userData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-user-data/index.html)는 사용자 수준 데이터입니다.
- [`classData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-data/index.html)는 클래스 수준 데이터입니다. 즉, 사용자가 다른 클래스에 있는 명령이나 입력으로 이동할 때까지 데이터가 저장됩니다. (함수 모드에서는 사용자 데이터처럼 작동합니다)

기본적으로 구현은 [`ConcurrentHashMap`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.collections/java.util.concurrent.-concurrent-map/)을 통해 제공되지만, 원하는 데이터 저장 도구를 사용하여 [`UserData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-user-data/index.html) 및 [`ClassData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-data/index.html) 인터페이스를 통해 변경할 수 있습니다.


> [!CAUTION]
> 필요한 코드 생성 바인딩을 사용할 수 있도록 gradle `kspKotlin` 또는 관련 KSP 태스크를 실행하는 것을 잊지 마세요.


변경하려면 구현 아래에 `@CtxProvider` 어노테이션을 추가하고 gradle KSP 태스크(또는 빌드)를 실행하기만 하면 됩니다.

```kotlin
@CtxProvider
class MyRedis : UserData<String> {
    // ...
}
```

### 관련 항목

* [홈](https://github.com/vendelieu/telegram-bot/wiki)
* [업데이트 파싱](Update-parsing.md)
---