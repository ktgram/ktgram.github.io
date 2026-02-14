---
---
title: बॉट संदर्भ
---

<p align="center">
  <img src="https://github.com/user-attachments/assets/60bb58ae-1806-4b8d-8550-833b09c2b606" alt="Bot context diagram" />
</p>

बॉट `UserData` और `ClassData` इंटरफेस के माध्यम से कुछ डेटा याद रखने की क्षमता भी प्रदान कर सकता है।

- [`userData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-user-data/index.html) उपयोगकर्ता-स्तरीय डेटा है।
- [`classData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-data/index.html) क्लास-स्तरीय डेटा है, अर्थात डेटा तब तक संग्रहीत रहेगा जब तक उपयोगकर्ता एक अलग क्लास में कमांड या इनपुट पर नहीं जाता। (फ़ंक्शन मोड में यह उपयोगकर्ता डेटा की तरह काम करेगा)

डिफ़ॉल्ट रूप से, कार्यान्वयन [`ConcurrentHashMap`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.collections/java.util.concurrent.-concurrent-map/) के माध्यम से प्रदान किया जाता है लेकिन इसे आपके द्वारा चुने गए डेटा स्टोरेज टूल्स का उपयोग करके [`UserData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-user-data/index.html) और [`ClassData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-data/index.html) इंटरफेस के माध्यम से बदला जा सकता है।


> [!CAUTION]
> आवश्यक कोडजेन बाइंडिंग उपलब्ध कराने के लिए ग्रेडल `kspKotlin`/या कोई प्रासंगिक ksp टास्क चलाना न भूलें।


इसे बदलने के लिए, आपको बस अपने कार्यान्वयन पर `@CtxProvider` एनोटेशन लगाना है और ग्रेडल ksp टास्क (या बिल्ड) चलाना है।

```kotlin
@CtxProvider
class MyRedis : UserData<String> {
    // ...
}
```

### देखें भी

* [होम](https://github.com/vendelieu/telegram-bot/wiki)
* [अपडेट पार्सिंग](Update-parsing.md)
---