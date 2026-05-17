---
---
title: F.A.Q
---

### `AbstractMethodError` exception

Если вы получаете такое исключение при запуске вашего приложения:

```kotlin
Exception in thread "DefaultDispatcher-worker-1" java.lang.AbstractMethodError: 'kotlinx.serialization.KSerializer[] kotlinx.serialization.internal.GeneratedSerializer.typeParametersSerializers()'
	at eu.vendeli.tgbot.types.options.GetUpdatesOptions$$serializer.typeParametersSerializers(GetUpdatesOptions.kt:6)
```

Это происходит потому, что ваша система сборки разрешает старую библиотеку сериализации, чья внутренняя механика отличается.  
Чтобы решить проблему, нужно заставить её использовать более новую версию, например, добавив следующее в ваш buildscript:

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

(Если бы это было хорошо описано в changelog, я бы никогда не обновлял его, потому что получаю множество сообщений об этой проблеме)

### How do I get the method's response?

Чтобы получить ответ и иметь возможность работать с ним, необходимо использовать `sendReturning` в конце метода вместо `send`.

В этом случае возвращается класс `Response`, который содержит ответ, успех или ошибку; дальше вам нужно либо обработать ошибку, либо просто вызвать `getOrNull()`.

Есть раздел о: [Processing responses](https://github.com/vendelieu/telegram-bot#processing-responses).

### I'm getting error while using `spring-boot-devtools`

Это происходит, потому что `spring-boot-devtools` имеет собственный `classloader` и не находит методы.

Нужно добавить в `resources/META-INF/spring-devtools.properties`:

```properties
restart.include.generated=/eu.vendeli
```

### How to change ktor engine

Если вы хотите изменить движок, используемый клиентом, просто измените [parameter](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/ktor-jvm-engine.html) в [plugin settings](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/index.html).

### How to use my favorite logging provider

Библиотека использует `slf4j-api`, и чтобы использовать провайдер, достаточно добавить его в зависимости.

Плагин библиотеки автоматически обнаруживает использование провайдера; если провайдер отсутствует, по умолчанию будет использован `logback`.

### Catch network exceptions within long-polling handler

Например, если у вас нестабильное соединение и необходимо перехватить ошибку, возможно, вам поможет такой подход:

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

Также вы можете посмотреть, как это реализовано в [spring-starter](https://github.com/vendelieu/telegram-bot/blob/1584d40f9a94a8c31bba9e7614c0070155630a52/spring-ktgram-starter/src/jvmMain/kotlin/eu/vendeli/spring/starter/TelegramAutoConfiguration.kt#L53).

---