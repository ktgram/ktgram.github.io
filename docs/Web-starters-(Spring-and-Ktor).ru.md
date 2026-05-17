---
---
title: Web Starters (Spring And Ktor)
---

### Spring starter

Модуль Spring Starter для библиотеки — это модуль автонастройки, который интегрирует функции Telegram‑ботов в приложения Spring Boot. Он использует возможности внедрения зависимостей и конфигурационных свойств Spring Boot для автоматической настройки Telegram‑ботов на основе предоставленной конфигурации. Эта библиотека особенно полезна разработчикам, желающим создавать Telegram‑боты с использованием Kotlin и Spring Boot, предлагая упрощённый подход к разработке и управлению ботами.

### Key Features

- **Auto-Configuration**: Библиотека автоматически настраивает Telegram‑ботов на основе предоставленных конфигурационных свойств, исключая необходимость ручной настройки.
- **Configuration Properties**: Поддерживает конфигурационные свойства для удобной настройки параметров бота, таких как токены, имена пакетов и идентификаторы.
- **Spring Integration**: Бесшовно интегрируется с экосистемой Spring, используя внедрение зависимостей Spring и контекст приложения для управления экземплярами ботов.
- **Coroutine Support**: Использует корутины Kotlin для асинхронных операций бота, обеспечивая эффективное и неблокирующее выполнение.

### Getting Started

Чтобы использовать Spring Starter Library для Telegram Bots, нужно добавить её как зависимость в ваш проект Spring Boot. Библиотека предназначена для работы с приложениями Spring Boot и требует наличия фреймворка Spring Boot.

#### Dependency

Добавьте следующую зависимость в ваш файл `build.gradle` или `pom.xml`:

```gradle
dependencies {
    implementation 'eu.vendeli:spring-starter:<version>'
}
```

Замените `<version>` на последнюю версию библиотеки.

#### Configuration

Библиотека использует `@ConfigurationProperties` Spring Boot для привязки конфигурационных свойств. Вы можете определить конфигурацию ботов в файле `application.properties` или `application.yml` вашего приложения Spring Boot.

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

После включения и настройки библиотеки она автоматически создаёт и конфигурирует экземпляры Telegram‑ботов на основе предоставленной конфигурации.

Она также поддерживает несколько экземпляров ботов; чтобы инициализировать несколько, просто добавьте новую запись в раздел bot:

```yaml
ktgram:
 bot:
    - token: YOUR_BOT_TOKEN
    - token: SECOND_BOT_TOKEN
```

### Advanced Configuration

Для более сложных настроек, таких как кастомизация поведения бота или интеграция с другими компонентами Spring, вы можете расширить класс `BotConfiguration` и изменить конфигурацию бота через его метод `applyCfg`. Пример см. [здесь](https://github.com/vendelieu/telegram-bot_template/blob/spring-bot/src/main/kotlin/com/example/springbot/configuration/BotConfig.kt).

> [!TIP]
> Чтобы настроить каждый инициализированный экземпляр с индивидуальной конфигурацией, различайте их по их идентификатору (класс BotConfiguration также имеет идентификатор).

### Ktor

Модуль предназначен для упрощения создания webhook‑сервера для Telegram‑ботов. Он позволяет разработчикам настраивать сервер, включая параметры SSL/TLS, и объявлять несколько Telegram‑ботов с пользовательскими конфигурациями. Процесс настройки гибок, позволяя адаптировать сервер под конкретные потребности.

### Installation

Чтобы установить ktor starter, добавьте дополнительную зависимость к основной:

```gradle
dependencies {
    implementation("eu.vendeli:ktor-starter:x.y.z") // there
    // change x.y.z to current library version
}
```

### Key Components

`serveWebhook` Function

Функция `serveWebhook` является ядром библиотеки. Она настраивает и запускает webhook‑сервер для Telegram‑ботов. Принимает два параметра:

- `wait`: Boolean, указывающий, должен ли сервер ожидать завершения приложения перед выключением. По умолчанию true.
- `serverBuilder`: Лямбда, конфигурирующая сервер. По умолчанию пустая лямбда.

### Configuration

* `WEBHOOK_PREFIX`: параметр, используемый в качестве префикса адреса для маршрута webhook‑listener. (по умолчанию "/")

#### Server Setup

- `server`: Метод для установки конфигурации сервера с использованием `EnvConfiguration` или `ManualConfiguration`.
- `engine`: Метод для настройки Netty‑движка приложения.
- `ktorModule`: Метод для добавления Ktor‑модулей в приложение.

Библиотека предоставляет широкий набор настраиваемых параметров сервера, включая хост, порт, настройки SSL и др. Существуют два конкретных варианта конфигурации:

* `EnvConfiguration`: Читает значения конфигурации из окружения с префиксом `KTGRAM_`.
* `ManualConfiguration`: Позволяет вручную задавать значения конфигурации, указывая параметры в функции `server {}`.

Список параметров, которые можно задать:

- `HOST`: Имя хоста или IP‑адрес сервера.
- `PORT`: Номер порта сервера.
- `SSL_PORT`: Номер порта для SSL/TLS соединений.
- `PEM_PRIVATE_KEY_PATH`: Путь к файлу приватного ключа PEM.
- `PEM_CHAIN_PATH`: Путь к файлу цепочки сертификатов PEM.
- `PEM_PRIVATE_KEY`: Пароль приватного ключа PEM в виде массива символов.
- `KEYSTORE_PATH`: Путь к файлу Java KeyStore.
- `KEYSTORE_PASSWORD`: Пароль к KeyStore.
- `KEY_ALIAS`: Псевдоним ключа в KeyStore.
- `SSL_ON`: Boolean, указывающий, включён ли SSL/TLS. По умолчанию true.

> [!TIP]
> Если PEM‑сертификаты присутствуют, модуль сам создаст хранилище jks из них по указанному пути.

#### Bot Configuration:

Чтобы сконфигурировать бота, вызовите `declareBot {}` с такими параметрами:

- `token`: Токен бота.
- `pckg`: Имя пакета бота.
- `configuration`: Лямбда для настройки бота.
- `handlingBehaviour`: Лямбда для установки поведения обработки ботом.
- `onInit`: Лямбда, выполняемая при инициализации бота.

### Example Usage

Чтобы использовать этот модуль, вызовите функцию `serveWebhook`, настройте её нужными параметрами и объявите ботов. Пример упрощённый:

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
> Не забудьте установить webhook, чтобы всё работало. :)

По умолчанию модуль будет обслуживать webhook‑концевые точки как `host/BOT_TOKEN`


---