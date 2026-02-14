---
---
title: Вопросы и ответы
---

### Исключение `AbstractMethodError`

Если при запуске вашего приложения возникает такое исключение:

```kotlin
Exception in thread "DefaultDispatcher-worker-1" java.lang.AbstractMethodError: 'kotlinx.serialization.KSerializer[] kotlinx.serialization.internal.GeneratedSerializer.typeParametersSerializers()'
	at eu.vendeli.tgbot.types.options.GetUpdatesOptions$$serializer.typeParametersSerializers(GetUpdatesOptions.kt:6)
```

Это происходит потому что ваша система сборки использует старую библиотеку сериализации, чья внутренняя механика отличается.
Чтобы решить это, нужно использовать более новую версию, например добавив это в buildscript:

```kotlin
configurations.all {
    resolutionStrategy.eachDependency {
        val serdeVer = "x.x.x" // должна быть >= 1.8.0
        when(requested.module.toString()) {
            // json serialiazation
            "org.jetbrains.kotlinx:kotlinx-serialization-json" -> useVersion(serdeVer)
            "org.jetbrains.kotlinx:kotlinx-serialization-json-jvm" -> useVersion(serdeVer)
            "org.jetbrains.kotlinx:kotlinx-serialization-core" -> useVersion(serdeVer)
            "org.jetbrains.kotlinx:kotlinx-serialization-core-jvm" -> useVersion(serdeVer)
            "org.jetbrains.kotlinx:kotlinx-serialization-bom" -> useVersion(serdeVer)
        }
    }
}
```

(Если бы это было хорошо описано в changelog, я бы никогда не обновил, потому что получаю так много отчетов об этой проблеме)

### Как получить ответ от метода?

Чтобы получить ответ и иметь возможность работать с ним, нужно использовать `sendReturning` в конце метода вместо `send`.

В этом случае возвращается класс `Response`, который содержит ответ, успех или неудачу, далее нужно либо обработать неудачу, либо просто вызвать `getOrNull()`.

Есть раздел об этом: [Обработка ответов](https://github.com/vendelieu/telegram-bot#processing-responses).

### У меня возникает ошибка при использовании `spring-boot-devtools`

Это происходит потому что `spring-boot-devtools` имеет свой собственный `classloader` и не находит методы.

Нужно добавить в `resources/META-INF/spring-devtools.properties`:

```properties
restart.include.generated=/eu.vendeli
```

### Как изменить движок ktor

Если вы хотите изменить движок, используемый клиентом, вы можете просто изменить [параметр](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/ktor-jvm-engine.html) в [настройках плагина](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/index.html).

### Как использовать мой любимый провайдер логирования

Библиотека использует `slf4j-api` и для использования провайдера нужно просто добавить его в зависимости.

Плагин библиотеки автоматически определяет использование провайдера, если провайдер отсутствует, по умолчанию будет использоваться `logback`.

### Перехват сетевых исключений в обработчике long-polling

Например, если у вас нестабильное соединение и нужно перехватить ошибку из-за этого, возможно этот подход вам поможет:

```kotlin
fun main() {
    val bot = TelegramBot("TOKEN")

    try {
        bot.handleUpdates()
    } catch (e: Exception) {
        // обработка при необходимости
        
        bot.update.stopListener()
        bot.handleUpdates()
    }
}
```

Также вы можете посмотреть как это сделано в [spring-starter](https://github.com/vendelieu/telegram-bot/blob/1584d40f9a94a8c31bba9e7614c0070155630a52/spring-ktgram-starter/src/jvmMain/kotlin/eu/vendeli/spring/starter/TelegramAutoConfiguration.kt#L53).