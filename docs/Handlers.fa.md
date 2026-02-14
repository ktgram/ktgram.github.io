---
---
title: Handlers
---


### Variety of Handlers

در توسعه ربات، به‌ویژه در سیستم‌هایی که شامل تعاملات کاربری هستند، مدیریت و پردازش دستورات و رویدادها به‌صورت کارآمد بسیار حیاتی است.

این annotationها توابعی را که برای پردازش دستورات، ورودی‌ها یا آپدیت‌های خاص طراحی شده‌اند علامت‌گذاری می‌کنند و متادیتایی مانند کلیدواژه‌های دستور، scope‌ها و guards فراهم می‌کنند.

### Annotations Overview

#### CommandHandler

Annotation `CommandHandler` برای علامت‌گذاری توابعی که دستورات خاص را پردازش می‌کنند استفاده می‌شود. این annotation شامل خواصی است که کلیدواژه‌های دستور و scope را تعریف می‌کند.

-   **value**: کلیدواژه‌هایی را که با دستور مرتبط هستند مشخص می‌کند.
-   **scope**: متنی را که دستور در آن بررسی خواهد شد مشخص می‌کند.

```kotlin
@CommandHandler(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommandHandler.CallbackQuery

نسخه تخصصی annotation `CommandHandler` که به طور خاص برای مدیریت callback queries طراحی شده است. شامل خواص مشابه `CommandHandler` است، با تمرکز بر روی دستورات مرتبط با callback.

_در واقع همان `@CommandHandler` با `UpdateType.CALLBACK_QUERY` scope از پیش تعیین شده است_.

-   **value**: کلیدواژه‌هایی را که با دستور مرتبط هستند مشخص می‌کند.
-   **autoAnswer**: به‌صورت خودکار به `callbackQuery` پاسخ دهید (قبل از پردازش `answerCallbackQuery` را فراخوانی کنید).


```kotlin
@CommandHandler.CallbackQuery(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### CommonHandler

Annotation `CommonHandler` برای توابعی است که دستوراتی با اولویت کمتر نسبت به `CommandHandler` و `InputHandler` را پردازش می‌کند. در سطح منبع استفاده می‌شود و راهی انعطاف‌پذیر برای تعریف common command handlers فراهم می‌کند.

**توجه داشته باشید، اولویت فقط درون `@CommonHandler`ها کار می‌کند (یعنی روی دیگر handlers تأثیر نمی‌گذارد).**

##### CommonHandler.Text

این annotation برای تطبیق متن در مقابل آپدیت‌ها مشخص شده است. شامل خواصی برای تعریف متن تطبیقی، شرایط فیلتر، اولویت و scope است.

-   **value**: متنی که در مقابل آپدیت‌های دریافتی تطبیق داده می‌شود.
-   **filter**: یک کلاس که شرایطی را که در فرآیند تطبیق استفاده می‌شود تعریف می‌کند.
-   **priority**: سطح اولویت handler، که 0 بالاترین اولویت است.
-   **scope**: متنی که در آن تطبیق متن بررسی خواهد شد.

```kotlin
@CommonHandler.Text(["text"], filter = isNewUserFilter::class, priority = 10)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommonHandler.Regex

مشابه `CommonHandler.Text`، این annotation برای تطبیق آپدیت‌ها بر اساس عبارات منظم استفاده می‌شود. شامل خواصی برای تعریف الگوی regex، options، شرایط فیلتر، اولویت و scope است.

-   **value**: الگوی regex برای تطبیق.
-   **options**: options regex که رفتار الگوی regex را تغییر می‌دهند.
-   **filter**: یک کلاس که شرایطی را که در فرآیند تطبیق استفاده می‌شود تعریف می‌کند.
-   **priority**: سطح اولویت handler، که 0 بالاترین اولویت است.
-   **scope**: متنی که در آن تطبیق regex بررسی خواهد شد.

```kotlin
@CommonHandler.Regex("^\d+$", scope = [UpdateType.EDITED_MESSAGE])
suspend fun test(update: EditedMessageUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### InputHandler

Annotation `InputHandler` توابعی را که رویدادهای ورودی خاص را پردازش می‌کنند علامت‌گذاری می‌کند. برای توابعی است که ورودی‌ها را در زمان اجرا مدیریت می‌کنند و شامل خواصی برای تعریف کلیدواژه‌های ورودی و scope است.

-   **value**: کلیدواژه‌هایی را که با رویداد ورودی مرتبط هستند مشخص می‌کند.

```kotlin
@InputHandler("text")
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UnprocessedHandler

Annotation `UnprocessedHandler` برای علامت‌گذاری توابعی که آپدیت‌هایی را که توسط سایر handlers پردازش نشده‌اند مدیریت می‌کنند استفاده می‌شود. اطمینان حاصل می‌کند که هر آپدیت غیرپردازش‌شده به طور مناسب مدیریت شود، با این حال فقط یک نقطه پردازش برای این نوع handler ممکن است.

```kotlin
@UnprocessedHandler
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UpdateHandler

Annotation `UpdateHandler` توابعی را که انواع خاصی از آپدیت‌های دریافتی را مدیریت می‌کنند علامت‌گذاری می‌کند. راهی برای دسته‌بندی و پردازش منظم انواع مختلف آپدیت فراهم می‌کند.

-   **type**: انواع آپدیت‌هایی که تابع handler پردازش خواهد کرد را مشخص می‌کند.

```kotlin
@UpdateHandler([UpdateType.PRE_CHECKOUT_QUERY])
suspend fun test(update: PreCheckoutQueryUpdate, user: User, bot: TelegramBot) {
    //...
}
```
### Handler Companion Annotations

همچنین annotation‌های اضافی وجود دارد که برای handlers اختیاری هستند و رفتار اختیاری handlers را تکمیل می‌کنند.

آن‌ها می‌توانند هم روی توابعی که handler روی آن‌ها اعمال شده است و هم روی کلاس‌ها قرار گیرند، در مورد دوم به‌طور خودکار روی تمام handlers در آن کلاس اعمال خواهند شد، اما اگر نیاز باشد می‌توان رفتار جداگانه برای برخی توابع داشت.

یعنی اعمال با اولویتی این‌گونه است، `Function` > `Class`، که function اولویت بالاتری دارد.

#### Rate Limiting

علاوه بر این، مکانیسم محدودیت نرخی را که در annotation‌ها توضیح داده شده است نیز آشکار می‌کنیم.

می‌توانید محدودیت‌های کلی برای هر کاربر تنظیم کنید:

```kotlin
// ...
val bot = TelegramBot("BOT_TOKEN") {
    rateLimiter { // محدودیت‌های کلی
        limits = RateLimits(period = 10000, rate = 5)
    }
}
```

###### Handler specific

محدودیت‌های روی برخی اقدامات می‌توانند با استفاده از annotation `RateLimits` تعریف شوند، `CommandHandler`، `CommandHandler.CallbackQuery`، `InputHandler`، `CommonHandler` را پشتیبانی می‌کند.

```kotlin
@CommandHandler(["/start"])
@RateLimits(period = 1000L, rate = 1L)
suspend fun start(user: User, bot: TelegramBot) {
    // ...
}
```

#### Guard

می‌توانید guards را جداگانه برای کنترل دسترسی به handlers تعریف کنید، `CommandHandler`، `CommandHandler.CallbackQuery`، `InputHandler` را پشتیبانی می‌کند:

```kotlin
@CommandHandler(["text"])
@Guard(isAdminGuard::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### ArgParser

می‌توانید parser دلخواه آرگومان را جداگانه برای تغییر رفتار parse کردن پارامترها برای handlers تعریف کنید، `CommandHandler`، `CommandHandler.CallbackQuery`، `CommonHandler` را پشتیبانی می‌کند:

```kotlin
@CommandHandler(["text"])
@ArgParser(SpaceArgParser::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

**همچنین [`defaultArgParser`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.common/default-arg-parser.html) را ببینید**

### Conclusion

این annotation‌ها ابزارهای قوی و انعطاف‌پذیری برای مدیریت دستورات، ورودی‌ها و رویدادها فراهم می‌کنند، همچنین امکان تنظیم جداگانه محدودیت نرخ و guards را فراهم می‌آورند، که ساختار کلی و نگهداری توسعه ربات را تقویت می‌کند.

### See also

* [Activities & Processors](Activites-and-Processors.md)
* [Activity invocation](Activity-invocation.md)
* [FSM and Conversation handling](FSM-and-Conversation-handling.md)
* [Update parsing](Update-parsing.md)
* [Aide](Aide.md)