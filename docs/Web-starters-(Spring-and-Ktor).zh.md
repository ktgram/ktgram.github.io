---
title: Web 启动器（Spring 和 Ktor）
---

### Spring 启动器

Spring 启动器模块是一个自动配置模块，将 Telegram 机器人功能集成到 Spring Boot 应用程序中。它利用 Spring Boot 的依赖注入和配置属性的强大功能，根据提供的配置自动配置 Telegram 机器人。该库对于希望使用 Kotlin 和 Spring Boot 构建 Telegram 机器人的开发者特别有用，提供了一种简化的机器人开发和管理方法。

### 关键特性

- **自动配置**：该库根据提供的配置属性自动配置 Telegram 机器人，消除了手动设置的需要。
- **配置属性**：支持配置属性，便于自定义机器人设置，例如机器人令牌、包名称和标识符。
- **Spring 集成**：与 Spring 生态系统无缝集成，利用 Spring 的依赖注入和应用上下文来管理机器人实例。
- **协程支持**：利用 Kotlin 协程进行异步机器人操作，确保高效和非阻塞的执行。

### 开始使用

要使用 Telegram 机器人的 Spring 启动器库，您需要将其作为依赖项包含在您的 Spring Boot 项目中。该库旨在与 Spring Boot 应用程序一起使用，并需要 Spring Boot 框架才能正常工作。

#### 依赖项

将以下依赖项添加到您的 `build.gradle` 或 `pom.xml` 文件中：

```gradle
dependencies {
    implementation 'eu.vendeli:spring-starter:<version>'
}
```

将 `<version>` 替换为库的最新版本。

#### 配置

该库使用 Spring Boot 的 `@ConfigurationProperties` 来绑定配置属性。您可以在 Spring Boot 应用程序的 `application.properties` 或 `application.yml` 文件中定义您的机器人配置。

```yaml
ktgram:
 autoStartPolling: true
 shareHttpClient: true
 bot:
    - token: YOUR_BOT_TOKEN
      pckg: com.example.bot
      identifier: MyBot
```

#### 使用

一旦库被包含并配置，它将根据提供的配置自动创建和配置 Telegram 机器人实例。

它还支持多个机器人实例，要初始化多个实例，只需在机器人部分声明为新条目：

```yaml
ktgram:
 bot:
    - token: YOUR_BOT_TOKEN
    - token: SECOND_BOT_TOKEN
```

### 高级配置

对于更高级的配置，例如自定义机器人行为或与其他 Spring 组件集成，您可以扩展 `BotConfiguration` 类，并通过其 `applyCfg` 方法更改机器人配置，您可以在 [这里](https://github.com/vendelieu/telegram-bot_template/blob/spring-bot/src/main/kotlin/com/example/springbot/configuration/BotConfig.kt) 查看示例。

> [!TIP]
> 要使用自定义配置配置每个初始化的实例，请通过其标识符区分它们（BotConfiguration 类也具有标识符）。

### Ktor

该模块旨在简化为 Telegram 机器人创建 webhook 服务器的过程。它允许开发者配置服务器，包括 SSL/TLS 设置，并声明多个具有自定义配置的 Telegram 机器人。设置过程灵活，使开发者能够根据特定需求定制服务器。

### 安装

要安装 Ktor 启动器，请将其添加到主依赖项中：

```gradle
dependencies {
    implementation("eu.vendeli:ktor-starter:x.y.z") // 在这里
    // 将 x.y.z 更改为当前库版本
}
```

### 关键组件

`serveWebhook` 函数

`serveWebhook` 函数是库的核心。它设置并启动 Telegram 机器人的 webhook 服务器。它接受两个参数：

- `wait`：一个布尔值，指示服务器在关闭之前是否应等待应用程序停止。默认为 true。
- `serverBuilder`：一个配置服务器的 lambda 函数。默认为空 lambda。

### 配置

* `WEBHOOK_PREFIX`：用于 webhook 监听器路由的地址前缀的参数。（默认为 "/"）

#### 服务器设置

- `server`：使用 EnvConfiguration 或 ManualConfiguration 设置服务器配置的方法。
- `engine`：配置 Netty 应用程序引擎的方法。
- `ktorModule`：将 Ktor 模块添加到应用程序的方法。

该库提供了广泛的可配置参数用于服务器，包括主机、端口、SSL 设置等。其配置有两种具体选项：

* `EnvConfiguration`：从带有 `KTGRAM_` 前缀的环境中读取配置值。
* `ManualConfiguration`：允许手动设置配置值，在 `server {}` 函数中设置您的参数。

可以设置 的参数列表包括：

- `HOST`：服务器的主机名或 IP 地址。
- `PORT`：服务器的端口号。
- `SSL_PORT`：SSL/TLS 连接的端口号。
- `PEM_PRIVATE_KEY_PATH`：PEM 私钥文件的路径。
- `PEM_CHAIN_PATH`：PEM 证书链文件的路径。
- `PEM_PRIVATE_KEY`：PEM 私钥的密码，作为字符数组。
- `KEYSTORE_PATH`：Java KeyStore 文件的路径。
- `KEYSTORE_PASSWORD`：KeyStore 的密码。
- `KEY_ALIAS`：KeyStore 中密钥的别名。
- `SSL_ON`：一个布尔值，指示是否应启用 SSL/TLS。默认为 true。

> [!TIP]
> 如果存在 pem 证书，模块将自动在指定路径创建 jks 存储。

#### 机器人配置：

要配置机器人，请调用 `declareBot {}`，该方法具有以下参数：

- `token`：机器人令牌。
- `pckg`：机器人的包名称。
- `configuration`：用于配置机器人的 lambda 函数。
- `handlingBehaviour`：用于设置机器人的处理行为的 lambda 函数。
- `onInit`：在机器人初始化时执行的 lambda 函数。

### 示例用法

要使用此模块，请调用 `serveWebhook` 函数，使用所需的设置进行配置，声明您的机器人。以下是一个简化的示例：

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
            // 配置其他机器人设置
        }
        // 如果需要，添加更多机器人或设置其他参数
    }
}
```

> [!CAUTION]
> 不要忘记设置 webhook 以使一切正常工作。 :)

默认情况下，模块将作为 `host/BOT_TOKEN` 提供 webhook 监听端点。