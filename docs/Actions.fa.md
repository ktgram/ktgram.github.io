---
---
title: Actions
---

### All requests is Actions
تمام درخواست‌های API تلگرام انواع مختلفی از رابط [`TgAction`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.action/-tg-action/index.html) هستند که روش‌های مختلفی را پیاده‌سازی می‌کنند مانند [`SendMessageAction`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.api.message/-send-message-action/index.html)، <br/>که به فرم [`message()`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.api.message/message.html) - type functions برای راحتی رابط کتابخانه بسته‌بندی شده‌اند.

<p align="center">
    <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/2d097d60-1907-4ca1-8ad3-3ee8d223f8eb" alt="Actions diagram" />
</p>

هر `Action` ممکن است روش‌های مختلفی داشته باشد، بسته به [ویژگی‌های](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-feature/index.html) در دسترس.

### ویژگی‌ها

عملکردهای مختلف می‌توانند ویژگی‌های [مختلف](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-feature/index.html) داشته باشند بسته به API Bot تلگرام، مانند:
[`OptionsFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-options-feature/index.html)،
[`MarkupFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-markup-feature/index.html)
[`EntitiesFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-entities-feature/index.html)
[`CaptionFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-caption-feature/index.html).

بیایید به آن‌ها نزدیک‌تر نگاه کنیم:

### گزینه‌ها
برای مثال، [`OptionsFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-options-feature/index.html) برای پاس دادن پارامترهای اختیاری استفاده می‌شود.

هر عملکرد نوع خود از گزینه‌ها را دارد، مربوط به آن را می‌توانید در خود `Action` در پارامتر `options`، در بخش ویژگی‌ها مشاهده کنید. <br/>برای مثال، `sendMessage` که شامل داده‌کلاس [`MessageOptions`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.options/-message-options/index.html) با پارامترهای مختلف به عنوان گزینه‌هاست.

مثال استفاده:

```kotlin
message{ "*Test*" }.options {
    parseMode = ParseMode.Markdown
}.send(user, bot)
```
### Markup

همچنین روشی برای ارسال markup وجود دارد که تمام انواع [کیبوردها](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.marker/-keyboard/index.html) را پشتیبانی می‌کند: <br/>[`ReplyKeyboardMarkup`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-reply-keyboard-markup/index.html)، [`InlineKeyboardMarkup`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-inline-keyboard-markup/index.html)، [`ForceReply`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-force-reply/index.html)، [`ReplyKeyboardRemove`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-reply-keyboard-remove/index.html).

#### Inline Keyboard Markup

این سازنده به شما امکان می‌دهد دکمه‌های inline با هر ترکیبی از پارامترها بسازید.

```kotlin
message{ "Test" }.inlineKeyboardMarkup {
    "name" callback "callbackData"         //
    "buttonName" url "https://google.com"  //--- این دو دکمه در یک ردیف خواهند بود.
    newLine() // یا br()
    "otherButton" webAppInfo "data"       // این در ردیف دیگری خواهد بود

    // شما همچنین می‌توانید از یک سبک متفاوت درون سازنده استفاده کنید:
    callbackData("buttonName") { "callbackData" }
}.send(user, bot)

```

جزئیات بیشتر می‌توانید در مستندات سازنده [مشاهده کنید](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.builders/-inline-keyboard-markup-builder/index.html).

#### Reply Keyboard Markup

این سازنده به شما امکان می‌دهد دکمه‌های منو بسازید.

```kotlin
message{ "Test" }.replyKeyboardMarkup {
  + "Menu button"     // شما می‌توانید دکمه‌ها را با استفاده از اپراتور plus اضافه کنید
  + "Menu button 2"
  br() // برو به ردیف دوم
  "Send polls 👀" requestPoll true   // دکمه با پارامتر

  options {
    resizeKeyboard = true
  }
}.send(user, bot)
```

گزینه‌های اضافی قابل اجرا روی کیبورد را می‌توانید در [`ReplyKeyboardMarkupOptions`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.options/-reply-keyboard-markup-options/index.html) مشاهده کنید.

برای جزئیات بیشتر در مورد روش‌ها، مستندات سازنده [را ببینید](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.builders/-reply-keyboard-markup-builder/index.html).

استفاده از DSL برای جمع‌آوری markup کیبورد بیشتر راحت است، اما اگر لازم بود، شما همچنین می‌توانید markup را به صورت دستی اضافه کنید.

```kotlin
message{ "*Test*" }.markup {
    InlineKeyboardMarkup(
        InlineKeyboardButton("test", callbackData = "testCallback")
    )
}.send(user, bot)

```

```kotlin
message{ "*Test*" }.markup {
    ReplyKeyboardMarkup(
        KeyboardButton("Test menu button")
    )
}.send(user, bot)
```

### Entities
همچنین روشی برای ارسال [`MessageEntity`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.msg/-message-entity/index.html) وجود دارد.

مثال استفاده:

```kotlin
message{ "Test \$hello" }.replyKeyboardMarkup {
    +"Test menu button"
}.entities {
    5 to 15 url "https://google.com" // add TextLink
    entity(EntityType.Bold, 0, 4)
    entity(EntityType.Cashtag, 5, 5) // backslash شمرده نمی‌شود (چون برای کامپایلر استفاده می‌شود)
}.send(user, bot)
```

#### Entities متنی.

Entities همچنین می‌توانند از طریق متن برخی سازنده‌ها اضافه شوند، آن‌ها با رابط خاص [EntitiesContextBuilder](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.builders/-entities-ctx-builder/index.html) برچسب‌گذاری می‌شوند، که در ویژگی caption نیز وجود دارد.

مثال استفاده:

```kotlin
message { "usual text " - bold { "this is bold text" } - " continue usual" }.send(user, bot)
```

تمام انواع [نوع entity](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.msg/-entity-type/index.html) پشتیبانی می‌شود.

### Caption
همچنین، متد `caption` می‌تواند برای افزودن زیرنویس به فایل‌های رسانه‌ای استفاده شود.

مثال استفاده:

```kotlin
photo { "FILE_ID" }.caption { "Test caption" }.send(user, bot)
```


### همچنین ببینید

* [Bot context](Bot-Context.md)
* [FSM | Conversation handling](FSM-and-Conversation-handling.md)