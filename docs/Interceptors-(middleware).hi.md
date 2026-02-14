---
---
title: इंटरसेप्टर (मिडलवेयर)
---

### इंटरसेप्टर: आपके बॉट के लिए क्रॉस-कटिंग लॉजिक

टेलीग्राम बॉट बनाते समय, आप अक्सर हैंडलर्स के बीच सेटअप, चेक या क्लीनअप को दोहराते हैं। इंटरसेप्टर आपको हैंडलर्स के आसपास साझा लॉजिक प्लग करने देते हैं, जिससे हैंडलर्स केंद्रित और बनाए रखने योग्य बने रहते हैं।

यहां *telegram-bot* में इंटरसेप्टर कैसे काम करते हैं और उनका उपयोग कैसे करें।

### इंटरसेप्टर क्या हैं? (सरल व्याख्या)

इंटरसेप्टर फ़ंक्शन हैं जो अपडेट प्रोसेसिंग पाइपलाइन में विशिष्ट बिंदुओं पर चलते हैं। वे आपको अनुमति देते हैं:
- प्रोसेसिंग संदर्भ का निरीक्षण और संशोधन
- क्रॉस-कटिंग लॉजिक जोड़ना (लॉगिंग, प्रमाणीकरण, मेट्रिक्स)
- यदि आवश्यक हो तो प्रोसेसिंग को जल्दी रोकना
- प्रोसेसिंग के बाद संसाधनों की सफाई करना

इंटरसेप्टर को चेकपॉइंट के रूप में सोचें जिससे हर अपडेट हैंडलर निष्पादन से पहले, दौरान और बाद में गुजरता है।


### प्रोसेसिंग पाइपलाइन

बॉट अपडेट को सात चरणों वाली पाइपलाइन के माध्यम से प्रोसेस करता है:

| चरण | कब चलता है | आप इसका उपयोग किस लिए कर सकते हैं |
|-------|--------------|-------------------------|
| **सेटअप** | जैसे ही अपडेट आता है, प्रोसेसिंग से पहले | ✔ वैश्विक दर सीमित करना<br>✔ स्पैम या दूषित अपडेट को फ़िल्टर करना<br>✔ प्रारंभिक लॉगिंग<br>✔ साझा संदर्भ सेटअप |
| **पार्सिंग** | सेटअप के बाद, कमांड और पैरामीटर निकालता है | ✔ कस्टम कमांड पार्सिंग<br>✔ पार्स किए गए डेटा के साथ संदर्भ को समृद्ध करना<br>✔ अपडेट संरचना को मान्य करना |
| **मैच** | उपयुक्त हैंडलर (कमांड/इनपुट/कॉमन) खोजता है | ✔ हैंडलर चयन को ओवरराइड करना<br>✔ कस्टम इनपुट हैंडलिंग लॉजिक<br>✔ मिलान किए गए हैंडलर्स को लॉग करना |
| **मान्यकरण** | हैंडलर मिलने के बाद, निष्पादन से पहले | ✔ हैंडलर-विशिष्ट अनुमतियाँ<br>✔ प्रति हैंडलर दर सीमित करना<br>✔ गार्ड चेक<br>✔ यदि शर्तें पूरी नहीं होती हैं तो प्रोसेसिंग रद्द करना |
| **प्रीइनवोक** | हैंडलर चलने से तुरंत पहले | ✔ अंतिम-मिनट चेक<br>✔ टाइमर/मेट्रिक्स शुरू करना<br>✔ हैंडलर के लिए संदर्भ को समृद्ध करना<br>✔ हैंडलर व्यवहार को संशोधित करना |
| **इनवोक** | हैंडलर यहाँ निष्पादित होता है | ✔ हैंडलर निष्पादन को लपेटना<br>✔ त्रुटि हैंडलिंग<br>✔ हैंडलर परिणामों को लॉग करना |
| **पोस्टइनवोक** | हैंडलर पूरा होने के बाद (सफलता या विफलता) | ✔ संसाधनों की सफाई<br>✔ परिणामों को लॉग करना<br>✔ त्रुटियों पर फ़ॉलबैक संदेश भेजना<br>✔ लौटने से पहले परिणामों को संशोधित करना |


### इंटरसेप्टर बनाना

एक इंटरसेप्टर एक साधारण फ़ंक्शन है जो `ProcessingContext` प्राप्त करता है:

```kotlin
import eu.vendeli.tgbot.core.PipelineInterceptor
import eu.vendeli.tgbot.types.component.ProcessingContext

val myInterceptor: PipelineInterceptor = { context ->
    // आपका लॉजिक यहाँ
    println("Processing update: ${context.update.updateId}")
}
```

या लैम्ब्डा का उपयोग करके:

```kotlin
val loggingInterceptor = PipelineInterceptor { context ->
    val logger = context.bot.config.loggerFactory.get("MyInterceptor")
    logger.info("Processing update #${context.update.updateId}")
}
```


### इंटरसेप्टर रजिस्टर करना

प्रोसेसिंग पाइपलाइन पर इंटरसेप्टर रजिस्टर करें:

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")
    
    // सेटअप चरण के लिए इंटरसेप्टर रजिस्टर करें
    bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
        // जांचें कि उपयोगकर्ता प्रतिबंधित है या नहीं
        val user = context.update.userOrNull
        if (user != null && isBanned(user.id)) {
            context.finish() // प्रोसेसिंग रोकें
            return@intercept
        }
    }
    
    // प्रीइनवोक चरण के लिए इंटरसेप्टर रजिस्टर करें
    bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
        val startTime = System.currentTimeMillis()
        // स्टार्ट समय स्टोर करें
    }
    
    // पोस्टइनवोक चरण के लिए इंटरसेप्टर रजिस्टर करें
    bot.update.pipeline.intercept(ProcessingPipePhase.PostInvoke) { context ->
        val startTime = // स्टार्ट समय प्राप्त करें
        if (startTime != null) {
            val duration = System.currentTimeMillis() - startTime
            println("Handler took ${duration}ms")
        }
    }
    
    bot.handleUpdates()
}
```

### वास्तविक उदाहरण: प्रमाणीकरण और मेट्रिक्स

उदाहरण: एक बॉट जिसमें कुछ कमांड के लिए प्रमाणीकरण की आवश्यकता होती है, हैंडलर निष्पादन समय मापता है, और सभी कमांड को लॉग करता है।

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")
    
    // सेटअप चरण: जांचें कि उपयोगकर्ता प्रमाणित है या नहीं
    bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
        val user = context.update.userOrNull ?: return@intercept
        
        if (!isAuthenticated(user.id)) {
            message { "Please authenticate first using /login" }
                .send(user, context.bot)
            context.finish()
        }
    }
    
    // प्रीइनवोक चरण: टाइमर शुरू करें और अनुमतियाँ जांचें
    bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
        val activity = context.activity ?: return@intercept
        val user = context.update.userOrNull ?: return@intercept
        
        // जांचें कि उपयोगकर्ता के पास यह विशिष्ट हैंडलर उपयोग करने की अनुमति है या नहीं
        if (!hasPermission(user.id, activity)) {
            message { "You don't have permission to use this command." }
                .send(user, context.bot)
            context.finish()
            return@intercept
        }
        
        // टाइमर शुरू करें
        // स्टार्ट समय स्टोर करें
    }
    
    // पोस्टइनवोक चरण: लॉग और सफाई
    bot.update.pipeline.intercept(ProcessingPipePhase.PostInvoke) { context ->
        val activity = context.activity ?: return@intercept
        val startTime = // स्टार्ट समय प्राप्त करें
        
        if (startTime != null) {
            val duration = System.currentTimeMillis() - startTime
            val logger = context.bot.config.loggerFactory.get("Metrics")
            logger.info(
                "Handler ${activity::class.simpleName} took ${duration}ms " +
                "for user ${context.update.userOrNull?.id}"
            )
        }
    }
    
    bot.handleUpdates()
}
```


### ProcessingContext

`ProcessingContext` निम्नलिखित तक पहुंच प्रदान करता है:

- **`update: ProcessedUpdate`** - प्रोसेस किया जा रहा वर्तमान अपडेट
- **`bot: TelegramBot`** - बॉट इंस्टेंस
- **`registry: ActivityRegistry`** - एक्टिविटी रजिस्ट्री
- **`parsedInput: String`** - पार्स किया गया कमांड/इनपुट टेक्स्ट
- **`parameters: Map<String, String>`** - पार्स किए गए कमांड पैरामीटर
- **`activity: Activity?`** - रिज़ॉल्व किया गया हैंडलर (मैच चरण तक null)
- **`shouldProceed: Boolean`** - क्या प्रोसेसिंग जारी रहनी चाहिए
- **`additionalContext: AdditionalContext`** - अतिरिक्त संदर्भ डेटा
- **`finish()`** - प्रोसेसिंग को जल्दी रोकें

#### प्रोसेसिंग को जल्दी रोकना

`context.finish()` कॉल करके प्रोसेसिंग रोकें:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.Validation) { context ->
    if (someCondition) {
        context.finish() // आगे के चरण नहीं चलेंगे
    }
}
```

#### कस्टम डेटा स्टोर करना

इंटरसेप्टर्स के बीच डेटा पास करने के लिए `additionalContext` का उपयोग करें:

```kotlin
// प्रीइनवोक में
context.additionalContext["userId"] = context.update.userOrNull?.id

// पोस्टइनवोक में
val userId = context.additionalContext["userId"] as? Long
```


### कई इंटरसेप्टर

आप एक ही चरण के लिए कई इंटरसेप्टर रजिस्टर कर सकते हैं। वे रजिस्ट्रेशन क्रम में निष्पादित होते हैं:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    println("First interceptor")
}

bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    println("Second interceptor")
}

// जब कोई अपडेट प्रोसेस होता है:
// Output: "First interceptor"
// Output: "Second interceptor"
```

यदि कोई इंटरसेप्टर `context.finish()` कॉल करता है, तो उस चरण के बाद के इंटरसेप्टर छोड़ दिए जाते हैं, और बाद के चरण नहीं चलेंगे।


### बेस्ट प्रैक्टिसेस

#### 1. सही चरण का उपयोग करें

- सेटअप: वैश्विक चेक, फ़िल्टरिंग, प्रारंभिक सेटअप
- पार्सिंग: कस्टम पार्सिंग लॉजिक
- मैच: हैंडलर चयन लॉजिक
- मान्यकरण: अनुमतियाँ, दर सीमाएँ, गार्ड
- प्रीइनवोक: हैंडलर-विशिष्ट तैयारी
- इनवोक: आमतौर पर डिफ़ॉल्ट इंटरसेप्टर द्वारा हैंडल किया जाता है
- पोस्टइनवोक: सफाई, लॉगिंग, त्रुटि हैंडलिंग

#### 2. इंटरसेप्टर्स को केंद्रित रखें

प्रत्येक इंटरसेप्टर को एक ही चीज़ करनी चाहिए:

```kotlin
// ✅ अच्छा - केंद्रित इंटरसेप्टर
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    if (isBanned(context.update.userOrNull?.id)) {
        context.finish()
    }
}

// ❌ टालें - बहुत कुछ कर रहा है
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    // प्रमाणीकरण
    // लॉगिंग
    // मेट्रिक्स
    // दर सीमित करना
    // ... बहुत कुछ!
}
```

#### 3. त्रुटियों को सौम्यता से हैंडल करें

इंटरसेप्टर्स को बॉट को क्रैश नहीं करना चाहिए:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
    try {
        // आपका लॉजिक
    } catch (e: Exception) {
        val logger = context.bot.config.loggerFactory.get("Interceptor")
        logger.error("Interceptor error", e)
        // जब तक आप प्रोसेसिंग रोकना नहीं चाहते तब तक context.finish() न कॉल करें
    }
}
```

#### 4. संसाधनों की सफाई करें

यदि आप `प्रीइनवोक` में संसाधन खोलते हैं, तो `पोस्टइनवोक` में उनकी सफाई करें:

```kotlin
var timer: Timer? = null

bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
    timer = Timer()
    context.additionalContext["timer"] = timer
}

bot.update.pipeline.intercept(ProcessingPipePhase.PostInvoke) { context ->
    val timer = context.additionalContext["timer"] as? Timer
    timer?.stop()
}
```

#### 5. क्रम मायने रखता है

जिस क्रम में आप चाहते हैं उस क्रम में इंटरसेप्टर रजिस्टर करें:

```kotlin
// पहले अधिक सामान्य चेक
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { 
    // वैश्विक प्रतिबंध चेक
}

// बाद में अधिक विशिष्ट चेक
bot.update.pipeline.intercept(ProcessingPipePhase.Validation) { 
    // हैंडलर-विशिष्ट अनुमति चेक
}
```

#### 6. इंटरसेप्टर्स का उपयोग क्रॉस-कटिंग कॉन्सर्न के लिए करें

इंटरसेप्टर्स आदर्श हैं:
- ✅ प्रमाणीकरण/अनुमति
- ✅ लॉगिंग
- ✅ मेट्रिक्स/प्रदर्शन मॉनिटरिंग
- ✅ दर सीमित करना
- ✅ त्रुटि हैंडलिंग
- ✅ रिक्वेस्ट/रिस्पॉन्स ट्रांसफॉर्मेशन

हैंडलर-विशिष्ट लॉजिक के लिए, उसे हैंडलर में ही रखें।


### डिफ़ॉल्ट इंटरसेप्टर

फ्रेमवर्क में कोर फ़ंक्शनैलिटी के लिए डिफ़ॉल्ट इंटरसेप्टर शामिल हैं:

- **DefaultSetupInterceptor**: वैश्विक दर सीमित करना
- **DefaultParsingInterceptor**: कमांड पार्सिंग
- **DefaultMatchInterceptor**: हैंडलर मैचिंग (कमांड, इनपुट, कॉमन मैचर)
- **DefaultValidationInterceptor**: गार्ड चेक और प्रति-हैंडलर दर सीमित करना
- **DefaultInvokeInterceptor**: हैंडलर निष्पादन और त्रुटि हैंडलिंग

आपके कस्टम इंटरसेप्टर इन डिफ़ॉल्ट के साथ-साथ चलते हैं। आप डिफ़ॉल्ट से पहले या बाद में लॉजिक जोड़ सकते हैं, लेकिन आप डिफ़ॉल्ट इंटरसेप्टर नहीं हटा सकते।

---

### उन्नत: शर्तीय इंटरसेप्टर

आप इंटरसेप्टर्स को शर्तीय बना सकते हैं:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
    val activity = context.activity ?: return@intercept
    
    // केवल विशिष्ट हैंडलर्स पर लागू करें
    if (activity::class.simpleName?.contains("Admin") == true) {
        // एडमिन-विशिष्ट लॉजिक
        checkAdminPermissions(context)
    }
}
```


### सारांश

इंटरसेप्टर आपके बॉट में क्रॉस-कटिंग लॉजिक जोड़ने का साफ़ तरीका प्रदान करते हैं:

- ✅ **सात चरण** प्रोसेसिंग के विभिन्न चरणों के लिए
- ✅ **सरल API**: बस `PipelineInterceptor` लागू करें
- ✅ **लचीला**: प्रति चरण कई इंटरसेप्टर रजिस्टर करें
- ✅ **शक्तिशाली**: पूर्ण प्रोसेसिंग संदर्भ तक पहुंच
- ✅ **सुरक्षित**: `context.finish()` के साथ प्रोसेसिंग को जल्दी रोक सकते हैं

इंटरसेप्टर्स का उपयोग अपने हैंडलर्स को व्यावसायिक लॉजिक पर केंद्रित रखने के लिए करें जबकि प्रमाणीकरण, लॉगिंग और मेट्रिक्स जैसे साझा कॉन्सर्न को केंद्रीकृत तरीके से हैंडल करें।

---

### इसे भी देखें

* [Functional handling DSL](Functional-handling-DSL.md) - फ़ंक्शनल अपडेट प्रोसेसिंग
* [Guards](Guards.md) - हैंडलर-स्तरीय अनुमति चेक
---