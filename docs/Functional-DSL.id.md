---
---
title: Functional Dsl
---

### To ~~infinity~~ functional dsl and beyond!

Bot mendukung pengaturan konteks baik berbasis anotasi maupun functional dsl. Anda dapat menggabungkan kedua pendekatan tersebut.

### Functional DSL

Functional DSL adalah cara berbeda untuk mendefinisikan konteks bot.

Contoh:

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

### Commands dan Inputs

Anda dapat menangani baik `commands` maupun `inputs` menggunakan functional DSL.

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

Pada `onCommand`, parameter yang diurai tersedia sebagai `Map<String, String>` berdasarkan konfigurasi Anda.

#### Inputs

Anda dapat menggunakan inputs melalui [`bot.inputListener`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot/-telegram-bot/input-listener.html).

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

Untuk alur input multi-langkah, gunakan `inputChain`:

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

Chain secara otomatis melanjutkan ke langkah berikutnya kecuali kondisi break terpenuhi. Jika kondisi break cocok dan `repeat` adalah `true` (default), pengguna tetap pada langkah saat ini.

#### Update Type Handlers

Tangani tipe update tertentu secara langsung:

```kotlin
bot.setFunctionality {
    onUpdate(UpdateType.MESSAGE, UpdateType.CALLBACK_QUERY) {
        // Handle both message and callback query updates
        println("Received update: ${update.type}")
    }
}
```

#### Common Matchers

Cocokkan konten teks (bukan hanya commands) menggunakan `common`:

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

Tangani updates yang tidak diproses oleh handler manapun:

```kotlin
bot.setFunctionality {
    whenNotHandled {
        message { "I didn't understand that." }.send(user, bot)
    }
}
```

### Advanced Configuration

#### Rate Limiting

Terapkan batasan rate ke handler manapun:

```kotlin
bot.setFunctionality {
    onCommand("/expensive", rateLimits = RateLimits(5, 60)) {
        // This command can only be called 5 times per 60 seconds
        message { "Processing..." }.send(user, bot)
    }
}
```

#### Guards

Gunakan guards untuk menambahkan logika validasi kustom:

```kotlin
bot.setFunctionality {
    onCommand("/admin", guard = AdminGuard::class) {
        message { "Admin command executed" }.send(user, bot)
    }
}
```

#### Argument Parsing

Kustomisasi cara argumen command diurai:

```kotlin
bot.setFunctionality {
    onCommand("/custom", argParser = CustomArgParser::class) {
        // parameters will be parsed using CustomArgParser
        message { "Parameters: $parameters" }.send(user, bot)
    }
}
```

### Menggabungkan Functional dan Annotation-Based setting

Anda dapat menggunakan kedua pendekatan dalam bot yang sama:

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

Kedua handler terdaftar dalam `ActivityRegistry` yang sama dan bekerja secara seamless bersama-sama.

### Lihat juga

* [Action](Actions.md)
* [Useful utilities](Useful-utilities-and-tips.md)
---