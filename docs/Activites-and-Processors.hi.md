---
---
title: Activites And Processors
---

### Introduction

`Activity` इस लाइब्रेरी की शर्तों में वह अमूर्त इकाई है जो `@CommandHandler`, `@InputHandler`, `@UnprocessedHandler`, `@CommonHandler`, `@UpdateHandler`, और `@WizardHandler` जैसी इकाइयों का सामान्यीकरण है।

साथ ही [handlers article](Handlers.md) देखें।

### Collecting activities

Activities को **compile time** पर **ktnip** KSP प्रोसेसर द्वारा खोजा और जोड़ा जाता है। [Functional DSL](Handlers#functional-dsl.md) एकमात्र अपवाद है — `bot.setFunctionality { ... }` के माध्यम से परिभाषित हैंडलर रनटाइम पर रजिस्टर्ड होते हैं।

यदि आप पैकेज की खोज सीमा को सीमित करना चाहते हैं, तो प्लगइन में एक पैरामीटर पास कर सकते हैं:

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

ध्यान दें कि ऐसे मामले में, एकत्रित actions को सही ढंग से प्रोसेस करने के लिए, आपको स्वयं इंस्टेंस में भी पैकेज निर्दिष्ट करना होगा।

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.mybot")

    bot.handleUpdates()
    // start long-polling listener
}
```

यह विकल्प कई bot इंस्टेंस चलाने के लिए जोड़ा गया है:

```gradle
ktGram {
    packages = listOf("com.example.mybot", "com.example.mybot2")
}
```


या यदि आप प्लगइन का उपयोग नहीं कर रहे हैं, तो विभिन्न पैकेज निर्दिष्ट करने के लिए `;` सेपरेटर का उपयोग करें:

```gradle
ksp {
    arg("package", "com.example.mybot;com.example.mybot2")
}
```

### Processing

#### Webhooks

अपने कंट्रोलर (या किसी अन्य स्थान जहाँ `webhook` प्रोसेस किया जाता है) में आप कॉल करते हैं: [`bot.update.parseAndHandle(webhookString)`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.core/-tg-update-handler/index.html#706360827%2FFunctions%2F-880831646)

#### Long polling

कॉल करें: `bot.handleUpdates()` या `bot.update.setListener { handle(it) }` के माध्यम से


### See also

* [Update parsing](Update-parsing.md)
* [Activity invocation](Activity-invocation.md)
* [Actions](Actions.md)

---