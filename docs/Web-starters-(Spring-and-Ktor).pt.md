---
---
title: Web Starters (Spring And Ktor)
---

### Spring starter

O módulo Spring Starter para a biblioteca é um módulo de auto-configuração que integra funcionalidades de bots do Telegram em aplicações Spring Boot. Ele aproveita o poder da injeção de dependência e propriedades de configuração do Spring Boot para configurar automaticamente bots do Telegram com base na configuração fornecida. Esta biblioteca é particularmente útil para desenvolvedores que desejam construir bots do Telegram usando Kotlin e Spring Boot, oferecendo uma abordagem simplificada para desenvolvimento e gerenciamento de bots.

### Principais Recursos

- **Auto-Configuração**: A biblioteca configura automaticamente bots do Telegram com base nas propriedades de configuração fornecidas, eliminando a necessidade de configuração manual.
- **Propriedades de Configuração**: Suporta propriedades de configuração para fácil personalização de configurações de bot, como tokens de bot, nomes de pacotes e identificadores.
- **Integração Spring**: Integra-se perfeitamente com o ecossistema Spring, utilizando a injeção de dependência e contexto de aplicação do Spring para gerenciar instâncias de bot.
- **Suporte a Coroutines**: Aproveita as coroutines do Kotlin para operações assíncronas de bot, garantindo execução eficiente e não bloqueante.

### Começando

Para usar a Biblioteca Spring Starter para Bots do Telegram, você precisa incluí-la como dependência no seu projeto Spring Boot. A biblioteca foi projetada para funcionar com aplicações Spring Boot e requer o framework Spring Boot para funcionar.

#### Dependência

Adicione a seguinte dependência ao seu arquivo `build.gradle` ou `pom.xml`:

```gradle
dependencies {
    implementation 'eu.vendeli:spring-starter:<version>'
}
```

Substitua `<version>` pela versão mais recente da biblioteca.

#### Configuração

A biblioteca usa `@ConfigurationProperties` do Spring Boot para vincular propriedades de configuração. Você pode definir suas configurações de bot no arquivo `application.properties` ou `application.yml` da sua aplicação Spring Boot.

```yaml
ktgram:
 autoStartPolling: true
 shareHttpClient: true
 bot:
    - token: YOUR_BOT_TOKEN
      pckg: com.example.bot
      identifier: MyBot
```

#### Uso

Uma vez que a biblioteca esteja incluída e configurada, ela cria e configura automaticamente instâncias de bots do Telegram com base na configuração fornecida.

Ela também suporta múltiplas instâncias de bot, para inicializar várias basta declará-las como nova entrada na seção bot:

```yaml
ktgram:
 bot:
    - token: YOUR_BOT_TOKEN
    - token: SECOND_BOT_TOKEN
```

### Configuração Avançada

Para configurações mais avançadas, como personalizar o comportamento do bot ou integrar com outros componentes Spring, você pode estender a classe `BotConfiguration` e alterar a configuração do bot através do seu método `applyCfg`, você pode ver um exemplo [aqui](https://github.com/vendelieu/telegram-bot_template/blob/spring-bot/src/main/kotlin/com/example/springbot/configuration/BotConfig.kt).

> [!TIP]
> Para configurar cada instância inicializada com uma configuração personalizada, distinga-as por seu identificador (a classe BotConfiguration também tem um identificador).

### Ktor

O módulo foi projetado para facilitar a criação de um servidor webhook para bots do Telegram. Ele permite que os desenvolvedores configurem o servidor, incluindo configurações SSL/TLS, e declarem múltiplos bots do Telegram com configurações personalizadas. O processo de configuração é flexível, permitindo que os desenvolvedores adaptem o servidor às suas necessidades específicas.

### Instalação

Para instalar o starter do ktor, adicione adicionalmente à dependência principal:

```gradle
dependencies {
    implementation("eu.vendeli:ktor-starter:x.y.z") // there
    // change x.y.z to current library version
}
```

### Principais Componentes

Função `serveWebhook`

A função serveWebhook é o núcleo da biblioteca. Ela configura e inicia o servidor webhook para bots do Telegram. Ela aceita dois parâmetros:

- `wait`: Um booleano indicando se o servidor deve esperar o aplicativo parar antes de desligar. Padrão é true.
- `serverBuilder`: Uma função lambda que configura o servidor. Padrão é uma lambda vazia.

### Configuração

* `WEBHOOK_PREFIX`: é o parâmetro que será usado como prefixo de endereço para a rota do listener do webhook. (padrão é "/")

#### Configuração do Servidor

- `server`: Um método para definir a configuração do servidor usando `EnvConfiguration` ou `ManualConfiguration`.
- `engine`: Um método para configurar o motor de aplicação Netty.
- `ktorModule`: Um método para adicionar módulos Ktor à aplicação.

A biblioteca fornece uma ampla gama de parâmetros configuráveis para o servidor, incluindo host, porta, configurações SSL e mais. Existem duas opções concretas para sua configuração:

* `EnvConfiguration`: Lê valores de configuração do ambiente com prefixo `KTGRAM_`.
* `ManualConfiguration`: Permite configuração manual de valores de configuração, defina seus parâmetros na função `server {}`.

Há uma lista de parâmetros que podem ser definidos:

- `HOST`: O hostname ou endereço IP do servidor.
- `PORT`: O número da porta para o servidor.
- `SSL_PORT`: O número da porta para conexões SSL/TLS.
- `PEM_PRIVATE_KEY_PATH`: O caminho para o arquivo da chave privada PEM.
- `PEM_CHAIN_PATH`: O caminho para o arquivo da cadeia de certificados PEM.
- `PEM_PRIVATE_KEY`: A SENHA da chave privada PEM como um array de caracteres.
- `KEYSTORE_PATH`: O caminho para o arquivo Java KeyStore.
- `KEYSTORE_PASSWORD`: A senha para o KeyStore.
- `KEY_ALIAS`: O alias para a chave no KeyStore.
- `SSL_ON`: Um booleano indicando se SSL/TLS deve ser habilitado. Padrão é true.

> [!TIP]
> Se certificados pem estiverem presentes, o módulo em si criará um armazenamento jks a partir deles no caminho especificado.

#### Configuração do Bot:

Para configurar o bot, chame `declareBot {}` que tem tais parâmetros:

- `token`: O token do bot.
- `pckg`: O nome do pacote para o bot.
- `configuration`: Uma função lambda para configurar o bot.
- `handlingBehaviour`: Uma função lambda para definir o comportamento de manipulação do bot.
- `onInit`: Uma função lambda a ser executada quando o bot for inicializado.

### Exemplo de Uso

Para usar este módulo, chame a função `serveWebhook`, configure-a com suas configurações desejadas, declare seus bots. Aqui está um exemplo simplificado:

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
> Não se esqueça de configurar o webhook para fazer tudo funcionar. :)

Por padrão, o módulo servirá endpoints de listening de webhook como `host/BOT_TOKEN`


---