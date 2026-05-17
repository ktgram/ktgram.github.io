---
---
title: Web Starters (Spring And Ktor)
---

### Spring starter

Spring Starter 模块是一个自动配置模块，将 Telegram 机器人功能集成到 Spring Boot 应用中。它利用 Spring Boot 的依赖注入和配置属性的强大功能，基于提供的配置自动配置 Telegram 机器人。该库特别适用于希望使用 Kotlin 和 Spring Boot 构建 Telegram 机器人的开发者，提供了一种简化的机器人开发和管理方法。

### Key Features

- **Auto-Configuration**：库会根据提供的配置属性自动配置 Telegram 机器人，省去手动设置的步骤。
- **Configuration Properties**：支持通过配置属性轻松自定义机器人设置，例如机器人令牌、包名和标识符。
- **Spring Integration**：无缝集成到 Spring 生态系统，利用 Spring 的依赖注入和应用上下文管理机器人实例。
- **Coroutine Support**：使用 Kotlin 协程实现异步机器人操作，确保高效且非阻塞的执行。

### Getting Started

要在 Telegram 机器人项目中使用 Spring Starter Library，需要在 Spring Boot 项目中将其作为依赖添加。该库设计用于 Spring Boot 应用，并依赖 Spring Boot 框架才能工作。

#### Dependency

在你的 `build.gradle` 或 `pom.xml` 文件中添加以下依赖：

```gradle
dependencies {
    implementation 'eu.vendeli:spring-starter:<version>'
}
```

将 `<version>` 替换为库的最新版本。

#### Configuration

库使用 Spring Boot 的 `@ConfigurationProperties` 绑定配置属性。你可以在 Spring Boot 应用的 `application.properties` 或 `application.yml` 文件中定义机器人配置。

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

一旦库被引入并配置，它会根据提供的配置自动创建并配置 Telegram 机器人实例。

它还支持多个机器人实例，只需在 bot 部分声明新的条目即可初始化多个实例：

```yaml
ktgram:
 bot:
    - token: YOUR_BOT_TOKEN
    - token: SECOND_BOT_TOKEN
```

### Advanced Configuration

对于更高级的配置，例如自定义机器人行为或与其他 Spring 组件集成，你可以扩展 `BotConfiguration` 类并通过其 `applyCfg` 方法修改机器人配置，示例请参见 [there](https://github.com/vendelieu/telegram-bot_template/blob/spring-bot/src/main/kotlin/com/example/springbot/configuration/BotConfig.kt)。

> [!TIP]
> 若要为每个已初始化的实例配置自定义设置，请通过它们的 identifier 区分（BotConfiguration 类同样有 identifier）。

### Ktor

该模块旨在帮助创建 Telegram 机器人的 webhook 服务器。它允许开发者配置服务器，包括 SSL/TLS 设置，并声明具有自定义配置的多个 Telegram 机器人。设置过程灵活，开发者可以根据具体需求定制服务器。

### Installation

要安装 ktor starter，请在主依赖中额外添加：

```gradle
dependencies {
    implementation("eu.vendeli:ktor-starter:x.y.z") // there
    // change x.y.z to current library version
}
```

### Key Components

`serveWebhook` Function

`serveWebhook` 函数是库的核心。它为 Telegram 机器人设置并启动 webhook 服务器。它接受两个参数：

- `wait`：一个布尔值，指示服务器在应用停止前是否等待关闭。默认 true。
- `serverBuilder`：配置服务器的 lambda 函数。默认是空 lambda。

### Configuration

* `WEBHOOK_PREFIX`：用于 webhook 监听路由地址前缀的参数。（默认 “/”）

#### Server Setup

- `server`：使用 EnvConfiguration 或 ManualConfiguration 设置服务器配置的方法。
- `engine`：配置 Netty 应用引擎的方法。
- `ktorModule`：向应用添加 Ktor 模块的方法。

库提供了广泛的可配置参数，包括主机、端口、SSL 设置等。配置方式有两种具体选项：

* `EnvConfiguration`：从环境变量中读取以 `KTGRAM_` 为前缀的配置值。
* `ManualConfiguration`：在 `server {}` 函数中手动设置配置值。

可设置的参数列表：

- `HOST`：服务器的主机名或 IP 地址。
- `PORT`：服务器端口号。
- `SSL_PORT`：SSL/TLS 连接的端口号。
- `PEM_PRIVATE_KEY_PATH`：PEM 私钥文件的路径。
- `PEM_CHAIN_PATH`：PEM 证书链文件的路径。
- `PEM_PRIVATE_KEY`：PEM 私钥密码，以字符数组形式提供。
- `KEYSTORE_PATH`：Java KeyStore 文件的路径。
- `KEYSTORE_PASSWORD`：KeyStore 的密码。
- `KEY_ALIAS`：KeyStore 中密钥的别名。
- `SSL_ON`：布尔值，指示是否启用 SSL/TLS。默认 true。

> [!TIP]
> 如果存在 PEM 证书，模块本身会在指定路径创建一个 jks 存储。

#### Bot Configuration:

要配置机器人，请调用 `declareBot {}`，它包含以下参数：

- `token`：机器人令牌。
- `pckg`：机器人的包名。
- `configuration`：用于配置机器人的 lambda 函数。
- `handlingBehaviour`：用于设置机器人处理行为的 lambda 函数。
- `onInit`：机器人初始化时执行的 lambda 函数。

### Example Usage

使用该模块时，调用 `serveWebhook` 函数，使用所需设置进行配置，并声明你的机器人。下面是一个简化示例：

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
> 别忘了设置 webhook，否则一切无法正常工作。 :)

默认情况下，模块会将 webhook 监听端点提供为 `host/BOT_TOKEN`


---