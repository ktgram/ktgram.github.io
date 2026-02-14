---
---
title: बॉट कॉन्फ़िगरेशन
---

लाइब्रेरी कई कॉन्फ़िगरेशन विकल्प प्रदान करती है, आप [`BotConfiguration`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.configuration/-bot-configuration/index.html) क्लास विवरण में API संदर्भ देख सकते हैं।

बॉट को कॉन्फ़िगर करने के दो तरीके भी हैं:

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

इस इंटरफ़ेस के कार्यान्वयन को सेकेंडरी कंस्ट्रक्टर के माध्यम से पास किया जा सकता है और उदाहरण इसके अनुसार कॉन्फ़िगर किया जाएगा।

```kotlin
val bot = TelegramBot(ConfigLoaderImpl)
```

वर्तमान में कई मॉड्यूल प्रदान किए गए हैं जो इस इंटरफ़ेस को लागू करते हैं जैसे `ktgram-config-env`, `ktgram-config-toml`।

### BotConfiguration अवलोकन

#### BotConfiguration

`BotConfiguration` क्लास बॉट को कॉन्फ़िगर करने के लिए केंद्रीय हब है। इसमें बॉट की पहचान करने, API होस्ट सेट करने, यह निर्धारित करने के लिए गुण हैं कि क्या बॉट परीक्षण वातावरण में काम करता है, इनपुट को संभालना, क्लासों का प्रबंधन करना, और इनपुट ऑटो-हटाने को नियंत्रित करना। इसके अलावा, यह दर सीमित करने, HTTP क्लाइंट कॉन्फ़िगरेशन, लॉगिंग, अपडेट सुनने और कमांड पार्सिंग के लिए आंतरिक गुण प्रदान करता है।

##### गुण

- `identifier`: मल्टी-बॉट प्रोसेसिंग के दौरान विभिन्न बॉट उदाहरणों की पहचान करता है।
- `apiHost`: Telegram API का होस्ट।
- `isTestEnv`: यह दर्शाता है कि क्या बॉट परीक्षण वातावरण में काम करता है।
- `inputListener`: इनपुट हैंडलिंग क्लास का उदाहरण।
- `classManager`: क्लास प्राप्त करने के लिए उपयोग किया जाने वाला प्रबंधक।
- `inputAutoRemoval`: प्रोसेसिंग के दौरान इनपुट पॉइंट के ऑटो-हटाने को नियंत्रित करने वाला फ़्लैग।
- `exceptionHandlingStrategy`: अपवादों को संभालने के लिए रणनीति को परिभाषित करता है।
    * `CollectToChannel` - `TgUpdateHandler.caughtExceptions` में एकत्र करें।
    * `Throw` - `TgException` के साथ फिर से फेंकें।
    * `DoNothing` - कुछ न करें :)
    * `Handle` - कस्टम हैंडलर सेट करें।
- `throwExOnActionsFailure`: किसी भी बॉट अनुरोध के विफल होने पर अपवाद फेंकता है।

##### कॉन्फ़िगरेशन ब्लॉक

`BotConfiguration` अपने आंतरिक घटकों को कॉन्फ़िगर करने के लिए फ़ंक्शन भी प्रदान करता है:

- `httpClient(block: HttpConfiguration.() -> Unit)`: HTTP क्लाइंट को कॉन्फ़िगर करता है।
- `logging(block: LoggingConfiguration.() -> Unit)`: लॉगिंग को कॉन्फ़िगर करता है।
- `rateLimiter(block: RateLimiterConfiguration.() -> Unit)`: अनुरोध सीमित करने को कॉन्फ़िगर करता है।
- `updatesListener(block: UpdatesListenerConfiguration.() -> Unit)`: अपडेट सुनने वाले को कॉन्फ़िगर करता है।
- `commandParsing(block: CommandParsingConfiguration.() -> Unit)`: कमांड पार्सिंग पैटर्न को निर्दिष्ट करता है।

### संबद्ध कॉन्फ़िगरेशन क्लासेस

#### RateLimiterConfiguration

वैश्विक दर सीमित करने को कॉन्फ़िगर करता है।

- `limits`: वैश्विक दर सीमाएँ।
- `mechanism`: दर सीमित करने के लिए उपयोग किया जाने वाला तंत्र, डिफ़ॉल्ट TokenBucket एल्गोरिदम है।
- `exceededAction`: सीमा पार होने पर लागू की जाने वाली क्रिया।

#### HttpConfiguration

बॉट के HTTP क्लाइंट के लिए कॉन्फ़िगरेशन सम्मिलित करता है।

- `requestTimeoutMillis`: अनुरोध टाइमआउट मिलीसेकंड में।
- `connectTimeoutMillis`: कनेक्शन टाइमआउट मिलीसेकंड में।
- `socketTimeoutMillis`: सॉकेट टाइमआउट मिलीसेकंड में।
- `maxRequestRetry`: HTTP अनुरोधों के लिए अधिकतम रीट्राई।
- `retryStrategy`: रीट्राई के लिए रणनीति, अनुकूलन योग्य।
- `retryDelay`: प्रत्येक रीट्राई पर टाइमआउट के लिए गुणक।
- `proxy`: HTTP कॉल के लिए प्रॉक्सी सेटिंग्स।
- `additionalHeaders`: हर अनुरोध पर लागू होने वाले हेडर।

#### LoggingConfiguration

बॉट क्रियाओं और HTTP अनुरोधों के लिए लॉगिंग स्तरों का प्रबंधन करता है।

- `botLogLevel`: बॉट क्रियाओं के लिए लॉग का स्तर।
- `httpLogLevel`: HTTP अनुरोधों के लिए लॉग का स्तर।

#### UpdatesListenerConfiguration

अपडेट खींचने से संबंधित पैरामीटर को कॉन्फ़िगर करता है।

- `dispatcher`: आने वाले अपडेट एकत्र करने के लिए डिस्पैचर।
- `processingDispatcher`: अपडेट को प्रोसेस करने के लिए डिस्पैचर।
- `pullingDelay`: प्रत्येक खींचने के अनुरोध के बाद देरी।
- `updatesPollingTimeout`: लंबे-पोलिंग तंत्र के लिए टाइमआउट विकल्प।

#### CommandParsingConfiguration

कमांड पार्सिंग के लिए पैरामीटर को निर्दिष्ट करता है।

- `commandDelimiter`: कमांड और पैरामीटर के बीच अलग करने वाला।
- `parametersDelimiter`: पैरामीटर के बीच अलग करने वाला।
- `parameterValueDelimiter`: पैरामीटर के की और मान के बीच अलग करने वाला।
- `restrictSpacesInCommands`: यह दर्शाता है कि क्या कमांड में स्थानों को कमांड के अंत के रूप में माना जाना चाहिए।
- `useIdentifierInGroupCommands`: समूह कमांड में @ सम्मिलित करने वाले कमांड से मेल खाने के लिए बॉट के पहचानकर्ता का उपयोग करता है।

### उदाहरण कॉन्फ़िगरेशन

यहाँ इन क्लासों का उपयोग करके बॉट को कॉन्फ़िगर करने का एक उदाहरण है:

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

यह कॉन्फ़िगरेशन विशिष्ट पहचानकर्ताओं के साथ एक बॉट सेट करता है, परीक्षण वातावरण मोड को सक्षम करता है, दर सीमित करने, HTTP क्लाइंट सेटिंग्स, लॉगिंग स्तरों, अपडेट सुनने वाले पैरामीटर और कमांड पार्सिंग नियमों को कॉन्फ़िगर करता है।

इन कॉन्फ़िगरेशन विकल्पों का लाभ उठाकर, डेवलपर्स अपने बॉट को विशिष्ट आवश्यकताओं को पूरा करने और विभिन्न परिचालन परिदृश्यों में प्रदर्शन को अनुकूलित करने के लिए बारीकी से समायोजित कर सकते हैं।
---