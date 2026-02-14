---
---
title: Bot Configuration
---

库提供了丰富的配置选项，你可以在 [`BotConfiguration`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.configuration/-bot-configuration/index.html) 类描述中查看 API 参考。

配置 bot 有两种方法：

### Configurator lambda

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

### ConfigLoader 接口

还可以通过特殊的 [`ConfigLoader`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.helper/-config-loader/index.html) 接口进行配置，<br/> 你可以从外部源（`properties`、`command line args` 等）加载设置。

可以通过次构造函数传入此接口的实现，实例将相应地进行配置。

```kotlin
val bot = TelegramBot(ConfigLoaderImpl)
```

目前提供了几个实现此接口的模块，如 `ktgram-config-env`、`ktgram-config-toml`。

### BotConfiguration 概述

#### BotConfiguration

`BotConfiguration` 类是配置 bot 的中心枢纽。它包括用于标识 bot、设置 API 主机、确定 bot 是否在测试环境中运行、处理输入、管理类和控制输入自动删除的属性。此外，它还提供了速率限制、HTTP 客户端配置、日志记录、更新监听和命令解析的内部属性。

##### 属性

- `identifier`: 在多 bot 处理期间标识不同的 bot 实例。
- `apiHost`: Telegram API 的主机。
- `isTestEnv`: 指示 bot 是否在测试环境中运行。
- `inputListener`: 输入处理类的实例。
- `classManager`: 用于获取类的管理器。
- `inputAutoRemoval`: 在处理期间调节输入点自动删除的标志。
- `exceptionHandlingStrategy`: 定义异常处理策略。
    * `CollectToChannel` - 收集到 `TgUpdateHandler.caughtExceptions`。
    * `Throw` - 再次抛出并包装在 `TgException` 中。
    * `DoNothing` - 什么都不做 :)
    * `Handle` - 设置自定义处理程序。
- `throwExOnActionsFailure`: 当任何 bot 请求失败时抛出异常。

##### 配置块

`BotConfiguration` 还提供了配置其内部组件的函数：

- `httpClient(block: HttpConfiguration.() -> Unit)`: 配置 HTTP 客户端。
- `logging(block: LoggingConfiguration.() -> Unit)`: 配置日志记录。
- `rateLimiter(block: RateLimiterConfiguration.() -> Unit)`: 配置请求限制。
- `updatesListener(block: UpdatesListenerConfiguration.() -> Unit)`: 配置更新监听器。
- `commandParsing(block: CommandParsingConfiguration.() -> Unit)`: 指定命令解析模式。

### 关联配置类

#### RateLimiterConfiguration

配置全局速率限制。

- `limits`: 全局速率限制。
- `mechanism`: 用于速率限制的机制，默认为 TokenBucket 算法。
- `exceededAction`: 超出限制时应用的动作。

#### HttpConfiguration

包含 bot 的 HTTP 客户端配置。

- `requestTimeoutMillis`: 请求超时（毫秒）。
- `connectTimeoutMillis`: 连接超时（毫秒）。
- `socketTimeoutMillis`: Socket 超时（毫秒）。
- `maxRequestRetry`: HTTP 请求的最大重试次数。
- `retryStrategy`: 重试策略，可自定义。
- `retryDelay`: 每次重试的超时倍数。
- `proxy`: HTTP 调用的代理设置。
- `additionalHeaders`: 应用于每个请求 headers。

#### LoggingConfiguration

管理 bot 操作和 HTTP 请求的日志级别。

- `botLogLevel`: bot 操作的日志级别。
- `httpLogLevel`: HTTP 请求的日志级别。

#### UpdatesListenerConfiguration

配置与拉取更新相关的参数。

- `dispatcher`: 收集传入更新的调度器。
- `processingDispatcher`: 处理更新的调度器。
- `pullingDelay`: 每次拉取请求后的延迟。
- `updatesPollingTimeout`: 长轮询机制的超时选项。

#### CommandParsingConfiguration

指定命令解析的参数。

- `commandDelimiter`: 命令和参数之间的分隔符。
- `parametersDelimiter`: 参数之间的分隔符。
- `parameterValueDelimiter`: 参数键和值之间的分隔符。
- `restrictSpacesInCommands`: 指示是否将命令中的空格视为命令的结束。
- `useIdentifierInGroupCommands`: 使用 bot 的标识符匹配包含 @ 的命令。

### 示例配置

这是一个如何使用这些类配置 bot 的示例：

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

此配置设置了一个具有特定标识符的 bot，启用了测试环境模式，配置了速率限制、HTTP 客户端设置、日志级别、更新监听器参数和命令解析规则。

通过利用这些配置选项，开发者可以微调他们的 bot 以满足特定需求，并在各种操作场景中优化性能。