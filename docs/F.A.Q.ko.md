---
---
title: 자주 묻는 질문
---

### `AbstractMethodError` 예외

애플리케이션 시작 시 다음과 같은 예외가 발생하는 경우:

```kotlin
Exception in thread "DefaultDispatcher-worker-1" java.lang.AbstractMethodError: 'kotlinx.serialization.KSerializer[] kotlinx.serialization.internal.GeneratedSerializer.typeParametersSerializers()'
	at eu.vendeli.tgbot.types.options.GetUpdatesOptions$$serializer.typeParametersSerializers(GetUpdatesOptions.kt:6)
```

이것은 빌드 시스템이 내부 메커니즘이 다른 이전 버전의 직렬화 라이브러리를 참조하기 때문에 발생합니다.
이를 해결하려면 더 최신 버전을 사용하도록 설정해야 합니다. 예를 들어 빌드스크립트에 다음을 추가할 수 있습니다:

```kotlin
configurations.all {
    resolutionStrategy.eachDependency {
        val serdeVer = "x.x.x" // should be >= 1.8.0
        when(requested.module.toString()) {
            // json serialiazaton
            "org.jetbrains.kotlinx:kotlinx-serialization-json" -> useVersion(serdeVer)
            "org.jetbrains.kotlinx:kotlinx-serialization-json-jvm" -> useVersion(serdeVer)
            "org.jetbrains.kotlinx:kotlinx-serialization-core" -> useVersion(serdeVer)
            "org.jetbrains.kotlinx:kotlinx-serialization-core-jvm" -> useVersion(serdeVer)
            "org.jetbrains.kotlinx:kotlinx-serialization-bom" -> useVersion(serdeVer)
        }
    }
}
```

(변경사항이 변경 로그에 잘 설명되어 있었다면 이 문제에 대한 보고를 이렇게 많이 받지 않았을 것입니다)

### 메서드의 응답을 어떻게 얻나요?

응답을 얻고 이를 조작하려면 `send` 대신 메서드 끝에 `sendReturning`을 사용해야 합니다.

이 경우 `Response` 클래스가 반환되며, 이 클래스에는 응답, 성공 또는 실패가 포함됩니다. 그 후에는 실패를 처리하거나 단순히 `getOrNull()`을 호출하면 됩니다.

관련 내용은 다음 섹션을 참조하세요: [응답 처리](https://github.com/vendelieu/telegram-bot#processing-responses).

### `spring-boot-devtools` 사용 시 오류가 발생합니다

이 문제는 `spring-boot-devtools`가 자체 `classloader`를 가지고 있고 메서드를 찾지 못하기 때문에 발생합니다.

`resources/META-INF/spring-devtools.properties`에 다음을 추가해야 합니다:

```properties
restart.include.generated=/eu.vendeli
```

### ktor 엔진 변경 방법

클라이언트에서 사용하는 엔진을 변경하려면 [설정](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/ktor-jvm-engine.html)의 [매개변수](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/index.html)를 간단히 변경할 수 있습니다.

### 선호하는 로깅 제공업체 사용 방법

라이브러리는 `slf4j-api`를 사용하며, 제공업체를 사용하려면 해당 제공업체를 의존성에 추가하기만 하면 됩니다.

라이브러리 플러그인은 제공업체 사용을 자동으로 감지하며, 제공업체가 누락된 경우 기본값으로 `logback`이 사용됩니다.

### long-polling 핸들러 내에서 네트워크 예외 처리

예를 들어 불안정한 연결이 있고 이로 인해 오류를 잡아야 하는 경우, 다음 접근 방식이 도움이 될 수 있습니다:

```kotlin
fun main() {
    val bot = TelegramBot("TOKEN")

    try {
        bot.handleUpdates()
    } catch (e: Exception) {
        // handle if needed
        
        bot.update.stopListener()
        bot.handleUpdates()
    }
}
```

또한 [spring-starter](https://github.com/vendelieu/telegram-bot/blob/1584d40f9a94a8c31bba9e7614c0070155630a52/spring-ktgram-starter/src/jvmMain/kotlin/eu/vendeli/spring/starter/TelegramAutoConfiguration.kt#L53)에서 구현된 방식을 확인해볼 수 있습니다.

---