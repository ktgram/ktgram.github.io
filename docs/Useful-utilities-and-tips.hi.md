---
---
title: उपयोगी उपयोगिताएँ और युक्तियाँ
---


### ProcessedUpdate के साथ कार्य करना

[`ProcessedUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processed-update/index.html) एक सामान्य वर्ग है जो अपडेट के लिए है जो मूल डेटा के आधार पर विभिन्न प्रकारों ([`MessageUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-message-update/index.html), [`CallbackQueryUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-callback-query-update/index.html), आदि) में प्रदान किया जा सकता है।

इसलिए आप आने वाले डेटा के प्रकार की जाँच कर सकते हैं और स्मार्टकास्ट के साथ आगे विशिष्ट डेटा को संचालित कर सकते हैं, उदाहरण के लिए:

```kotlin
// ...
if (update !is MessageUpdate) {
    message { "Only messages are allowed" }.send(user, bot)
    return
}
// आगे, ProcessedUpdate को MessageUpdate के रूप में देखा जाएगा।
```

इसमें [`UserReference`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-user-reference/index.html) इंटरफ़ेस भी है जो यह जाँचने देता है कि क्या अंदर उपयोगकर्ता संदर्भ है, उदाहरण उपयोग मामला:

```kotlin
val user = if(update is UserReference) update.user else null

```

यदि आवश्यक हो तो हमेशा मूल [`update`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types/-update/index.html) अपडेट पैरामीटर में होता है।


### निर्भरता इंजेक्शन

लाइब्रेरी सरल तंत्र का उपयोग करती है जहाँ आपके अपडेट प्रोसेसिंग विधियाँ प्रदान किए गए एनोटेशन के साथ एनोटेट होती हैं।

[`ClassManagerImpl`](https://github.com/vendelieu/telegram-bot/blob/master/telegram-bot/src/commonMain/kotlin/eu/vendeli/tgbot/implementations/ClassManagerImpl.kt) को डिफ़ॉल्ट रूप से एनोटेटेड विधियों को आमंत्रित करने के लिए उपयोग किया जाता है।

लेकिन यदि आप इसके लिए कुछ अन्य लाइब्रेरीज़ का उपयोग करना चाहते हैं तो आप [`ClassManager`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-manager/index.html) इंटरफ़ेस को पुन: परिभाषित कर सकते हैं, <br/>अपनी पसंदीदा तंत्र का उपयोग करके और इसे बॉट को प्रारंभ करते समय पास कर सकते हैं।

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.controllers") {
        classManager = ClassManagerImpl()
    }

    bot.handleUpdates()
}
```

### अपडेट को फ़िल्टर करना

यदि कोई जटिल शर्तें नहीं हैं तो आप सरलता से कुछ अपडेट को प्रोसेस किए जाने के लिए फ़िल्टर कर सकते हैं:

```kotlin
// वह फ़ंक्शन जहाँ अपडेट फ़िल्टरिंग शर्त परिभाषित है
fun filteringFun(update: Update): Boolean = update.message?.text.isNullOrBlank()

fun main() = runBlocking {
  val bot = TelegramBot("BOT_TOKEN")

  // अपडेट के लिए अधिक विशिष्ट प्रोसेसिंग प्रवाह सेट करना
  bot.update.setListener {
    if(filteringFun(it)) return@setListener

    // इसलिए सरलता से, यदि श्रोता हैंडलर फ़ंक्शन तक पहुँचने से पहले स्कोप से बाहर निकल जाता है, तो वह फ़िल्टरिंग कर रहा है।
    // वास्तव में आप वहाँ सीधे यदि-शर्त लिख सकते हैं return@setListener के साथ या फ़िल्टरिंग को अलग वर्ग में विस्तारित कर सकते हैं।

    handle(it) // या ब्लॉक के साथ मैनुअल हैंडलिंग तरीका
  }
}
```

अपने कमांड मिलान या बहिष्करण प्रक्रिया में फ़िल्टरिंग को शामिल करने के लिए गार्ड या `@CommonHandler` देखें।

### विभिन्न विधियों के लिए विकल्पों को सामान्यीकृत करना

यदि आपको अक्सर समान वैकल्पिक पैरामीटर लागू करने होते हैं, तो आप अपने लिए उपयुक्त समान फ़ंक्शन लिख सकते हैं और बॉयलरप्लेट कोड को हल्का कर सकते हैं :)

कुछ सामान्य गुण [विभिन्न इंटरफ़ेस](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.options/-options/index.html) में अलग किए गए हैं।

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


// ... और आपके कोड में

message { "test" }.markdownMode().send(to, via)

```