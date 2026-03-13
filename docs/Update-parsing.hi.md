---
---
title: अद्यतन पार्सिंग
---

### टेक्स्ट पेलोड

कुछ अद्यतनों में टेक्स्ट पेलोड हो सकता है जिसे आगे की प्रक्रिया के लिए पार्स किया जा सकता है। आइए उन्हें देखें:

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

सूचीबद्ध अद्यतनों से, एक विशिष्ट पैरामीटर चुना जाता है और [`TextReference`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-text-reference/index.html) के रूप में आगे की पार्सिंग के लिए लिया जाता है।

### पार्सिंग

चयनित पैरामीटर उपयुक्त कॉन्फ़िगर किए गए डिलीमिटर्स के साथ कमांड और उसके पैरामीटर में पार्स किए जाते हैं।

कॉन्फ़िगरेशन [`commandParsing`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.configuration/-bot-configuration/command-parsing.html) ब्लॉक देखें।

आप नीचे दिए गए आरेख में देख सकते हैं कि कौन से घटक लक्ष्य फ़ंक्शन के किन हिस्सों से मैप किए गए हैं।

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/7489099a-cca8-4049-a374-efaf6ce52128" alt="टेक्स्ट पार्सिंग आरेख" />
</p>

### @ParamMapping

सुविधा के लिए या किसी विशेष मामले के लिए [`@ParamMapping`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-param-mapping/index.html) नामक एक एनोटेशन भी है।

यह आपको आने वाले टेक्स्ट से पैरामीटर के नाम को किसी भी पैरामीटर में मैप करने की अनुमति देता है।

यह तब भी सुविधाजनक है जब आपका आने वाला डेटा सीमित हो, उदाहरण के लिए, `CallbackData` (64 अक्षर)।

उपयोग का उदाहरण देखें:
`greeting?name=Adam`

```kotlin
@CommandHandler(["greeting"])
suspend fun greeting(@ParamMapping("name") anyParameterName: String, user: User, bot: TelegramBot) {
    message { "Hello, $anyParameterName" }.send(to = user, via = bot)
}
```

और यह अनाम पैरामीटर पकड़ने के लिए भी उपयोग किया जा सकता है, उन मामलों में जहां पार्सर इस तरह से सेटअप किया गया हो कि पैरामीटर नाम छोड़ दिए जाते हैं या वे अनुपस्थित होते हैं, जो 'param_n' पैटर्न द्वारा पास हो जाते हैं, जहां `n` इसकी क्रम संख्या है।

उदाहरण के लिए इस तरह का टेक्स्ट - `myCommand?p1=v1&v2&p3=&p4=v4&p5=`, इस तरह पार्स किया जाएगा:
* कमांड - `myCommand`
* पैरामीटर
  * `p1` = `v1`
  * `param_2` = `v2`
  * `p3` = ``
  * `p4` = `v4`
  * `p5` = ``

जैसा कि आप देख सकते हैं चूंकि दूसरा पैरामीटर घोषित नाम नहीं रखता है इसलिए इसे `param_2` के रूप में प्रस्तुत किया गया है।

तो आप कॉलबैक में ही चर नामों को संक्षिप्त कर सकते हैं और कोड में स्पष्ट पठनीय नामों का उपयोग कर सकते हैं।

### Deeplink

ऊपर दी गई जानकारी को ध्यान में रखते हुए यदि आप अपने स्टार्ट कमांड में deeplink की अपेक्षा करते हैं तो आप इसे इस तरह पकड़ सकते हैं:

```kotlin
@CommandHandler(["/start"])
suspend fun start(@ParamMapping("param_1") deeplink: String?, user: User, bot: TelegramBot) {
    message { "deeplink is $deeplink" }.send(to = user, via = bot)
}
```

### ग्रुप कमांड

`commandParsing` कॉन्फ़िगरेशन में हमारे पास [`useIdentifierInGroupCommands`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.configuration/-command-parsing-configuration/use-identifier-in-group-commands.html) पैरामीटर है जब यह चालू होता है, तो हम कमांड मिलान प्रक्रिया में `TelegramBot.identifier` का उपयोग कर सकते हैं (यदि आप वर्णित पैरामीटर का उपयोग कर रहे हैं तो इसे बदलना न भूलें), यह कई बॉट्स के बीच समान कमांडों को अलग करने में मदद करता है, अन्यथा `@MyBot` भाग को बस छोड़ दिया जाएगा।

### भी देखें

* [एक्टिविटी आमंत्रण](Activity-invocation.md)
* [एक्टिविटीज़ और प्रोसेसर](Activites-and-Processors.md)
* [एक्शन](Actions.md)