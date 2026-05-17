---
---
title: Activites And Processors
---

### Introduction

`Activity`는 이 라이브러리에서 `@CommandHandler`, `@InputHandler`, `@UnprocessedHandler`, `@CommonHandler`, `@UpdateHandler`, `@WizardHandler`와 같은 엔티티를 일반화한 추상 엔티티입니다.

또한 [handlers article](Handlers.md)를 확인하십시오.

### Collecting activities

Activities는 **컴파일 타임**에 **ktnip** KSP 프로세서에 의해 발견되고 연결됩니다. 예외는 하나뿐인데, `bot.setFunctionality { ... }`를 통해 정의된 핸들러는 런타임에 등록되는 [Functional DSL](Handlers#functional-dsl.md)입니다.

패키지를 검색할 영역을 제한하려면 플러그인에 매개변수를 전달할 수 있습니다:

```gradle
ktGram {
    packages = listOf("com.example.mybot")
}
```

또는 플러그인 없이 ksp를 통해:

```gradle
ksp {
    arg("package", "com.example.mybot")
}
```

이 경우, 수집된 액션이 올바르게 처리되도록 인스턴스 자체에도 패키지를 지정해야 합니다.

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.mybot")

    bot.handleUpdates()
    // start long-polling listener
}
```

여러 봇 인스턴스를 실행할 수 있도록 이 옵션이 추가되었습니다:

```gradle
ktGram {
    packages = listOf("com.example.mybot", "com.example.mybot2")
}
```


또는 플러그인을 사용하지 않고 다른 패키지를 지정하려면 `;` 구분자를 사용해야 합니다:

```gradle
ksp {
    arg("package", "com.example.mybot;com.example.mybot2")
}
```

### Processing

#### Webhooks

컨트롤러(또는 `webhook`이 처리되는 다른 위치)에서 다음을 호출합니다: [`bot.update.parseAndHandle(webhookString)`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.core/-tg-update-handler/index.html#706360827%2FFunctions%2F-880831646)

#### Long polling

`bot.handleUpdates()`를 호출하거나 `bot.update.setListener { handle(it) }`를 통해 호출합니다.

### See also

* [Update parsing](Update-parsing.md)
* [Activity invocation](Activity-invocation.md)
* [Actions](Actions.md)

---