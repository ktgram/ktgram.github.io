---
---
title: DSL عملکردی
---

### به ~~بی‌نهایت~~ DSL عملکردی و فراتر!

ربات از دو رویکرد مبتنی بر نشانه‌گذاری و DSL عملکردی برای تنظیم متن برای پشتیبانی می‌کند. می‌توانید هر دو رویکرد را ترکیب کنید.

### DSL عملکردی

DSL عملکردی فقط یک روش متفاوت برای تعریف متن ربات است.

مثال:

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

### دستورات و ورودی‌ها

با استفاده از DSL عملکردی می‌توانید هم `دستورات` و هم `ورودی‌ها` را مدیریت کنید.

#### دستورات

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

    bot.setFunctionality {
        // دستور معمولی
        onCommand("/start") {
            message { "Hello" }.send(user, bot)
        }
        
        // مطابقت دستور مبتنی بر regex
        onCommand("""(red|green|blue)""".toRegex()) {
            message { "you typed ${update.text} color" }.send(user, bot)
        }
    }
}
```

در `onCommand`، پارامترهای تجزیه شده به عنوان `Map<String, String>` بر اساس تنظیمات شما در دسترس هستند.

#### ورودی‌ها

می‌توانید از ورودی‌ها از طریق [`bot.inputListener`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot/-telegram-bot/input-listener.html) استفاده کنید.

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

#### زنجیره‌های ورودی

برای جریان‌های ورودی چندمرحله‌ای، از `inputChain` استفاده کنید:

```kotlin
bot.setFunctionality {
    inputChain("conversation") {
        message { "Nice to meet you, ${update.text}" }.send(user, bot)
        message { "What is your favorite food?" }.send(user, bot)
    }.breakIf({ update.text == "peanut butter" }) { // شرط شکست زنجیره
        message { "Oh, too bad, I'm allergic to it." }.send(user, bot)
        // عملی که زمانی که شرط مطابقت دارد اعمال می‌شود
    }.andThen {
        // نقطه ورودی بعدی اگر شرط شکست مطابقت نداشته باشد
        message { "Great choice!" }.send(user, bot)
    }
}
```

زنجیره به طور خودکار به گام بعدی پیش می‌رود مگر اینکه شرط شکستی مطابقت داشته باشد. اگر شرط شکست مطابقت داشته باشد و `repeat` برابر `true` (پیش‌فرض) باشد، کاربر در گام فعلی باقی می‌ماند.

#### مدیریت نوع به‌روزرسانی

می‌توانید مستقیماً انواع به‌روزرسانی خاص را مدیریت کنید:

```kotlin
bot.setFunctionality {
    onUpdate(UpdateType.MESSAGE, UpdateType.CALLBACK_QUERY) {
        // مدیریت هر دو نوع به‌روزرسانی پیام و درخواست بازخورد
        println("Received update: ${update.type}")
    }
}
```

#### مطابق‌کننده‌های متداول

متن را (نه فقط دستورات) با استفاده از `common` مطابقت دهید:

```kotlin
bot.setFunctionality {
    // مطابقت رشته
    common("hello") {
        message { "Hi there!" }.send(user, bot)
    }
    
    // مطابقت regex
    common("""\d+""".toRegex()) {
        message { "You sent a number!" }.send(user, bot)
    }
}
```

#### مدیریت فیلترشده

به‌روزرسانی‌هایی که توسط هیچ مدیریت‌کننده‌ای پردازش نشدند را مدیریت کنید:

```kotlin
bot.setFunctionality {
    whenNotHandled {
        message { "I didn't understand that." }.send(user, bot)
    }
}
```

### تنظیمات پیشرفته

#### محدودیت نرخ

محدودیت نرخ را به هر مدیریت‌کننده اعمال کنید:

```kotlin
bot.setFunctionality {
    onCommand("/expensive", rateLimits = RateLimits(5, 60)) {
        // این دستور فقط 5 بار در هر 60 ثانیه قابل فراخوانی است
        message { "Processing..." }.send(user, bot)
    }
}
```

#### محافظ‌ها

برای اضافه کردن منطق اعتبارسنجی سفارشی از محافظ‌ها استفاده کنید:

```kotlin
bot.setFunctionality {
    onCommand("/admin", guard = AdminGuard::class) {
        message { "Admin command executed" }.send(user, bot)
    }
}
```

#### تجزیه آرگومان

می‌توانید تجزیه‌کننده آرگومان را سفارشی کنید:

```kotlin
bot.setFunctionality {
    onCommand("/custom", argParser = CustomArgParser::class) {
        // پارامترها با استفاده از CustomArgParser تجزیه خواهند شد
        message { "Parameters: $parameters" }.send(user, bot)
    }
}
```

### ترکیب رویکردهای عملکردی و مبتنی بر نشانه‌گذاری

می‌توانید هر دو رویکرد را در یک ربات استفاده کنید:

```kotlin
// مدیریت‌کننده مبتنی بر نشانه‌گذاری
@CommandHandler(["/register"])
suspend fun register(ctx: CommandContext) {
    message { "Registration started" }.send(ctx.user, ctx.bot)
}

// مدیریت‌کننده عملکردی
bot.setFunctionality {
    onCommand("/help") {
        message { "Available commands: /register, /help" }.send(user, bot)
    }
}
```

هر دو مدیریت‌کننده در یک `ActivityRegistry` ثبت می‌شوند و بدون مشکل با هم کار می‌کنند.

### همچنین ببینید

* [عمل](Actions.md)
* [ابزارهای مفید](Useful-utilities-and-tips.md)
---