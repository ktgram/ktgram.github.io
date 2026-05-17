---
---
title: Useful Utilities And Tips
---


### Operating with ProcessedUpdate

[`ProcessedUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processed-update/index.html) एक generic class है updates के लिए जिसे, मूल डेटा के आधार पर, विभिन्न प्रकारों में प्रदान किया जा सकता है ([`MessageUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-message-update/index.html), [`CallbackQueryUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-callback-query-update/index.html), आदि)।

इसलिए आप आने वाले डेटा के प्रकार की जाँच कर सकते हैं और smartcasts के साथ कुछ डेटा को आगे बदल सकते हैं, उदाहरण के लिए:

```kotlin
// ...
if (update !is MessageUpdate) {
    message { "Only messages are allowed" }.send(user, bot)
    return
}
// Further on, ProcessedUpdate will be perceived as MessageUpdate.
```

एक [`UserReference`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-user-reference/index.html) इंटरफ़ेस भी है जो आपको यह निर्धारित करने देता है कि क्या अंदर कोई उपयोगकर्ता संदर्भ है, उपयोग का उदाहरण:

```kotlin
val user = if(update is UserReference) update.user else null

```

यदि आवश्यक हो तो वहाँ हमेशा मूल [`update`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types/-update/index.html) अपडेट पैरामीटर में मौजूद रहता है।


### Dependency injection

लाइब्रेरी सरल तंत्र का उपयोग करती है क्लासों को इनिशियलाइज़ करने के लिए जहाँ आपके अपडेट प्रोसेसिंग मेथड्स प्रदान किए गए एनोटेशन के साथ एनोटेटेड होते हैं।

[`ClassManagerImpl`](https://github.com/vendelieu/telegram-bot/blob/master/telegram-bot/src/commonMain/kotlin/eu/vendeli/tgbot/implementations/ClassManagerImpl.kt) डिफॉल्ट रूप से एनोटेटेड मेथड्स को कॉल करने के लिये उपयोग किया जाता है।

लेकिन यदि आप इसके लिए कुछ अन्य लाइब्रेरीज़ का उपयोग करना चाहते हैं तो आप [`ClassManager`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-manager/index.html) इंटरफ़ेस को पुनर्परिभाषित कर सकते हैं, <br/>अपने पसंदीदा तंत्र का उपयोग करके और बॉट को इनिशियलाइज़ करते समय इसे पास कर सकते हैं।

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.controllers") {
        classManager = ClassManagerImpl()
    }

    bot.handleUpdates()
}
```

### Filtering updates

यदि जटिल शर्तें नहीं हैं तो आप केवल कुछ अपडेट्स को प्रोसेस होने से फ़िल्टर कर सकते हैं:

```kotlin
// function where updates filtering condition defined
fun filteringFun(update: Update): Boolean = update.message?.text.isNullOrBlank()

fun main() = runBlocking {
  val bot = TelegramBot("BOT_TOKEN")

  // setting more specific processing flow for updates
  bot.update.setListener {
    if(filteringFun(it)) return@setListener

    // so simply, if the listener left the scope before reaching the handler function, that it is filtering.
    // actually you can even write directly if-condition there with return@setListener or extend filtering to separate class.

    handle(it) // or manual handling way with block
  }
}
```

अपनी कमांड मैचिंग में फ़िल्टरिंग को शामिल करने या प्रोसेस को बाहर रखने के लिये गार्ड्स या `@CommonHandler` देखें।

### Generalize options for different methods

यदि आपको अक्सर वही वैकल्पिक पैरामीटर लागू करने की आवश्यकता है, तो आप एक समान फ़ंक्शन लिख सकते हैं जो आपके काम आए और boilerplate को हल्का कर दे :)

कुछ सामान्य प्रॉपर्टीज़ को [different interfaces](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.options/-options/index.html) में विभाजित किया गया है।

```kotlin
@Suppress("NOTHING_TO_INLINE")
inline fun <T, R, O> T.markdownMode(crossinline block: O.() -> Unit = {}): T
        where               T : TgAction<R>,
                            T : OptionsFeature<T, O>,
                            O : Options,
                            O : OptionsParseMode =
    options {
        parseMode = ParseMode.Markdown
        block()
    }


// ... and in your code

message { "test" }.markdownMode().send(to, via)

```


---