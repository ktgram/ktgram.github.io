---
---
title: Actions
---

### All requests is Actions
모든 Telegram API 요청은 다양한 [`TgAction`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.action/-tg-action/index.html) 인터페이스이며, 이는 [`SendMessageAction`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.api.message/-send-message-action/index.html)와 같은 다양한 메서드를 구현하며, 라이브러리 인터페이스의 편의를 위해 [`message()`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.api.message/message.html) 타입 함수 형태로 래핑되어 있습니다.

<p align="center">
    <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/2d097d60-1907-4ca1-8ad3-3ee8d223f8eb" alt="Actions diagram" />
</p>

각 `Action`은 사용 가능한 [`Feature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-feature/index.html)에 따라 고유의 가능한 메서드를 가질 수 있습니다.

### Features

다른 작업은 Telegram Bot API에 따라 다른 [`Features`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-feature/index.html)를 가질 수 있습니다. 예를 들어:
[`OptionsFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-options-feature/index.html),
[`MarkupFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-markup-feature/index.html)
[`EntitiesFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-entities-feature/index.html)
[`CaptionFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-caption-feature/index.html).

더 자세히 살펴보겠습니다:

### Options
예를 들어, [`OptionsFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-options-feature/index.html)는 선택적 매개변수를 전달하는 데 사용됩니다.

각 작업은 고유한 옵션 유형을 가지며, 해당 옵션은 `Action` 자체의 `options` 매개변수에서 속성 섹션에서 확인할 수 있습니다.<br/>예를 들어, `sendMessage`에는 다양한 옵션 매개변수가 있는 [`MessageOptions`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.options/-message-options/index.html) 데이터 클래스가 포함되어 있습니다.

사용 예시:

```kotlin
message{ "*Test*" }.options {
    parseMode = ParseMode.Markdown
}.send(user, bot)
```
### Markup

모든 종류의 [키보드](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.marker/-keyboard/index.html)를 지원하는 마크업을 보내는 메서드도 있습니다:<br/>[`ReplyKeyboardMarkup`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-reply-keyboard-markup/index.html), [`InlineKeyboardMarkup`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-inline-keyboard-markup/index.html), [`ForceReply`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-force-reply/index.html), [`ReplyKeyboardRemove`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-reply-keyboard-remove/index.html).

#### Inline Keyboard Markup

이 빌더를 사용하면 모든 조합의 매개변수로 인라인 버튼을 구성할 수 있습니다.

```kotlin
message{ "Test" }.inlineKeyboardMarkup {
    "name" callback "callbackData"         //
    "buttonName" url "https://google.com"  //--- 이 두 버튼은 동일한 행에 있습니다.
    newLine() // or br()
    "otherButton" webAppInfo "data"       // 다른 행에 있음

    // 빌더 내에서 다른 스타일도 사용할 수 있습니다:
    callbackData("buttonName") { "callbackData" }
}.send(user, bot)

```

자세한 내용은 빌더 [문서](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.builders/-inline-keyboard-markup-builder/index.html)에서 확인할 수 있습니다.

#### Reply Keyboard Markup

이 빌더를 사용하면 메뉴 버튼을 구성할 수 있습니다.

```kotlin
message{ "Test" }.replyKeyboardMarkup {
  + "Menu button"     // 단항 더하기 연산자를 사용하여 버튼 추가
  + "Menu button 2"
  br() // 두 번째 행으로 이동
  "Send polls 👀" requestPoll true   // 매개변수가 있는 버튼

  options {
    resizeKeyboard = true
  }
}.send(user, bot)
```

키보드에 적용 가능한 추가 옵션은 [`ReplyKeyboardMarkupOptions`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.options/-reply-keyboard-markup-options/index.html)에서 확인할 수 있습니다.

메서드에 대한 자세한 내용은 빌더 [문서](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.builders/-reply-keyboard-markup-builder/index.html)를 참조하세요.

키보드 마크업을 수집하기 위해 DSL을 사용하는 것이 가장 편리하지만, 필요하면 마크업을 수동으로 추가할 수도 있습니다.

```kotlin
message{ "*Test*" }.markup {
    InlineKeyboardMarkup(
        InlineKeyboardButton("test", callbackData = "testCallback")
    )
}.send(user, bot)

```

```kotlin
message{ "*Test*" }.markup {
    ReplyKeyboardMarkup(
        KeyboardButton("Test menu button")
    )
}.send(user, bot)
```

### Entities
[`MessageEntity`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.msg/-message-entity/index.html)를 보내는 메서드도 있습니다.

사용 예시:

```kotlin
message{ "Test \$hello" }.replyKeyboardMarkup {
    +"Test menu button"
}.entities {
    5 to 15 url "https://google.com" // TextLink 추가
    entity(EntityType.Bold, 0, 4)
    entity(EntityType.Cashtag, 5, 5) // 백슬래시는 컴파일러에 사용되므로 카운트되지 않음
}.send(user, bot)
```

#### Contextual entities.

엔터티는 일부 구문의 컨텍스트를 통해 추가할 수도 있으며, 이들은 특정 [EntitiesContextBuilder](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.builders/-entities-ctx-builder/index.html) 인터페이스로 표시됩니다. 이 인터페이스는 캡션 기능에도 존재합니다.

사용 예시:

```kotlin
message { "usual text " - bold { "this is bold text" } - " continue usual" }.send(user, bot)
```

모든 종류의 [엔터티 유형](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.msg/-entity-type/index.html)이 지원됩니다.

### Caption
또한 `caption` 메서드를 사용하여 미디어 파일에 캡션을 추가할 수 있습니다.

사용 예시:

```kotlin
photo { "FILE_ID" }.caption { "Test caption" }.send(user, bot)
```


### See also

* [Bot context](Bot-Context.md)
* [FSM | Conversation handling](FSM-and-Conversation-handling.md)