---
---
title: 홈
---

### 소개
라이브러리가 일반적으로 업데이트를 처리하는 방식에 대한 아이디어를 얻어봅시다:

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/442cc5f1-0256-425a-9f25-185fdd49fe0a" alt="처리 과정 다이어그램" />
</p>

업데이트를 수신한 후 라이브러리는 세 가지 주요 단계를 수행합니다.

### 처리

처리 단계는 수신된 업데이트를 해당 페이로드에 따라 [`ProcessedUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processed-update/index.html)의 적절한 하위 클래스로 재패키징하는 것입니다.

이 단계는 업데이트를 더 쉽게 처리하고 처리 기능을 확장하기 위해 필요합니다.

### 처리

다음은 주요 단계로, 여기서 실제 처리가 시작됩니다.

### 글로벌 RateLimiter

업데이트에 사용자가 있는 경우 글로벌 RateLimiter를 초과했는지 확인합니다.

### 텍스트 파싱

다음으로 페이로드에 따라 텍스트를 포함하는 특정 업데이트 컴포넌트를 선택하고 설정에 따라 파싱합니다.

더 자세한 내용은 [업데이트 파싱 문서](Update-parsing.md)를 참조하세요.

### 액티비티 찾기

처리 우선순위에 따라:

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/6178c410-9b9e-4045-9f03-4791b3f49894" alt="처리 우선순위 다이어그램" />
</p>

파싱된 데이터와 우리가 처리하는 액티비티 간의 일치를 찾습니다.
우선순위 다이어그램에서 볼 수 있듯이 `명령어`가 항상 먼저 처리됩니다.

즉, 업데이트의 텍스트 페이로드가 어떤 명령어와 일치하면 추가적인 `입력`, `일반` 검색 및 물론 `처리되지 않음` 작업 실행은 수행되지 않습니다.

유일한 예외는 `UpdateHandlers`가 병렬로 트리거된다는 점입니다.

#### 명령어

명령어와 그 처리 과정을 더 자세히 살펴보겠습니다.

처리 명령어용 어노테이션이 [`CommandHandler`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-command-handler/index.html)라고 불리지만 텔레그램 봇의 고전적인 개념보다 더 유연하다는 것을 알아챘을 것입니다.

##### 범위

이는 더 넓은 범위의 처리 가능성을 가지기 때문입니다. 즉, 타겟 함수는 텍스트 일치뿐만 아니라 적절한 업데이트 유형에 따라 정의될 수 있으며, 이것이 범위의 개념입니다.

따라서 각 명령어는 다른 범위 목록에 대해 다른 핸들러를 가질 수 있고, 반대로 여러 명령어에 대해 하나의 명령어가 있을 수도 있습니다.

아래에서 텍스트 페이로드와 범위별 매핑 방법을 볼 수 있습니다:

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/c870027e-750e-4bb8-a2ed-45ad93a55875" alt="명령어 범위 다이어그램" />
</p>

#### 입력

다음으로 텍스트 페이로드가 어떤 명령어와도 일치하지 않으면 입력 지점을 검색합니다.

이 개념은 명령줄 애플리케이션에서 입력 대기와 매우 유사합니다. 특정 사용자에 대해 봇 컨텍스트에 포인트를 설정하여 다음 입력을 처리하도록 하며, 입력 내용은 중요하지 않고 다음 업데이트에 `User`가 있어 설정된 입력 대기 포인트와 연관시킬 수 있기만 하면 됩니다.

아래에서 `명령어`와 일치하지 않는 경우 업데이트 처리의 예를 볼 수 있습니다.

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/925d3e05-0985-43d5-8d6f-b3f2786ff212" alt="우선순위 예시 다이어그램" />
</p>

#### 일반

핸들러가 `명령어`나 `입력`을 찾지 못하면 텍스트 페이로드를 `일반` 핸들러와 비교합니다.

남용하지 않고 사용하는 것을 권장합니다. 왜냐하면 모든 항목을 반복해서 확인하기 때문입니다.

#### 처리되지 않음

마지막 단계로, 핸들러가 일치하는 액티비티를 찾지 못하면 ([`UpdateHandler`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-update-handler/index.html)는 완전히 병렬로 작동하며 일반 액티비티로 간주되지 않음), [`UnprocessedHandler`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-unprocessed-handler/index.html)가 작동합니다. 설정된 경우 이 경우를 처리하며, 무언가 잘못되었음을 사용자에게 경고하는 데 유용할 수 있습니다.

더 자세한 내용은 [핸들러 문서](Handlers.md)를 참조하세요.

### 액티비티 RateLimiter

액티비티를 찾은 후에도 액티비티 매개변수에 지정된 매개변수에 따라 사용자의 RateLimiter를 확인합니다.

### 액티비티

액티비티는 텔레그램 봇 라이브러리가 처리할 수 있는 다양한 유형의 핸들러를 의미하며, 명령어, 입력, 정규식, 처리되지 않음 핸들러를 포함합니다.

### 호출

마지막 처리 단계는 찾은 액티비티의 호출입니다.

더 자세한 내용은 [호출 문서](Activity-invocation.md)를 참조하세요.

### 관련 문서

* [업데이트 파싱](Update-parsing.md)
* [액티비티 호출](Activity-invocation.md)
* [핸들러](Handlers.md)
* [봇 설정](Bot-configuration.md)
* [웹 스타터(Spring, Ktor)](Web-starters-(Spring-and-Ktor.md))
---