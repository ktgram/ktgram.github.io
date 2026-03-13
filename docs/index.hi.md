---
---
title: Home
---

### Intro
आइए देखते हैं कि लाइब्रेरी अपडेट को सामान्य रूप से कैसे संभालती है:

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/442cc5f1-0256-425a-9f25-185fdd49fe0a" alt="Handling process diagram" />
</p>

अपडेट प्राप्त करने के बाद, हम तीन मुख्य चरण देख सकते हैं जो लाइब्रेरी द्वारा किए जाते हैं।

### Processing

Processing वह है जो प्राप्त अपडेट को [`ProcessedUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processed-update/index.html) की उपयुक्त सबक्लास में पुनः पैकेज करता है जो वहन किए जा रहे पेलोड पर निर्भर करता है।

यह चरण अपडेट को संचालित करना आसान बनाने और प्रोसेसिंग क्षमताओं का विस्तार करने के लिए आवश्यक है।

### Handling

अगला मुख्य चरण आता है, यहाँ हम स्वयं हैंडलिंग पर पहुँचते हैं।

### Global RateLimiter

यदि अपडेट में कोई उपयोगकर्ता है, तो हम ग्लोबल रेट लिमिटर की सीमा की जाँच करते हैं।

### Parse text

अगला, पेलोड के आधार पर, हम विशेष अपडेट घटक को लेते हैं जिसमें पाठ होता है और इसे कॉन्फ़िगरेशन के अनुसार पार्स करते हैं।

अधिक विस्तार से आप [update parsing article](Update-parsing.md) में देख सकते हैं।

### Find Activity

प्रोसेसिंग प्राथमिकता के अनुसार:

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/6178c410-9b9e-4045-9f03-4791b3f49894" alt="Handling priority diagram" />
</p>

हम पार्स किए गए डेटा और हम जिन गतिविधियों पर काम कर रहे हैं के बीच संबंध की तलाश कर रहे हैं।
जैसा कि हम प्राथमिकता आरेख पर देख सकते हैं, `Commands` हमेशा पहले आते हैं।

अर्थात यदि अपडेट में पाठ लोड किसी भी कमांड से मेल खाता है, तो आगे की खोज `Inputs`, `Common` और निश्चित रूप से `Unprocessed` क्रिया का निष्पादन नहीं किया जाएगा।

एकमात्र बात यह है कि यदि कोई `UpdateHandlers` होगा तो वह समानांतर में ट्रिगर होगा।

#### Commands

आइए कमांड और उनकी प्रोसेसिंग पर अधिक विस्तार से नज़र डालते हैं।

जैसा कि आपने देखा होगा, हालांकि प्रोसेसिंग कमांड के लिए एनोटेशन को [`CommandHandler`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-command-handler/index.html) कहा जाता है, यह टेलीग्राम बॉट्स में क्लासिक अवधारणा से अधिक बहुमुखी है।

##### Scopes

यह इसलिए है क्योंकि इसमें प्रोसेसिंग संभावनाओं की व्यापक सीमा है, अर्थात लक्ष्य फ़ंक्शन को न केवल पाठ मिलान पर बल्कि उपयुक्त अपडेट के प्रकार पर भी परिभाषित किया जा सकता है, यह स्कोप की अवधारणा है।

तदनुसार, प्रत्येक कमांड के पास स्कोप की भिन्न सूची के लिए अलग-अलग हैंडलर हो सकते हैं, या इसके विपरीत, कई के लिए एक कमांड हो सकता है।

नीचे आप देख सकते हैं कि पाठ पेलोड और स्कोप द्वारा मैपिंग कैसे की जाती है:

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/c870027e-750e-4bb8-a2ed-45ad93a55875" alt="Command scope diagram" />
</p>

#### Inputs

अगला, यदि पाठ पेलोड किसी भी कमांड से मेल नहीं खाता है तो इनपुट पॉइंट्स की खोज की जाती है।

अवधारणा कमांडलाइन एप्लिकेशन में इनपुट प्रतीक्षा के समान है, आप बॉट कंटेक्स्ट में किसी विशेष उपयोगकर्ता के लिए एक पॉइंट रखते हैं जो उसके अगले इनपुट को संभालेगा, इससे कोई फर्क नहीं पड़ता कि इसमें क्या है, मुख्य बात यह है कि अगला अपडेट में `User` होना चाहिए ताकि इसे सेट इनपुट प्रतीक्षा पॉइंट से संबंधित किया जा सके।

नीचे आप देख सकते हैं कि जब `Commands` पर कोई मिलान नहीं होता है तो अपडेट की प्रोसेसिंग का एक उदाहरण:

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/925d3e05-0985-43d5-8d6f-b3f2786ff212" alt="Priority example diagram" />
</p>

#### Commons

यदि हैंडलर कोई `commands` या `inputs` नहीं पाता है, तो यह पाठ लोड की जाँच `common` हैंडलर्स के खिलाफ करता है।

हम इसका दुरुपयोग किए बिना उपयोग करने की सलाह देते हैं, क्योंकि यह सभी प्रविष्टियों पर पुनरावृत्ति करके जाँच करता है।

#### Unprocessed

और अंतिम चरण, यदि हैंडलर कोई मिलान गतिविधि नहीं पाता है ([`UpdateHandler`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-update-handler/index.html) पूरी तरह से समानांतर में काम करता है और सामान्य गतिविधि नहीं माना जाता), तो [`UnprocessedHandler`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-unprocessed-handler/index.html) सक्रिय हो जाता है, यदि यह सेट है, तो यह इस मामले को संभालेगा, यह उपयोगकर्ता को चेतावनी देने के लिए उपयोगी हो सकता है कि कुछ गलत हो गया है।

अधिक विस्तार से [Handlers article](Handlers.md) में पढ़ें।

### Activity RateLimiter

गतिविधि खोजने के बाद, यह गतिविधि पैरामीटर में निर्दिष्ट पैरामीटर के अनुसार उपयोगकर्ता की दर सीमाओं की भी जाँच करता है।

### Activity

Activity से तात्पर्य टेलीग्राम बॉट लाइब्रेरी द्वारा संभाली जा सकने वाली विभिन्न प्रकार के हैंडलर से है, जिसमें Commands, Inputs, Regexes और Unprocessed हैंडलर शामिल हैं।

### Invocation

अंतिम प्रोसेसिंग चरण पाए गए गतिविधि का आह्वान है।

अधिक विवरण [invocation article](Activity-invocation.md) में पाया जा सकता है।

### See also

* [Update parsing](Update-parsing.md)
* [Activity invocation](Activity-invocation.md)
* [Handlers](Handlers.md)
* [Bot configuration](Bot-configuration.md)
* [Web starters (Spring, Ktor)](Web-starters-(Spring-and-Ktor.md))
---