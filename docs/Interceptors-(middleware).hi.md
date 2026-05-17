---
---
title: Interceptors (Middleware)
---

### Interceptors: Cross-Cutting Logic for Your Bot

जब आप एक Telegram बॉट बनाते हैं, तो अक्सर हैंडलर्स के बीच सेटअप, चेक्स या क्लीनअप दोहराते हैं। Interceptors आपको हैंडलर्स के आसपास साझा लॉजिक प्लग इन करने देते हैं, जिससे हैंडलर्स केंद्रित और मेंटेनेबल रहते हैं।

यहाँ *telegram-bot* में interceptors कैसे काम करते हैं और उन्हें कैसे उपयोग किया जाता है।

### What Are Interceptors? (Simple Explanation)

Interceptors फ़ंक्शन होते हैं जो अपडेट प्रोसेसिंग पाइपलाइन के विशिष्ट बिंदुओं पर चलते हैं। वे आपको:
- प्रोसेसिंग कॉन्टेक्स्ट की जाँच और संशोधन करने देते हैं
- क्रॉस-कटिंग लॉजिक (लॉगिंग, ऑथ, मेट्रिक्स) जोड़ते हैं
- आवश्यक होने पर प्रोसेसिंग को जल्दी रोक सकते हैं
- प्रोसेसिंग के बाद संसाधनों की सफ़ाई करते हैं

इन्हें ऐसे चेकपॉइंट समझें जिनसे हर अपडेट हैंडलर निष्पादन से पहले, दौरान और बाद पास करता है।

### The Processing Pipeline

बॉट अपडेट्स को सात चरणों वाली पाइपलाइन के माध्यम से प्रोसेस करता है:

| Phase | When It Runs | What You Can Use It For |
|-------|--------------|-------------------------|
| **Setup** | अपडेट के आने पर, किसी भी प्रोसेसिंग से पहले | ✔ ग्लोबल रेट लिमिटिंग<br>✔ स्पैम या मालफ़ॉर्म्ड अपडेट को फ़िल्टर करें<br>✔ शुरुआती लॉगिंग<br>✔ साझा कॉन्टेक्स्ट सेटअप |
| **Parsing** | सेटअप के बाद, कमांड और पैरामीटर निकालता है | ✔ कस्टम कमांड पार्सिंग<br>✔ पार्स्ड डेटा के साथ कॉन्टेक्स्ट को समृद्ध करें<br>✔ अपडेट संरचना को वैलिडेट करें |
| **Match** | उपयुक्त हैंडलर (Command/Input/Common) ढूँढता है | ✔ हैंडलर चयन को ओवरराइड करें<br>✔ कस्टम इनपुट हैंडलिंग लॉजिक<br>✔ मैच्ड हैंडलर्स को लॉग करें |
| **Validation** | हैंडलर मिलने के बाद, इन्कोरेशन से पहले | ✔ हैंडलर-विशिष्ट परमिशन्स<br>✔ प्रति हैंडलर रेट लिमिटिंग<br>✔ गार्ड चेक्स<br>✔ यदि शर्तें पूरी नहीं हों तो प्रोसेसिंग कैंसल करें |
| **PreInvoke** | हैंडलर चलने से ठीक पहले | ✔ अंतिम मिनट की चेक्स<br>✔ टाइमर/मेट्रिक्स शुरू करें<br>✔ हैंडलर के लिए कॉन्टेक्स्ट समृद्ध करें<br>✔ हैंडलर व्यवहार को बदलें |
| **Invoke** | यहाँ हैंडलर चलाया जाता है | ✔ हैंडलर निष्पादन को रैप करें<br>✔ एरर हैंडलिंग<br>✔ हैंडलर परिणामों को लॉग करें |
| **PostInvoke** | हैंडलर समाप्त होने के बाद (सफल या विफल) | ✔ रिसोर्सेज़ क्लीनअप<br>✔ परिणाम लॉग करें<br>✔ एरर पर फ़ॉलबैक संदेश भेजें<br>✔ रिटर्न से पहले परिणाम बदलें |

### Creating an Interceptor

एक interceptor एक साधारण फ़ंक्शन है जो `ProcessingContext` प्राप्त करता है:

```kotlin
import eu.vendeli.tgbot.core.PipelineInterceptor
import eu.vendeli.tgbot.types.component.ProcessingContext

val myInterceptor: PipelineInterceptor = { context ->
    // Your logic here
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

### Registering Interceptors

इंटरसेप्टर्स को प्रोसेसिंग पाइपलाइन पर रजिस्टर करें:

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")
    
    // Register an interceptor for the Setup phase
    bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
        // Check if user is banned
        val user = context.update.userOrNull
        if (user != null && isBanned(user.id)) {
            context.finish() // Stop processing
            return@intercept
        }
    }
    
    // Register an interceptor for the PreInvoke phase
    bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
        val startTime = System.currentTimeMillis()
        // store start time
    }
    
    // Register an interceptor for the PostInvoke phase
    bot.update.pipeline.intercept(ProcessingPipePhase.PostInvoke) { context ->
        val startTime = // get start time
        if (startTime != null) {
            val duration = System.currentTimeMillis() - startTime
            println("Handler took ${duration}ms")
        }
    }
    
    bot.handleUpdates()
}
```

### Real-World Example: Authentication & Metrics

उदाहरण: एक बॉट जो कुछ कमांड्स के लिए ऑथेंटिकेशन की आवश्यकता रखता है, हैंडलर एक्ज़ीक्यूशन टाइम मापता है, और सभी कमांड्स को लॉग करता है।

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")
    
    // Setup phase: Check if user is authenticated
    bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
        val user = context.update.userOrNull ?: return@intercept
        
        if (!isAuthenticated(user.id)) {
            message { "Please authenticate first using /login" }
                .send(user, context.bot)
            context.finish()
        }
    }
    
    // PreInvoke phase: Start timer and check permissions
    bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
        val activity = context.activity ?: return@intercept
        val user = context.update.userOrNull ?: return@intercept
        
        // Check if user has permission for this specific handler
        if (!hasPermission(user.id, activity)) {
            message { "You don't have permission to use this command." }
                .send(user, context.bot)
            context.finish()
            return@intercept
        }
        
        // Start timer
        // store start time
    }
    
    // PostInvoke phase: Log and cleanup
    bot.update.pipeline.intercept(ProcessingPipePhase.PostInvoke) { context ->
        val activity = context.activity ?: return@intercept
        val startTime = // get start time
        
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

`ProcessingContext` निम्नलिखित प्रदान करता है:

- **`update: ProcessedUpdate`** - वर्तमान अपडेट जो प्रोसेस हो रहा है
- **`bot: TelegramBot`** - बॉट इंस्टेंस
- **`registry: ActivityRegistry`** - एक्टिविटी रेगिस्ट्री
- **`parsedInput: String`** - पार्स किया गया कमांड/इनपुट टेक्स्ट
- **`parameters: Map<String, String>`** - पार्स्ड कमांड पैरामीटर्स
- **`activity: Activity?`** - रिज़ॉल्व्ड हैंडलर (Match फेज़ तक null)
- **`shouldProceed: Boolean`** - क्या प्रोसेसिंग जारी रहनी चाहिए
- **`additionalContext: AdditionalContext`** - अतिरिक्त कॉन्टेक्स्ट डेटा
- **`finish()`** - जल्दी प्रोसेसिंग रोकें

#### Stopping Processing Early

`context.finish()` को कॉल करें ताकि प्रोसेसिंग रुक जाए:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.Validation) { context ->
    if (someCondition) {
        context.finish() // No further phases will execute
    }
}
```

#### Storing Custom Data

इंटरसेप्टर्स के बीच डेटा पास करने के लिए `additionalContext` का उपयोग करें:

```kotlin
// In PreInvoke
context.additionalContext["userId"] = context.update.userOrNull?.id

// In PostInvoke
val userId = context.additionalContext["userId"] as? Long
```


### Multiple Interceptors

आप एक ही चरण के लिए कई इंटरसेप्टर्स रजिस्टर कर सकते हैं। वे रजिस्ट्रेशन क्रम में चलेंगे:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    println("First interceptor")
}

bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    println("Second interceptor")
}

// When an update is processed:
// Output: "First interceptor"
// Output: "Second interceptor"
```

यदि कोई इंटरसेप्टर `context.finish()` कॉल करता है, तो उसी चरण के बाद के इंटरसेप्टर्स स्किप हो जाएंगे, और बाद के चरण नहीं चलेंगे।

### Best Practices

#### 1. Use the Right Phase

- Setup: ग्लोबल चेक्स, फ़िल्टरिंग, शुरुआती सेटअप
- Parsing: कस्टम पार्सिंग लॉजिक
- Match: हैंडलर चयन लॉजिक
- Validation: परमिशन्स, रेट लिमिट्स, गार्ड्स
- PreInvoke: हैंडलर-विशिष्ट तैयारी
- Invoke: आमतौर पर डिफ़ॉल्ट इंटरसेप्टर द्वारा हैंडल किया जाता है
- PostInvoke: क्लीनअप, लॉगिंग, एरर हैंडलिंग

#### 2. Keep Interceptors Focused

हर इंटरसेप्टर को एक काम करना चाहिए:

```kotlin
// ✅ Good - focused interceptor
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    if (isBanned(context.update.userOrNull?.id)) {
        context.finish()
    }
}

// ❌ Avoid - doing too much
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    // Authentication
    // Logging
    // Metrics
    // Rate limiting
    // ... too much!
}
```

#### 3. Handle Errors Gracefully

इंटरसेप्टर बॉट को क्रैश नहीं करना चाहिए:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
    try {
        // Your logic
    } catch (e: Exception) {
        val logger = context.bot.config.loggerFactory.get("Interceptor")
        logger.error("Interceptor error", e)
        // Don't call context.finish() unless you want to stop processing
    }
}
```

#### 4. Clean Up Resources

यदि आप `PreInvoke` में संसाधन खोलते हैं, तो उन्हें `PostInvoke` में साफ़ करें:

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

#### 5. Order Matters

इंटरसेप्टर्स को उस क्रम में रजिस्टर करें जिसमें आप चाहते हैं कि वे चलें:

```kotlin
// More general checks first
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { 
    // Global ban check
}

// More specific checks later
bot.update.pipeline.intercept(ProcessingPipePhase.Validation) { 
    // Handler-specific permission check
}
```

#### 6. Use Interceptors for Cross-Cutting Concerns

इंटरसेप्टर्स आदर्श हैं:
- ✅ ऑथेंटिकेशन/ऑथराइजेशन
- ✅ लॉगिंग
- ✅ मेट्रिक्स/परफ़ॉर्मेंस मॉनिटरिंग
- ✅ रेट लिमिटिंग
- ✅ एरर हैंडलिंग
- ✅ रिक्वेस्ट/रेस्पॉन्स ट्रांसफ़ॉर्मेशन

हैंडलर-विशिष्ट लॉजिक को हैंडलर में रखें।

### Default Interceptors

फ़्रेमवर्क में कोर फ़ंक्शनैलिटी के लिए डिफ़ॉल्ट इंटरसेप्टर्स शामिल हैं:

- **DefaultSetupInterceptor**: ग्लोबल रेट लिमिटिंग
- **DefaultParsingInterceptor**: कमांड पार्सिंग
- **DefaultMatchInterceptor**: हैंडलर मैचिंग (कमांड्स, इनपुट्स, कॉमन मैचर्स)
- **DefaultValidationInterceptor**: गार्ड चेक्स और प्रति-हैंडलर रेट लिमिटिंग
- **DefaultInvokeInterceptor**: हैंडलर निष्पादन और एरर हैंडलिंग

आपके कस्टम इंटरसेप्टर्स इन डिफ़ॉल्ट्स के साथ चलेंगे। आप डिफ़ॉल्ट इंटरसेप्टर्स से पहले या बाद में लॉजिक जोड़ सकते हैं, लेकिन उन्हें हटाया नहीं जा सकता।

---

### Advanced: Conditional Interceptors

आप इंटरसेप्टर को शर्तीय बना सकते हैं:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
    val activity = context.activity ?: return@intercept
    
    // Only apply to specific handlers
    if (activity::class.simpleName?.contains("Admin") == true) {
        // Admin-specific logic
        checkAdminPermissions(context)
    }
}
```


### Summary

इंटरसेप्टर्स आपके बॉट में क्रॉस-कटिंग लॉजिक जोड़ने का एक साफ़ तरीका प्रदान करते हैं:

- ✅ **सेवन चरण** विभिन्न प्रोसेसिंग स्टेज़ के लिए
- ✅ **सरल API**: सिर्फ `PipelineInterceptor` इम्प्लीमेंट करें
- ✅ **लचीला**: प्रति चरण कई इंटरसेप्टर रजिस्टर कर सकते हैं
- ✅ **शक्तिशाली**: पूरा प्रोसेसिंग कॉन्टेक्स्ट एक्सेस करा
- ✅ **सेफ़**: `context.finish()` से जल्दी प्रोसेसिंग रोक सकते हैं

इंटरसेप्टर्स का उपयोग करके अपने हैंडलर्स को बिज़नेस लॉजिक पर केंद्रित रखें, जबकि ऑथेंटिकेशन, लॉगिंग और मेट्रिक्स जैसी साझा चिंताओं को केंद्रित तरीके से संभालें।

---

### See also

* [Handlers (incl. Functional DSL)](Handlers.md) - Annotation- और DSL-आधारित हैंडलर परिभाषा
* [Sessions](Sessions.md) - प्रति-चैट / प्रति-यूज़र स्थिति और मेसेज ट्रैकिंग
* [Guards](Guards.md) - हैंडलर-लेवल परमिशन चेक्स
---