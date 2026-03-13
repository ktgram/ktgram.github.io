---
---
title: एफएसएम और संवाद संभालना
---

लाइब्रेरी एफएसएम मैकेनिज्म को भी सपोर्ट करती है, जो उपयोगकर्ता इनपुट के प्रगतिशील प्रसंस्करण के लिए एक मैकेनिज्म है जिसमें गलत इनपुट संभालना शामिल है।

> [!NOTE]
> TL;DR: उदाहरण [वहाँ](https://github.com/vendelieu/telegram-bot_template/tree/conversation) देखें।

### सिद्धांत में

आइए कल्पना करें कि एक स्थिति जहाँ आपको उपयोगकर्ता सर्वेक्षण एकत्र करने की आवश्यकता है, आप एक ही चरण में किसी व्यक्ति के सभी डेटा के लिए पूछ सकते हैं, लेकिन पैरामीटर में से एक के गलत इनपुट के साथ, उपयोगकर्ता और हम दोनों के लिए यह कठिन होगा, और प्रत्येक चरण विशिष्ट इनपुट डेटा के आधार पर अलग हो सकता है।

अब डेटा के चरण-दर-चरण इनपुट की कल्पना करें, जहाँ बॉट उपयोगकर्ता के साथ संवाद मोड में प्रवेश करता है।

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/2e84fa00-e59c-4352-8665-83be3b971e7b" alt="संभालने की प्रक्रिया आरेख" />
</p>

हरे तीर त्रुटियों के बिना चरणों के माध्यम से संक्रमण की प्रक्रिया को इंगित करते हैं, नीले तीर वर्तमान स्थिति को सहेजना और पुन: इनपुट की प्रतीक्षा करना दर्शाते हैं (उदाहरण के लिए, यदि उपयोगकर्ता ने संकेत दिया कि वह -100 वर्ष का है, तो उसे आयु के लिए फिर से पूछना चाहिए), और लाल वाले पूरी प्रक्रिया से बाहर निकलना दिखाते हैं किसी भी कमांड या किसी अन्य अर्थपूर्ण रद्दीकरण के कारण।

### व्यवहार में

विज़ार्ड सिस्टम टेलीग्राम बॉट्स में बहु-चरणीय उपयोगकर्ता इंटरैक्शन को सक्षम बनाता है। यह उपयोगकर्ताओं को चरणों की एक श्रृंखला के माध्यम से मार्गदर्शन करता है, इनपुट को मान्य करता है, स्थिति को संग्रहीत करता है, और चरणों के बीच संक्रमण करता है।

**मुख्य लाभ:**
- **प्रकार-सुरक्षित**: स्थिति एक्सेस के लिए संकलन-समय प्रकार जाँच
- **घोषणात्मक**: नेस्टेड क्लास/ऑब्जेक्ट्स के रूप में चरणों को परिभाषित करें
- **लचीला**: शर्तीय संक्रमण, छलांग, और पुन: प्रयासों के लिए समर्थन
- **स्थितिजन्य**: प्लग करने योग्य स्टोरेज बैकएंड के साथ स्वचालित स्थिति स्थायित्व
- **एकीकृत**: मौजूदा एक्टिविटी सिस्टम के साथ काम करता है

### मुख्य अवधारणाएँ

#### विज़ार्डस्टेप

एक `विज़ार्डस्टेप` विज़ार्ड प्रवाह में एक एकल चरण का प्रतिनिधित्व करता है। प्रत्येक चरण को लागू करना चाहिए:

- **`onEntry(ctx: WizardContext)`**: जब उपयोगकर्ता इस चरण में प्रवेश करता है तो बुलाया जाता है। इसका उपयोग उपयोगकर्ता को प्रेरित करने के लिए करें।
- **`onRetry(ctx: WizardContext)`**: जब मान्यकरण विफल हो जाता है और चरण को पुन: प्रयास करना चाहिए तो बुलाया जाता है। इसका उपयोग त्रुटि संदेश दिखाने के लिए करें।
- **`validate(ctx: WizardContext): Transition`**: वर्तमान इनपुट को मान्य करता है और अगला क्या होता है यह दर्शाने वाला `Transition` लौटाता है।
- **`store(ctx: WizardContext): Any?`** (वैकल्पिक): इस चरण के लिए संग्रहीत करने के लिए मान लौटाता है। `null` लौटाएँ यदि चरण स्थिति संग्रहीत नहीं करता है।

```kotlin
object NameStep : WizardStep(isInitial = true) {
    override suspend fun onEntry(ctx: WizardContext) {
        message { "What is your name?" }.send(ctx.user, ctx.bot)
    }
    
    override suspend fun onRetry(ctx: WizardContext) {
        message { "Name cannot be empty. Please try again." }.send(ctx.user, ctx.bot)
    }
    
    override suspend fun validate(ctx: WizardContext): Transition {
        return if (ctx.update.text.isNullOrBlank()) {
            Transition.Retry
        } else {
            Transition.Next
        }
    }
    
    override suspend fun store(ctx: WizardContext): String {
        return ctx.update.text!!
    }
}
```

> [!NOTE]
> यदि कुछ चरण प्रारंभिक के रूप में चिह्नित नहीं है -> पहले घोषित चरण को माना जाता है।

#### संक्रमण

एक `Transition` मान्यकरण के बाद क्या होता है यह निर्धारित करता है:

- **`Transition.Next`**: अनुक्रम में अगले चरण पर जाएँ
- **`Transition.JumpTo(step: KClass<out WizardStep>)`**: किसी विशिष्ट चरण पर जाएँ
- **`Transition.Retry`**: वर्तमान चरण को पुन: प्रयास करें (मान्यकरण विफल रहा)
- **`Transition.Finish`**: विज़ार्ड समाप्त करें

```kotlin
// इनपुट के आधार पर शर्तीय छलांग
override suspend fun validate(ctx: WizardContext): Transition {
    val age = ctx.update.text?.toIntOrNull()
    return when {
        age == null -> Transition.Retry
        age < 18 -> Transition.JumpTo(UnderageStep::class)
        else -> Transition.Next
    }
}
```

#### विज़ार्डकंटेक्स्ट

`विज़ार्डकंटेक्स्ट` प्रदान करता है:
- **`user: User`**: वर्तमान उपयोगकर्ता
- **`update: ProcessedUpdate`**: वर्तमान अपडेट
- **`bot: TelegramBot`**: बॉट इंस्टेंस
- **`userReference: UserChatReference`**: स्थिति संग्रहण के लिए उपयोगकर्ता और चैट ID संदर्भ

साथ ही प्रकार-सुरक्षित स्थिति एक्सेस विधियाँ (KSP द्वारा उत्पन्न)।

---

### विज़ार्ड को परिभाषित करना

#### मूल संरचना

एक विज़ार्ड `@WizardHandler` एनोटेशन के साथ एक क्लास या ऑब्जेक्ट के रूप में परिभाषित किया गया है:

```kotlin
@WizardHandler(trigger = ["/survey"])
object SurveyWizard {
    object NameStep : WizardStep(isInitial = true) {
        // ... चरण कार्यान्वयन
    }
    
    object AgeStep : WizardStep {
        // ... चरण कार्यान्वयन
    }
    
    object FinishStep : WizardStep {
        // ... चरण कार्यान्वयन
    }
}
```

#### एनोटेशन पैरामीटर

**`@WizardHandler`** स्वीकार करता है:
- **`trigger: Array<String>`**: विज़ार्ड शुरू करने वाले कमांड (उदाहरण के लिए, `["/start", "/survey"]`)
- **`scope: Array<UpdateType>`**: सुनने के लिए अपडेट प्रकार (डिफ़ॉल्ट: `[UpdateType.MESSAGE]`)
- **`stateManagers: Array<KClass<out WizardStateManager<*>>>`**: चरण डेटा संग्रहीत करने के लिए स्टेट मैनेजर क्लास

---

### स्थिति प्रबंधन

#### विज़ार्डस्टेटमैनेजर

स्थिति `विज़ार्डस्टेटमैनेजर<T>` कार्यान्वयनों का उपयोग करके संग्रहीत की जाती है। प्रत्येक प्रबंधक किसी विशिष्ट प्रकार को संभालता है:

```kotlin
interface WizardStateManager<T : Any> {
    suspend fun get(key: KClass<out WizardStep>, reference: UserChatReference): T?
    suspend fun set(key: KClass<out WizardStep>, reference: UserChatReference, value: T)
    suspend fun del(key: KClass<out WizardStep>, reference: UserChatReference)
}
```

देखें भी: [MapStateManager<T>](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-state-manager/index.html), [MapStringStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-string-state-manager/index.html), [MapIntStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-int-state-manager/index.html), [MapLongStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-long-state-manager/index.html)।

#### स्वचालित मिलान

KSP `store()` रिटर्न प्रकार के आधार पर चरणों को स्टेट मैनेजर्स से मिलाता है:

```kotlin
@WizardHandler(
    trigger = ["/survey"],
    stateManagers = [StringStateManager::class, IntStateManager::class]
)
object SurveyWizard {
    object NameStep : WizardStep(isInitial = true) {
        override suspend fun store(ctx: WizardContext): String {
            return ctx.update.text!! // StringStateManager से मेल खाता है
        }
    }
    
    object AgeStep : WizardStep {
        override suspend fun store(ctx: WizardContext): Int {
            return ctx.update.text!!.toInt() // IntStateManager से मेल खाता है
        }
    }
}
```

#### प्रति-चरण ओवरराइड

किसी विशिष्ट चरण के लिए स्टेट मैनेजर को `@WizardHandler.StateManager` का उपयोग करके ओवरराइड करें:

```kotlin
@WizardHandler(
    trigger = ["/survey"],
    stateManagers = [DefaultStateManager::class]
)
object SurveyWizard {
    object NameStep : WizardStep(isInitial = true) {
        // DefaultStateManager का उपयोग करता है
    }
    
    @WizardHandler.StateManager(CustomStateManager::class)
    object AgeStep : WizardStep {
        // CustomStateManager के बजाय उपयोग करता है
    }
}
```

---

### प्रकार-सुरक्षित स्थिति एक्सेस

KSP प्रत्येक स्थिति संग्रहीत करने वाले चरण के लिए `विज़ार्डकंटेक्स्ट` पर प्रकार-सुरक्षित एक्सटेंशन फ़ंक्शन उत्पन्न करता है।

#### उत्पन्न फ़ंक्शन

किसी चरण के लिए जो एक `String` संग्रहीत करता है:

```kotlin
// KSP द्वारा स्वचालित रूप से उत्पन्न
suspend inline fun <reified S : WizardStep> WizardContext.getState(): String?
suspend inline fun <reified S : WizardStep> WizardContext.setState(value: String)
suspend inline fun <reified S : WizardStep> WizardContext.delState()
```

#### उपयोग

```kotlin
object FinishStep : WizardStep {
    override suspend fun onEntry(ctx: WizardContext) {
        // प्रकार-सुरक्षित एक्सेस - String? (nullable) लौटाता है
        val name: String? = ctx.getState<NameStep>()
        
        // प्रकार-सुरक्षित एक्सेस - Int? (nullable) लौटाता है
        val age: Int? = ctx.getState<AgeStep>()
        
        val summary = buildString {
            appendLine("Name: $name")
            appendLine("Age: $age")
        }
        
        message { summary }.send(ctx.user, ctx.bot)
    }
    
    override suspend fun onRetry(ctx: WizardContext) = Unit
    
    override suspend fun validate(ctx: WizardContext): Transition {
        return Transition.Finish
    }
}
```

#### फ़ॉलबैक विधियाँ

यदि प्रकार-सुरक्षित विधियाँ उपलब्ध नहीं हैं, तो फ़ॉलबैक विधियों का उपयोग करें:

```kotlin
// फ़ॉलबैक - Any? लौटाता है
val name = ctx.getState(NameStep::class)

// फ़ॉलबैक - Any? स्वीकार करता है
ctx.setState(NameStep::class, "John")
ctx.delState(NameStep::class)
```

---

### पूर्ण उदाहरण

#### उपयोगकर्ता पंजीकरण विज़ार्ड

```kotlin
@WizardHandler(
    trigger = ["/register"],
    stateManagers = [StringStateManager::class, IntStateManager::class]
)
object RegistrationWizard {
    object NameStep : WizardStep(isInitial = true) {
        override suspend fun onEntry(ctx: WizardContext) {
            message { "What is your name?" }.send(ctx.user, ctx.bot)
        }
        
        override suspend fun onRetry(ctx: WizardContext) {
            message { "Please enter a valid name." }.send(ctx.user, ctx.bot)
        }
        
        override suspend fun validate(ctx: WizardContext): Transition {
            val name = ctx.update.text?.trim()
            return if (name.isNullOrBlank() || name.length < 2) {
                Transition.Retry
            } else {
                Transition.Next
            }
        }
        
        override suspend fun store(ctx: WizardContext): String {
            return ctx.update.text!!.trim()
        }
    }
    
    object AgeStep : WizardStep {
        override suspend fun onEntry(ctx: WizardContext) {
            message { "How old are you?" }.send(ctx.user, ctx.bot)
        }
        
        override suspend fun onRetry(ctx: WizardContext) {
            message { "Please enter a valid age (must be a number)." }.send(ctx.user, ctx.bot)
        }
        
        override suspend fun validate(ctx: WizardContext): Transition {
            val age = ctx.update.text?.toIntOrNull()
            return when {
                age == null -> Transition.Retry
                age < 0 || age > 150 -> Transition.Retry
                age < 18 -> Transition.JumpTo(UnderageStep::class)
                else -> Transition.Next
            }
        }
        
        override suspend fun store(ctx: WizardContext): Int {
            return ctx.update.text!!.toInt()
        }
    }
    
    object UnderageStep : WizardStep {
        override suspend fun onEntry(ctx: WizardContext) {
            message { 
                "Sorry, you must be 18 or older to register." 
            }.send(ctx.user, ctx.bot)
        }
        
        override suspend fun onRetry(ctx: WizardContext) = Unit
        
        override suspend fun validate(ctx: WizardContext): Transition {
            return Transition.Finish
        }
    }
    
    object ConfirmationStep : WizardStep {
        override suspend fun onEntry(ctx: WizardContext) {
            // प्रकार-सुरक्षित स्थिति एक्सेस
            val name: String? = ctx.getState<NameStep>()
            val age: Int? = ctx.getState<AgeStep>()
            
            val confirmation = buildString {
                appendLine("Please confirm your information:")
                appendLine("Name: $name")
                appendLine("Age: $age")
                appendLine()
                appendLine("Reply 'yes' to confirm or 'no' to start over.")
            }
            
            message { confirmation }.send(ctx.user, ctx.bot)
        }
        
        override suspend fun onRetry(ctx: WizardContext) {
            message { "Please reply 'yes' or 'no'." }.send(ctx.user, ctx.bot)
        }
        
        override suspend fun validate(ctx: WizardContext): Transition {
            val response = ctx.update.text?.lowercase()?.trim()
            return when (response) {
                "yes" -> Transition.Finish
                "no" -> Transition.JumpTo(NameStep::class) // शुरू से शुरू करें
                else -> Transition.Retry
            }
        }
    }
    
    object FinishStep : WizardStep {
        override suspend fun onEntry(ctx: WizardContext) {
            val name: String? = ctx.getState<NameStep>()
            val age: Int? = ctx.getState<AgeStep>()
            
            // डेटाबेस में सहेजें, पुष्टि भेजें, आदि।
            message { 
                "Registration complete! Welcome, $name (age $age)." 
            }.send(ctx.user, ctx.bot)
        }
        
        override suspend fun onRetry(ctx: WizardContext) = Unit
        
        override suspend fun validate(ctx: WizardContext): Transition {
            return Transition.Finish
        }
    }
}
```

---

### उन्नत सुविधाएँ

#### शर्तीय संक्रमण

`Transition.JumpTo` का उपयोग शर्तीय प्रवाह के लिए करें:

```kotlin
override suspend fun validate(ctx: WizardContext): Transition {
    val choice = ctx.update.text?.lowercase()
    return when (choice) {
        "premium" -> Transition.JumpTo(PremiumStep::class)
        "basic" -> Transition.JumpTo(BasicStep::class)
        else -> Transition.Retry
    }
}
```

#### राज्यहीन चरण

चरणों को स्थिति संग्रहीत करने की आवश्यकता नहीं है। बस `store()` से `null` लौटाएँ (या जैसा है रखें):

```kotlin
object ConfirmationStep : WizardStep {
    override suspend fun store(ctx: WizardContext): Any? = null
    // ... बाकी कार्यान्वयन
}
```

#### कस्टम स्टेट मैनेजर

कस्टम स्टोरेज (डेटाबेस, Redis, आदि) के लिए `WizardStateManager<T>` कार्यान्वित करें:

```kotlin
class DatabaseStateManager : WizardStateManager<String> {
    override suspend fun get(
        key: KClass<out WizardStep>,
        reference: UserChatReference
    ): String? {
        // डेटाबेस से लोड करें
        return database.getWizardState(reference.userId, key.qualifiedName)
    }
    
    override suspend fun set(
        key: KClass<out WizardStep>,
        reference: UserChatReference,
        value: String
    ) {
        // डेटाबेस में सहेजें
        database.saveWizardState(reference.userId, key.qualifiedName, value)
    }
    
    override suspend fun del(
        key: KClass<out WizardStep>,
        reference: UserChatReference
    ) {
        // डेटाबेस से हटाएँ
        database.deleteWizardState(reference.userId, key.qualifiedName)
    }
}
```

---

### यह आंतरिक रूप से कैसे काम करता है

#### कोड उत्पादन

KSP उत्पन्न करता है:

1. **WizardActivity**: `WizardActivity` का विस्तार करने वाला एक ठोस कार्यान्वयन जिसमें हार्डकोडेड चरण होते हैं
2. **Start Activity**: कमांड ट्रिगर को संभालता है और विज़ार्ड शुरू करता है
3. **Input Activity**: विज़ार्ड प्रवाह के दौरान उपयोगकर्ता इनपुट को संभालता है
4. **State Accessors**: स्थिति एक्सेस के लिए प्रकार-सुरक्षित एक्सटेंशन फ़ंक्शन

#### प्रवाह

1. उपयोगकर्ता `/register` भेजता है → Start Activity बुलाया जाता है
2. Start Activity `WizardContext` बनाता है और `wizardActivity.start(ctx)` को कॉल करता है
3. `start()` प्रारंभिक चरण में प्रवेश करता है और वर्तमान चरण को ट्रैक करने के लिए `inputListener` सेट करता है
4. उपयोगकर्ता एक संदेश भेजता है → Input Activity बुलाया जाता है
5. Input Activity `wizardActivity.handleInput(ctx)` को कॉल करता है
6. `handleInput()` इनपुट को मान्य करता है, स्थिति को स्थायी बनाता है, और अगले चरण पर संक्रमण करता है
7. प्रक्रिया तब तक दोहराई जाती है जब तक `Transition.Finish` वापस नहीं आ जाता

#### स्थिति स्थायित्व

- मान्यकरण के बाद स्थिति को स्थायी बनाया जाता है (संक्रमण से पहले)
- प्रत्येक चरण का `store()` रिटर्न मान मिलान करने वाले `WizardStateManager` का उपयोग करके सहेजा जाता है
- स्थिति उपयोगकर्ता और चैट प्रति स्कोप होती है (`UserChatReference`)

---

### सर्वोत्तम अभ्यास

#### 1. हमेशा स्पष्ट संकेत दें

```kotlin
override suspend fun onEntry(ctx: WizardContext) {
    message { 
        "Please enter your email address:\n" +
        "(Format: user@example.com)" 
    }.send(ctx.user, ctx.bot)
}
```

#### 2. मान्यकरण त्रुटियों को सौम्यता से संभालें

```kotlin
override suspend fun onRetry(ctx: WizardContext) {
    message { 
        "Invalid email format. Please try again.\n" +
        "Example: user@example.com" 
    }.send(ctx.user, ctx.bot)
}
```

#### 3. प्रकार-सुरक्षित स्थिति एक्सेस का उपयोग करें

उत्पन्न प्रकार-सुरक्षित विधियों को प्राथमिकता दें:

```kotlin
// ✅ अच्छा - प्रकार-सुरक्षित
val name: String? = ctx.getState<NameStep>()

// ❌ टालें - प्रकार सुरक्षा खो देता है
val name = ctx.getState(NameStep::class) as? String
```

#### 4. चरणों को केंद्रित रखें

प्रत्येक चरण की एक एकल जिम्मेदारी होनी चाहिए:

```kotlin
// ✅ अच्छा - केंद्रित चरण
object EmailStep : WizardStep {
    // केवल ईमेल संग्रह को संभालता है
}

// ❌ टालें - बहुत अधिक तर्क
object PersonalInfoStep : WizardStep {
    // नाम, ईमेल, फोन, पता संभालता है...
}
```

#### 5. सार्थक चरण नामों का उपयोग करें

```kotlin
// ✅ अच्छा
object EmailVerificationStep : WizardStep

// ❌ टालें
object Step2 : WizardStep
```

#### 6. जब आवश्यक हो तो स्थिति साफ़ करें

यदि आपको मैन्युअल रूप से स्थिति साफ़ करने की आवश्यकता है:

```kotlin
object CancelStep : WizardStep {
    override suspend fun onEntry(ctx: WizardContext) {
        // सभी विज़ार्ड स्थिति साफ़ करें
        ctx.delState<NameStep>()
        ctx.delState<AgeStep>()
        
        message { "Registration cancelled." }.send(ctx.user, ctx.bot)
    }
}
```

---

### सारांश

विज़ार्ड सिस्टम प्रदान करता है:
- ✅ **प्रकार-सुरक्षित** संकलन-समय जाँच के साथ स्थिति प्रबंधन
- ✅ **घोषणात्मक** नेस्टेड क्लास के रूप में चरण परिभाषाएँ
- ✅ **लचीला** शर्तीय तर्क के साथ संक्रमण
- ✅ **स्वचालित** KSP द्वारा कोड उत्पादन
- ✅ **एकीकृत** मौजूदा एक्टिविटी सिस्टम के साथ
- ✅ **प्लग करने योग्य** स्टेट स्टोरेज बैकएंड

`@WizardHandler` के साथ एक क्लास को एनोटेट करके और अपने चरणों को नेस्टेड `WizardStep` ऑब्जेक्ट्स के रूप में परिभाषित करके विज़ार्ड बनाना शुरू करें!
यदि आपके कोई प्रश्न हैं तो हमसे चैट में संपर्क करें, हम मदद करने के लिए तैयार हैं :)
---