---
---
title: F.A.Q
---

### `AbstractMethodError` 异常

如果您在应用程序启动时遇到这样的异常：

```kotlin
Exception in thread "DefaultDispatcher-worker-1" java.lang.AbstractMethodError: 'kotlinx.serialization.KSerializer[] kotlinx.serialization.internal.GeneratedSerializer.typeParametersSerializers()'
	at eu.vendeli.tgbot.types.options.GetUpdatesOptions$$serializer.typeParametersSerializers(GetUpdatesOptions.kt:6)
```

这是因为您的构建系统解析了旧的序列化库，其内部机制不同。要解决这个问题，您应该让它使用更新的版本，例如通过在您的构建脚本中添加以下内容：

```kotlin
configurations.all {
    resolutionStrategy.eachDependency {
        val serdeVer = "x.x.x" // 应 >= 1.8.0
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

(如果这在变更日志中有详细说明，我永远不会升级它，因为我收到了太多关于这个问题的报告)

### 如何获取方法的响应？

要获取响应并能够操作，您需要在方法的末尾使用 `sendReturning` 而不是 `send`。

在这种情况下会返回 `Response` 类，其中包含响应，成功或失败，接下来您需要处理失败或直接调用 `getOrNull()`。

这里有关于：[处理响应](https://github.com/vendelieu/telegram-bot#processing-responses) 的章节。

### 使用 `spring-boot-devtools` 时出现错误

这是因为 `spring-boot-devtools` 有自己的 `classloader`，它找不到方法。

您需要在 `resources/META-INF/spring-devtools.properties` 中添加：

```properties
restart.include.generated=/eu.vendeli
```

### 如何更改 ktor 引擎

如果您想更改客户端使用的引擎，您可以简单地更改 [参数](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/ktor-jvm-engine.html) 在 [插件设置](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/index.html) 中。

### 如何使用我喜欢的日志提供商

库使用 `slf4j-api`，要使用提供商，您只需将其添加到依赖项中。

库插件会自动检测提供商的使用，如果缺少提供商，默认会使用 `logback`。

### 在长轮询处理程序中捕获网络异常

例如，如果您有不稳定的连接并需要因为这个原因捕获错误，也许这种方法会对您有所帮助：

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

您还可以查看 [spring-starter](https://github.com/vendelieu/telegram-bot/blob/1584d40f9a94a8c31bba9e7614c0070155630a52/spring-ktgram-starter/src/jvmMain/kotlin/eu/vendeli/spring/starter/TelegramAutoConfiguration.kt#L53) 中是如何实现的。