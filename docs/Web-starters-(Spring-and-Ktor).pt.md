---
---
title: Web Starters (Spring And Ktor)
---

### Spring starter

O módulo Spring Starter para a biblioteca é um módulo de auto‑configuração que integra as funcionalidades de bot do Telegram em aplicações Spring Boot. Ele aproveita o poder da injeção de dependências e das propriedades de configuração do Spring Boot para configurar automaticamente bots do Telegram com base nas configurações fornecidas. Esta biblioteca é particularmente útil para desenvolvedores que desejam criar bots do Telegram usando Kotlin e Spring Boot, oferecendo uma abordagem simplificada para desenvolvimento e gerenciamento de bots.

### Key Features

- **Auto-Configuration**: A biblioteca configura automaticamente bots do Telegram com base nas propriedades de configuração fornecidas, eliminando a necessidade de configuração manual.
- **Configuration Properties**: Suporta propriedades de configuração para fácil personalização das definições do bot, como tokens, nomes de pacotes e identificadores.
- **Spring Integration**: Integra-se perfeitamente ao ecossistema Spring, utilizando a injeção de dependências e o contexto de aplicação do Spring para gerenciar instâncias de bot.
- **Coroutine Support**: Aproveita corrotinas Kotlin para operações assíncronas de bot, garantindo execução eficiente e não bloqueante.

### Getting Started

Para usar a Spring Starter Library para Bots do Telegram, você precisa incluí‑la como dependência no seu projeto Spring Boot. A biblioteca foi projetada para funcionar com aplicações Spring Boot e requer o framework Spring Boot para operar.

#### Dependency

Adicione a dependência a seguir no seu arquivo `build.gradle` ou `pom.xml`:

```gradle
dependencies {
    implementation 'eu.vendeli:spring-starter:<version>'
}
```

Substitua `<version>` pela versão mais recente da biblioteca.

#### Configuration

A biblioteca usa `@ConfigurationProperties` do Spring Boot para fazer o binding das propriedades de configuração. Você pode definir as configurações do seu bot no arquivo `application.properties` ou `application.yml` da sua aplicação Spring Boot.

```yaml
ktgram:
 autoStartPolling: true
 shareHttpClient: true
 bot:
    - token: YOUR_BOT_TOKEN
      pckg: com.example.bot
      identifier: MyBot
```

#### Usage

Uma vez que a biblioteca esteja incluída e configurada, ela cria e configura automaticamente instâncias de bot do Telegram com base nas configurações fornecidas.

Ela também suporta múltiplas instâncias de bot; para inicializar várias basta declará‑las como novas entradas na seção bot:

```yaml
ktgram:
 bot:
    - token: YOUR_BOT_TOKEN
    - token: SECOND_BOT_TOKEN
```

### Advanced Configuration

Para configurações mais avançadas, como personalizar o comportamento do bot ou integrar com outros componentes Spring, você pode estender a classe `BotConfiguration` e alterar a configuração do bot através do método `applyCfg`. Veja um exemplo [aqui](https://github.com/vendelieu/telegram-bot_template/blob/spring-bot/src/main/kotlin/com/example/springbot/configuration/BotConfig.kt).

> [!TIP]
> Para configurar cada instância inicializada com uma configuração personalizada, distinga‑as pelo seu identificador (a classe BotConfiguration também possui um identificador).

### Ktor

O módulo foi projetado para facilitar a criação de um servidor webhook para bots do Telegram. Ele permite que desenvolvedores configurem o servidor, incluindo as definições SSL/TLS, e declarem múltiplos bots do Telegram com configurações personalizadas. O processo de configuração é flexível, permitindo que os desenvolvedores adaptem o servidor às suas necessidades específicas.

### Installation

Para instalar o ktor starter, adicione o seguinte à dependência principal:

```gradle
dependencies {
    implementation("eu.vendeli:ktor-starter:x.y.z") // there
    // change x.y.z to current library version
}
```

### Key Components

`serveWebhook` Function

A função `serveWebhook` é o núcleo da biblioteca. Ela configura e inicia o servidor webhook para bots do Telegram. Aceita dois parâmetros:

- `wait`: Um booleano indicando se o servidor deve aguardar a aplicação parar antes de encerrar. O padrão é true.
- `serverBuilder`: Uma função lambda que configura o servidor. O padrão é uma lambda vazia.

### Configuration

* `WEBHOOK_PREFIX`: parâmetro usado como prefixo de endereço para a rota do listener webhook. (padrão “/”)

#### Server Setup

- `server`: Método para definir a configuração do servidor usando `EnvConfiguration` ou `ManualConfiguration`.
- `engine`: Método para configurar o motor de aplicação Netty.
- `ktorModule`: Método para adicionar módulos Ktor à aplicação.

A biblioteca oferece ampla gama de parâmetros configuráveis para o servidor, incluindo host, porta, configurações SSL e mais. Existem duas opções concretas para sua configuração:

* `EnvConfiguration`: Lê valores de configuração do ambiente com prefixo `KTGRAM_`.
* `ManualConfiguration`: Permite definir manualmente os valores de configuração, configure seus parâmetros na função `server {}`.

Segue a lista de parâmetros que podem ser definidos:

- `HOST`: Nome do host ou endereço IP do servidor.
- `PORT`: Número da porta do servidor.
- `SSL_PORT`: Número da porta para conexões SSL/TLS.
- `PEM_PRIVATE_KEY_PATH`: Caminho para o arquivo PEM da chave privada.
- `PEM_CHAIN_PATH`: Caminho para o arquivo PEM da cadeia de certificados.
- `PEM_PRIVATE_KEY`: SENHA da chave privada PEM como array de caracteres.
- `KEYSTORE_PATH`: Caminho para o arquivo Java KeyStore.
- `KEYSTORE_PASSWORD`: Senha do KeyStore.
- `KEY_ALIAS`: Alias da chave no KeyStore.
- `SSL_ON`: Booleano indicando se SSL/TLS deve estar habilitado. O padrão é true.

> [!TIP]
> Se certificados PEM estiverem presentes, o próprio módulo criará um armazenamento jks a partir deles no caminho especificado.

#### Bot Configuration:

Para configurar o bot, chame `declareBot {}` que possui os seguintes parâmetros:

- `token`: O token do bot.
- `pckg`: O nome do pacote do bot.
- `configuration`: Função lambda para configurar o bot.
- `handlingBehaviour`: Função lambda para definir o comportamento de tratamento do bot.
- `onInit`: Função lambda a ser executada quando o bot for inicializado.

### Example Usage

Para usar este módulo, chame a função `serveWebhook`, configure‑a com as definições desejadas e declare seus bots. Veja um exemplo simplificado:

```kotlin
fun main() = runBlocking {
    serveWebhook {
        server {
            HOST = "0.0.0.0"
            PORT = 8080
            SSL_PORT = 8443

            PEM_PRIVATE_KEY_PATH = "/etc/letsencrypt/live/example.com/privkey.pem"
            PEM_CHAIN_PATH = "/etc/letsencrypt/live/example.com/fullchain.pem"
            PEM_PRIVATE_KEY = "pem_changeit".toCharArray()

            KEYSTORE_PATH = "/etc/ssl/certs/java/cacerts/bot_keystore.jks"
            KEYSTORE_PASSWORD = "changeit".toCharArray()
            // Set other configuration parameters as needed
        }
        declareBot {
            token = "YOUR_BOT_TOKEN"
            // Configure other bot settings
        }
        // Add more bots or set other parameters if needed
    }
}
```

> [!CAUTION]
> Não se esqueça de definir o webhook para que tudo funcione. :)

Por padrão o módulo servirá endpoints de listener webhook como `host/BOT_TOKEN`


---