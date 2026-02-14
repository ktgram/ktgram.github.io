---
---
title: Activites And Processors
---

### 소개

이 라이브러리 용어에서 `Activity`는 `@CommandHandler`, `@InputHandler`, `@UnprocessedHandler`, `@CommonHandler`와 같은 엔티티의 일반화된 추상 엔티티입니다.

[handlers 문서](Handlers.md)도 참조하세요.

### Activity 수집

Activity는 컴파일 타임에 모든 컨텍스트를 수집하고 준비합니다(함수형 DSL을 통해 정의된 것 제외).

패키지 검색 범위를 제한하려면 플러그인에 매개변수를 전달할 수 있습니다:

```gradle
ktGram {
    packages = listOf("com.example.mybot")
}
```

또는 ksp를 통해 플러그인 없이:

```gradle
ksp {
    arg("package", "com.example.mybot")
}
```

이 경우 수집된 작업들이 올바르게 처리되려면 인스턴스 자체에서도 패키지를 지정해야 합니다.

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.mybot")

    bot.handleUpdates()
    // 장기 폴링 리스너 시작
}
```

이 옵션은 여러 봇 인스턴스를 실행할 수 있도록 추가되었습니다:

```gradle
ktGram {
    packages = listOf("com.example.mybot", "com.example.mybot2")
}
```

또는 플러그인을 사용하지 않고 다른 패키지를 지정하려면 `;` 구분자로 지정해야 합니다:

```gradle
ksp {
    arg("package", "com.example.mybot;com.example.mybot2")
}
```

### 처리

#### 웹훅

컨트롤러(또는 웹훅이 처리되는 다른 장소)에서 다음을 호출합니다: [`bot.update.parseAndHandle(webhookString)`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.core/-tg-update-handler/index.html#706360827%2FFunctions%2F-880831646)

#### 장기 폴링

다음을 호출합니다: `bot.handleUpdates()` 또는 `bot.update.setListener { handle(it) }`를 통해

### 참조

* [업데이트 파싱](Update-parsing.md)
* [Activity 호출](Activity-invocation.md)
* [작업](Actions.md)