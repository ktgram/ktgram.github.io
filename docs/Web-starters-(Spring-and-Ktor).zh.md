---
---
title: Web Starters (Spring And Ktor)
---

### Spring starter

Spring Starter模块是一个自动配置模块，用于将Telegram bot功能集成到Spring Boot应用程序中。它利用了Spring Boot的依赖注入和配置属性功能，根据提供的配置自动配置Telegram bot。这个库对于希望使用Kotlin和Spring Boot构建Telegram bot的开发者特别有用，提供了一种流畅的bot开发和管理方法。

### 主要特性

- **自动配置**: 库根据提供的配置属性自动配置Telegram bot，无需手动设置。
- **配置属性**: 支持配置属性以便轻松自定义bot设置，例如bot令牌、包名和标识符。
- **Spring集成**: 与Spring生态系统无缝集成，利用Spring的依赖注入和应用上下文管理bot实例。
- **协程支持**: 利用Kotlin协程进行异步bot操作，确保高效且非阻塞的执行。

### 入门指南

要使用Spring Starter Library for Telegram Bots，您需要在Spring Boot项目中将其作为依赖项包含。该库设计为与Spring Boot应用程序一起工作，需要Spring Boot框架才能正常运行。

#### 依赖项

将以下依赖项添加到您的 `build.gradle` 或 `pom.xml` 文件中：

```gradle
dependencies {
    implementation 'eu.vendeli:spring-starter:<version>'
}
```

将 `<version>` 替换为库的最新版本。

#### 配置

该库使用Spring Boot的 `@ConfigurationProperties` 来绑定配置属性。您可以在Spring Boot应用程序的 `application.properties` 或 `application.yml` 文件中定义bot配置。

```yaml
ktgram:
 autoStartPolling: true
 shareHttpClient: true
 bot:
    - token: YOUR_BOT_TOKEN
      pckg: com.example.bot
      identifier: MyBot
```

#### 使用方法

包含并配置库后，它会根据提供的配置自动创建和配置Telegram bot实例。

它还支持多个bot实例，要初始化多个实例，只需在bot部分声明新的条目：

```yaml
ktgram:
 bot:
    - token: YOUR_BOT_TOKEN
    - token: SECOND_BOT_TOKEN
```

### 高级配置

对于更高级的配置，如自定义bot行为或与其他Spring组件集成，您可以扩展 `BotConfiguration` 类并通过其 `applyCfg` 方法更改bot配置，您可以在[这里](https://github.com/vendelieu/telegram-bot_template/blob/spring-bot/src/main/kotlin/com/example/springbot/configuration/BotConfig.kt)看到示例。

> [!TIP]
> 要使用自定义配置配置每个初始化的实例，通过其标识符区分它们（BotConfiguration类也有标识符）。

### Ktor

该模块旨在促进为Telegram bot创建webhook服务器。它允许开发者配置服务器，包括SSL/TLS设置，并声明具有自定义配置的多个Telegram bot。设置过程灵活，使开发者能够根据具体需求定制服务器。

### 安装

要安装ktor starter，请在主依赖项中添加：

```gradle
dependencies {
    implementation("eu.vendeli:ktor-starter:x.y.z") // there
    // 将x.y.z更改为当前库版本
}
```

### 关键组件

`serveWebhook` 函数

serveWebhook函数是库的核心。它为Telegram bot设置和启动webhook服务器。它接受两个参数：

- `wait`: 一个布尔值，指示服务器是否应该在关闭之前等待应用程序停止。默认为true。
- `serverBuilder`: 一个lambda函数，用于配置服务器。默认为一个空lambda。

### 配置

* `WEBHOOK_PREFIX`: 它是一个参数，将用于webhook监听器路由的地址前缀。(默认为 "/")

#### 服务器设置

- `server`: 一种使用EnvConfiguration或ManualConfiguration设置服务器配置的方法。
- `engine`: 一种配置Netty应用引擎的方法。
- `ktorModule`: 一种将Ktor模块添加到应用程序的方法。

该库为服务器提供了广泛的可配置参数，包括主机、端口、SSL设置等。有两种具体的配置选项：

* `EnvConfiguration`: 从带有 `KTGRAM_` 前缀的环境中读取配置值。
* `ManualConfiguration`: 允许手动设置配置值，在 `server {}` 函数中设置参数。

以下是可以设置的参数列表：

- `HOST`: 服务器的主机名或IP地址。
- `PORT`: 服务器的端口号。
- `SSL_PORT`: SSL/TLS连接的端口号。
- `PEM_PRIVATE_KEY_PATH`: PEM私钥文件路径。
- `PEM_CHAIN_PATH`: PEM证书链文件路径。
- `PEM_PRIVATE_KEY`: 以字符数组形式表示的PEM私钥密码。
- `KEYSTORE_PATH`: Java密钥库文件路径。
- `KEYSTORE_PASSWORD`: 密钥库密码。
- `KEY_ALIAS`: 密钥库中密钥的别名。
- `SSL_ON`: 一个布尔值，指示是否应启用SSL/TLS。默认为true。

> [!TIP]
> 如果存在pem证书，模块本身将在指定路径创建jks存储。

#### Bot配置：

要配置bot，调用 `declareBot {}`，它有以下参数：

- `token`: Bot令牌。
- `pckg`: Bot的包名。
- `configuration`: 用于配置bot的lambda函数。
- `handlingBehaviour`: 用于设置bot处理行为的lambda函数。
- `onInit`: bot初始化时执行的lambda函数。

### 示例用法

要使用此模块，调用 `serveWebhook` 函数，使用所需设置进行配置，声明您的bot。这是一个简化的示例：

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
            // 根据需要设置其他配置参数
        }
        declareBot {
            token = "YOUR_BOT_TOKEN"
            // 配置其他bot设置
        }
        // 如有需要，添加更多bot或设置其他参数
    }
}
```

> [!CAUTION]
> 别忘了设置webhook以使一切正常工作。 :)

默认情况下，模块将webhook监听端点作为 `host/BOT_TOKEN` 提供


---