---
---
title: Activity Invocation
---

Activity invocation के दौरान, बॉट कंटेक्स्ट को पास करना संभव है, क्योंकि इसे लक्ष्य फ़ंक्शन्स में पैरामीटर के रूप में घोषित किया गया है।

जो पैरामीटर पास किए जा सकते हैं:

* [`ProcessedUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processed-update/index.html) (और इसकी सभी सबक्लासेस) - वर्तमान प्रोसेसिंग अपडेट।
* [`ProcessingContext`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processing-context/index.html) - एक्टिविटी हैंडलिंग का निम्न स्तरीय कंटेक्स्ट।
* [`User`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types/-user/index.html) - यदि मौजूद है।
* [`Chat`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.chat/-chat/index.html) - यदि मौजूद है।
* [`TelegramBot`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot/-telegram-bot/index.html) - वर्तमान बॉट इंस्टेंस।

कस्टम प्रकार जोड़ना भी संभव है पास करने के लिए।

ऐसा करने के लिए, एक क्लास जोड़ें जो [`Autowiring<T>`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.marker/-autowiring/index.html) को implement करती है और इसे [`@Injectable`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-injectable/index.html) एनोटेशन से चिह्नित करें।

`Autowiring` इंटरफ़ेस को implement करने के बाद - `T` लक्ष्य फ़ंक्शन्स में पास करने के लिए उपलब्ध होगा और इंटरफ़ेस में वर्णित विधि के माध्यम से प्राप्त किया जाएगा।

```kotlin
@Injectable
object UserResolver : Autowiring<UserRecord> {
    override suspend fun get(update: ProcessedUpdate, bot: TelegramBot): UserRecord? {
        return userRepository.getUserByTgId(update.user.id)
    }
}
```

फ़ंक्शन्स में घोषित अन्य पैरामीटर parsed पैरामीटर में **खोजे** जाएंगे।

इसके अतिरिक्त, पास करते समय parsed पैरामीटर को निश्चित प्रकारों में कास्ट किया जा सकता है, यहाँ उनकी सूची है:

- `String`
- `Integer`
- `Long`
- `Short`
- `Float`
- `Double`

इसके अलावा, ध्यान दें कि यदि पैरामीटर घोषित हैं और गायब हैं (या parsed पैरामीटर में या उदाहरण के लिए `Update` में `User` गायब है) या घोषित प्रकार फ़ंक्शन में प्राप्त पैरामीटर से मेल नहीं खाता, **`null`** पास किया जाएगा इसलिए सावधान रहें।

सब कुछ संक्षेप में, यहाँ नीचे एक उदाहरण है कि फ़ंक्शन पैरामीटर आमतौर पर कैसे बनाए जाते हैं:

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/3c1d7830-8e5d-45fb-82bb-ac63f08c3782" alt="Invokation process diagram" />
</p>

### See also

* [Update parsing](Update-parsing.md)
* [Activities & Processors](Activites-and-Processors.md)
---