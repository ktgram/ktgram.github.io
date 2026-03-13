---
---
title: Конфигурация бота
---

Библиотека предоставляет множество опций конфигурации, вы можете ознакомиться с API в описании класса [`BotConfiguration`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.configuration/-bot-configuration/index.html).

Существует также два подхода к конфигурированию бота:

### Lambda Configurator

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

### Интерфейс ConfigLoader

Также существует возможность конфигурирования через специальный интерфейс [`ConfigLoader`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.helper/-config-loader/index.html),<br/> который вы можете использовать для загрузки настроек из внешних источников (`properties`, `command line args` и т.д.).

Реализация этого интерфейса может быть передана через вторичный конструктор и экземпляр будет сконфигурирован соответствующим образом.

```kotlin
val bot = TelegramBot(ConfigLoaderImpl)
```

В настоящее время предоставлено несколько модулей, реализующих этот интерфейс, таких как `ktgram-config-env`, `ktgram-config-toml`.

### Обзор BotConfiguration

#### BotConfiguration

Класс `BotConfiguration` является центральным узлом для конфигурирования бота. Он включает свойства для идентификации бота, настройки хоста API, определения того, работает ли бот в тестовой среде, обработки входных данных, управления классами и контроля автоудаления входных данных. Кроме того, он предоставляет внутренние свойства для ограничения частоты запросов, конфигурации HTTP-клиента, логирования, прослушивания обновлений и разбора команд.

##### Свойства

- `identifier`: Идентифицирует различные экземпляры бота во время мультиботовой обработки.
- `apiHost`: Хост Telegram API.
- `isTestEnv`: Флаг, указывающий работает ли бот в тестовой среде.
- `inputListener`: Экземпляр класса обработки входных данных.
- `classManager`: Менеджер, используемый для получения классов.
- `inputAutoRemoval`: Флаг, регулирующий автоудаление точки входа во время обработки.
- `exceptionHandlingStrategy`: Определяет стратегию обработки исключений.
    * `CollectToChannel` - Собирать в `TgUpdateHandler.caughtExceptions`.
    * `Throw` - Бросать снова, обернутым в `TgException`.
    * `DoNothing` - Ничего не делать :)
    * `Handle` - Установить пользовательский обработчик.
- `throwExOnActionsFailure`: Бросает исключение когда любой запрос бота завершается неудачей.

##### Блоки конфигурации

`BotConfiguration` также предлагает функции для конфигурирования своих внутренних компонентов:

- `httpClient(block: HttpConfiguration.() -> Unit)`: Конфигурирует HTTP-клиент.
- `logging(block: LoggingConfiguration.() -> Unit)`: Конфигурирует логирование.
- `rateLimiter(block: RateLimiterConfiguration.() -> Unit)`: Конфигурирует ограничение частоты запросов.
- `updatesListener(block: UpdatesListenerConfiguration.() -> Unit)`: Конфигурирует прослушиватель обновлений.
- `commandParsing(block: CommandParsingConfiguration.() -> Unit)`: Указывает шаблон разбора команд.

### Связанные классы конфигурации

#### RateLimiterConfiguration

Конфигурирует глобальное ограничение частоты запросов.

- `limits`: Глобальные ограничения частоты запросов.
- `mechanism`: Механизм, используемый для ограничения частоты запросов, по умолчанию используется алгоритм TokenBucket.
- `exceededAction`: Действие, применяемое когда лимит превышен.

#### HttpConfiguration

Содержит конфигурацию для HTTP-клиента бота.

- `requestTimeoutMillis`: Таймаут запроса в миллисекундах.
- `connectTimeoutMillis`: Таймаут подключения в миллисекундах.
- `socketTimeoutMillis`: Таймаут сокета в миллисекундах.
- `maxRequestRetry`: Максимальное количество повторных попыток для HTTP-запросов.
- `retryStrategy`: Стратегия для повторных попыток, настраиваемая.
- `retryDelay`: Множитель для таймаута при каждой повторной попытке.
- `proxy`: Настройки прокси для HTTP-вызовов.
- `additionalHeaders`: Заголовки, применяемые к каждому запросу.

#### LoggingConfiguration

Управляет уровнями логирования для действий бота и HTTP-запросов.

- `botLogLevel`: Уровень логов для действий бота.
- `httpLogLevel`: Уровень логов для HTTP-запросов.

#### UpdatesListenerConfiguration

Конфигурирует параметры, связанные с получением обновлений.

- `dispatcher`: Диспетчер для сбора входящих обновлений.
- `processingDispatcher`: Диспетчер для обработки обновлений.
- `pullingDelay`: Задержка после каждого запроса на получение.
- `updatesPollingTimeout`: Таймаут опции для механизма длинного опроса.

#### CommandParsingConfiguration

Задает параметры для разбора команд.

- `commandDelimiter`: Разделитель между командой и параметрами.
- `parametersDelimiter`: Разделитель между параметрами.
- `parameterValueDelimiter`: Разделитель между ключом и значением параметра.
- `restrictSpacesInCommands`: Флаг, указывающий следует ли рассматривать пробелы в командах как конец команды.
- `useIdentifierInGroupCommands`: Использует идентификатор бота для сопоставления команд, содержащих @.

### Пример конфигурации

Вот пример того, как сконфигурировать бота с использованием этих классов:

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

Эта конфигурация устанавливает бот с конкретными идентификаторами, включает режим тестовой среды, конфигурирует ограничение частоты запросов, настройки HTTP-клиента, уровни логирования, параметры прослушивателя обновлений и правила разбора команд.

Используя эти опции конфигурации, разработчики могут точно настроить своих ботов для удовлетворения конкретных требований и оптимизации производительности в различных сценариях эксплуатации.
---