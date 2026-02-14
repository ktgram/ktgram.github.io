---
---
title: به‌روزرسانی پارسینگ
---

### بار متنی

برخی از به‌روزرسانی‌ها ممکن است بار متنی داشته باشند که می‌توان آن‌ها را برای پردازش بیشتر تجزیه کرد. بیایید به آن‌ها نگاهی بیندازیم:

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

از به‌روزرسانی‌های فهرست شده، یک پارامتر خاص انتخاب و به عنوان [`TextReference`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-text-reference/index.html) برای پردازش بیشتر در نظر گرفته می‌شود.

### پارسینگ

پارامترهای انتخاب شده با جداکننده‌های پیکربندی شده مناسب به دستور و پارامترهای آن تجزیه می‌شوند.

پیکربندی بلوک [`commandParsing`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.configuration/-bot-configuration/command-parsing.html) را مشاهده کنید.

می‌توانید در نمودار زیر ببینید کدام کامپوننت‌ها به کدام بخش از تابع هدف نگاشت شده‌اند.

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/7489099a-cca8-4049-a374-efaf6ce52128" alt="نمودار تجزیه متن" />
</p>

### @ParamMapping

همچنین یک انتزاع به نام [`@ParamMapping`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-param-mapping/index.html) برای راحتی یا هر مورد خاصی وجود دارد.

به شما اجازه می‌دهد نام پارامتر را از متن ورودی به هر پارامتری نگاشت کنید.

این همچنین برای زمانی که داده ورودی شما محدود است راحت است، به عنوان مثال `CallbackData` (64 کاراکتر).

مثال استفاده را مشاهده کنید:
`greeting?name=Adam`

```kotlin
@CommandHandler(["greeting"])
suspend fun greeting(@ParamMapping("name") anyParameterName: String, user: User, bot: TelegramBot) {
    message { "Hello, $anyParameterName" }.send(to = user, via = bot)
}
```

و همچنین می‌تواند برای گرفتن پارامترهای بدون نام استفاده شود، در مواردی که پارس‌گر طوری تنظیم شده که نام پارامترها رد شوند یا حتی وجود نداشته باشند، که با الگوی 'param_n' عبور می‌کند، جایی که `n` توالی آن است.

برای مثال متن زیر - `myCommand?p1=v1&v2&p3=&p4=v4&p5=`، به این صورت تجزیه می‌شود:
* دستور - `myCommand`
* پارامترها
  * `p1` = `v1`
  * `param_2` = `v2`
  * `p3` = ``
  * `p4` = `v4`
  * `p5` = ``

همان‌طور که می‌بینید از آنجا که پارامتر دوم نام اعلام شده ندارد، به عنوان `param_2` نمایش داده می‌شود.

پس می‌توانید نام متغیرها را در کالبک خود کوتاه کنید و از نام‌های خوانا و روشن در کد استفاده کنید.

### Deeplink

با توجه به اطلاعات بالا، اگر در دستور start خود deeplink انتظار دارید می‌توانید آن را با:

```kotlin
@CommandHandler(["/start"])
suspend fun start(@ParamMapping("param_1") deeplink: String?, user: User, bot: TelegramBot) {
    message { "deeplink is $deeplink" }.send(to = user, via = bot)
}
```

بگیرید.

### دستورات گروهی

در پیکربندی `commandParsing` ما پارامتر [`useIdentifierInGroupCommands`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.configuration/-command-parsing-configuration/use-identifier-in-group-commands.html) داریم که وقتی روشن است، می‌توانیم از `TelegramBot.identifier` (فراموش نکنید که اگر از پارامتر توصیف شده استفاده می‌کنید آن را تغییر دهید) در فرآیند تطبیق دستور استفاده کنیم، این به جداسازی دستورات مشابه بین چندین ربات کمک می‌کند، در غیر این صورت بخش `@MyBot` صرفاً رد می‌شود.

### همچنین ببینید

* [فعال‌سازی فعالیت](Activity-invocation.md)
* [فعالیت‌ها و پردازش‌گرها](Activites-and-Processors.md)
* [اقدامات](Actions.md)