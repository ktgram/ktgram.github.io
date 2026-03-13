---
---
title: बॉट कॉन्फ़िगरेशन
---

लाइब्रेरी कई कॉन्फ़िगरेशन विकल्प प्रदान करती है, आप [`BotConfiguration`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.configuration/-bot-configuration/index.html) क्लास विवरण में एपीआई संदर्भ देख सकते हैं।

बॉट को कॉन्फ़िगर करने के लिए दो तरीके भी हैं:

### कॉन्फ़िगरेटर लैम्ब्डा

```kotlin
// ...
val bot = TelegramBot("BOT_TOKEN") {
  inputListener = RedisInputListenerImpl()
  classManager = KoinClassManagerImpl()
  logging {
      botLogLevel = LogLvl.DEBUG
  }
}
// ...
```

### ConfigLoader इंटरफ़ेस

एक विशेष [`ConfigLoader`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.helper/-config-loader/index.html) इंटरफ़ेस के माध्यम से कॉन्फ़िगर करने की भी क्षमता है,<br/> जिसका उपयोग आप बाहरी स्रोतों (`properties`, `command line args`, आदि) से सेटिंग्स लोड करने के लिए कर सकते हैं।

इस इंटरफ़ेस के कार्यान्वयन को सेकेंडरी कंस्ट्रक्टर के माध्यम से पास किया जा सकता है और उदाहरण इसी अनुसार कॉन्फ़िगर किया जाएगा।

```kotlin
val bot = TelegramBot(ConfigLoaderImpl)
```

वर्तमान में कई मॉड्यूल प्रदान किए गए हैं जो इस इंटरफ़ेस को लागू करते हैं जैसे `ktgram-config-env`, `ktgram-config-toml`।

### BotConfiguration अवलोकन

#### BotConfiguration

`BotConfiguration` क्लास बॉट को कॉन्फ़िगर करने के लिए केंद्रीय हब है। इसमें बॉट की पहचान करने, एपीआई होस्ट सेट करने, यह निर्धारित करने के लिए गुण शामिल हैं कि क्या बॉट टेस्ट वातावरण में काम करता है, इनपुट को संभालना, क्लासेस का प्रबंधन करना, और इनपुट ऑटो-हटाने को नियंत्रित करना। इसके अतिरिक्त, यह रेट लिमिटिंग, HTTP क्लाइंट कॉन्फ़िगरेशन, लॉगिंग, अपडेट लिसनिंग, और कमांड पार्सिंग के लिए आंतरिक गुण प्रदान करता है।

##### गुण

- `identifier`: मल्टी-बॉट प्रोसेसिंग के दौरान विभिन्न बॉट उदाहरणों की पहचान करता है।
- `apiHost`: टेलीग्राम एपीआई का होस्ट।
- `isTestEnv`: यह निर्धारित करने वाला फ्लैग कि क्या बॉट टेस्ट वातावरण में काम करता है।
- `inputListener`: इनपुट हैंडलिंग क्लास का उदाहरण।
- `classManager`: क्लासेस प्राप्त करने के लिए उपयोग किया जाने वाला मैनेजर।
- `inputAutoRemoval`: प्रोसेसिंग के दौरान इनपुट पॉइंट के ऑटो-डिलीशन को नियंत्रित करने वाला फ्लैग।
- `exceptionHandlingStrategy`: अपवादों को संभालने की रणनीति को परिभाषित करता है।
    * `CollectToChannel` - `TgUpdateHandler.caughtExceptions` में एकत्र करें।
    * `Throw` - फिर से `TgException` के साथ फेंकें।
    * `DoNothing` - कुछ न करें :)
    * `Handle` - कस्टम हैंडलर सेट करें।
- `throwExOnActionsFailure`: किसी भी बॉट रिक्वेस्ट के विफल होने पर अपवाद फेंकता है।

##### कॉन्फ़िगरेशन ब्लॉक

`BotConfiguration` अपने आंतरिक घटकों को कॉन्फ़िगर करने के लिए फ़ंक्शंस भी प्रदान करता है:

- `httpClient(block: HttpConfiguration.() -> Unit)`: HTTP क्लाइंट को कॉन्फ़िगर करता है।
- `logging(block: LoggingConfiguration.() -> Unit)`: लॉगिंग को कॉन्फ़िगर करता है।
- `rateLimiter(block: RateLimiterConfiguration.() -> Unit)`: रिक्वेस्ट लिमिटिंग को कॉन्फ़िगर करता है।
- `updatesListener(block: UpdatesListenerConfiguration.() -> Unit)`: अपडेट्स लिसनर को कॉन्फ़िगर करता है।
- `commandParsing(block: CommandParsingConfiguration.() -> Unit)`: कमांड पार्सिंग पैटर्न निर्दिष्ट करता है।

### संबंधित कॉन्फ़िगरेशन क्लासेस

#### RateLimiterConfiguration

ग्लोबल रेट लिमिटिंग को कॉन्फ़िगर करता है।

- `limits`: ग्लोबल रेट लिमिट्स।
- `mechanism`: रेट लिमिटिंग के लिए उपयोग किया जाने वाला तंत्र, डिफ़ॉल्ट टोकनबकेट एल्गोरिदम है।
- `exceededAction`: जब सीमा पार हो जाए तो लागू की जाने वाली क्रिया।

#### HttpConfiguration

बॉट के HTTP क्लाइंट के लिए कॉन्फ़िगरेशन शामिल करता है।

- `requestTimeoutMillis`: मिलीसेकंड में रिक्वेस्ट टाइमआउट।
- `connectTimeoutMillis`: कनेक्शन टाइमआउट मिलीसेकंड में।
- `socketTimeoutMillis`: सॉकेट टाइमआउट मिलीसेकंड में।
- `maxRequestRetry`: HTTP रिक्वेस्ट के लिए अधिकतम रीट्राई।
- `retryStrategy`: रीट्राई के लिए रणनीति, अनुकूलन योग्य।
- `retryDelay`: प्रत्येक रीट्राई पर टाइमआउट के लिए गुणक।
- `proxy`: HTTP कॉल्स के लिए प्रॉक्सी सेटिंग्स।
- `additionalHeaders`: हर रिक्वेस्ट पर लागू होने वाले हेडर।

#### LoggingConfiguration

बॉट एक्शन और HTTP रिक्वेस्ट के लिए लॉगिंग स्तरों का प्रबंधन करता है।

- `botLogLevel`: बॉट एक्शन के लिए लॉग्स का स्तर।
- `httpLogLevel`: HTTP रिक्वेस्ट के लिए लॉग्स का स्तर।

#### UpdatesListenerConfiguration

अपडेट्स खींचने से संबंधित पैरामीटर को कॉन्फ़िगर करता है।

- `dispatcher`: आने वाले अपडेट्स एकत्र करने के लिए डिस्पैचर।
- `processingDispatcher`: अपडेट्स को प्रोसेस करने के लिए डिस्पैचर।
- `pullingDelay`: प्रत्येक खींचने वाली रिक्वेस्ट के बाद देरी।
- `updatesPollingTimeout`: लॉन्ग-पोलिंग तंत्र के लिए टाइमआउट विकल्प।

#### CommandParsingConfiguration

कमांड पार्सिंग के लिए पैरामीटर निर्दिष्ट करता है।

- `commandDelimiter`: कमांड और पैरामीटर के बीच अलग करने वाला।
- `parametersDelimiter`: पैरामीटर के बीच अलग करने वाला।
- `parameterValueDelimiter`: पैरामीटर की कुंजी और मान के बीच अलग करने वाला।
- `restrictSpacesInCommands`: यह निर्धारित करने वाला फ्लैग कि क्या कमांड्स में स्पेस को कमांड का अंत माना जाना चाहिए।
- `useIdentifierInGroupCommands`: बॉट के पहचानकर्ता का उपयोग @ युक्त कमांड्स से मेल करने के लिए करता है।

### उदाहरण कॉन्फ़िगरेशन

यहाँ इन क्लासेस का उपयोग करके बॉट को कॉन्फ़िगर करने का एक उदाहरण है:

```kotlin
val bot = TelegramBot("TOKEN") {
    identifier = "MyBot",
    apiHost = "https://api.telegram.org",
    isTestEnv = true,
    inputListener = InputListenerMapImpl(),
    classManager = ClassManagerImpl(),

    httpClient {
        requestTimeoutMillis = 5000L
        connectTimeoutMillis = 3000L
        socketTimeoutMillis = 2000L
    }
    logging {
        botLogLevel = LogLvl.DEBUG
        httpLogLevel = HttpLogLevel.BODY
    }
    updatesListener {
        dispatcher = Dispatchers.IO
        processingDispatcher = Dispatchers.Unconfined
        pullingDelay = 1000L
    }
    commandParsing {
        commandDelimiter = '*'
        parametersDelimiter = '&'
        restrictSpacesInCommands = true
    }
}
```

यह कॉन्फ़िगरेशन विशिष्ट पहचानकर्ताओं के साथ एक बॉट सेट करता है, टेस्ट वातावरण मोड को सक्षम करता है, रेट लिमिटिंग को कॉन्फ़िगर करता है, HTTP क्लाइंट सेटिंग्स, लॉगिंग स्तर, अपडेट लिसनर पैरामीटर, और कमांड पार्सिंग नियम।

इन कॉन्फ़िगरेशन विकल्पों का लाभ उठाकर, डेवलपर्स अपने बॉट्स को विशिष्ट आवश्यकताओं को पूरा करने और विभिन्न संचालन परिदृश्यों में प्रदर्शन को अनुकूलित करने के लिए फ़ाइन-ट्यून कर सकते हैं।
---