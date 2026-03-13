---
---
title: به‌روزرسانی تجزیه
---

### محتوای متنی

برخی از به‌روزرسانی‌ها ممکن است حاوی محتوای متنی باشند که برای پردازش بیشتر قابل تجزیه هستند. بیایید به آن‌ها نگاهی بیندازیم:

* `MessageUpdate` -> `message.text`
* `EditedMessageUpdate` -> `editedMessage.text`
* `ChannelPostUpdate` -> `channelPost.text`
* `EditedChannelPostUpdate` -> `editedChannelPost.text`
* `InlineQueryUpdate` -> `inlineQuery.query`
* `ChosenInlineResultUpdate` -> `chosenInlineResult.query`
* `CallbackQueryUpdate` -> `callbackQuery.data`
* `ShippingQueryUpdate` -> `shippingQuery.invoicePayload`
* `PreCheckoutQueryUpdate` -> `preCheckoutQuery.invoicePayload`
* `PollUpdate` -> `poll.question`
* `PurchasedPaidMediaUpdate` -> `purchasedPaidMedia.paidMediaPayload`

از به‌روزرسانی‌های لیست شده، یک پارامتر خاص انتخاب شده و به عنوان [`TextReference`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-text-reference/index.html) در نظر گرفته شده و برای تجزیه بیشتر استفاده می‌شود.

### تجزیه

پارامترهای انتخاب شده با جداکننده‌های پیکربندی شده مناسب به فرمان و پارامترهای آن تجزیه می‌شوند.

پیکربندی [`commandParsing`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.configuration/-bot-configuration/command-parsing.html) را مشاهده کنید.

در نمودار زیر می‌توانید ببینید کدام کامپوننت‌ها به کدام بخش از تابع هدف نگاشت شده‌اند.

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/7489099a-cca8-4049-a374-efaf6ce52128" alt="نمودار تجزیه متن" />
</p>

### @ParamMapping

برای راحتی یا هر مورد خاص، یک آنوتشن به نام [`@ParamMapping`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-param-mapping/index.html) نیز وجود دارد.

این آنوتشن به شما امکان می‌دهد نام پارامتر از متن ورودی را به هر پارامتری نگاشت دهید.

این کار همچنین برای زمانی که داده ورودی شما محدود است، مانند `CallbackData` (64 کاراکتر)، راحت است.

مثالی از کاربرد را مشاهده کنید:
`greeting?name=Adam`

```kotlin
@CommandHandler(["greeting"])
suspend fun greeting(@ParamMapping("name") anyParameterName: String, user: User, bot: TelegramBot) {
    message { "Hello, $anyParameterName" }.send(to = user, via = bot)
}
```

همچنین می‌تواند برای گرفتن پارامترهای بدون نام استفاده شود، در مواردی که تجزیه‌گر به گونه‌ای تنظیم شده باشد که نام پارامترها رد می‌شوند یا حتی وجود نداشته باشند، که با الگوی 'param_n' عبور می‌کند، که در آن `n` توالی آن است.

برای مثال، این متن - `myCommand?p1=v1&v2&p3=&p4=v4&p5=`، به این صورت تجزیه می‌شود:
* فرمان - `myCommand`
* پارامترها
  * `p1` = `v1`
  * `param_2` = `v2`
  * `p3` = ``
  * `p4` = `v4`
  * `p5` = ``

همان‌طور که می‌بینید از آنجا که پارامتر دوم نام اعلام شده ندارد، به عنوان `param_2` نمایش داده شده است.

بنابراین می‌توانید نام متغیرها را در کال‌بک خود مخفی کنید و از نام‌های قابل خواندن واضح در کد استفاده کنید.

### لینک عمیق

با توجه به اطلاعات بالا، اگر در فرمان شروع خود انتظار لینک عمیق دارید، می‌توانید آن را به این صورت بگیرید:

```kotlin
@CommandHandler(["/start"])
suspend fun start(@ParamMapping("param_1") deeplink: String?, user: User, bot: TelegramBot) {
    message { "deeplink is $deeplink" }.send(to = user, via = bot)
}
```

### فرمان‌های گروهی

در پیکربندی `commandParsing` ما پارامتری به نام [`useIdentifierInGroupCommands`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.configuration/-command-parsing-configuration/use-identifier-in-group-commands.html) داریم که وقتی فعال باشد، می‌توانیم از `TelegramBot.identifier` (فراموش نکنید که اگر از این پارامتر استفاده می‌کنید آن را تغییر دهید) در فرآیند تطبیق فرمان استفاده کنیم، این کار به جداسازی فرمان‌های مشابه بین چندین ربات کمک می‌کند، در غیر این صورت بخش `@MyBot` صرفاً رد خواهد شد.

### همچنین ببینید

* [فعال‌سازی فعالیت](Activity-invocation.md)
* [فعالیت‌ها و پردازنده‌ها](Activites-and-Processors.md)
* [اقدامات](Actions.md)