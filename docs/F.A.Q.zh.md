---
---
title: 常见问题解答
---

### `AbstractMethodError` 异常

如果在启动应用程序时遇到此异常：

```kotlin
Exception in thread "DefaultDispatcher-worker-1" java.lang.AbstractMethodError: 'kotlinx.serialization.KSerializer[] kotlinx.serialization.internal.GeneratedSerializer.typeParametersSerializers()'
	at eu.vendeli.tgbot.types.options.GetUpdatesOptions$$serializer.typeParametersSerializers(GetUpdatesOptions.kt:6)
```

这是因为你的构建系统解析了旧的序列化库，其内部机制不同。
要解决这个问题，你需要让它使用更新的版本，例如通过在 buildscript 中添加以下内容：

```kotlin
configurations.all {
    resolutionStrategy.eachDependency {
        val serdeVer = "x.x.x" // 应该 >= 1.8.0
        when(requested.module.toString()) {
            // json 序列化
            "org.jetbrains.kotlinx:kotlinx-serialization-json" -> useVersion(serdeVer)
            "org.jetbrains.kotlinx:kotlinx-serialization-json-jvm" -> useVersion(serdeVer)
            "org.jetbrains.kotlinx:kotlinx-serialization-core" -> useVersion(serdeVer)
            "org.jetbrains.kotlinx:kotlinx-serialization-core-jvm" -> useVersion(serdeVer)
            "org.jetbrains.kotlinx:kotlinx-serialization-bom" -> useVersion(serdeVer)
        }
    }
}
```

(如果在变更日志中有很好的描述，我永远不会升级它，因为我收到了很多关于此问题的报告)

### 如何获取方法的响应？

要获取响应并能够操作，你需要使用方法的末尾的 `sendReturning` 而不是 `send`。

在这种情况下，会返回 `Response` 类，它包含响应、成功或失败，接下来你需要处理失败或直接调用 `getOrNull()`。

这里有一节关于：[处理响应](https://github.com/vendelieu/telegram-bot#processing-responses)。

### 使用 `spring-boot-devtools` 时出现错误

这是因为 `spring-boot-devtools` 有自己的 `classloader`，它找不到方法。

你需要将以下内容添加到 `resources/META-INF/spring-devtools.properties`：

```properties
restart.include.generated=/eu.vendeli
```

### 如何更改 ktor 引擎

如果你想更改客户端使用的引擎，你可以简单地更改[参数](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/ktor-jvm-engine.html)在[插件设置](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/index.html)中。

### 如何使用我最喜欢的日志提供程序

该库使用 `slf4j-api`，要使用提供程序，你只需要将其添加到依赖项中。

库插件会自动检测提供程序的使用，如果缺少提供程序，将默认使用 `logback`。

### 在长轮询处理程序中捕获网络异常

例如，如果你有不稳定的连接并需要因为这个原因捕获错误，也许这种方法会对你有帮助：

```kotlin
fun main() {
    val bot = TelegramBot("TOKEN")

    try {
        bot.handleUpdates()
    } catch (e: Exception) {
        // 如果需要处理
        
        bot.update.stopListener()
        bot.handleUpdates()
    }
}
```

你也可以看看[spring-starter](https://github.com/vendelieu/telegram-bot/blob/1584d40f9a94a8c31bba9e7614c0070155630a52/spring-ktgram-starter/src/jvmMain/kotlin/eu/vendeli/spring/starter/TelegramAutoConfiguration.kt#L53)中是如何实现的。