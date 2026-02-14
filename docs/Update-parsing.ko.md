---
---
title: 업데이트 파싱
---

### 텍스트 페이로드

특정 업데이트는 추가 처리를 위해 파싱할 수 있는 텍스트 페이로드를 가질 수 있습니다. 살펴보겠습니다:

* `MessageUpdate` -> `message.text`
* `EditedMessageUpdate` -> `editedMessage.text`
* `ChannelPostUpdate` -> `channelPost.text`
* `EditedChannelPostUpdate` -> `editedChannelPost.text`
* `InlineQueryUpdate` -> `inlineQuery.query`
* `ChosenInlineResultUpdate` -> `chosenInlineResult.query`
* `CallbackQueryUpdate` -> `callbackQuery.data`
* `ShippingQueryUpdate` -> `shippingQuery.invoicePayload`
* `PreCheckoutQueryUpdate` -> `preCheckoutQuery.invoicePayload`
* `PollUpdate` -> `poll.question`
* `PurchasedPaidMediaUpdate` -> `purchasedPaidMedia.paidMediaPayload`

나열된 업데이트에서 특정 파라미터가 선택되어 [`TextReference`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-text-reference/index.html)로 가져와 추가 파싱을 위해 사용됩니다.

### 파싱

선택된 파라미터는 적절하게 구성된 구분자로 파싱되어 명령과 그에 대한 파라미터로 변환됩니다.

[`commandParsing`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.configuration/-bot-configuration/command-parsing.html) 구성 블록을 참조하세요.

아래 다이어그램에서 어떤 컴포넌트가 대상 함수의 어떤 부분에 매핑되는지 볼 수 있습니다.

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/7489099a-cca8-4049-a374-efaf6ce52128" alt="텍스트 파싱 다이어그램" />
</p>

### @ParamMapping

편의를 위해 또는 특별한 경우를 위해 [`@ParamMapping`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-param-mapping/index.html)이라는 어노테이션도 있습니다.

이 어노테이션을 통해 들어오는 텍스트에서 파라미터 이름을 어떤 파라미터에든 매핑할 수 있습니다.

예를 들어 `CallbackData`(64자)와 같이 들어오는 데이터가 제한적인 경우에도 편리합니다.

사용 예시:
`greeting?name=Adam`

```kotlin
@CommandHandler(["greeting"])
suspend fun greeting(@ParamMapping("name") anyParameterName: String, user: User, bot: TelegramBot) {
    message { "Hello, $anyParameterName" }.send(to = user, via = bot)
}
```

또한 파서가 파라미터 이름을 건너뛰거나 없도록 설정된 경우 이름 없는 파라미터를 캐치하는 데에도 사용할 수 있으며, 'param_n' 패턴으로 전달되는데 여기서 `n`은 순서입니다.

예를 들어 다음 텍스트 - `myCommand?p1=v1&v2&p3=&p4=v4&p5=`는 다음과 같이 파싱됩니다:
* 명령 - `myCommand`
* 파라미터
  * `p1` = `v1`
  * `param_2` = `v2`
  * `p3` = ``
  * `p4` = `v4`
  * `p5` = ``

보시다시피 두 번째 파라미터는 선언된 이름이 없으므로 `param_2`로 표현됩니다.

따라서 콜백에서 변수 이름을 축약하고 코드에서 명확하고 읽기 쉬운 이름을 사용할 수 있습니다.

### 딥링크

위의 정보를 고려할 때 start 명령에서 딥링크를 예상한다면 다음처럼 캐치할 수 있습니다:

```kotlin
@CommandHandler(["/start"])
suspend fun start(@ParamMapping("param_1") deeplink: String?, user: User, bot: TelegramBot) {
    message { "deeplink is $deeplink" }.send(to = user, via = bot)
}
```

### 그룹 명령

`commandParsing` 구성에서 [`useIdentifierInGroupCommands`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.configuration/-command-parsing-configuration/use-identifier-in-group-commands.html) 파라미터가 활성화되면 `TelegramBot.identifier`(설명된 파라미터를 사용하는 경우 이를 변경하는 것을 잊지 마세요)를 명령 일치 프로세스에서 사용할 수 있으며, 여러 봇 간에 유사한 명령을 분리하는 데 도움이 됩니다. 그렇지 않으면 `@MyBot` 부분은 단순히 건너뛰어집니다.

### 참고 자료

* [활동 호출](Activity-invocation.md)
* [활동 및 프로세서](Activites-and-Processors.md)
* [작업](Actions.md)