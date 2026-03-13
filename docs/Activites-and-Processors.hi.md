---
---
title: Activites And Processors
---

### परिचय

इस लाइब्रेरी के शब्दों में, `Activity` एक अमूर्त इकाई है जो `@CommandHandler`, `@InputHandler`, `@UnprocessedHandler`, और `@CommonHandler` जैसी इकाइयों का सामान्यीकरण है।

कृपया [handlers article](Handlers.md) भी देखें।

### गतिविधियों को एकत्र करना

गतिविधियों को कंपाइल समय में एकत्रित और तैयार किया जाता है (फंक्शनल डीएसएल के माध्यम से परिभाषित को छोड़कर)।

यदि आप उस क्षेत्र को सीमित करना चाहते हैं जिसमें पैकेज की खोज की जाएगी, तो आप प्लगइन को पैरामीटर पास कर सकते हैं:

```gradle
ktGram {
    packages = listOf("com.example.mybot")
}
```

या प्लगइन के बिना ksp के माध्यम से:

```kotlin
ksp {
    arg("package", "com.example.mybot")
}
```

ध्यान दें कि इस तरह के मामले में, एकत्रित क्रियाओं को सही ढंग से संसाधित करने के लिए, आपको इंस्टेंस में स्वयं पैकेज भी निर्दिष्ट करना होगा।

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.mybot")

    bot.handleUpdates()
    // लंबे-पोलिंग श्रोता शुरू करें
}
```

यह विकल्प इसलिए जोड़ा गया है ताकि एकाधिक बॉट इंस्टेंस चलाए जा सकें:

```gradle
ktGram {
    packages = listOf("com.example.mybot", "com.example.mybot2")
}
```


या यदि आप प्लगइन का उपयोग नहीं कर रहे हैं तो विभिन्न पैकेज निर्दिष्ट करने के लिए आपको उन्हें `;` सेपरेटर के साथ निर्दिष्ट करना होगा:

```gradle
ksp {
    arg("package", "com.example.mybot;com.example.mybot2")
}
```

### प्रोसेसिंग

#### वेबहुक

अपने कंट्रोलर (या किसी अन्य स्थान पर जहां `webhook` संसाधित होता है) में, आप कॉल करते हैं: [`bot.update.parseAndHandle(webhookString)`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.core/-tg-update-handler/index.html#706360827%2FFunctions%2F-880831646)

#### लंबे-पोलिंग

कॉल करें: `bot.handleUpdates()` या `bot.update.setListener { handle(it) }` के माध्यम से


### इसे भी देखें

* [Update parsing](Update-parsing.md)
* [Activity invocation](Activity-invocation.md)
* [Actions](Actions.md)