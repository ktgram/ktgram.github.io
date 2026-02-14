---
---
title: Activites And Processors
---

### परिचय

इस लाइब्रेरी के संदर्भ में `Activity` वह अमूर्त इकाई है जो `@CommandHandler`, `@InputHandler`, `@UnprocessedHandler`, और `@CommonHandler` जैसी इकाइयों का सामान्यीकरण है।

[handlers article](Handlers.md) लेख भी देखें।

### गतिविधियों का संकलन

गतिविधियों को संकलन समय में सभी संदर्भों के साथ एकत्रित और तैयार किया जाता है (कार्यात्मक डीएसएल के माध्यम से परिभाषित को छोड़कर)।

यदि आप उस क्षेत्र को सीमित करना चाहते हैं जिसमें पैकेज की खोज की जाएगी, तो आप प्लगइन में पैरामीटर पास कर सकते हैं:

```gradle
ktGram {
    packages = listOf("com.example.mybot")
}
```

या प्लगइन के बिना ksp के माध्यम से:

```gradle
ksp {
    arg("package", "com.example.mybot")
}
```

ध्यान दें कि ऐसे मामले में, एकत्रित क्रियाओं को सही ढंग से संसाधित करने के लिए, आपको स्वयं उदाहरण में भी पैकेज निर्दिष्ट करना होगा।

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.mybot")

    bot.handleUpdates()
    // long-polling listener शुरू करें
}
```

यह विकल्प इसलिए जोड़ा गया है ताकि एकाधिक बॉट उदाहरण चलाए जा सकें:

```gradle
ktGram {
    packages = listOf("com.example.mybot", "com.example.mybot2")
}
```


या यदि आप प्लगइन का उपयोग नहीं कर रहे हैं तो विभिन्न पैकेज निर्दिष्ट करने के लिए आपको उन्हें `;` अलग करने वाले के साथ निर्दिष्ट करना होगा:

```gradle
ksp {
    arg("package", "com.example.mybot;com.example.mybot2")
}
```

### प्रसंस्करण

#### वेबहुक

अपने नियंत्रक (या किसी अन्य स्थान पर जहां `webhook` संसाधित किया जाता है) में, आप कॉल करें: [`bot.update.parseAndHandle(webhookString)`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.core/-tg-update-handler/index.html#706360827%2FFunctions%2F-880831646)

#### लंबा पोलिंग

कॉल करें: `bot.handleUpdates()` या `bot.update.setListener { handle(it) }` के माध्यम से


### देखें भी

* [Update parsing](Update-parsing.md)
* [Activity invocation](Activity-invocation.md)
* [Actions](Actions.md)

---