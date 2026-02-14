---
---
title: Web Starters (Spring And Ktor)
---

### Spring starter

라이브러리를 위한 Spring Starter 모듈은 Spring Boot 애플리케이션에 Telegram 봇 기능을 통합하는 자동 설정 모듈입니다. 제공된 설정에 따라 Telegram 봇을 자동으로 구성하기 위해 Spring Boot의 의존성 주입과 설정 속성의 힘을 활용합니다. 이 라이브러리는 Kotlin과 Spring Boot를 사용하여 Telegram 봇을 구축하려는 개발자에게 특히 유용하며, 봇 개발 및 관리에 대한 간소화된 접근 방식을 제공합니다.

### 주요 기능

- **자동 설정**: 라이브러리는 제공된 설정 속성에 따라 Telegram 봇을 자동으로 구성하여 수동 설정의 필요성을 없앱니다.
- **설정 속성**: 봇 토큰, 패키지 이름, 식별자 등 봇 설정의 쉬운 사용자 정의를 위한 설정 속성을 지원합니다.
- **Spring 통합**: Spring 생태계와 원활하게 통합되어 Spring의 의존성 주입과 애플리케이션 컨텍스트를 활용하여 봇 인스턴스를 관리합니다.
- **코루틴 지원**: Kotlin 코루틴을 비동기 봇 작업에 활용하여 효율적이고 논블로킹 실행을 보장합니다.

### 시작하기

Spring Starter 라이브러리를 사용하려면 Spring Boot 프로젝트에 종속성으로 포함해야 합니다. 이 라이브러리는 Spring Boot 애플리케이션과 함께 작동하도록 설계되었으며 기능을 위해 Spring Boot 프레임워크가 필요합니다.

#### 종속성

`build.gradle` 또는 `pom.xml` 파일에 다음 종속성을 추가하세요:

```gradle
dependencies {
    implementation 'eu.vendeli:spring-starter:<version>'
}
```

`<version>`을 라이브러리의 최신 버전으로 바꿉니다.

#### 설정

라이브러리는 Spring Boot의 `@ConfigurationProperties`를 사용하여 설정 속성을 바인딩합니다. Spring Boot 애플리케이션의 `application.properties` 또는 `application.yml` 파일에 봇 설정을 정의할 수 있습니다.

```yaml
ktgram:
 autoStartPolling: true
 shareHttpClient: true
 bot:
    - token: YOUR_BOT_TOKEN
      pckg: com.example.bot
      identifier: MyBot
```

#### 사용법

라이브러리가 포함되고 설정되면 제공된 설정에 따라 Telegram 봇 인스턴스를 자동으로 생성하고 구성합니다.

또한 여러 봇 인스턴스를 지원합니다. 여러 개를 초기화하려면 봇 섹션에서 새 항목으로 선언하기만 하면 됩니다:

```yaml
ktgram:
 bot:
    - token: YOUR_BOT_TOKEN
    - token: SECOND_BOT_TOKEN
```

### 고급 설정

봇 동작 사용자 정의나 다른 Spring 컴포넌트와의 통합과 같은 더 고급 설정의 경우 `BotConfiguration` 클래스를 확장하고 `applyCfg` 메서드를 통해 봇 설정을 변경할 수 있습니다. 예제는 [여기](https://github.com/vendelieu/telegram-bot_template/blob/spring-bot/src/main/kotlin/com/example/springbot/configuration/BotConfig.kt)에서 확인할 수 있습니다.

> [!TIP]
> 초기화된 각 인스턴스를 사용자 정의 설정으로 구성하려면 식별자로 구분하세요(BotConfiguration 클래스에도 식별자가 있습니다).

### Ktor

이 모듈은 Telegram 봇을 위한 웹훅 서버 생성을 용이하게 하도록 설계되었습니다. 개발자가 서버를 구성할 수 있게 해주며, SSL/TLS 설정을 포함하고 사용자 정의 설정으로 여러 Telegram 봇을 선언할 수 있습니다. 설정 프로세스는 유연하여 개발자가 특정 요구 사항에 맞게 서버를 조정할 수 있습니다.

### 설치

Ktor starter를 설치하려면 주 종속성에 추가하세요:

```gradle
dependencies {
    implementation("eu.vendeli:ktor-starter:x.y.z") // 여기
    // x.y.z를 현재 라이브러리 버전으로 변경
}
```

### 주요 컴포넌트

`serveWebhook` 함수

serveWebhook 함수는 라이브러리의 핵심입니다. Telegram 봇을 위한 웹훅 서버를 설정하고 시작합니다. 두 개의 매개변수를 받습니다:

- `wait`: 서버가 종료되기 전에 애플리케이션이 중지될 때까지 대기해야 하는지 여부를 나타내는 부울값입니다. 기본값은 true입니다.
- `serverBuilder`: 서버를 구성하는 람다 함수입니다. 기본값은 빈 람다입니다.

### 설정

* `WEBHOOK_PREFIX`: 웹훅 리스너 라우트에 사용될 주소 접두사입니다(기본값은 "/"입니다).

#### 서버 설정

- `server`: EnvConfiguration 또는 ManualConfiguration을 사용하여 서버 설정을 설정하는 메서드입니다.
- `engine`: Netty 애플리케이션 엔진을 구성하는 메서드입니다.
- `ktorModule`: 애플리케이션에 Ktor 모듈을 추가하는 메서드입니다.

라이브러리는 호스트, 포트, SSL 설정 등 서버에 대한 다양한 구성 가능한 매개변수를 제공합니다. 이를 구성하는 두 가지 구체적인 옵션이 있습니다:

* `EnvConfiguration`: `KTGRAM_` 접두사가 있는 환경에서 구성 값을 읽습니다.
* `ManualConfiguration`: 구성 값의 수동 설정을 허용하며, `server {}` 함수에서 매개변수를 설정합니다.

설정할 수 있는 매개변수 목록은 다음과 같습니다:

- `HOST`: 서버의 호스트 이름 또는 IP 주소입니다.
- `PORT`: 서버의 포트 번호입니다.
- `SSL_PORT`: SSL/TLS 연결의 포트 번호입니다.
- `PEM_PRIVATE_KEY_PATH`: PEM 개인 키 파일의 경로입니다.
- `PEM_CHAIN_PATH`: PEM 인증서 체인 파일의 경로입니다.
- `PEM_PRIVATE_KEY`: 문자 배열로 된 PEM 개인 키 비밀번호입니다.
- `KEYSTORE_PATH`: Java KeyStore 파일의 경로입니다.
- `KEYSTORE_PASSWORD`: KeyStore의 비밀번호입니다.
- `KEY_ALIAS`: KeyStore의 키에 대한 별칭입니다.
- `SSL_ON`: SSL/TLS를 활성화해야 하는지 여부를 나타내는 부울값입니다. 기본값은 true입니다.

> [!TIP]
> PEM 인증서가 있으면 모듈 자체가 지정된 경로에서 이를 사용하여 jks 스토리지를 생성합니다.

#### 봇 설정:

봇을 구성하려면 다음과 같은 매개변수를 가진 `declareBot {}`를 호출하세요:

- `token`: 봇 토큰입니다.
- `pckg`: 봇의 패키지 이름입니다.
- `configuration`: 봇을 구성하는 람다 함수입니다.
- `handlingBehaviour`: 봇의 처리 동작을 설정하는 람다 함수입니다.
- `onInit`: 봇이 초기화될 때 실행될 람다 함수입니다.

### 예제 사용법

이 모듈을 사용하려면 `serveWebhook` 함수를 호출하고 원하는 설정으로 구성한 후 봇을 선언하세요. 간단한 예제는 다음과 같습니다:

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
            // 필요한 다른 구성 매개변수 설정
        }
        declareBot {
            token = "YOUR_BOT_TOKEN"
            // 다른 봇 설정 구성
        }
        // 필요한 경우 더 많은 봇을 추가하거나 다른 매개변수를 설정
    }
}
```

> [!CAUTION]
> 모든 것이 작동하도록 웹훅을 설정하는 것을 잊지 마세요. :)

기본적으로 모듈은 웹훅 리스닝 엔드포인트를 `host/BOT_TOKEN`으로 제공합니다.


---

STRUCTURAL INTEGRITY MODE:

You must produce output that is byte-structurally compatible with the input Markdown.

Rules:
- The number of code blocks must match exactly.
- The number of headings must match exactly.
- All fenced code blocks must remain unchanged.
- All URLs must remain identical.
- All inline code spans must remain identical.
- Do not merge or split paragraphs.
- Do not normalize spacing.