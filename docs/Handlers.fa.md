---
---
title: Handlers
---


### Variety of Handlers

در توسعه ربات، به ویژه در سیستم‌هایی که شامل تعاملات کاربری هستند، مدیریت و پردازش دستورات و رویدادها به‌صورت کارآمد بسیار حیاتی است.

این نشانه‌گذاری‌ها توابعی را مشخص می‌کنند که برای پردازش دستورات، ورودی‌ها یا به‌روزرسانی‌های خاص طراحی شده‌اند و داده‌های متا مانند کلمات کلیدی دستور، حوزه‌ها و نگهبانان را ارائه می‌دهند.

### Annotations Overview

#### CommandHandler

نشانه‌گذاری `CommandHandler` برای مشخص کردن توابعی که دستورات خاص را پردازش می‌کنند استفاده می‌شود. این نشانه‌گذاری شامل ویژگی‌هایی است که کلمات کلیدی و حوزه دستور را تعریف می‌کند.

-   **value**: کلمات کلیدی مرتبط با دستور را مشخص می‌کند.
-   **scope**: زمینه یا حوزه‌ای را تعیین می‌کند که در آن دستور چک خواهد شد.

```kotlin
@CommandHandler(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommandHandler.CallbackQuery

نسخه تخصصی از نشانه‌گذاری `CommandHandler` که به طور خاص برای مدیریت درخواست‌های بازخورد طراحی شده است. این نشانه‌گذاری شامل ویژگی‌های مشابه `CommandHandler` است که بر روی دستورات مرتبط با بازخورد تمرکز دارد.

_در واقع این دقیقاً همان کاری را انجام می‌دهد که `@CommandHandler` با مقدار از پیش تعیین شده `UpdateType.CALLBACK_QUERY` برای حوزه انجام می‌دهد_.

-   **value**: کلمات کلیدی مرتبط با دستور را مشخص می‌کند.
-   **autoAnswer**: به‌طور خودکار به `callbackQuery` پاسخ دهد (قبل از مدیریت `answerCallbackQuery` را فراخوانی کند).


```kotlin
@CommandHandler.CallbackQuery(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### CommonHandler

نشانه‌گذاری `CommonHandler` برای توابعی است که دستورات با اولویت کمتر نسبت به `CommandHandler` و `InputHandler` را پردازش می‌کنند. این نشانه‌گذاری در سطح منبع استفاده می‌شود و راهی منعطف برای تعریف مدیران دستورات متداول فراهم می‌کند.

**توجه داشته باشید که اولویت تنها درون `@CommonHandler` خودش کار می‌کند (یعنی بر روی سایر مدیران تأثیر نمی‌گذارد).**

##### CommonHandler.Text

این نشانه‌گذاری برای تطبیق متن در برابر به‌روزرسانی‌ها استفاده می‌شود. شامل ویژگی‌هایی برای تعریف متن تطبیقی، شرایط فیلتر کردن، اولویت و حوزه است.

-   **value**: متنی که در برابر به‌روزرسانی‌های ورودی تطبیق داده می‌شود.
-   **filter**: کلاسی که شرایطی را تعریف می‌کند که در فرآیند تطبیق استفاده می‌شود.
-   **priority**: سطح اولویت مدیر، که 0 بالاترین اولویت است.
-   **scope**: زمینه یا حوزه‌ای که در آن تطبیق متن چک خواهد شد.

```kotlin
@CommonHandler.Text(["text"], filter = isNewUserFilter::class, priority = 10)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommonHandler.Regex

مشابه `CommonHandler.Text`، این نشانه‌گذاری برای تطبیق به‌روزرسانی‌ها بر اساس عبارات منظم استفاده می‌شود. شامل ویژگی‌هایی برای تعریف الگوی regex، گزینه‌ها، شرایط فیلتر کردن، اولویت و حوزه است.

-   **value**: الگوی regex برای تطبیق.
-   **options**: گزینه‌های regex که رفتار الگوی regex را تغییر می‌دهند.
-   **filter**: کلاسی که شرایطی را تعریف می‌کند که در فرآیند تطبیق استفاده می‌شود.
-   **priority**: سطح اولویت مدیر، که 0 بالاترین اولویت است.
-   **scope**: زمینه یا حوزه‌ای که در آن تطبیق regex چک خواهد شد.

```kotlin
@CommonHandler.Regex("^\d+$", scope = [UpdateType.EDITED_MESSAGE])
suspend fun test(update: EditedMessageUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### InputHandler

نشانه‌گذاری `InputHandler` توابعی را مشخص می‌کند که رویدادهای ورودی خاص را پردازش می‌کنند. این نشانه‌گذاری برای توابعی است که ورودی‌ها را در زمان اجرا مدیریت می‌کنند و شامل ویژگی‌هایی برای تعریف کلمات کلیدی ورودی و حوزه‌هاست.

-   **value**: کلمات کلیدی مرتبط با رویداد ورودی را مشخص می‌کند.

```kotlin
@InputHandler("text")
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UnprocessedHandler

نشانه‌گذاری `UnprocessedHandler` برای مشخص کردن توابعی استفاده می‌شود که به‌روزرسانی‌هایی که توسط سایر مدیران پردازش نشده‌اند را مدیریت می‌کنند. این نشانه‌گذاری تضمین می‌کند که هر به‌روزرسانی غیرپردازش شده به طور مناسب مدیریت شود و فقط یک نقطه پردازش برای این نوع از مدیر ممکن است.

```kotlin
@UnprocessedHandler
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UpdateHandler

نشانه‌گذاری `UpdateHandler` توابعی را مشخص می‌کند که انواع خاصی از به‌روزرسانی‌های ورودی را مدیریت می‌کنند. این نشانه‌گذاری راهی برای دسته‌بندی و پردازش منظم انواع مختلف به‌روزرسانی فراهم می‌کند.

-   **type**: انواع به‌روزرسانی‌هایی که تابع مدیر روی آن‌ها پردازش می‌کند را مشخص می‌کند.

```kotlin
@UpdateHandler([UpdateType.PRE_CHECKOUT_QUERY])
suspend fun test(update: PreCheckoutQueryUpdate, user: User, bot: TelegramBot) {
    //...
}
```
### Handler Companion Annotations

همچنین نشانه‌گذاری‌های اضافی وجود دارد که برای مدیران اختیاری هستند و رفتار اختیاری مدیران را تکمیل می‌کنند.

این نشانه‌گذاری‌ها می‌توانند هم در توابعی که یک مدیر روی آن اعمال شده و هم در کلاس‌ها قرار گیرند، در مورد دوم آن‌ها به‌طور خودکار روی تمام مدیران در آن کلاس اعمال خواهند شد، اما در صورت نیاز می‌توان رفتار جداگانه‌ای برای بعضی توابع داشت.

یعنی اولویت اعمال اینگونه است، `تابع` > `کلاس`، که تابع اولویت بالاتری دارد.

#### Rate Limiting

علاوه بر این، مکانیزم محدود کردن نرخ توصیف شده در نشانه‌گذاری‌ها نیز آشکار می‌شود.

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

محدودیت‌های روی بعضی عملیات می‌توانند با استفاده از نشانه‌گذاری `RateLimits` تعریف شوند، که برای `@CommandHandler`، `@CommandHandler.CallbackQuery`، `@InputHandler` و `@CommonHandler` پشتیبانی می‌شود.

```kotlin
@CommandHandler(["/start"])
@RateLimits(period = 1000L, rate = 1L)
suspend fun start(user: User, bot: TelegramBot) {
    // ...
}
```

#### Guard

می‌توانید نگهبانان را جداگانه تعریف کنید تا دسترسی به مدیران را کنترل کنید، که برای `@CommandHandler`، `@CommandHandler.CallbackQuery` و `@InputHandler` پشتیبانی می‌شود:

```kotlin
@CommandHandler(["text"])
@Guard(isAdminGuard::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### ArgParser

می‌توانید پارسر آرگومان سفارشی را جداگانه تعریف کنید تا رفتار تجزیه پارامترها برای مدیران را تغییر دهید، که برای `@CommandHandler`، `@CommandHandler.CallbackQuery` و `@CommonHandler` پشتیبانی می‌شود:

```kotlin
@CommandHandler(["text"])
@ArgParser(SpaceArgParser::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

**همچنین ببینید [`defaultArgParser`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.common/default-arg-parser.html)**

### Conclusion

این نشانه‌گذاری‌ها ابزارهای قدرتمند و منعطفی برای مدیریت دستورات، ورودی‌ها و رویدادها فراهم می‌کنند، به همراه امکان تنظیم جداگانه محدودیت‌های نرخ و نگهبانان، که ساختار کلی و نگهداری توسعه ربات را بهبود می‌بخشد.

### See also

* [Activities & Processors](Activites-and-Processors.md)
* [Activity invocation](Activity-invocation.md)
* [FSM and Conversation handling](FSM-and-Conversation-handling.md)
* [Update parsing](Update-parsing.md)