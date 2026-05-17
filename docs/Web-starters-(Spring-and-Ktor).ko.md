---
---
title: Web Starters (Spring And Ktor)
---

### Spring starter

Spring Starter 모듈은 라이브러리를 위한 자동 구성 모듈로, Telegram 봇 기능을 Spring Boot 애플리케이션에 통합합니다. Spring Boot의 의존성 주입 및 구성 속성의 힘을 활용하여 제공된 구성에 따라 Telegram 봇을 자동으로 설정합니다. 이 라이브러리는 Kotlin과 Spring Boot를 사용하여 Telegram 봇을 구축하려는 개발자에게 특히 유용하며, 봇 개발 및 관리를 위한 간소화된 접근 방식을 제공합니다.

### Key Features

- **Auto-Configuration**: 라이브러리는 제공된 구성 속성을 기반으로 Telegram 봇을 자동으로 설정하여 수동 설정의 필요성을 없앱니다.
- **Configuration Properties**: 봇 토큰, 패키지 이름, 식별자와 같은 봇 설정을 쉽게 사용자 지정할 수 있도록 구성 속성을 지원합니다.
- **Spring Integration**: Spring의 의존성 주입 및 애플리케이션 컨텍스트를 활용하여 봇 인스턴스를 관리함으로써 Spring 생태계와 원활히 통합됩니다.
- **Coroutine Support**: Kotlin 코루틴을 활용하여 비동기 봇 작업을 수행하고 효율적이며 논블로킹 실행을 보장합니다.

### Getting Started

Telegram Bots용 Spring Starter Library를 사용하려면 Spring Boot 프로젝트에 종속성으로 포함해야 합니다. 이 라이브러리는 Spring Boot 애플리케이션과 함께 작동하도록 설계되었으며, Spring Boot 프레임워크가 필요합니다.

#### Dependency

`build.gradle` 또는 `pom.xml` 파일에 다음 종속성을 추가하십시오:

```gradle
dependencies {
    implementation 'eu.vendeli:spring-starter:<version>'
}
```

`<version>`을 라이브러리의 최신 버전으로 교체하십시오.

#### Configuration

라이브러리는 Spring Boot의 `@ConfigurationProperties`를 사용하여 구성 속성을 바인딩합니다. Spring Boot 애플리케이션의 `application.properties` 또는 `application.yml` 파일에 봇 구성을 정의할 수 있습니다.

```yaml
ktgram:
 autoStartPolling: true
 shareHttpClient: true
 bot:
    - token: YOUR_BOT_TOKEN
      pckg: com.example.bot
      identifier: MyBot
```

#### Usage

라이브러리를 포함하고 구성하면 제공된 구성에 따라 Telegram 봇 인스턴스를 자동으로 생성하고 설정합니다.

여러 봇 인스턴스를 지원하므로, 여러 개를 초기화하려면 bot 섹션에 새 항목을 선언하십시오:

```yaml
ktgram:
 bot:
    - token: YOUR_BOT_TOKEN
    - token: SECOND_BOT_TOKEN
```

### Advanced Configuration

봇 동작을 사용자 정의하거나 다른 Spring 구성 요소와 통합하는 등 보다 고급 설정이 필요하면 `BotConfiguration` 클래스를 확장하고 `applyCfg` 메서드를 통해 봇 구성을 변경할 수 있습니다. 예시는 [여기](https://github.com/vendelieu/telegram-bot_template/blob/spring-bot/src/main/kotlin/com/example/springbot/configuration/BotConfig.kt)에서 확인하십시오.

> [!TIP]
> 각 초기화된 인스턴스를 사용자 정의 구성으로 설정하려면 식별자를 사용해 구분하십시오 (BotConfiguration 클래스에도 식별자가 있습니다).

### Ktor

이 모듈은 Telegram 봇을 위한 webhook 서버 생성을 쉽게 해줍니다. 개발자는 SSL/TLS 설정을 포함한 서버를 구성하고, 사용자 정의 구성을 가진 여러 Telegram 봇을 선언할 수 있습니다. 설정 과정은 유연하여 개발자가 필요에 맞게 서버를 맞춤화할 수 있습니다.

### Installation

ktor starter를 설치하려면 메인 종속성에 추가하십시오:

```gradle
dependencies {
    implementation("eu.vendeli:ktor-starter:x.y.z") // there
    // change x.y.z to current library version
}
```

### Key Components

`serveWebhook` Function

`serveWebhook` 함수는 라이브러리의 핵심입니다. Telegram 봇을 위한 webhook 서버를 설정하고 시작합니다. 두 개의 매개변수를 받습니다:

- `wait`: 서버가 애플리케이션 종료를 기다렸다가 종료할지 여부를 나타내는 boolean 값입니다. 기본값은 true입니다.
- `serverBuilder`: 서버를 구성하는 람다 함수입니다. 기본값은 빈 람다입니다.

### Configuration

* `WEBHOOK_PREFIX`: webhook 리스너 라우트의 주소 접두사로 사용되는 매개변수입니다. (기본값은 "/")

#### Server Setup

- `server`: EnvConfiguration 또는 ManualConfiguration 중 하나를 사용하여 서버 구성을 설정하는 메서드입니다.
- `engine`: Netty 애플리케이션 엔진을 구성하는 메서드입니다.
- `ktorModule`: 애플리케이션에 Ktor 모듈을 추가하는 메서드입니다.

라이브러리는 호스트, 포트, SSL 설정 등 서버에 대한 다양한 구성 매개변수를 제공합니다. 구성 방법에는 두 가지 구체적인 옵션이 있습니다:

* `EnvConfiguration`: `KTGRAM_` 접두사가 붙은 환경 변수에서 구성 값을 읽습니다.
* `ManualConfiguration`: `server {}` 함수 내에서 매개변수를 수동으로 설정합니다.

설정 가능한 매개변수 목록:

- `HOST`: 서버의 호스트명 또는 IP 주소.
- `PORT`: 서버 포트 번호.
- `SSL_PORT`: SSL/TLS 연결용 포트 번호.
- `PEM_PRIVATE_KEY_PATH`: PEM 개인 키 파일 경로.
- `PEM_CHAIN_PATH`: PEM 인증서 체인 파일 경로.
- `PEM_PRIVATE_KEY`: PEM 개인 키 비밀번호 문자 배열.
- `KEYSTORE_PATH`: Java KeyStore 파일 경로.
- `KEYSTORE_PASSWORD`: KeyStore 비밀번호.
- `KEY_ALIAS`: KeyStore 내 키 별명.
- `SSL_ON`: SSL/TLS 사용 여부를 나타내는 boolean 값. 기본값은 true입니다.

> [!TIP]
> PEM 인증서가 존재하면 모듈 자체가 지정된 경로에 jks 스토리지를 생성합니다.

#### Bot Configuration:

봇을 구성하려면 `declareBot {}` 를 호출하고 다음 매개변수를 사용하십시오:

- `token`: 봇 토큰.
- `pckg`: 봇의 패키지 이름.
- `configuration`: 봇을 구성하는 람다 함수.
- `handlingBehaviour`: 봇의 처리 동작을 설정하는 람다 함수.
- `onInit`: 봇이 초기화될 때 실행되는 람다 함수.

### Example Usage

이 모듈을 사용하려면 `serveWebhook` 함수를 호출하고 원하는 설정으로 구성한 뒤 봇을 선언하십시오. 간단한 예시는 다음과 같습니다:

```kotlin
fun main() = runBlocking {
    serveWebhook {
        server {
            HOST = "0.0.0.0"
            PORT = 8080
            SSL_PORT = 8443

            PEM_PRIVATE_KEY_PATH = "/etc/letsencrypt/live/example.com/privkey.pem"
            PEM_CHAIN_PATH = "/etc/letsencrypt/live/example.com/fullchain.pem"
            PEM_PRIVATE_KEY = "pem_changeit".toCharArray()

            KEYSTORE_PATH = "/etc/ssl/certs/java/cacerts/bot_keystore.jks"
            KEYSTORE_PASSWORD = "changeit".toCharArray()
            // Set other configuration parameters as needed
        }
        declareBot {
            token = "YOUR_BOT_TOKEN"
            // Configure other bot settings
        }
        // Add more bots or set other parameters if needed
    }
}
```

> [!CAUTION]
> 모든 것이 작동하도록 webhook을 설정하는 것을 잊지 마세요. :)

기본적으로 모듈은 `host/BOT_TOKEN` 형태로 webhook 청취 엔드포인트를 제공합니다.


---