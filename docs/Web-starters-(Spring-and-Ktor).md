---
title: Web-Starters-(Spring-And-Ktor)
---

# Spring starter

The Spring Starter module for library is an auto-configuration module that integrates Telegram bot functionalities into Spring Boot applications. It leverages the power of Spring Boot's dependency injection and configuration properties to automatically configure Telegram bots based on the provided configuration. This library is particularly useful for developers looking to build Telegram bots using Kotlin and Spring Boot, offering a streamlined approach to bot development and management.

## Key Features

- **Auto-Configuration**: The library automatically configures Telegram bots based on the provided configuration properties, eliminating the need for manual setup.
- **Configuration Properties**: It supports configuration properties for easy customization of bot settings, such as bot tokens, package names, and identifiers.
- **Spring Integration**: Seamlessly integrates with the Spring ecosystem, utilizing Spring's dependency injection and application context for managing bot instances.
- **Coroutine Support**: Leverages Kotlin coroutines for asynchronous bot operations, ensuring efficient and non-blocking execution.

## Getting Started

To use the Spring Starter Library for Telegram Bots, you need to include it as a dependency in your Spring Boot project. The library is designed to work with Spring Boot applications and requires the Spring Boot framework to function.

### Dependency

Add the following dependency to your `build.gradle` or `pom.xml` file:

```gradle
dependencies {
    implementation 'eu.vendeli:spring-starter:<version>'
}
```

Replace `<version>` with the latest version of the library.

### Configuration

The library uses Spring Boot's `@ConfigurationProperties` to bind configuration properties. You can define your bot configurations in the `application.properties` or `application.yml` file of your Spring Boot application.

```yaml
ktgram:
 autoStartPolling: true
 shareHttpClient: true
 bot:
    - token: YOUR_BOT_TOKEN
      pckg: com.example.bot
      identifier: MyBot
```

### Usage

Once the library is included and configured, it automatically creates and configures Telegram bot instances based on the provided configuration.

It also supports multiple bot instances, to initialize several ones just declare it as new entry in bot section:

```yaml
ktgram:
 bot:
    - token: YOUR_BOT_TOKEN
    - token: SECOND_BOT_TOKEN
```

## Advanced Configuration

For more advanced configurations, such as customizing bot behavior or integrating with other Spring components, you can extend the `BotConfiguration` class and change bot configuration through its `applyCfg` method, you can see example [there](https://github.com/vendelieu/telegram-bot_template/blob/spring-bot/src/main/kotlin/com/example/springbot/configuration/BotConfig.kt).

> [!TIP]
> To configure each initialized instance with a custom configuration, distinguish them by their identifier (the BotConfiguration class also has an identifier).

# Ktor

The module is designed to facilitate the creation of a webhook server for Telegram bots. It allows developers to configure the server, including SSL/TLS settings, and declare multiple Telegram bots with custom configurations. The setup process is flexible, enabling developers to tailor the server to their specific needs.

## Installation

To install ktor starter add additional to main dependency:

```gradle
dependencies {
    implementation("eu.vendeli:ktor-starter:x.y.z") // there
    // change x.y.z to current library version
}
```

## Key Components

`serveWebhook` Function

The serveWebhook function is the core of the library. It sets up and starts the webhook server for Telegram bots. It accepts two parameters:

- `wait`: A boolean indicating whether the server should wait for the application to stop before shutting down. Defaults to true.
- `serverBuilder`: A lambda function that configures the server. Defaults to an empty lambda.

# Configuration

* `WEBHOOK_PREFIX`: it's paramter that will be used for address prefix for webhook listener route. (defaults to "/")

### Server Setup

- `server`: A method to set the server configuration using either EnvConfiguration or ManualConfiguration.
- `engine`: A method to configure the Netty application engine.
- `ktorModule`: A method to add Ktor modules to the application.

The library provides wide range of configurable parameters for the server, including host, port, SSL settings, and more. There are two concrete options for its configuring: 

* `EnvConfiguration`: Reads configuration values from environment with `KTGRAM_` prefix.
* `ManualConfiguration`: Allows for manual setting of configuration values, set your parameters in `server {}` function.

There's list of parameters that can be set:

- `HOST`: The hostname or IP address of the server.
- `PORT`: The port number for the server.
- `SSL_PORT`: The port number for SSL/TLS connections.
- `PEM_PRIVATE_KEY_PATH`: The path to the PEM private key file.
- `PEM_CHAIN_PATH`: The path to the PEM certificate chain file.
- `PEM_PRIVATE_KEY`: The PEM private key PASSWORD as a character array.
- `KEYSTORE_PATH`: The path to the Java KeyStore file.
- `KEYSTORE_PASSWORD`: The password for the KeyStore.
- `KEY_ALIAS`: The alias for the key in the KeyStore.
- `SSL_ON`: A boolean indicating whether SSL/TLS should be enabled. Defaults to true.

> [!TIP]
> If pem certificates are present, the module itself will create a jks storage from them at the specified path.

### Bot Configuration:

To configure bot call `declareBot {}` which have such parameters:

- `token`: The bot token.
- `pckg`: The package name for the bot.
- `configuration`: A lambda function for configuring the bot.
- `handlingBehaviour`: A lambda function for setting the bot's handling behavior.
- `onInit`: A lambda function to be executed when the bot is initialized.

## Example Usage

To use this module, call `serveWebhook` function, configure it with your desired settings, declare your bots. Here's a simplified example:

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
> Don't forget to set webhook to make everything work. :)

By default module will serve webhook listenening endpoints as `host/BOT_TOKEN`

