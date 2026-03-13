---
---
title: कार्रवाइयाँ
---

### सभी अनुरोध कार्रवाइयाँ हैं
सभी टेलीग्राम API अनुरोध विभिन्न प्रकार के [`TgAction`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.action/-tg-action/index.html) इंटरफेस हैं जो विभिन्न विधियों को लागू करते हैं जैसे [`SendMessageAction`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.api.message/-send-message-action/index.html), <br/>जो [`message()`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.api.message/message.html) - प्रकार के फ़ंक्शन के रूप में लपेटे गए हैं लाइब्रेरी इंटरफ़ेस की सुविधा के लिए।

<p align="center">
    <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/2d097d60-1907-4ca1-8ad3-3ee8d223f8eb" alt="Actions diagram" />
</p>

प्रत्येक `कार्रवाई` की अपनी संभावित विधियाँ हो सकती हैं, उपलब्ध [`Feature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-feature/index.html) पर निर्भर करता है।

### सुविधाएँ

विभिन्न कार्रवाइयों में विभिन्न [`Features`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-feature/index.html) हो सकते हैं टेलीग्राम बॉट API पर निर्भर करता है, जैसे:
[`OptionsFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-options-feature/index.html),
[`MarkupFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-markup-feature/index.html)
[`EntitiesFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-entities-feature/index.html)
[`CaptionFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-caption-feature/index.html).

आइए उन्हें करीब से देखें:

### विकल्प
उदाहरण के लिए, [`OptionsFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-options-feature/index.html) का उपयोग वैकल्पिक पैरामीटर पास करने के लिए किया जाता है।

प्रत्येक कार्रवाई के अपने विकल्पों का प्रकार होता है, संबंधित आप `कार्रवाई` में स्वयं `विकल्प` पैरामीटर में गुण अनुभाग में देख सकते हैं। <br/>उदाहरण के लिए, `sendMessage` जिसमें विभिन्न पैरामीटर विकल्पों के साथ [`MessageOptions`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.options/-message-options/index.html) डेटा क्लास होता है।

उपयोग का उदाहरण:

```kotlin
message{ "*Test*" }.options {
    parseMode = ParseMode.Markdown
}.send(user, bot)
```
### मार्कअप

कीबोर्ड के सभी प्रकार के [कीबोर्ड](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.marker/-keyboard/index.html) भेजने के लिए एक विधि भी है: <br/>[`ReplyKeyboardMarkup`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-reply-keyboard-markup/index.html), [`InlineKeyboardMarkup`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-inline-keyboard-markup/index.html), [`ForceReply`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-force-reply/index.html), [`ReplyKeyboardRemove`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-reply-keyboard-remove/index.html).

#### इनलाइन कीबोर्ड मार्कअप

यह बिल्डर आपको किसी भी पैरामीटर संयोजन के साथ इनलाइन बटन बनाने की अनुमति देता है।

```kotlin
message{ "Test" }.inlineKeyboardMarkup {
    "name" callback "callbackData"         //
    "buttonName" url "https://google.com"  //--- ये दो बटन एक ही पंक्ति में होंगे।
    newLine() // या br()
    "otherButton" webAppInfo "data"       // यह अन्य पंक्ति में होगा

    // आप बिल्डर के भीतर विभिन्न शैलियों का भी उपयोग कर सकते हैं:
    callbackData("buttonName") { "callbackData" }
}.send(user, bot)

```

अधिक विवरण बिल्डर [दस्तावेज़ीकरण](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.builders/-inline-keyboard-markup-builder/index.html) में देखा जा सकता है।

#### रिप्लाई कीबोर्ड मार्कअप

यह बिल्डर मेनू बटन बनाने की अनुमति देता है।

```kotlin
message{ "Test" }.replyKeyboardMarkup {
  + "Menu button"     // आप यूनरी प्लस ऑपरेटर का उपयोग करके बटन जोड़ सकते हैं
  + "Menu button 2"
  br() // दूसरी पंक्ति पर जाएं
  "Send polls 👀" requestPoll true   // पैरामीटर के साथ बटन

  options {
    resizeKeyboard = true
  }
}.send(user, bot)
```

कीबोर्ड पर लागू होने वाले अतिरिक्त विकल्प [`ReplyKeyboardMarkupOptions`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.options/-reply-keyboard-markup-options/index.html) में देखे जा सकते हैं।

विधियों के बारे में अधिक विवरण के लिए बिल्डर [दस्तावेज़ीकरण](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.builders/-reply-keyboard-markup-builder/index.html) देखें।

कीबोर्ड मार्कअप एकत्र करने के लिए डीएसएल का उपयोग करना अधिकतर सुविधाजनक है, लेकिन यदि आवश्यक हो, तो आप मार्कअप को मैन्युअल रूप से भी जोड़ सकते हैं।

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

### इकाइयाँ
[`MessageEntity`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.msg/-message-entity/index.html) भेजने के लिए एक विधि भी है।

उपयोग का उदाहरण:

```kotlin
message{ "Test \$hello" }.replyKeyboardMarkup {
    +"Test menu button"
}.entities {
    5 to 15 url "https://google.com" // TextLink जोड़ें
    entity(EntityType.Bold, 0, 4)
    entity(EntityType.Cashtag, 5, 5) // बैकस्लैश गिनती में नहीं आता (क्योंकि इसका उपयोग कंपाइलर के लिए किया जाता है)
}.send(user, bot)
```

#### संदर्भात्मक इकाइयाँ।

इकाइयाँ कुछ निर्माणों के संदर्भ के माध्यम से भी जोड़ी जा सकती हैं, उन्हें विशिष्ट [EntitiesContextBuilder](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.builders/-entities-ctx-builder/index.html) इंटरफ़ेस द्वारा लेबल किया जाता है, यह कैप्शन सुविधा में भी मौजूद है।

उपयोग का उदाहरण:

```kotlin
message { "usual text " - bold { "this is bold text" } - " continue usual" }.send(user, bot)
```

सभी प्रकार की [इकाई प्रकार](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.msg/-entity-type/index.html) समर्थित हैं।

### कैप्शन
इसके अलावा, मीडिया फ़ाइलों के लिए कैप्शन जोड़ने के लिए `caption` विधि का उपयोग किया जा सकता है।

उपयोग का उदाहरण:

```kotlin
photo { "FILE_ID" }.caption { "Test caption" }.send(user, bot)
```


### भी देखें

* [बॉट संदर्भ](Bot-Context.md)
* [FSM | संवाद संभालना](FSM-and-Conversation-handling.md)