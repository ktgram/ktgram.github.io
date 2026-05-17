---
---
title: F.A.Q
---

### `AbstractMethodError` exception

यदि आप अपने अनुप्रयोग के स्टार्टअप पर इस प्रकार का अपवाद प्राप्त कर रहे हैं:

```kotlin
Exception in thread "DefaultDispatcher-worker-1" java.lang.AbstractMethodError: 'kotlinx.serialization.KSerializer[] kotlinx.serialization.internal.GeneratedSerializer.typeParametersSerializers()'
	at eu.vendeli.tgbot.types.options.GetUpdatesOptions$$serializer.typeParametersSerializers(GetUpdatesOptions.kt:6)
```

यह इसलिए हो रहा है क्योंकि आपका बिल्ड सिस्टम पुरानी सीरियलाइज़ेशन लाइब्रेरी को हल कर रहा है जिसका इंटर्नल मैकेनिज़्म अलग है। इसे हल करने के लिए आपको अधिक नवीनतम संस्करण का प्रयोग करना चाहिए, उदाहरण के लिए अपने बिल्डस्क्रिप्ट में यह जोड़ें:

```kotlin
configurations.all {
    resolutionStrategy.eachDependency {
        val serdeVer = "x.x.x" // should be >= 1.8.0
        when(requested.module.toString()) {
            // json serialiazaton
            "org.jetbrains.kotlinx:kotlinx-serialization-json" -> useVersion(serdeVer)
            "org.jetbrains.kotlinx:kotlinx-serialization-json-jvm" -> useVersion(serdeVer)
            "org.jetbrains.kotlinx:kotlinx-serialization-core" -> useVersion(serdeVer)
            "org.jetbrains.kotlinx:kotlinx-serialization-core-jvm" -> useVersion(serdeVer)
            "org.jetbrains.kotlinx:kotlinx-serialization-bom" -> useVersion(serdeVer)
        }
    }
}
```

(यदि यह चेंजलॉग में ठीक से वर्णित था तो मैं इसे कभी अपग्रेड नहीं करता क्योंकि मुझे इस समस्या पर बहुत सारे रिपोर्ट मिलते थे)

### How do I get the method's response?

एक प्रतिक्रिया प्राप्त करने और उस पर काम करने के लिए, आपको `send` की बजाय मेथड के अंत में `sendReturning` का उपयोग करना होगा।

इस मामले में `Response` क्लास वापस आती है, जिसमें प्रतिक्रिया, सफलता या विफलता शामिल होती है, आगे आपको या तो विफलता को संभालना होगा या बस `getOrNull()` कॉल करना होगा।

सेक्शन के बारे में देखें: [Processing responses](https://github.com/vendelieu/telegram-bot#processing-responses).

### I'm getting error while using `spring-boot-devtools`

यह इसलिए होता है क्योंकि `spring-boot-devtools` का अपना `classloader` होता है और वह मेथड नहीं ढूँढ पाता।

आपको `resources/META-INF/spring-devtools.properties` में जोड़ना होगा:

```properties
restart.include.generated=/eu.vendeli
```

### How to change ktor engine

यदि आप क्लाएंट द्वारा उपयोग किए जाने वाले इंजन को बदलना चाहते हैं तो आप बस [पैरामीटर](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/ktor-jvm-engine.html) को [प्लगइन सेटिंग्स](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/index.html) में बदल सकते हैं।

### How to use my favorite logging provider

यह लाइब्रेरी `slf4j-api` का उपयोग करती है और प्रोवाइडर को उपयोग करने के लिए आपको उसे डिपेंडेंसीज़ में जोड़ना होगा।

लाइब्रेरी प्लगइन स्वतः ही प्रोवाइडर के उपयोग का पता लगाता है, यदि प्रोवाइडर अनुपलब्ध है, तो डिफ़ॉल्ट रूप से `logback` उपयोग किया जाएगा।

### Catch network exceptions within long-polling handler

उदाहरण के लिए यदि आपका कनेक्शन अस्थिर है और आपको इस कारण से त्रुटि को पकड़ना है, तो संभवतः यह तरीका मदद करेगा:

```kotlin
fun main() {
    val bot = TelegramBot("TOKEN")

    try {
        bot.handleUpdates()
    } catch (e: Exception) {
        // handle if needed
        
        bot.update.stopListener()
        bot.handleUpdates()
    }
}
```

आप [spring-starter](https://github.com/vendelieu/telegram-bot/blob/1584d40f9a94a8c31bba9e7614c0070155630a52/spring-ktgram-starter/src/jvmMain/kotlin/eu/vendeli/spring/starter/TelegramAutoConfiguration.kt#L53) में इसे कैसे किया गया है, भी देख सकते हैं।

---