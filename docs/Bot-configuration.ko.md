---
---
title: 봇 구성
---

라이브러리는 다양한 구성 옵션을 제공하며, [`BotConfiguration`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.configuration/-bot-configuration/index.html) 클래스 설명에서 API 참조를 확인할 수 있습니다.

봇을 구성하는 두 가지 접근 방식도 있습니다:

### Configurator 람다

```kotlin
// ...
val bot = TelegramBot("BOT_TOKEN") {
  inputListener = RedisInputListenerImpl()
  classManager = KoinClassManagerImpl()
  logging {
      botLogLevel = LogLvl.DEBUG
  }
}
// ...
```

### ConfigLoader 인터페이스

[`ConfigLoader`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.helper/-config-loader/index.html) 인터페이스를 통해 구성할 수도 있습니다.<br/> 이를 사용하여 `properties`, `command line args` 등의 외부 소스에서 설정을 로드할 수 있습니다.

이 인터페이스의 구현은 보조 생성자를 통해 전달할 수 있으며, 인스턴스는 이에 따라 구성됩니다.

```kotlin
val bot = TelegramBot(ConfigLoaderImpl)
```

현재 `ktgram-config-env`, `ktgram-config-toml`과 같이 이 인터페이스를 구현하는 여러 모듈이 제공됩니다.

### BotConfiguration 개요

#### BotConfiguration

`BotConfiguration` 클래스는 봇 구성의 중앙 허브입니다. 봇 식별, API 호스트 설정, 봇이 테스트 환경에서 작동하는지 여부 결정, 입력 처리, 클래스 관리, 입력 자동 제거 제어 속성을 포함합니다. 또한 속도 제한, HTTP 클라이언트 구성, 로깅, 업데이트 수신, 명령 구문 분석을 위한 내부 속성을 제공합니다.

##### 속성

- `identifier`: 다중 봇 처리 중 서로 다른 봇 인스턴스를 식별합니다.
- `apiHost`: Telegram API의 호스트입니다.
- `isTestEnv`: 봇이 테스트 환경에서 작동하는지 여부를 나타내는 플래그입니다.
- `inputListener`: 입력 처리 클래스의 인스턴스입니다.
- `classManager`: 클래스를 가져오는 데 사용되는 관리자입니다.
- `inputAutoRemoval`: 처리 중 입력 지점의 자동 삭제를 조절하는 플래그입니다.
- `exceptionHandlingStrategy`: 예외 처리 전략을 정의합니다.
    * `CollectToChannel` - `TgUpdateHandler.caughtExceptions`로 수집합니다.
    * `Throw` - `TgException`으로 다시 던집니다.
    * `DoNothing` - 아무것도 하지 않습니다 :)
    * `Handle` - 사용자 정의 핸들러를 설정합니다.
- `throwExOnActionsFailure`: 봇 요청이 실패할 때 예외를 던집니다.

##### 구성 블록

`BotConfiguration`은 내부 구성 요소를 구성하는 기능도 제공합니다:

- `httpClient(block: HttpConfiguration.() -> Unit)`: HTTP 클라이언트를 구성합니다.
- `logging(block: LoggingConfiguration.() -> Unit)`: 로깅을 구성합니다.
- `rateLimiter(block: RateLimiterConfiguration.() -> Unit)`: 요청 제한을 구성합니다.
- `updatesListener(block: UpdatesListenerConfiguration.() -> Unit)`: 업데이트 수신기를 구성합니다.
- `commandParsing(block: CommandParsingConfiguration.() -> Unit)`: 명령 구문 분석 패턴을 지정합니다.

### 관련 구성 클래스

#### RateLimiterConfiguration

전역 속도 제한을 구성합니다.

- `limits`: 전역 속도 제한입니다.
- `mechanism`: 속도 제한에 사용되는 메커니즘, 기본값은 TokenBucket 알고리즘입니다.
- `exceededAction`: 제한을 초과할 때 적용되는 작업입니다.

#### HttpConfiguration

봇의 HTTP 클라이언트 구성을 포함합니다.

- `requestTimeoutMillis`: 요청 제한 시간(밀리초 단위).
- `connectTimeoutMillis`: 연결 제한 시간(밀리초 단위).
- `socketTimeoutMillis`: 소켓 제한 시간(밀리초 단위).
- `maxRequestRetry`: HTTP 요청의 최대 재시도 횟수입니다.
- `retryStrategy`: 재시도 전략, 사용자 정의 가능합니다.
- `retryDelay`: 각 재시도에서 제한 시간의 승수입니다.
- `proxy`: HTTP 호출을 위한 프록시 설정입니다.
- `additionalHeaders`: 모든 요청에 적용되는 헤더입니다.

#### LoggingConfiguration

봇 작업 및 HTTP 요청에 대한 로깅 수준을 관리합니다.

- `botLogLevel`: 봇 작업에 대한 로그 수준입니다.
- `httpLogLevel`: HTTP 요청에 대한 로그 수준입니다.

#### UpdatesListenerConfiguration

업데이트 가져오기와 관련된 매개변수를 구성합니다.

- `dispatcher`: 들어오는 업데이트를 수집하는 디스패처입니다.
- `processingDispatcher`: 업데이트를 처리하는 디스패처입니다.
- `pullingDelay`: 각 가져오기 요청 후 지연 시간입니다.
- `updatesPollingTimeout`: 장기 폴링 메커니즘에 대한 제한 시간 옵션입니다.

#### CommandParsingConfiguration

명령 구문 분석에 대한 매개변수를 지정합니다.

- `commandDelimiter`: 명령과 매개변수 사이의 구분자입니다.
- `parametersDelimiter`: 매개변수 사이의 구분자입니다.
- `parameterValueDelimiter`: 매개변수의 키와 값 사이의 구분자입니다.
- `restrictSpacesInCommands`: 명령의 공백을 명령의 끝으로 처리할지 여부를 나타내는 플래그입니다.
- `useIdentifierInGroupCommands`: 봇 식별자를 사용하여 @를 포함하는 명령을 일치시킵니다.

### 구성 예시

다음은 이러한 클래스를 사용하여 봇을 구성하는 예시입니다:

```kotlin
val bot = TelegramBot("TOKEN") {
    identifier = "MyBot",
    apiHost = "https://api.telegram.org",
    isTestEnv = true,
    inputListener = InputListenerMapImpl(),
    classManager = ClassManagerImpl(),

    httpClient {
        requestTimeoutMillis = 5000L
        connectTimeoutMillis = 3000L
        socketTimeoutMillis = 2000L
    }
    logging {
        botLogLevel = LogLvl.DEBUG
        httpLogLevel = HttpLogLevel.BODY
    }
    updatesListener {
        dispatcher = Dispatchers.IO
        processingDispatcher = Dispatchers.Unconfined
        pullingDelay = 1000L
    }
    commandParsing {
        commandDelimiter = '*'
        parametersDelimiter = '&'
        restrictSpacesInCommands = true
    }
}
```

이 구성은 특정 식별자를 사용하여 봇을 설정하고, 테스트 환경 모드를 활성화하며, 속도 제한, HTTP 클라이언트 설정, 로깅 수준, 업데이트 수신기 매개변수, 명령 구문 분석 규칙을 구성합니다.

개발자는 이러한 구성 옵션을 활용하여 특정 요구 사항을 충족하고 다양한 운영 시나리오에서 성능을 최적화하도록 봇을 세밀하게 조정할 수 있습니다.