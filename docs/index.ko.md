---
---
title: 홈
---

### 소개
라이브러리가 일반적으로 업데이트를 처리하는 방법에 대한 아이디어를 얻어봅시다:

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/442cc5f1-0256-425a-9f25-185fdd49fe0a" alt="처리 프로세스 다이어그램" />
</p>

업데이트를 수신한 후, 라이브러리는 세 가지 주요 단계를 수행합니다.

### 처리

처리는 수신된 업데이트를 전달된 페이로드에 따라 [`ProcessedUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processed-update/index.html)의 적절한 하위 클래스로 다시 패키징하는 과정입니다.

이 단계는 업데이트를 더 쉽게 처리하고 처리 기능을 확장할 수 있도록 필요합니다.

### 처리

다음은 주요 단계로, 여기서 실제 처리가 이루어집니다.

### 전역 RateLimiter

업데이트에 사용자가 있는 경우, 전역 RateLimiter를 초과했는지 확인합니다.

### 텍스트 파싱

다음으로, 페이로드에 따라 텍스트를 포함하는 특정 업데이트 컴포넌트를 가져와 설정에 따라 파싱합니다.

더 자세한 내용은 [업데이트 파싱 문서](Update-parsing.md)를 참조하세요.

### 액티비티 찾기

처리 우선순위에 따라:

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/6178c410-9b9e-4045-9f03-4791b3f49894" alt="처리 우선순위 다이어그램" />
</p>

파싱된 데이터와 우리가 처리하는 액티비티 간의 일치 항목을 찾습니다.
우선순위 다이어그램에서 볼 수 있듯이, `Commands`가 항상 먼저 옵니다.

즉, 업데이트의 텍스트 로드가 어떤 명령과 일치하는 경우, 더 이상 `Inputs`, `Common`을 검색하거나 물론 `Unprocessed` 작업을 실행하지 않습니다.

유일한 예외는 `UpdateHandlers`가 병렬로 트리거된다는 점입니다.

#### Commands

명령과 그 처리에 대해 자세히 살펴봅시다.

보셨겠지만, 명령을 처리하기 위한 어노테이션이 [`CommandHandler`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-command-handler/index.html)라고 불리지만, Telegram 봇의 고전적인 개념보다 더 다재다능합니다.

##### 스코프

이는 더 넓은 범위의 처리 가능성을 가지기 때문입니다. 즉, 대상 함수는 텍스트 일치뿐만 아니라 적절한 업데이트 유형에 따라 정의될 수 있으며, 이것이 스코프의 개념입니다.

따라서 각 명령은 다른 스코프 목록에 대해 다른 핸들러를 가질 수 있고, 또는 그 반대로 여러 명령에 대해 하나의 명령을 가질 수 있습니다.

아래에서 텍스트 페이로드와 스코프별 매핑이 어떻게 이루어지는지 볼 수 있습니다:

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/c870027e-750e-4bb8-a2ed-45ad93a55875" alt="명령 스코프 다이어그램" />
</p>

#### Inputs

다음으로, 텍스트 페이로드가 어떤 명령과도 일치하지 않으면 입력 포인트를 검색합니다.

이 개념은 명령줄 애플리케이션에서 입력을 기다리는 것과 매우 유사합니다. 특정 사용자에 대해 봇 컨텍스트에 포인트를 설정하여 다음 입력을 처리하도록 하며, 내용이 무엇이든 상관없습니다. 다음 업데이트에 `User`가 있어 설정된 입력 대기 포인트와 연관시킬 수 있는 것이 중요합니다.

아래에서 `Commands`와 일치하지 않는 업데이트 처리 예제를 볼 수 있습니다.

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/925d3e05-0985-43d5-8d6f-b3f2786ff212" alt="우선순위 예제 다이어그램" />
</p>

#### Commons

핸들러가 `commands`나 `inputs`를 찾지 못하면 텍스트 로드를 `common` 핸들러와 비교합니다.

반복문을 통해 모든 항목을 확인하기 때문에 과도하게 사용하지 않는 것을 권장합니다.

#### Unprocessed

최종 단계로, 핸들러가 일치하는 액티비티를 찾지 못하면([`UpdateHandler`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-update-handler/index.html)는 완전히 병렬로 작동하며 일반적인 액티비티로 간주되지 않습니다), [`UnprocessedHandler`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-unprocessed-handler/index.html)가 작동합니다. 설정되어 있으면 이 경우를 처리하며, 무언가 잘못되었음을 사용자에게 경고하는 데 유용할 수 있습니다.

더 자세한 내용은 [핸들러 문서](Handlers.md)를 참조하세요.

### 액티비티 RateLimiter

액티비티를 찾은 후, 액티비티 파라미터에서 지정한 매개변수에 따라 사용자의 RateLimiter를 확인합니다.

### 액티비티

액티비티는 Telegram 봇 라이브러리가 처리할 수 있는 다양한 유형의 핸들러를 의미하며, Commands, Inputs, Regexes 및 Unprocessed 핸들러를 포함합니다.

### 호출

최종 처리 단계는 찾은 액티비티의 호출입니다.

더 자세한 내용은 [호출 문서](Activity-invocation.md)를 참조하세요.

### 참고 자료

* [업데이트 파싱](Update-parsing.md)
* [액티비티 호출](Activity-invocation.md)
* [핸들러](Handlers.md)
* [봇 설정](Bot-configuration.md)
* [웹 스타터(Spring, Ktor)](Web-starters-(Spring-and-Ktor.md))
---