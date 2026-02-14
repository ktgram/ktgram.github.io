---
---
title: एफएसएम और संवाद हैंडलिंग
---

लाइब्रेरी एफएसएम मैकेनिज्म का भी समर्थन करती है, जो उपयोगकर्ता इनपुट के प्रगतिशील प्रसंस्करण के लिए एक तंत्र है जिसमें गलत इनपुट हैंडलिंग शामिल है।

> [!NOTE]
> TL;DR: उदाहरण [वहां](https://github.com/vendelieu/telegram-bot_template/tree/conversation) देखें।

### सिद्धांत में

आइए कल्पना करें कि आपको उपयोगकर्ता सर्वेक्षण एकत्र करने की आवश्यकता है, आप एक चरण में व्यक्ति के सभी डेटा के लिए पूछ सकते हैं, लेकिन पैरामीटर में से एक के गलत इनपुट के साथ, उपयोगकर्ता और हम दोनों के लिए इसे मुश्किल होगा, और प्रत्येक चरण कुछ इनपुट डेटा के आधार पर अलग हो सकता है।

अब चरण-दर-चरण डेटा इनपुट की कल्पना करें, जहां बॉट उपयोगकर्ता के साथ संवाद मोड में प्रवेश करता है।

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/2e84fa00-e59c-4352-8665-83be3b971e7b" alt="प्रक्रिया आरेख को संभालना" />
</p>

हरे तीर बिना किसी त्रुटि के चरणों के माध्यम से संक्रमण की प्रक्रिया को इंगित करते हैं, नीले तीर वर्तमान स्थिति को बचाने और पुन: इनपुट की प्रतीक्षा करने का मतलब है (उदाहरण के लिए, यदि उपयोगकर्ता ने इंगित किया कि वह -100 वर्ष का है, तो इसे आयु के लिए फिर से पूछना चाहिए), और लाल रंग पूरी प्रक्रिया से बाहर निकलना दिखाते हैं किसी भी कमांड या किसी अन्य अर्थ रद्दीकरण के कारण।

### व्यवहार में

विज़ार्ड सिस्टम टेलीग्राम बॉट्स में मल्टी-स्टेप उपयोगकर्ता इंटरैक्शन को सक्षम बनाता है। यह उपयोगकर्ताओं को चरणों की एक श्रृंखला के माध्यम से मार्गदर्शन करता है, इनपुट को मान्य करता है, स्थिति को संग्रहीत करता है, और चरणों के बीच संक्रमण करता है।

**मुख्य लाभ:**
- **टाइप-सुरक्षित**: स्थिति पहुंच के लिए संकलन-समय प्रकार जांच
- **घोषणात्मक**: नेस्टेड क्लास/ऑब्जेक्ट के रूप में चरणों को परिभाषित करें
- **लचीला**: शर्तीय संक्रमण, कूद और पुन: प्रयासों के लिए समर्थन
- **स्टेटफुल**: प्लग करने योग्य भंडारण बैकएंड के साथ स्वचालित स्थिति स्थायित्व
- **एकीकृत**: मौजूदा एक्टिविटी सिस्टम के साथ काम करता है

### मूल अवधारणाएँ

#### विज़ार्डस्टेप

एक `विज़ार्डस्टेप` विज़ार्ड प्रवाह में एक एकल चरण का प्रतिनिधित्व करता है। प्रत्येक चरण को लागू करना चाहिए:

- **`onEntry(ctx: WizardContext)`**: जब उपयोगकर्ता इस चरण में प्रवेश करता है तो कहा जाता है। इसका उपयोग उपयोगकर्ता से पूछने के लिए करें।
- **`onRetry(ctx: WizardContext)`**: जब सत्यापन विफल हो जाता है और चरण को पुन: प्रयास करना चाहिए तो कहा जाता है। त्रुटि संदेश दिखाने के लिए इसका उपयोग करें।
- **`validate(ctx: WizardContext): Transition`**: वर्तमान इनपुट को मान्य करता है और अगला क्या होता है यह इंगित करते हुए एक `Transition` लौटाता है।
- **`store(ctx: WizardContext): Any?`** (वैकल्पिक): इस चरण के लिए बनाए रखने के लिए मान लौटाता है। `null` लौटाएं यदि चरण स्थिति को संग्रहीत नहीं करता है।

```kotlin
object NameStep : WizardStep(isInitial = true) {
    override suspend fun onEntry(ctx: WizardContext) {
        message { "आपका नाम क्या है?" }.send(ctx.user, ctx.bot)
    }
    
    override suspend fun onRetry(ctx: WizardContext) {
        message { "नाम खाली नहीं हो सकता। कृपया पुन: प्रयास करें।" }.send(ctx.user, ctx.bot)
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

एक `संक्रमण` सत्यापन के बाद क्या होता है यह निर्धारित करता है:

- **`Transition.Next`**: अनुक्रम में अगले चरण पर जाएं
- **`Transition.JumpTo(step: KClass<out WizardStep>)`**: किसी विशिष्ट चरण पर कूदें
- **`Transition.Retry`**: वर्तमान चरण को पुन: प्रयास करें (सत्यापन विफल)
- **`Transition.Finish`**: विज़ार्ड समाप्त करें

```kotlin
// इनपुट के आधार पर शर्तीय कूद
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
- **`bot: TelegramBot`**: बॉट उदाहरण
- **`userReference: UserChatReference`**: स्थिति भंडारण के लिए उपयोगकर्ता और चैट आईडी संदर्भ

प्लस टाइप-सुरक्षित स्थिति पहुंच विधियाँ (KSP द्वारा उत्पन्न)।

---

### विज़ार्ड को परिभाषित करना

#### बुनियादी संरचना

एक विज़ार्ड को `@WizardHandler` एनोटेशन के साथ एक क्लास या ऑब्जेक्ट के रूप में परिभाषित किया गया है:

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
- **`trigger: Array<String>`**: विज़ार्ड शुरू करने वाले कमांड (जैसे, `["/start", "/survey"]`)
- **`scope: Array<UpdateType>`**: सुनने के लिए अपडेट प्रकार (डिफ़ॉल्ट: `[UpdateType.MESSAGE]`)
- **`stateManagers: Array<KClass<out WizardStateManager<*>>>`**: चरण डेटा संग्रहीत करने के लिए राज्य प्रबंधक कक्षाएं

---

### स्थिति प्रबंधन

#### विज़ार्डस्टेटमैनेजर

स्थिति `विज़ार्डस्टेटमैनेजर<T>` कार्यान्वयन का उपयोग करके संग्रहीत की जाती है। प्रत्येक प्रबंधक एक विशिष्ट प्रकार को संभालता है:

```kotlin
interface WizardStateManager<T : Any> {
    suspend fun get(key: KClass<out WizardStep>, reference: UserChatReference): T?
    suspend fun set(key: KClass<out WizardStep>, reference: UserChatReference, value: T)
    suspend fun del(key: KClass<out WizardStep>, reference: UserChatReference)
}
```

यह भी देखें: [MapStateManager<T>](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-state-manager/index.html), [MapStringStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-string-state-manager/index.html), [MapIntStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-int-state-manager/index.html), [MapLongStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-long-state-manager/index.html)।

#### स्वचालित मिलान

KSP `store()` रिटर्न प्रकार के आधार पर चरणों को राज्य प्रबंधकों से मिलाता है:

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

`@WizardHandler.StateManager` का उपयोग करके किसी विशिष्ट चरण के लिए राज्य प्रबंधक को ओवरराइड करें:

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
        // इसके बजाय CustomStateManager का उपयोग करता है
    }
}
```

---

### टाइप-सुरक्षित स्थिति पहुंच

KSP प्रत्येक चरण के लिए टाइप-सुरक्षित एक्सटेंशन फ़ंक्शंस उत्पन्न करता है जो स्थिति को संग्रहीत करता है।

#### उत्पन्न फ़ंक्शंस

एक चरण के लिए जो एक `String` संग्रहीत करता है:

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
        // टाइप-सुरक्षित पहुंच - String? (नल योग्य) लौटाता है
        val name: String? = ctx.getState<NameStep>()
        
        // टाइप-सुरक्षित पहुंच - Int? (नल योग्य) लौटाता है
        val age: Int? = ctx.getState<AgeStep>()
        
        val summary = buildString {
            appendLine("नाम: $name")
            appendLine("आयु: $age")
        }
        
        message { summary }.send(ctx.user, ctx.bot)
    }
    
    override suspend fun onRetry(ctx: WizardContext) = Unit
    
    override suspend fun validate(ctx: WizardContext): Transition {
        return Transition.Finish
    }
}
```

#### फॉलबैक विधियाँ

यदि टाइप-सुरक्षित विधियाँ उपलब्ध नहीं हैं, तो फॉलबैक विधियों का उपयोग करें:

```kotlin
// फॉलबैक - Any? लौटाता है
val name = ctx.getState(NameStep::class)

// फॉलबैक - Any? स्वीकार करता है
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
            message { "आपका नाम क्या है?" }.send(ctx.user, ctx.bot)
        }
        
        override suspend fun onRetry(ctx: WizardContext) {
            message { "कृपया एक वैध नाम दर्ज करें।" }.send(ctx.user, ctx.bot)
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
            message { "आपकी आयु क्या है?" }.send(ctx.user, ctx.bot)
        }
        
        override suspend fun onRetry(ctx: WizardContext) {
            message { "कृपया एक वैध आयु दर्ज करें (एक संख्या होनी चाहिए)." }.send(ctx.user, ctx.bot)
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
                "क्षमा करें, पंजीकरण के लिए आपकी आयु 18 या उससे अधिक होनी चाहिए।" 
            }.send(ctx.user, ctx.bot)
        }
        
        override suspend fun onRetry(ctx: WizardContext) = Unit
        
        override suspend fun validate(ctx: WizardContext): Transition {
            return Transition.Finish
        }
    }
    
    object ConfirmationStep : WizardStep {
        override suspend fun onEntry(ctx: WizardContext) {
            // टाइप-सुरक्षित स्थिति पहुंच
            val name: String? = ctx.getState<NameStep>()
            val age: Int? = ctx.getState<AgeStep>()
            
            val confirmation = buildString {
                appendLine("कृपया अपनी जानकारी की पुष्टि करें:")
                appendLine("नाम: $name")
                appendLine("आयु: $age")
                appendLine()
                appendLine("पुष्टि के लिए 'हाँ' या पुन: शुरू करने के लिए 'नहीं' का उत्तर दें।")
            }
            
            message { confirmation }.send(ctx.user, ctx.bot)
        }
        
        override suspend fun onRetry(ctx: WizardContext) {
            message { "कृपया 'हाँ' या 'नहीं' का उत्तर दें।" }.send(ctx.user, ctx.bot)
        }
        
        override suspend fun validate(ctx: WizardContext): Transition {
            val response = ctx.update.text?.lowercase()?.trim()
            return when (response) {
                "हाँ" -> Transition.Finish
                "नहीं" -> Transition.JumpTo(NameStep::class) // पुन: शुरू करें
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
                "पंजीकरण पूरा! स्वागत है, $name (आयु $age)." 
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

शर्तीय प्रवाह के लिए `Transition.JumpTo` का उपयोग करें:

```kotlin
override suspend fun validate(ctx: WizardContext): Transition {
    val choice = ctx.update.text?.lowercase()
    return when (choice) {
        "प्रीमियम" -> Transition.JumpTo(PremiumStep::class)
        "बेसिक" -> Transition.JumpTo(BasicStep::class)
        else -> Transition.Retry
    }
}
```

#### स्टेटलेस चरण

चरणों को स्थिति संग्रहीत करने की आवश्यकता नहीं है। बस `store()` से `null` लौटाएं (या जैसा है छोड़ दें):

```kotlin
object ConfirmationStep : WizardStep {
    override suspend fun store(ctx: WizardContext): Any? = null
    // ... शेष कार्यान्वयन
}
```

#### कस्टम राज्य प्रबंधक

कस्टम भंडारण (डेटाबेस, Redis, आदि) के लिए `WizardStateManager<T>` लागू करें:

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
        // डेटाबेस से हटाएं
        database.deleteWizardState(reference.userId, key.qualifiedName)
    }
}
```

---

### यह आंतरिक रूप से कैसे काम करता है

#### कोड उत्पादन

KSP उत्पन्न करता है:

1. **WizardActivity**: हार्डकोड चरणों के साथ `WizardActivity` का एक ठोस कार्यान्वयन
2. **स्टार्ट एक्टिविटी**: कमांड ट्रिगर को संभालता है और विज़ार्ड शुरू करता है
3. **इनपुट एक्टिविटी**: विज़ार्ड प्रवाह के दौरान उपयोगकर्ता इनपुट को संभालता है
4. **स्थिति एक्सेसर्स**: स्थिति पहुंच के लिए टाइप-सुरक्षित एक्सटेंशन फ़ंक्शंस

#### प्रवाह

1. उपयोगकर्ता `/register` भेजता है → स्टार्ट एक्टिविटी बुलाई जाती है
2. स्टार्ट एक्टिविटी `WizardContext` बनाता है और `wizardActivity.start(ctx)` कॉल करता है
3. `start()` प्रारंभिक चरण में प्रवेश करता है और वर्तमान चरण को ट्रैक करने के लिए `inputListener` सेट करता है
4. उपयोगकर्ता संदेश भेजता है → इनपुट एक्टिविटी बुलाई जाती है
5. इनपुट एक्टिविटी `wizardActivity.handleInput(ctx)` कॉल करता है
6. `handleInput()` इनपुट को मान्य करता है, स्थिति को बनाए रखता है, और अगले चरण पर संक्रमण करता है
7. प्रक्रिया तब तक दोहराती है जब तक `Transition.Finish` वापस नहीं आ जाता

#### स्थिति स्थायित्व

- सफल सत्यापन के बाद स्थिति बनाए रखी जाती है (संक्रमण से पहले)
- प्रत्येक चरण का `store()` रिटर्न मान मिलान `WizardStateManager` का उपयोग करके सहेजा जाता है
- स्थिति प्रति उपयोगकर्ता और चैट (`UserChatReference`) पर स्कोप की जाती है

---

### सर्वोत्तम अभ्यास

#### 1. हमेशा स्पष्ट संकेत दें

```kotlin
override suspend fun onEntry(ctx: WizardContext) {
    message { 
        "कृपया अपना ईमेल पता दर्ज करें:\n" +
        "(प्रारूप: user@example.com)" 
    }.send(ctx.user, ctx.bot)
}
```

#### 2. सत्यापन त्रुटियों को सौम्यता से संभालें

```kotlin
override suspend fun onRetry(ctx: WizardContext) {
    message { 
        "अमान्य ईमेल प्रारूप। कृपया पुन: प्रयास करें।\n" +
        "उदाहरण: user@example.com" 
    }.send(ctx.user, ctx.bot)
}
```

#### 3. टाइप-सुरक्षित स्थिति पहुंच का उपयोग करें

उत्पन्न टाइप-सुरक्षित विधियों को प्राथमिकता दें:

```kotlin
// ✅ अच्छा - टाइप-सुरक्षित
val name: String? = ctx.getState<NameStep>()

// ❌ टालें - टाइप सुरक्षा खो देता है
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
    // नाम, ईमेल, फ़ोन, पता संभालता है...
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
        
        message { "पंजीकरण रद्द कर दिया गया।" }.send(ctx.user, ctx.bot)
    }
}
```

---

### सारांश

विज़ार्ड सिस्टम प्रदान करता है:
- ✅ **टाइप-सुरक्षित** स्थिति प्रबंधन संकलन-समय जांच के साथ
- ✅ **घोषणात्मक** नेस्टेड क्लास के रूप में चरण परिभाषाएँ
- ✅ **लचीला** शर्तीय तर्क के साथ संक्रमण
- ✅ **स्वचालित** KSP के माध्यम से कोड उत्पादन
- ✅ **एकीकृत** मौजूदा एक्टिविटी सिस्टम के साथ
- ✅ **प्लग करने योग्य** राज्य भंडारण बैकएंड

विज़ार्ड बनाना शुरू करें `@WizardHandler` एनोटेशन के साथ एक क्लास को एनोट करके और अपने चरणों को नेस्टेड `WizardStep` ऑब्जेक्ट के रूप में परिभाषित करके!
यदि आपके कोई प्रश्न हैं तो हमसे चैट में संपर्क करें, हम मदद करने के लिए तैयार हैं :)
---