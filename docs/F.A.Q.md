---
title: F.A.Q
---

### `AbstractMethodError` exception

If you getting such exception on the startup of your application:

```kotlin
Exception in thread "DefaultDispatcher-worker-1" java.lang.AbstractMethodError: 'kotlinx.serialization.KSerializer[] kotlinx.serialization.internal.GeneratedSerializer.typeParametersSerializers()'
	at eu.vendeli.tgbot.types.options.GetUpdatesOptions$$serializer.typeParametersSerializers(GetUpdatesOptions.kt:6)
```

It happening because your build system resolving old serialization library which internal mechanics differs.
To solve it you should make it use more newer version, for example by adding this to your buildscript:

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

(If it was well described in changelog I would never upgraded it bc I getting so much reports on this issue)

### How do I get the method's response?

To get a response and be able to operate over, you need to use `sendReturning` at the end of the method instead of `send`.

In this case the `Response` class is returned, which contains the response, success or failure, further you need to either handle the failure or just call `getOrNull()`.

There's section about: [Processing responses](https://github.com/vendelieu/telegram-bot#processing-responses).

### I'm getting error while using `spring-boot-devtools`

This happens because `spring-boot-devtools` has its own `classloader` and it does not find methods.

You need to add to `resources/META-INF/spring-devtools.properties`:

```properties
restart.include.generated=/eu.vendeli
```

### How to change ktor engine

If you want to change the engine used by the client you can simply change the [parameter](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/ktor-jvm-engine.html) in the [plugin settings](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/index.html).

### How to use my favorite logging provider

The library uses `slf4j-api` and to use the provider you just need to add it to the dependencies.

The library plugin automatically detects the use of the provider, if provider is missing, `logback` will be used by default.

### Catch network exceptions within long-polling handler

For example if you have an unstable connection and need to catch an error because of this, perhaps this approach will help you:

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

Also you can take a look how it's done in [spring-starter](https://github.com/vendelieu/telegram-bot/blob/1584d40f9a94a8c31bba9e7614c0070155630a52/spring-ktgram-starter/src/jvmMain/kotlin/eu/vendeli/spring/starter/TelegramAutoConfiguration.kt#L53).
