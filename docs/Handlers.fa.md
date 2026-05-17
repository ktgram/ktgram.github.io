---
---
title: Handlers
---


### Variety of Handlers

در توسعه ربات، به‌ویژه در سیستم‌هایی که شامل تعاملات کاربر هستند، مدیریت و پردازش کارآمد دستورات و‌رویدادها اهمیت بالایی دارد.

این حاشیه‌نویسی‌ها توابعی را نشان می‌دهند که برای پردازش دستورات، ورودی‌ها یا به‌روزرسانی‌های خاص طراحی شده‌اند و متادیتاهایی مانند کلیدواژه‌های دستور، محدوده‌ها و نگهبان‌ها را فراهم می‌کنند.

### Annotations Overview

#### CommandHandler

حاشیه‌نویسی `CommandHandler` برای علامت‌گذاری توابعی استفاده می‌شود که دستورات خاصی را پردازش می‌کنند. این حاشیه‌نویسی شامل ویژگی‌هایی است که کلیدواژه‌ها و محدودهٔ دستور را تعریف می‌کند.

-   **value**: کلیدواژه‌های مرتبط با دستور را مشخص می‌کند.
-   **scope**: زمینه یا محدوده‌ای که در آن دستور بررسی می‌شود را تعیین می‌کند.

```kotlin
@CommandHandler(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommandHandler.CallbackQuery

نسخهٔ ویژه‌ای از حاشیه‌نویسی `CommandHandler` که به‌طور خاص برای پردازش کوئری‌های کال‌بک طراحی شده است. ویژگی‌های مشابهی با `CommandHandler` دارد، اما تمرکز بر دستورات مرتبط با کال‌بک است.

_در واقع این همان `@CommandHandler` با یک محدودهٔ پیش‌تنظیم‌شدهٔ `UpdateType.CALLBACK_QUERY` است_.

-   **value**: کلیدواژه‌های مرتبط با دستور را مشخص می‌کند.
-   **autoAnswer**: به‌صورت خودکار به `callbackQuery` پاسخ می‌دهد (قبل از پردازش `answerCallbackQuery` را فراخوانی می‌کند).


```kotlin
@CommandHandler.CallbackQuery(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### CommonHandler

حاشیه‌نویسی `CommonHandler` برای توابعی در نظر گرفته شده است که دستورات را با اولویت پایین‌تری نسبت به `CommandHandler` و `InputHandler` پردازش می‌کنند. این حاشیه‌نویسی در سطح سورس استفاده می‌شود و روشی انعطاف‌پذیر برای تعریف هندلرهای عمومی فراهم می‌کند.

**توجه داشته باشید، اولویت فقط درون `@CommonHandler`ها کار می‌کند (یعنی بر دیگر هندلرها تأثیری ندارد).**

##### CommonHandler.Text

این حاشیه‌نویسی برای تطبیق متن با به‌روزرسانی‌ها استفاده می‌شود. ویژگی‌هایی برای تعریف متن تطبیقی، شرایط فیلتر، اولویت و محدوده دارد.

-   **value**: متنی که با به‌روزرسانی‌های ورودی مقایسه می‌شود.
-   **filter**: کلاسی که شرایط استفاده‌شده در فرآیند تطبیق را تعریف می‌کند.
-   **priority**: سطح اولویت هندلر؛ ۰ بالاترین اولویت است.
-   **scope**: زمینه یا محدوده‌ای که تطبیق متن در آن بررسی می‌شود.

```kotlin
@CommonHandler.Text(["text"], filter = isNewUserFilter::class, priority = 10)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommonHandler.Regex

مشابه `CommonHandler.Text`، این حاشیه‌نویسی برای تطبیق به‌روزرسانی‌ها بر پایهٔ عبارات منظم استفاده می‌شود. ویژگی‌هایی برای تعریف الگوی Regex، گزینه‌ها، شرایط فیلتر، اولویت و محدوده دارد.

-   **value**: الگوی regex استفاده‌شده برای تطبیق.
-   **options**: گزینه‌های regex که رفتار الگو را تغییر می‌دهند.
-   **filter**: کلاسی که شرایط استفاده‌شده در فرآیند تطبیق را تعریف می‌کند.
-   **priority**: سطح اولویت هندلر؛ ۰ بالاترین اولویت است.
-   **scope**: زمینه یا محدوده‌ای که تطبیق regex در آن بررسی می‌شود.

```kotlin
@CommonHandler.Regex("^\d+$", scope = [UpdateType.EDITED_MESSAGE])
suspend fun test(update: EditedMessageUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### InputHandler

حاشیه‌نویسی `InputHandler` توابعی را علامت‌گذاری می‌کند که رویدادهای ورودی خاصی را پردازش می‌کنند. این حاشیه‌نویسی برای توابعی است که ورودی‌ها را در زمان اجرا مدیریت می‌کنند و ویژگی‌هایی برای تعریف کلیدواژه‌های ورودی و محدوده دارد.

-   **value**: کلیدواژه‌های مرتبط با رویداد ورودی را مشخص می‌کند.

```kotlin
@InputHandler("text")
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UnprocessedHandler

حاشیه‌نویسی `UnprocessedHandler` برای علامت‌گذاری توابعی استفاده می‌شود که به‌روزرسانی‌هایی را که توسط دیگر هندلرها پردازش نشده‌اند، مدیریت می‌کنند. این اطمینان را می‌دهد که هر به‌روزرسانی نا‌پردازش‌دیده به‌درستی مدیریت می‌شود و تنها یک نقطه پردازش برای این نوع هندلر ممکن است.

```kotlin
@UnprocessedHandler
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UpdateHandler

حاشیه‌نویسی `UpdateHandler` توابعی را علامت‌گذاری می‌کند که انواع خاصی از به‌روزرسانی‌های ورودی را مدیریت می‌کنند. این روش به‌طور سیستماتیک دسته‌بندی و پردازش انواع مختلف به‌روزرسانی را ممکن می‌سازد.

-   **type**: انواع به‌روزرسانی‌هایی که تابع هندلر آن‌ها را پردازش می‌کند را مشخص می‌کند.
-   **messageKind** *(added in 9.5)*: مجموعهٔ اختیاری [`MessageKind`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-message-kind/index.html)ها که ارسال را به به‌روزرسانی‌های حاوی پیام با نوع منطبق محدود می‌کند. خالی (پیش‌فرض) یعنی هر نوعی منطبق است.

```kotlin
@UpdateHandler([UpdateType.PRE_CHECKOUT_QUERY])
suspend fun test(update: PreCheckoutQueryUpdate, user: User, bot: TelegramBot) {
    //...
}
```

##### Filtering by `MessageKind`

از پارامتر `messageKind` برای واکنش فقط به یک زیرمجموعهٔ خاص از به‌روزرسانی‌های پیام (عکس، متن، رویدادهای سرویس و …) استفاده کنید به‌جای بررسی دستی فیلدهای nullable:

```kotlin
@UpdateHandler(type = [UpdateType.MESSAGE], messageKind = [MessageKind.PHOTO])
suspend fun onPhoto(update: MessageUpdate, bot: TelegramBot) {
    //...
}
```
### Handler Companion Annotations

همچنین حاشیه‌نویسی‌های تکمیلی وجود دارند که اختیاری برای هندلرها هستند و رفتار اختیاری آن‌ها را تکمیل می‌کنند.

آنها می‌توانند هم روی توابعی که هندلر به‌آن‌ها اعمال می‌شود و هم روی کلاس‌ها قرار بگیرند؛ در حالت دوم به‌صورت خودکار بر تمام هندلرهای آن کلاس اعمال می‌شوند، ولی در صورت نیاز می‌توان رفتار جداگانه‌ای برای برخی توابع تعیین کرد.

به‌عبارت دیگر، اولویت اعمال به این شکل است: `Function` > `Class`، به‌طوری‌که تابع دارای اولویت بالاتری است.

#### Rate Limiting

علاوه بر این، مکانیزم محدودکردن نرخ (rate limiting) که در حاشیه‌نویسی‌ها توصیف شده است را نیز می‌توان مشاهده کرد.

می‌توانید محدودیت‌های کلی برای هر کاربر تنظیم کنید:

```kotlin
// ...
val bot = TelegramBot("BOT_TOKEN") {
    rateLimiter { // general limits
        limits = RateLimits(period = 10000, rate = 5)
    }
}
```

###### Handler specific

محدودیت‌ها برای برخی اقدامات می‌توانند با استفاده از حاشیه‌نویسی `RateLimits` تعریف شوند؛ این حاشیه‌نویسی توسط `@CommandHandler`، `@CommandHandler.CallbackQuery`، `@InputHandler`، `@CommonHandler` پشتیبانی می‌شود.

```kotlin
@CommandHandler(["/start"])
@RateLimits(period = 1000L, rate = 1L)
suspend fun start(user: User, bot: TelegramBot) {
    // ...
}
```

#### Guard

می‌توانید نگهبان‌ها (guards) را به‌صورت جداگانه تعریف کنید تا دسترسی به هندلرها کنترل شود؛ این قابلیت توسط `@CommandHandler`، `@CommandHandler.CallbackQuery`، `@InputHandler` پشتیبانی می‌شود:

```kotlin
@CommandHandler(["text"])
@Guard(isAdminGuard::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### ArgParser

می‌توانید تجزیه‌کنندهٔ آرگومان سفارشی را به‌صورت جداگانه تعریف کنید تا رفتار پارس پارامترها برای هندلرها تغییر کند؛ این قابلیت توسط `@CommandHandler`، `@CommandHandler.CallbackQuery`، `@CommonHandler` پشتیبانی می‌شود:

```kotlin
@CommandHandler(["text"])
@ArgParser(SpaceArgParser::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

**see also [`defaultArgParser`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.common/default-arg-parser.html)**

### Functional DSL

هر یک از حاشیه‌نویسی‌های بالا معادل خود را در **DSL تابعی** دارند، راهی جایگزین برای اعلان هندلرها در زمان اجرا از طریق `bot.setFunctionality { … }`. هر دو رویکرد از همان `ActivityRegistry` استفاده می‌کنند و می‌توانند به‌آزادانه در یک ربات ترکیب شوند.

| Annotation | DSL counterpart |
|------------|-----------------|
| `@CommandHandler` | `onCommand(...)` |
| `@CommandHandler.CallbackQuery` | `onCommand(..., scope = [UpdateType.CALLBACK_QUERY])` |
| `@InputHandler` / input chains | `onInput(...)` / `inputChain(...)` |
| `@CommonHandler` | `common(...)` |
| `@UpdateHandler` | `onUpdate(...)` |
| `@UnprocessedHandler` | `whenNotHandled { ... }` |

مثال حداقل:

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

### Commands

```kotlin
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
```

درون بلوک `onCommand`، پارامترهای تجزیه‌شده به‌صورت `Map<String, String>` در دسترس هستند که توسط پیکربندی فعال `commandParsing` شکل می‌گیرند.

### Inputs

```kotlin
bot.setFunctionality {
    onCommand("/start") {
        message { "Hello, what's your name?" }.send(user, bot)
        bot.inputListener[user] = "testInput"
    }

    onInput("testInput") {
        message { "Hey, nice to meet you, ${update.text}" }.send(user, bot)
    }
}
```

به [`bot.inputListener`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot/-telegram-bot/input-listener.html) برای API ذخیره‌سازی مراجعه کنید.

#### Input chains

برای جریان‌های ورودی چند‑مرحله‌ای از `inputChain` استفاده کنید:

```kotlin
bot.setFunctionality {
    inputChain("conversation") {
        message { "Nice to meet you, ${update.text}" }.send(user, bot)
        message { "What is your favorite food?" }.send(user, bot)
    }.breakIf({ update.text == "peanut butter" }) {     // chain break condition
        message { "Oh, too bad, I'm allergic to it." }.send(user, bot)
    }.andThen {
        // next step when the break condition didn't match
        message { "Great choice!" }.send(user, bot)
    }
}
```

زنجیره به‌صورت خودکار به گام بعدی می‌رود مگر این که شرط قطع برقرار شود؛ وقتی `repeat = true` (پیش‌فرض) باشد، یک قطع مطابق کاربر را در گام فعلی نگه می‌دارد.

> برای جریان‌های چند‑مرحله‌ای پیشرفته‌تر با وضعیت تایپ‌شده و اعتبارسنجی، ترجیحاً از [`@WizardHandler`](FSM-and-Conversation-handling.md) استفاده کنید.

### Update type handlers

```kotlin
bot.setFunctionality {
    onUpdate(UpdateType.MESSAGE, UpdateType.CALLBACK_QUERY) {
        println("Received update: ${update.type}")
    }
}
```

### Common matchers

```kotlin
bot.setFunctionality {
    common("hello") {
        message { "Hi there!" }.send(user, bot)
    }

    common("""\d+""".toRegex()) {
        message { "You sent a number!" }.send(user, bot)
    }
}
```

### Fallback handler

```kotlin
bot.setFunctionality {
    whenNotHandled {
        message { "I didn't understand that." }.send(user, bot)
    }
}
```

### Companion options

محدودیت‌های نرخ، نگهبان‌ها و تجزیه‌کننده‌های آرگومان به‌صورت مستقیم به عنوان پارامترهای نامدار به‌جای حاشیه‌نویسی‌های جداگانه پاس داده می‌شوند:

```kotlin
bot.setFunctionality {
    onCommand("/expensive", rateLimits = RateLimits(rate = 5, period = 60_000)) {
        message { "Processing..." }.send(user, bot)
    }

    onCommand("/admin", guard = AdminGuard::class) {
        message { "Admin command executed" }.send(user, bot)
    }

    onCommand("/custom", argParser = CustomArgParser::class) {
        message { "Parameters: $parameters" }.send(user, bot)
    }
}
```

### Combining DSL and annotations

هر دو سبک می‌توانند همزمان وجود داشته باشند — همان‌طور که ثبت می‌شوند، به‌همان شیوه ارسال می‌شوند:

```kotlin
@CommandHandler(["/register"])
suspend fun register(user: User, bot: TelegramBot) {
    message { "Registration started" }.send(user, bot)
}

bot.setFunctionality {
    onCommand("/help") {
        message { "Available commands: /register, /help" }.send(user, bot)
    }
}
```

### Conclusion

این حاشیه‌نویسی‌ها ابزارهای قدرتمند و انعطاف‌پذیری برای مدیریت دستورات، ورودی‌ها و رویدادها فراهم می‌کنند، در حالی که امکان پیکربندی‌های جداگانهٔ محدودیت‌های نرخ و نگهبان‌ها را می‌دهند و ساختار کلی و نگهداری توسعه ربات را بهبود می‌بخشند.

### See also

* [Activities & Processors](Activites-and-Processors.md)
* [Activity invocation](Activity-invocation.md)
* [FSM and Conversation handling](FSM-and-Conversation-handling.md)
* [Sessions](Sessions.md)
* [Update parsing](Update-parsing.md)

---