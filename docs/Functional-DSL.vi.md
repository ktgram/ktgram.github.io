---
---
title: Functional Dsl
---

### Đến ~~vô cực~~ functional dsl và xa hơn!

Bot hỗ trợ cả hai cách thiết lập ngữ cảnh dựa trên annotation và functional dsl. Bạn có thể kết hợp cả hai cách tiếp cận.

### Functional DSL

Functional DSL chỉ là một cách khác để định nghĩa ngữ cảnh bot.

Ví dụ:

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

    bot.setFunctionality {
        onChosenInlineResult {
            println("got a result ${update.chosenInlineResult.resultId} from ${update.user}")
        }
    }
}
```

### Commands và Inputs

Bạn có thể xử lý cả `commands` và `inputs` sử dụng functional DSL.

#### Commands

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

    bot.setFunctionality {
        // Regular command
        onCommand("/start") {
            message { "Hello" }.send(user, bot)
        }
        
        // Regex-based command matching
        onCommand("""(red|green|blue)""".toRegex()) {
            message { "you typed ${update.text} color" }.send(user, bot)
        }
    }
}
```

Trong `onCommand`, các tham số đã được parse có sẵn dưới dạng `Map<String, String>` dựa trên cấu hình của bạn.

#### Inputs

Bạn có thể sử dụng inputs thông qua [`bot.inputListener`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot/-telegram-bot/input-listener.html).

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

    bot.setFunctionality {
        onCommand("/start") {
            message { "Hello, what's your name?" }.send(user, bot)
            bot.inputListener[user] = "testInput"
        }
        
        onInput("testInput") {
            message { "Hey, nice to meet you, ${update.text}" }.send(user, bot)
        }
    }
}
```

#### Input Chains

Đối với luồng input nhiều bước, sử dụng `inputChain`:

```kotlin
bot.setFunctionality {
    inputChain("conversation") {
        message { "Nice to meet you, ${update.text}" }.send(user, bot)
        message { "What is your favorite food?" }.send(user, bot)
    }.breakIf({ update.text == "peanut butter" }) { // chain break condition
        message { "Oh, too bad, I'm allergic to it." }.send(user, bot)
        // action that will be applied when condition matches
    }.andThen {
        // next input point if break condition doesn't match
        message { "Great choice!" }.send(user, bot)
    }
}
```

Chuỗi tự động chuyển sang bước tiếp theo trừ khi điều kiện break được đáp ứng. Nếu điều kiện break được đáp ứng và `repeat` là `true` (mặc định), người dùng sẽ ở lại bước hiện tại.

#### Update Type Handlers

Xử lý trực tiếp các loại update cụ thể:

```kotlin
bot.setFunctionality {
    onUpdate(UpdateType.MESSAGE, UpdateType.CALLBACK_QUERY) {
        // Handle both message and callback query updates
        println("Received update: ${update.type}")
    }
}
```

#### Common Matchers

Match nội dung văn bản (không chỉ commands) sử dụng `common`:

```kotlin
bot.setFunctionality {
    // String matching
    common("hello") {
        message { "Hi there!" }.send(user, bot)
    }
    
    // Regex matching
    common("""\d+""".toRegex()) {
        message { "You sent a number!" }.send(user, bot)
    }
}
```

#### Fallback Handler

Xử lý các update không được xử lý bởi bất kỳ handler nào:

```kotlin
bot.setFunctionality {
    whenNotHandled {
        message { "I didn't understand that." }.send(user, bot)
    }
}
```

### Cấu hình Nâng cao

#### Rate Limiting

Áp dụng giới hạn tốc độ cho bất kỳ handler nào:

```kotlin
bot.setFunctionality {
    onCommand("/expensive", rateLimits = RateLimits(5, 60)) {
        // This command can only be called 5 times per 60 seconds
        message { "Processing..." }.send(user, bot)
    }
}
```

#### Guards

Sử dụng guards để thêm logic validation tùy chỉnh:

```kotlin
bot.setFunctionality {
    onCommand("/admin", guard = AdminGuard::class) {
        message { "Admin command executed" }.send(user, bot)
    }
}
```

#### Argument Parsing

Tùy chỉnh cách parse tham số command:

```kotlin
bot.setFunctionality {
    onCommand("/custom", argParser = CustomArgParser::class) {
        // parameters will be parsed using CustomArgParser
        message { "Parameters: $parameters" }.send(user, bot)
    }
}
```

### Kết hợp Functional và Annotation-Based setting

Bạn có thể sử dụng cả hai cách tiếp cận trong cùng một bot:

```kotlin
// Annotation-based handler
@CommandHandler(["/register"])
suspend fun register(ctx: CommandContext) {
    message { "Registration started" }.send(ctx.user, ctx.bot)
}

// Functional handler
bot.setFunctionality {
    onCommand("/help") {
        message { "Available commands: /register, /help" }.send(user, bot)
    }
}
```

Cả hai handlers đều được đăng ký trong cùng một `ActivityRegistry` và hoạt động liền mạch với nhau.

### See also

* [Action](Actions.md)
* [Useful utilities](Useful-utilities-and-tips.md)
---