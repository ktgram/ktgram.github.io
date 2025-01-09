Library provides plenty of configuration options, you can see api reference in the [`BotConfiguration`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.internal.configuration/-bot-configuration/index.html) class description.

There are also two approaches to configuring the bot:

# Configurator lambda

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

# ConfigLoader interface

There is also the ability to configure through a special [`ConfigLoader`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.helper/-config-loader/index.html) interface,\
 which you can use to load settings from external sources (`properties`, `command line args`, etc.).

The implementation of this interface can be passed through a secondary constructor and the instance will be configured accordingly.

```kotlin
val bot = TelegramBot(ConfigLoaderImpl)
```

Currently there's several modules provided that implements this interface like `ktgram-config-env`, `ktgram-config-toml`.

# BotConfiguration Overview

### BotConfiguration

The `BotConfiguration` class is the central hub for configuring a bot. It includes properties for identifying the bot, setting up the API host, determining whether the bot operates in a test environment, handling inputs, managing classes, and controlling input auto-removal. Additionally, it provides internal properties for rate limiting, HTTP client configuration, logging, update listening, and command parsing.

#### Properties

- `identifier`: Identifies different bot instances during multi-bot processing.
- `apiHost`: Host of the Telegram API.
- `isTestEnv`: Flag indicating whether the bot operates in a test environment.
- `inputListener`: Instance of the input handling class.
- `classManager`: Manager used to get classes.
- `inputAutoRemoval`: Flag regulating the auto-deletion of the input point during processing.
- `exceptionHandlingStrategy`: Defines the strategy for handling exceptions.
    * `CollectToChannel` - Collect to `TgUpdateHandler.caughtExceptions`.
    * `Throw` - Throw again wrapped with `TgException`.
    * `DoNothing` - Do nothing :)
    * `Handle` - Set custom handler.
- `throwExOnActionsFailure`: Throws an exception when any bot request fails.

#### Configuration Blocks

`BotConfiguration` also offers functions to configure its internal components:

- `httpClient(block: HttpConfiguration.() -> Unit)`: Configures the HTTP client.
- `logging(block: LoggingConfiguration.() -> Unit)`: Configures logging.
- `rateLimiter(block: RateLimiterConfiguration.() -> Unit)`: Configures request limiting.
- `updatesListener(block: UpdatesListenerConfiguration.() -> Unit)`: Configures the updates listener.
- `commandParsing(block: CommandParsingConfiguration.() -> Unit)`: Specifies command parsing pattern.

## Associated Configuration Classes

### RateLimiterConfiguration

Configures global rate limiting.

- `limits`: Global rate limits.
- `mechanism`: Mechanism used for rate limiting, default is TokenBucket algorithm.
- `exceededAction`: Action applied when the limit is exceeded.

### HttpConfiguration

Contains configuration for the bot's HTTP client.

- `requestTimeoutMillis`: Request timeout in milliseconds.
- `connectTimeoutMillis`: Connection timeout in milliseconds.
- `socketTimeoutMillis`: Socket timeout in milliseconds.
- `maxRequestRetry`: Maximum retry for HTTP requests.
- `retryStrategy`: Strategy for retries, customizable.
- `retryDelay`: Multiplier for timeout at each retry.
- `proxy`: Proxy settings for HTTP calls.
- `additionalHeaders`: Headers applied to every request.

### LoggingConfiguration

Manages logging levels for bot actions and HTTP requests.

- `botLogLevel`: Level of logs for bot actions.
- `httpLogLevel`: Level of logs for HTTP requests.

### UpdatesListenerConfiguration

Configures parameters related to pulling updates.

- `dispatcher`: Dispatcher for collecting incoming updates.
- `processingDispatcher`: Dispatcher for processing updates.
- `pullingDelay`: Delay after each pulling request.
- `updatesPollingTimeout`: Timeout option for long-polling mechanism.

### CommandParsingConfiguration

Specifies parameters for command parsing.

- `commandDelimiter`: Separator between command and parameters.
- `parametersDelimiter`: Separator between parameters.
- `parameterValueDelimiter`: Separator between key and value of parameter.
- `restrictSpacesInCommands`: Flag indicating if spaces in commands should be treated as the end of the command.
- `useIdentifierInGroupCommands`: Uses bot's identifier to match commands containing @.

## Example Configuration

Here's an example of how to configure a bot using these classes:

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

This configuration sets up a bot with specific identifiers, enables test environment mode, configures rate limiting, HTTP client settings, logging levels, update listener parameters, and command parsing rules.

By leveraging these configuration options, developers can fine-tune their bots to meet specific requirements and optimize performance across various operational scenarios.