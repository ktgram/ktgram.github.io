---
title: 机器人配置
---

库提供了丰富的配置选项，您可以在 [`BotConfiguration`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.internal.configuration/-bot-configuration/index.html) 类描述中查看 API 参考。

配置机器人有两种方法：

### 配置器 lambda

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

还可以通过特殊的 [`ConfigLoader`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.helper/-config-loader/index.html) 接口进行配置，<br/>
您可以使用它从外部源加载设置（`properties`、`命令行参数` 等）。

该接口的实现可以通过二级构造函数传递，实例将相应地进行配置。

```kotlin
val bot = TelegramBot(ConfigLoaderImpl)
```

目前提供了几个实现此接口的模块，如 `ktgram-config-env`、`ktgram-config-toml`。

### BotConfiguration 概述

#### BotConfiguration

`BotConfiguration` 类是配置机器人的中心枢纽。它包括用于识别机器人、设置 API 主机、确定机器人是否在测试环境中运行、处理输入、管理类以及控制输入自动删除的属性。此外，它还提供用于速率限制、HTTP 客户端配置、日志记录、更新监听和命令解析的内部属性。

##### 属性

- `identifier`：在多机器人处理期间识别不同的机器人实例。
- `apiHost`：Telegram API 的主机。
- `isTestEnv`：指示机器人是否在测试环境中运行的标志。
- `inputListener`：输入处理类的实例。
- `classManager`：用于获取类的管理器。
- `inputAutoRemoval`：在处理期间调节输入点自动删除的标志。
- `exceptionHandlingStrategy`：定义处理异常的策略。
    * `CollectToChannel` - 收集到 `TgUpdateHandler.caughtExceptions`。
    * `Throw` - 再次抛出并用 `TgException` 包装。
    * `DoNothing` - 什么也不做 :)
    * `Handle` - 设置自定义处理程序。
- `throwExOnActionsFailure`：当任何机器人请求失败时抛出异常。

##### 配置块

`BotConfiguration` 还提供了配置其内部组件的函数：

- `httpClient(block: HttpConfiguration.() -> Unit)`：配置 HTTP 客户端。
- `logging(block: LoggingConfiguration.() -> Unit)`：配置日志记录。
- `rateLimiter(block: RateLimiterConfiguration.() -> Unit)`：配置请求限制。
- `updatesListener(block: UpdatesListenerConfiguration.() -> Unit)`：配置更新监听器。
- `commandParsing(block: CommandParsingConfiguration.() -> Unit)`：指定命令解析模式。

### 相关配置类

#### RateLimiterConfiguration

配置全局速率限制。

- `limits`：全局速率限制。
- `mechanism`：用于速率限制的机制，默认是 TokenBucket 算法。
- `exceededAction`：超出限制时应用的操作。

#### HttpConfiguration

包含机器人的 HTTP 客户端的配置。

- `requestTimeoutMillis`：请求超时（毫秒）。
- `connectTimeoutMillis`：连接超时（毫秒）。
- `socketTimeoutMillis`：套接字超时（毫秒）。
- `maxRequestRetry`：HTTP 请求的最大重试次数。
- `retryStrategy`：重试策略，可自定义。
- `retryDelay`：每次重试的超时乘数。
- `proxy`：HTTP 调用的代理设置。
- `additionalHeaders`：应用于每个请求的头部。

#### LoggingConfiguration

管理机器人操作和 HTTP 请求的日志级别。

- `botLogLevel`：机器人操作的日志级别。
- `httpLogLevel`：HTTP 请求的日志级别。

#### UpdatesListenerConfiguration

配置与拉取更新相关的参数。

- `dispatcher`：用于收集传入更新的调度器。
- `processingDispatcher`：用于处理更新的调度器。
- `pullingDelay`：每次拉取请求后的延迟。
- `updatesPollingTimeout`：长轮询机制的超时选项。

#### CommandParsingConfiguration

指定命令解析的参数。

- `commandDelimiter`：命令和参数之间的分隔符。
- `parametersDelimiter`：参数之间的 分隔符。
- `parameterValueDelimiter`：参数的键和值之间的分隔符。
- `restrictSpacesInCommands`：指示是否将命令中的空格视为命令的结束。
- `useIdentifierInGroupCommands`：使用机器人的标识符来匹配包含 @ 的命令。

### 示例配置

以下是如何使用这些类配置机器人的示例：

```kotlin
val bot = TelegramBot("TOKEN") {
    identifier = "MyBot"
    apiHost = "https://api.telegram.org"
    isTestEnv = true
    inputListener = InputListenerMapImpl()
    classManager = ClassManagerImpl()

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

此配置为机器人设置了特定的标识符，启用了测试环境模式，配置了速率限制、HTTP 客户端设置、日志记录级别、更新监听器参数和命令解析规则。

通过利用这些配置选项，开发人员可以微调他们的机器人以满足特定要求，并在各种操作场景中优化性能。