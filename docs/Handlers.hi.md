---
---
title: Handlers
---


### Variety of Handlers

बॉट विकास में, विशेष रूप से उपयोगकर्ता अंतःक्रिया वाले सिस्टम में, कमांड और इवेंट्स को कुशलता से प्रबंधित और प्रोसेस करना अत्यावश्यक है।

ये एनोटेशन उन फ़ंक्शनों को चिह्नित करते हैं जो विशिष्ट कमांड, इनपुट या अपडेट्स को प्रोसेस करने के लिए डिज़ाइन किए गए हैं और कमांड कुंजी शब्द, स्कोप और गार्ड्स जैसी मेटाडेटा प्रदान करते हैं।

### Annotations Overview

#### CommandHandler

`CommandHandler` एनोटेशन का उपयोग उन फ़ंक्शनों को चिह्नित करने के लिए किया जाता है जो विशिष्ट कमांड्स को प्रोसेस करते हैं। इस एनोटेशन में कमांड के कुंजी शब्द और स्कोप को परिभाषित करने वाले प्रॉपर्टीज़ शामिल हैं।

-   **value**: कमांड से जुड़े कुंजी शब्द निर्दिष्ट करता है।
-   **scope**: वह संदर्भ या स्कोप निर्धारित करता है जिसमें कमांड की जाँच की जाएगी।

```kotlin
@CommandHandler(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommandHandler.CallbackQuery

`CommandHandler` का एक विशेष संस्करण जो विशेष रूप से कॉलबैक क्वेरीज़ को हैंडल करने के लिए डिज़ाइन किया गया है। इसमें `CommandHandler` के समान प्रॉपर्टीज़ होते हैं, लेकिन कॉलबैक-संबंधी कमांड्स पर केंद्रित होता है।

_यह वास्तव में सिर्फ `@CommandHandler` ही है जिसमें पूर्वनिर्धारित `UpdateType.CALLBACK_QUERY` स्कोप है_।

-   **value**: कमांड से जुड़े कुंजी शब्द निर्दिष्ट करता है।
-   **autoAnswer**: `callbackQuery` का स्वचालित उत्तर देता है (हैंडल करने से पहले `answerCallbackQuery` कॉल करता है)।

```kotlin
@CommandHandler.CallbackQuery(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### CommonHandler

`CommonHandler` एनोटेशन उन फ़ंक्शनों के लिए है जो `CommandHandler` और `InputHandler` की तुलना में कम प्राथमिकता के साथ कमांड प्रोसेस करते हैं। यह स्रोत स्तर पर उपयोग किया जाता है और सामान्य कमांड हैंडलर्स को परिभाषित करने का लचीला तरीका प्रदान करता है।

**ध्यान रखें, प्राथमिकता केवल `@CommonHandler` के भीतर कार्य करती है (यानी अन्य हैंडलर्स को प्रभावित नहीं करती)।**

##### CommonHandler.Text

यह एनोटेशन अपडेट्स के विरुद्ध टेक्स्ट मिलान को निर्दिष्ट करता है। इसमें मिलान टेक्स्ट, फ़िल्टरिंग शर्तें, प्राथमिकता और स्कोप को परिभाषित करने वाले प्रॉपर्टीज़ शामिल हैं।

-   **value**: आने वाले अपडेट्स के विरुद्ध मिलाने के लिए टेक्स्ट।
-   **filter**: ऐसी क्लास जो मिलान प्रक्रिया में उपयोग की जाने वाली शर्तों को परिभाषित करती है।
-   **priority**: हैंडलर की प्राथमिकता स्तर, जहाँ 0 सबसे उच्च प्राथमिकता है।
-   **scope**: वह संदर्भ या स्कोप जिसमें टेक्स्ट मिलान की जाँच की जाएगी।

```kotlin
@CommonHandler.Text(["text"], filter = isNewUserFilter::class, priority = 10)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommonHandler.Regex

`CommonHandler.Text` के समान, यह एनोटेशन नियमित अभिव्यक्तियों (regex) के आधार पर अपडेट्स को मिलान करने के लिए उपयोग किया जाता है। इसमें regex पैटर्न, विकल्प, फ़िल्टरिंग शर्तें, प्राथमिकता और स्कोप को परिभाषित करने वाले प्रॉपर्टीज़ शामिल हैं।

-   **value**: मिलान के लिए उपयोग किया जाने वाला regex पैटर्न।
-   **options**: regex पैटर्न के व्यवहार को बदलने वाले विकल्प।
-   **filter**: ऐसी क्लास जो मिलान प्रक्रिया में उपयोग की जाने वाली शर्तों को परिभाषित करती है।
-   **priority**: हैंडलर की प्राथमिकता स्तर, जहाँ 0 सबसे उच्च प्राथमिकता है।
-   **scope**: वह संदर्भ या स्कोप जिसमें regex मिलान की जाँच की जाएगी।

```kotlin
@CommonHandler.Regex("^\d+$", scope = [UpdateType.EDITED_MESSAGE])
suspend fun test(update: EditedMessageUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### InputHandler

`InputHandler` एनोटेशन उन फ़ंक्शनों को चिह्नित करता है जो विशिष्ट इनपुट इवेंट्स को प्रोसेस करते हैं। यह रनटाइम पर इनपुट्स को संभालने वाले फ़ंक्शनों के लिए अभिप्रेत है और इनपुट कुंजी शब्द और स्कोप को परिभाषित करने वाले प्रॉपर्टीज़ शामिल करता है।

-   **value**: इनपुट इवेंट से जुड़े कुंजी शब्द निर्दिष्ट करता है।

```kotlin
@InputHandler("text")
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UnprocessedHandler

`UnprocessedHandler` एनोटेशन उन फ़ंक्शनों को चिह्नित करने के लिए प्रयोग किया जाता है जो अन्य हैंडलर्स द्वारा प्रोसेस न किए गए अपडेट्स को संभालते हैं। यह सुनिश्चित करता है कि किसी भी अप्रसंस्कृत अपडेट को उचित रूप से प्रबंधित किया जाए, और इस हैंडलर प्रकार के लिए केवल एक प्रोसेसिंग पॉइंट संभव हो।

```kotlin
@UnprocessedHandler
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UpdateHandler

`UpdateHandler` एनोटेशन उन फ़ंक्शनों को चिह्नित करता है जो विशिष्ट प्रकार के इनकमिंग अपडेट्स को संभालते हैं। यह विभिन्न अपडेट प्रकारों को व्यवस्थित रूप से वर्गीकृत और प्रोसेस करने का तरीका प्रदान करता है।

-   **type**: उन अपडेट प्रकारों को निर्दिष्ट करता है जिन्हें हैंडलर फ़ंक्शन प्रोसेस करेगा।
-   **messageKind** *(added in 9.5)*: वैकल्पिक [`MessageKind`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-message-kind/index.html) का सेट जो डिस्पैच को उन संदेश-धारण करने वाले अपडेट्स तक सीमित करता है जिनका पता लगाया गया प्रकार मेल खाता है। डिफ़ॉल्ट (खाली) का मतलब किसी भी प्रकार से मेल खाता है।

```kotlin
@UpdateHandler([UpdateType.PRE_CHECKOUT_QUERY])
suspend fun test(update: PreCheckoutQueryUpdate, user: User, bot: TelegramBot) {
    //...
}
```

##### Filtering by `MessageKind`

`messageKind` पैरामीटर का उपयोग करके केवल संदेश अपडेट्स के किसी विशेष उपसमुच्चय (फ़ोटो, टेक्स्ट, सर्विस इवेंट्स, …) पर प्रतिक्रिया दें, बजाय हाथ से nullable फ़ील्ड्स की जांच करने के:

```kotlin
@UpdateHandler(type = [UpdateType.MESSAGE], messageKind = [MessageKind.PHOTO])
suspend fun onPhoto(update: MessageUpdate, bot: TelegramBot) {
    //...
}
```
### Handler Companion Annotations

हैंडलर्स के साथ वैकल्पिक अतिरिक्त एनोटेशन भी होते हैं, जो स्वयं हैंडलर्स के वैकल्पिक व्यवहार को पूरक करते हैं।

इन्हें फ़ंक्शन पर भी लगाया जा सकता है जहाँ हैंडलर लागू है और क्लास पर भी; बाद के मामले में यह क्लास की सभी हैंडलर्स पर स्वचालित रूप से लागू हो जाएंगे, लेकिन आवश्यकता होने पर कुछ फ़ंक्शनों के लिए अलग व्यवहार रखना संभव है।

उदाहरण के लिए, लागू करने की प्राथमिकता `Function` > `Class` है, जहाँ फ़ंक्शन की प्राथमिकता अधिक होती है।

#### Rate Limiting

अतिरिक्त रूप से, हम एनोटेशन में वर्णित रेट लिमिटिंग मैकेनिज़्म को भी दर्शाते हैं।

आप प्रत्येक उपयोगकर्ता के लिए सामान्य सीमाएँ सेट कर सकते हैं:

```kotlin
// ...
val bot = TelegramBot("BOT_TOKEN") {
    rateLimiter { // general limits
        limits = RateLimits(period = 10000, rate = 5)
    }
}
```

###### Handler specific

किसी विशेष कार्रवाई पर सीमाएँ `RateLimits` एनोटेशन के माध्यम से परिभाषित की जा सकती हैं, समर्थित `@CommandHandler`, `@CommandHandler.CallbackQuery`, `@InputHandler`, `@CommonHandler`।

```kotlin
@CommandHandler(["/start"])
@RateLimits(period = 1000L, rate = 1L)
suspend fun start(user: User, bot: TelegramBot) {
    // ...
}
```

#### Guard

आप गार्ड्स को अलग से परिभाषित करके हैंडलर्स तक पहुँच को नियंत्रित कर सकते हैं, समर्थित `@CommandHandler`, `@CommandHandler.CallbackQuery`, `@InputHandler` :

```kotlin
@CommandHandler(["text"])
@Guard(isAdminGuard::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### ArgParser

आप कस्टम आर्ग्युमेंट पार्सर को अलग से परिभाषित करके हैंडलर्स के पैरामीटर पार्सिंग व्यवहार को बदल सकते हैं, समर्थित `@CommandHandler`, `@CommandHandler.CallbackQuery`, `@CommonHandler`:

```kotlin
@CommandHandler(["text"])
@ArgParser(SpaceArgParser::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

**see also [`defaultArgParser`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.common/default-arg-parser.html)**

### Functional DSL

ऊपर उल्लेखित प्रत्येक एनोटेशन का **Functional DSL** में एक समकक्ष है, जो रनटाइम पर `bot.setFunctionality { … }` के माध्यम से हैंडलर्स घोषित करने का वैकल्पिक तरीका है। दोनों दृष्टिकोण एक ही `ActivityRegistry` को साझा करते हैं और एक ही बॉट में स्वतंत्र रूप से मिलाए जा सकते हैं।

| Annotation | DSL counterpart |
|------------|-----------------|
| `@CommandHandler` | `onCommand(...)` |
| `@CommandHandler.CallbackQuery` | `onCommand(..., scope = [UpdateType.CALLBACK_QUERY])` |
| `@InputHandler` / input chains | `onInput(...)` / `inputChain(...)` |
| `@CommonHandler` | `common(...)` |
| `@UpdateHandler` | `onUpdate(...)` |
| `@UnprocessedHandler` | `whenNotHandled { ... }` |

Minimal example:

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

    bot.setFunctionality {
        onChosenInlineResult {
            println("got a result ${update.chosenInlineResult.resultId} from ${update.user}")
        }
    }
}
```

### Commands

```kotlin
bot.setFunctionality {
    // Regular command
    onCommand("/start") {
        message { "Hello" }.send(user, bot)
    }

    // Regex-based command matching
    onCommand("""(red|green|blue)""".toRegex()) {
        message { "you typed ${update.text} color" }.send(user, bot)
    }
}
```

`onCommand` ब्लॉक के भीतर, पार्स किए गए पैरामीटर `Map<String, String>` के रूप में उपलब्ध होते हैं, जो सक्रिय `commandParsing` कॉन्फ़िगरेशन द्वारा आकारित होते हैं।

### Inputs

```kotlin
bot.setFunctionality {
    onCommand("/start") {
        message { "Hello, what's your name?" }.send(user, bot)
        bot.inputListener[user] = "testInput"
    }

    onInput("testInput") {
        message { "Hey, nice to meet you, ${update.text}" }.send(user, bot)
    }
}
```

स्टोरेज API के लिए देखें [`bot.inputListener`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot/-telegram-bot/input-listener.html)।

#### Input chains

बहु‑चरणीय इनपुट फ्लो के लिए `inputChain` का उपयोग करें:

```kotlin
bot.setFunctionality {
    inputChain("conversation") {
        message { "Nice to meet you, ${update.text}" }.send(user, bot)
        message { "What is your favorite food?" }.send(user, bot)
    }.breakIf({ update.text == "peanut butter" }) {     // chain break condition
        message { "Oh, too bad, I'm allergic to it." }.send(user, bot)
    }.andThen {
        // next step when the break condition didn't match
        message { "Great choice!" }.send(user, bot)
    }
}
```

चेन स्वतः आगे बढ़ती है जब तक कि ब्रेक कंडीशन नहीं मिलती; जब `repeat = true` (डिफ़ॉल्ट) हो, तो मिलती हुई ब्रेक उपयोगकर्ता को वर्तमान चरण पर रखती है।

> अधिक समृद्ध बहु‑चरणीय फ्लो के लिए टाइप्ड स्टेट और वैलिडेशन के साथ, बेहतर है कि [`@WizardHandler`](FSM-and-Conversation-handling.md) का उपयोग करें।

### Update type handlers

```kotlin
bot.setFunctionality {
    onUpdate(UpdateType.MESSAGE, UpdateType.CALLBACK_QUERY) {
        println("Received update: ${update.type}")
    }
}
```

### Common matchers

```kotlin
bot.setFunctionality {
    common("hello") {
        message { "Hi there!" }.send(user, bot)
    }

    common("""\d+""".toRegex()) {
        message { "You sent a number!" }.send(user, bot)
    }
}
```

### Fallback handler

```kotlin
bot.setFunctionality {
    whenNotHandled {
        message { "I didn't understand that." }.send(user, bot)
    }
}
```

### Companion options

रेट लिमिट, गार्ड, और आर्ग्युमेंट पार्सर्स को अलग एनोटेशन की बजाय नामित पैरामीटर के रूप में सीधे पास किया जाता है:

```kotlin
bot.setFunctionality {
    onCommand("/expensive", rateLimits = RateLimits(rate = 5, period = 60_000)) {
        message { "Processing..." }.send(user, bot)
    }

    onCommand("/admin", guard = AdminGuard::class) {
        message { "Admin command executed" }.send(user, bot)
    }

    onCommand("/custom", argParser = CustomArgParser::class) {
        message { "Parameters: $parameters" }.send(user, bot)
    }
}
```

### Combining DSL and annotations

दोनों शैलियाँ साथ में 존재 करती हैं — समान तरीके से रजिस्टर करें, समान तरीके से डिस्पैच करें:

```kotlin
@CommandHandler(["/register"])
suspend fun register(user: User, bot: TelegramBot) {
    message { "Registration started" }.send(user, bot)
}

bot.setFunctionality {
    onCommand("/help") {
        message { "Available commands: /register, /help" }.send(user, bot)
    }
}
```

### Conclusion

ये एनोटेशन कमांड, इनपुट और इवेंट्स को संभालने के लिए मजबूत और लचीले उपकरण प्रदान करते हैं, साथ ही रेट लिमिट और गार्ड्स के पृथक कॉन्फ़िगरेशन की अनुमति देते हैं, जिससे बॉट विकास की समग्र संरचना और रखरखाव क्षमता में सुधार होता है।

### See also

* [Activities & Processors](Activites-and-Processors.md)
* [Activity invocation](Activity-invocation.md)
* [FSM and Conversation handling](FSM-and-Conversation-handling.md)
* [Sessions](Sessions.md)
* [Update parsing](Update-parsing.md)

---