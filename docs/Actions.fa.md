---
---
title: Actions
---

### تمام درخواست‌ها اقدامات هستند
تمام درخواست‌های API تلگرام انواع مختلفی از رابط [`TgAction`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.action/-tg-action/index.html) هستند که روش‌های مختلفی مانند [`SendMessageAction`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.api.message/-send-message-action/index.html) را پیاده‌سازی می‌کنند، <br/>که به صورت توابع نوع [`message()`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.api.message/message.html) برای راحتی رابط کتابخانه بسته‌بندی شده‌اند.

<p align="center">
    <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/2d097d60-1907-4ca1-8ad3-3ee8d223f8eb" alt="نمودار اقدامات" />
</p>

هر `Action` ممکن است روش‌های مربوط به خودش را داشته باشد، بسته به [`Feature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-feature/index.html) در دسترس.

### ویژگی‌ها

اقدامات مختلف ممکن است ویژگی‌های مختلف [`Features`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-feature/index.html) را بر اساس API Bot تلگرام داشته باشند، مانند:
[`OptionsFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-options-feature/index.html)،
[`MarkupFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-markup-feature/index.html)
[`EntitiesFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-entities-feature/index.html)
[`CaptionFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-caption-feature/index.html).

بیایید نگاه دقیق‌تری به آنها بیندازیم:

### گزینه‌ها
برای مثال، [`OptionsFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-options-feature/index.html) برای گذراندن پارامترهای اختیاری استفاده می‌شود.

هر اقدام نوع خودش از گزینه‌ها را دارد، مربوط به آن را می‌توانید در خود `Action` در پارامتر `options`، در بخش خصوصیات مشاهده کنید. <br/>برای مثال، `sendMessage` که یک داده‌کلاس [`MessageOptions`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.options/-message-options/index.html) با پارامترهای مختلف به عنوان گزینه‌ها را شامل می‌شود.

مثال استفاده:

```kotlin
message{ "*Test*" }.options {
    parseMode = ParseMode.Markdown
}.send(user, bot)
```
### Markup

همچنین روشی برای ارسال markup وجود دارد که تمام نوع [کیبردها](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.marker/-keyboard/index.html) را پشتیبانی می‌کند: <br/>[`ReplyKeyboardMarkup`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-reply-keyboard-markup/index.html)، [`InlineKeyboardMarkup`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-inline-keyboard-markup/index.html)، [`ForceReply`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-force-reply/index.html)، [`ReplyKeyboardRemove`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-reply-keyboard-remove/index.html).

#### Inline Keyboard Markup

این builder به شما امکان می‌دهد دکمه‌های inline با هر ترکیبی از پارامترها بسازید.

```kotlin
message{ "Test" }.inlineKeyboardMarkup {
    "name" callback "callbackData"         //
    "buttonName" url "https://google.com"  //--- این دو دکمه در یک ردیف خواهند بود.
    newLine() // یا br()
    "otherButton" webAppInfo "data"       // این در ردیف دیگری خواهد بود

    // شما می‌توانید سبک متفاوتی را در درون builder استفاده کنید:
    callbackData("buttonName") { "callbackData" }
}.send(user, bot)

```

جزئیات بیشتر می‌توانید در [مستندات](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.builders/-inline-keyboard-markup-builder/index.html) builder مشاهده کنید.

#### Reply Keyboard Markup

این builder به شما امکان می‌دهد دکمه‌های منو بسازید.

```kotlin
message{ "Test" }.replyKeyboardMarkup {
  + "Menu button"     // شما می‌توانید دکمه‌ها را با استفاده از اپراتور plus اضافه کنید
  + "Menu button 2"
  br() // به ردیف دوم برو
  "Send polls 👀" requestPoll true   // دکمه با پارامتر

  options {
    resizeKeyboard = true
  }
}.send(user, bot)
```

گزینه‌های اضافی قابل اجرا روی کیبرد را می‌توانید در [`ReplyKeyboardMarkupOptions`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.options/-reply-keyboard-markup-options/index.html) مشاهده کنید.

برای جزئیات بیشتر در مورد روش‌ها می‌توانید [مستندات](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.builders/-reply-keyboard-markup-builder/index.html) builder را مشاهده کنید.

بیشتر راحت است که از DSL برای جمع‌آوری markup کیبرد استفاده کنید، اما اگر لازم بود، شما همچنین می‌توانید markup را به صورت دستی اضافه کنید.

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
    5 to 15 url "https://google.com" // اضافه کردن TextLink
    entity(EntityType.Bold, 0, 4)
    entity(EntityType.Cashtag, 5, 5) // بک‌اسلش شمرده نمی‌شود (چون برای کامپایلر استفاده می‌شود)
}.send(user, bot)
```

#### Entities متنی.

Entities همچنین می‌توانند از طریق متن ساختاری بعضی سازه‌ها اضافه شوند، آنها با رابط خاص [EntitiesContextBuilder](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.builders/-entities-ctx-builder/index.html) برچسب‌گذاری می‌شوند، که در ویژگی caption نیز وجود دارد.

مثال استفاده:

```kotlin
message { "متن معمولی " - bold { "این متن bold است" } - " ادامه معمولی" }.send(user, bot)
```

تمام انواع [نوع entity](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.msg/-entity-type/index.html) پشتیبانی می‌شود.

### Caption
همچنین متد `caption` می‌تواند برای اضافه کردن کپشن به فایل‌های رسانه‌ای استفاده شود.

مثال استفاده:

```kotlin
photo { "FILE_ID" }.caption { "Test caption" }.send(user, bot)
```


### همچنین ببینید

* [متن بات](Bot-Context.md)
* [FSM | مدیریت گفتگو](FSM-and-Conversation-handling.md)