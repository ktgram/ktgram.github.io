---
---
title: फंक्शनल डीएसएल
---

### To ~~infinity~~ functional dsl and beyond!

बॉट एनोटेशन-आधारित और फंक्शनल डीएसएल दोनों सेटिंग कंटेक्स्ट का समर्थन करता है। आप दोनों दृष्टिकोणों को मिला सकते हैं।

### फंक्शनल डीएसएल

फंक्शनल डीएसएल बॉट कंटेक्स्ट को परिभाषित करने का एक अलग तरीका है।

उदाहरण:

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

### कमांड और इनपुट

आप फंक्शनल डीएसएल का उपयोग करके `commands` और `inputs` दोनों को संभाल सकते हैं।

#### कमांड

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

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
}
```

`onCommand` में, पार्स किए गए पैरामीटर आपकी कॉन्फ़िगरेशन के आधार पर `Map<String, String>` के रूप में उपलब्ध हैं।

#### इनपुट

आप [`bot.inputListener`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot/-telegram-bot/input-listener.html) के माध्यम से इनपुट का उपयोग कर सकते हैं।

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

    bot.setFunctionality {
        onCommand("/start") {
            message { "Hello, what's your name?" }.send(user, bot)
            bot.inputListener[user] = "testInput"
        }
        
        onInput("testInput") {
            message { "Hey, nice to meet you, ${update.text}" }.send(user, bot)
        }
    }
}
```

#### इनपुट चेन

मल्टी-स्टेप इनपुट फ्लो के लिए, `inputChain` का उपयोग करें:

```kotlin
bot.setFunctionality {
    inputChain("conversation") {
        message { "Nice to meet you, ${update.text}" }.send(user, bot)
        message { "What is your favorite food?" }.send(user, bot)
    }.breakIf({ update.text == "peanut butter" }) { // chain break condition
        message { "Oh, too bad, I'm allergic to it." }.send(user, bot)
        // action that will be applied when condition matches
    }.andThen {
        // next input point if break condition doesn't match
        message { "Great choice!" }.send(user, bot)
    }
}
```

चेन स्वचालित रूप से अगले चरण पर आगे बढ़ती है जब तक कि कोई ब्रेक कंडीशन पूरी न हो। यदि कोई ब्रेक कंडीशन मैच होती है और `repeat` `true` (डिफ़ॉल्ट) है, तो उपयोगकर्ता वर्तमान चरण पर रहता है।

#### अपडेट प्रकार हैंडलर

विशिष्ट अपडेट प्रकारों को सीधे संभालें:

```kotlin
bot.setFunctionality {
    onUpdate(UpdateType.MESSAGE, UpdateType.CALLBACK_QUERY) {
        // Handle both message and callback query updates
        println("Received update: ${update.type}")
    }
}
```

#### सामान्य मैचर

`common` का उपयोग करके टेक्स्ट कंटेंट (केवल कमांड नहीं) से मिलान करें:

```kotlin
bot.setFunctionality {
    // String matching
    common("hello") {
        message { "Hi there!" }.send(user, bot)
    }
    
    // Regex matching
    common("""\d+""".toRegex()) {
        message { "You sent a number!" }.send(user, bot)
    }
}
```

#### फॉलबैक हैंडलर

उन अपडेट्स को संभालें जिन्हें किसी हैंडलर द्वारा प्रोसेस नहीं किया गया:

```kotlin
bot.setFunctionality {
    whenNotHandled {
        message { "I didn't understand that." }.send(user, bot)
    }
}
```

### एडवांस्ड कॉन्फ़िगरेशन

#### रेट लिमिटिंग

किसी भी हैंडलर पर रेट लिमिट लागू करें:

```kotlin
bot.setFunctionality {
    onCommand("/expensive", rateLimits = RateLimits(5, 60)) {
        // This command can only be called 5 times per 60 seconds
        message { "Processing..." }.send(user, bot)
    }
}
```

#### गार्ड

कस्टम वैलिडेशन लॉजिक जोड़ने के लिए गार्ड का उपयोग करें:

```kotlin
bot.setFunctionality {
    onCommand("/admin", guard = AdminGuard::class) {
        message { "Admin command executed" }.send(user, bot)
    }
}
```

#### आर्ग्युमेंट पार्सिंग

कमांड आर्ग्युमेंट्स को कैसे पार्स किया जाता है, इसे कस्टमाइज़ करें:

```kotlin
bot.setFunctionality {
    onCommand("/custom", argParser = CustomArgParser::class) {
        // parameters will be parsed using CustomArgParser
        message { "Parameters: $parameters" }.send(user, bot)
    }
}
```

### फंक्शनल और एनोटेशन-आधारित सेटिंग को मिलाना

आप एक ही बॉट में दोनों दृष्टिकोणों का उपयोग कर सकते हैं:

```kotlin
// Annotation-based handler
@CommandHandler(["/register"])
suspend fun register(ctx: CommandContext) {
    message { "Registration started" }.send(ctx.user, ctx.bot)
}

// Functional handler
bot.setFunctionality {
    onCommand("/help") {
        message { "Available commands: /register, /help" }.send(user, bot)
    }
}
```

दोनों हैंडलर एक ही `ActivityRegistry` में पंजीकृत हैं और सहजता से काम करते हैं।

### देखें भी

* [Action](Actions.md)
* [Useful utilities](Useful-utilities-and-tips.md)
---