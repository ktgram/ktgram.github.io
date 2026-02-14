---
---
title: 유용한 유틸리티와 팁
---


### ProcessedUpdate 작업

[`ProcessedUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processed-update/index.html)는 업데이트를 위한 제네릭 클래스로, 원본 데이터에 따라 다른 타입([`MessageUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-message-update/index.html), [`CallbackQueryUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-callback-query-update/index.html) 등)으로 제공될 수 있습니다.

따라서 들어오는 데이터의 타입을 확인하고 스마트캐스트를 통해 특정 데이터를 추가로 조작할 수 있습니다. 예를 들어:

```kotlin
// ...
if (update !is MessageUpdate) {
    message { "Only messages are allowed" }.send(user, bot)
    return
}
// 이후 ProcessedUpdate는 MessageUpdate로 인식됩니다.
```

내부에는 사용자 참조가 있는지 확인할 수 있는 [`UserReference`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-user-reference/index.html) 인터페이스도 있습니다. 사용 예시:

```kotlin
val user = if(update is UserReference) update.user else null

```

필요하다면 항상 원본 [`update`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types/-update/index.html)가 update 매개변수에 있습니다.


### 의존성 주입

라이브러리는 업데이트 처리 메서드가 제공된 어노테이션으로 표시된 클래스를 초기화하기 위해 간단한 메커니즘을 사용합니다.

[`ClassManagerImpl`](https://github.com/vendelieu/telegram-bot/blob/master/telegram-bot/src/commonMain/kotlin/eu/vendeli/tgbot/implementations/ClassManagerImpl.kt)는 기본적으로 어노테이션이 달린 메서드를 호출하는 데 사용됩니다.

하지만 다른 라이브러리를 사용하려면 [`ClassManager`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-manager/index.html) 인터페이스를 재정의하고<br/>선호하는 메커니즘을 사용한 후 봇 초기화 시 전달할 수 있습니다.

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.controllers") {
        classManager = ClassManagerImpl()
    }

    bot.handleUpdates()
}
```

### 업데이트 필터링

복잡한 조건이 필요하지 않다면 간단히 처리할 업데이트를 필터링할 수 있습니다:

```kotlin
// 업데이트 필터링 조건을 정의하는 함수
fun filteringFun(update: Update): Boolean = update.message?.text.isNullOrBlank()

fun main() = runBlocking {
  val bot = TelegramBot("BOT_TOKEN")

  // 업데이트에 대한 더 구체적인 처리 흐름 설정
  bot.update.setListener {
    if(filteringFun(it)) return@setListener

    // 따라서 리스너가 핸들러 함수에 도달하기 전에 범위를 벗어나면 필터링이 됩니다.
    // 실제로 직접 if-조건문을 작성하여 return@setListener을 사용하거나 필터링을 별도 클래스로 확장할 수도 있습니다.

    handle(it) // 또는 블록을 사용한 수동 처리 방법
  }
}
```

명령어 매칭 또는 제외 프로세스에 필터링을 포함하려면 guards 또는 `@CommonHandler`를 확인하세요.

### 다양한 메서드에 대한 옵션 일반화

동일한 선택적 매개변수를 자주 적용해야 한다면 사용자에게 맞는 유사한 함수를 작성하여 보일러플레이트 코드를 줄일 수 있습니다 :)

일반적인 속성 중 일부는 [다른 인터페이스](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.options/-options/index.html)로 분리되어 있습니다.

```kotlin
@Suppress("NOTHING_TO_INLINE")
inline fun <T, R, O> T.markdownMode(crossinline block: O.() -> Unit = {}): T
        where               T : TgAction<R>,
                            T : OptionsFeature<T, O>,
                            O : Options,
                            O : OptionsParseMode =
    options {
        parseMode = ParseMode.Markdown
        block()
    }


// ... 그리고 코드에서

message { "test" }.markdownMode().send(to, via)

```