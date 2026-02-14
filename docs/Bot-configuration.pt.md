---
---
title: Configuração do Bot
---

A biblioteca oferece muitas opções de configuração, você pode ver a referência da API na descrição da classe [`BotConfiguration`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.configuration/-bot-configuration/index.html).

Há também duas abordagens para configurar o bot:

### Lambda do Configurator

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

### Interface ConfigLoader

Há também a capacidade de configurar através de uma interface especial [`ConfigLoader`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.helper/-config-loader/index.html),<br/> que você pode usar para carregar configurações de fontes externas (`properties`, `command line args`, etc.).

A implementação desta interface pode ser passada através de um construtor secundário e a instância será configurada de acordo.

```kotlin
val bot = TelegramBot(ConfigLoaderImpl)
```

Atualmente há vários módulos fornecidos que implementam esta interface como `ktgram-config-env`, `ktgram-config-toml`.

### Visão Geral do BotConfiguration

#### BotConfiguration

A classe `BotConfiguration` é o centro principal para configurar um bot. Ela inclui propriedades para identificar o bot, configurar o host da API, determinar se o bot opera em um ambiente de teste, lidar com entradas, gerenciar classes e controlar a remoção automática de entradas. Além disso, ela fornece propriedades internas para limitação de taxa, configuração do cliente HTTP, logging, escuta de atualizações e análise de comandos.

##### Propriedades

- `identifier`: Identifica diferentes instâncias de bot durante o processamento multi-bot.
- `apiHost`: Host da API do Telegram.
- `isTestEnv`: Flag indicando se o bot opera em um ambiente de teste.
- `inputListener`: Instância da classe de tratamento de entrada.
- `classManager`: Gerenciador usado para obter classes.
- `inputAutoRemoval`: Flag regulando a exclusão automática do ponto de entrada durante o processamento.
- `exceptionHandlingStrategy`: Define a estratégia para tratamento de exceções.
    * `CollectToChannel` - Coleta para `TgUpdateHandler.caughtExceptions`.
    * `Throw` - Lança novamente envolvido com `TgException`.
    * `DoNothing` - Não faz nada :)
    * `Handle` - Define um manipulador personalizado.
- `throwExOnActionsFailure`: Lança uma exceção quando qualquer solicitação do bot falha.

##### Blocos de Configuração

O `BotConfiguration` também oferece funções para configurar seus componentes internos:

- `httpClient(block: HttpConfiguration.() -> Unit)`: Configura o cliente HTTP.
- `logging(block: LoggingConfiguration.() -> Unit)`: Configura logging.
- `rateLimiter(block: RateLimiterConfiguration.() -> Unit)`: Configura limitação de solicitações.
- `updatesListener(block: UpdatesListenerConfiguration.() -> Unit)`: Configura o escutador de atualizações.
- `commandParsing(block: CommandParsingConfiguration.() -> Unit)`: Especifica o padrão de análise de comandos.

### Classes de Configuração Associadas

#### RateLimiterConfiguration

Configura limitação global de taxa.

- `limits`: Limites globais de taxa.
- `mechanism`: Mecanismo usado para limitação de taxa, o padrão é o algoritmo TokenBucket.
- `exceededAction`: Ação aplicada quando o limite é excedido.

#### HttpConfiguration

Contém configuração para o cliente HTTP do bot.

- `requestTimeoutMillis`: Timeout de solicitação em milissegundos.
- `connectTimeoutMillis`: Timeout de conexão em milissegundos.
- `socketTimeoutMillis`: Timeout de socket em milissegundos.
- `maxRequestRetry`: Máximo de tentativas para solicitações HTTP.
- `retryStrategy`: Estratégia para tentativas, personalizável.
- `retryDelay`: Multiplicador para timeout em cada tentativa.
- `proxy`: Configurações de proxy para chamadas HTTP.
- `additionalHeaders`: Headers aplicados a cada solicitação.

#### LoggingConfiguration

Gerencia níveis de logging para ações do bot e solicitações HTTP.

- `botLogLevel`: Nível de logs para ações do bot.
- `httpLogLevel`: Nível de logs para solicitações HTTP.

#### UpdatesListenerConfiguration

Configura parâmetros relacionados à obtenção de atualizações.

- `dispatcher`: Dispatcher para coletar atualizações recebidas.
- `processingDispatcher`: Dispatcher para processar atualizações.
- `pullingDelay`: Delay após cada solicitação de obtenção.
- `updatesPollingTimeout`: Opção de timeout para mecanismo de long-polling.

#### CommandParsingConfiguration

Especifica parâmetros para análise de comandos.

- `commandDelimiter`: Separador entre comando e parâmetros.
- `parametersDelimiter`: Separador entre parâmetros.
- `parameterValueDelimiter`: Separador entre chave e valor do parâmetro.
- `restrictSpacesInCommands`: Flag indicando se espaços em comandos devem ser tratados como fim do comando.
- `useIdentifierInGroupCommands`: Usa o identificador do bot para corresponder comandos contendo @.

### Exemplo de Configuração

Aqui está um exemplo de como configurar um bot usando estas classes:

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

Esta configuração configura um bot com identificadores específicos, habilita o modo de ambiente de teste, configura limitação de taxa, configurações do cliente HTTP, níveis de logging, parâmetros do escutador de atualizações e regras de análise de comandos.

Ao aproveitar estas opções de configuração, os desenvolvedores podem ajustar seus bots para atender requisitos específicos e otimizar o desempenho em vários cenários operacionais.
---