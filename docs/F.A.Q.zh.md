---
title: 常见问题解答
---

### 如何获取方法的响应？

要获取响应并能够进行操作，您需要在方法末尾使用 `sendReturning` 而不是 `send`。

在这种情况下，将返回 `Response` 类，该类包含响应、成功或失败，您需要处理失败或仅调用 `getOrNull()`。

有关更多信息，请参见：[处理响应](https://github.com/vendelieu/telegram-bot#processing-responses)。

### 使用 `spring-boot-devtools` 时出现错误

这发生是因为 `spring-boot-devtools` 有自己的 `classloader`，并且找不到方法。

您需要在 `resources/META-INF/spring-devtools.properties` 中添加：

```properties
restart.include.generated=/eu.vendeli
```

### 如何更改 ktor 引擎

如果您想更改客户端使用的引擎，可以简单地更改 [参数](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/ktor-jvm-engine.html) 在 [插件设置](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/index.html) 中。

### 如何使用我喜欢的日志提供程序

该库使用 `slf4j-api`，要使用所需的提供程序，您只需将其添加到依赖项中。

库插件会自动检测提供程序的使用，如果缺失，将默认使用 `logback`。

### 在长轮询处理程序中捕获网络异常

例如，如果您有不稳定的连接并需要捕获因此产生的错误，或许这种方法会对您有所帮助：

```kotlin
fun main() {
    val bot = TelegramBot("TOKEN")

    try {
        bot.handleUpdates()
    } catch (e: Exception) {
        // 如有需要，处理异常
        
        bot.update.stopListener()
        bot.handleUpdates()
    }
}
```

您还可以查看 [spring-starter](https://github.com/vendelieu/telegram-bot/blob/1584d40f9a94a8c31bba9e7614c0070155630a52/spring-ktgram-starter/src/jvmMain/kotlin/eu/vendeli/spring/starter/TelegramAutoConfiguration.kt#L53) 中是如何实现的。