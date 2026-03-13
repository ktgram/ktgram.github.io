---
---
title: एक्टिविटी इनवोकेशन
---

एक्टिविटी इनवोकेशन के दौरान, बॉट कंटेक्स्ट पास करना संभव है, क्योंकि इसे टारगेट फंक्शन्स में पैरामीटर के रूप में घोषित किया गया है।

जो पैरामीटर पास किए जा सकते हैं:

* [`ProcessedUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processed-update/index.html) (और इसके सभी सबक्लास) - वर्तमान प्रोसेसिंग अपडेट।
* [`ProcessingContext`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processing-context/index.html) - एक्टिविटी हैंडलिंग का निम्न स्तरीय कंटेक्स्ट।
* [`User`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types/-user/index.html) - यदि उपलब्ध हो।
* [`Chat`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.chat/-chat/index.html) - यदि उपलब्ध हो।
* [`TelegramBot`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot/-telegram-bot/index.html) - वर्तमान बॉट इंस्टेंस।

कस्टम प्रकार पास करने के लिए जोड़ना भी संभव है।

ऐसा करने के लिए, [`Autowiring<T>`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.marker/-autowiring/index.html) को लागू करने वाली क्लास जोड़ें और इसे [`@Injectable`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-injectable/index.html) एनोटेशन से चिह्नित करें।

`Autowiring` इंटरफेस को लागू करने के बाद - `T` टारगेट फंक्शन्स में पास करने के लिए उपलब्ध होगा और इंटरफेस में वर्णित विधि के माध्यम से प्राप्त किया जाएगा।

```kotlin
@Injectable
object UserResolver : Autowiring<UserRecord> {
    override suspend fun get(update: ProcessedUpdate, bot: TelegramBot): UserRecord? {
        return userRepository.getUserByTgId(update.user.id)
    }
}
```

फंक्शन्स में घोषित अन्य पैरामीटर **खोजे** जाएंगे पार्स किए गए पैरामीटर में।

इसके अलावा, पास करते समय पार्स किए गए पैरामीटर को कुछ विशिष्ट प्रकारों में कास्ट किया जा सकता है, यहां उनकी सूची है:

- `String`
- `Integer`
- `Long`
- `Short`
- `Float`
- `Double`

इसके अतिरिक्त, ध्यान दें कि यदि पैरामीटर घोषित हैं और गायब हैं (या पार्स किए गए पैरामीटर में या उदाहरण के लिए `Update` में `User` गायब है) या घोषित प्रकार फंक्शन में प्राप्त पैरामीटर से मेल नहीं खाता, **`null`** पास किया जाएगा इसलिए सावधान रहें।

सब कुछ सारांशित करते हुए, नीचे यहां एक उदाहरण है कि फंक्शन पैरामीटर आमतौर पर कैसे बनते हैं:

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/3c1d7830-8e5d-45fb-82bb-ac63f08c3782" alt="इनवोकेशन प्रोसेस डायग्राम" />
</p>

### देखें भी

* [अपडेट पार्सिंग](Update-parsing.md)
* [एक्टिविटीज़ और प्रोसेसर्स](Activites-and-Processors.md)
---