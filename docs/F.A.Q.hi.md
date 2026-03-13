---
---
title: एफ.ए.क्यू
---

### `AbstractMethodError` अपवाद

यदि आपके एप्लिकेशन के स्टार्टअप पर इस तरह का अपवाद मिल रहा है:

```kotlin
Exception in thread "DefaultDispatcher-worker-1" java.lang.AbstractMethodError: 'kotlinx.serialization.KSerializer[] kotlinx.serialization.internal.GeneratedSerializer.typeParametersSerializers()'
	at eu.vendeli.tgbot.types.options.GetUpdatesOptions$$serializer.typeParametersSerializers(GetUpdatesOptions.kt:6)
```

यह इसलिए हो रहा है क्योंकि आपका बिल्ड सिस्टम पुराने सीरियलाइज़ेशन लाइब्रेरी को रिज़ॉल्व कर रहा है जिसकी आंतरिक मैकेनिक्स अलग है।
इसे हल करने के लिए आपको इसे नए संस्करण का उपयोग करने के लिए मजबूर करना होगा, उदाहरण के लिए अपने बिल्डस्क्रिप्ट में यह जोड़कर:

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

(अगर इसे चेंजलॉग में अच्छी तरह से वर्णित किया गया होता तो मैंने कभी अपग्रेड नहीं किया होता क्योंकि मुझे इस मुद्दे पर इतनी रिपोर्ट मिल रही हैं)

### मैं मेथड का रिस्पॉन्स कैसे प्राप्त करूं?

रिस्पॉन्स प्राप्त करने और उस पर काम करने में सक्षम होने के लिए, आपको `send` के बजाय अंत में `sendReturning` का उपयोग करने की आवश्यकता है।

इस मामले में `Response` क्लास लौटाई जाती है, जिसमें रिस्पॉन्स, सफलता या विफलता होती है, आगे आपको या तो विफलता को संभालना होगा या बस `getOrNull()` को कॉल करना होगा।

इसके बारे में एक अनुभाग है: [रिस्पॉन्स को प्रोसेस करना](https://github.com/vendelieu/telegram-bot#processing-responses)।

### मैं `spring-boot-devtools` का उपयोग करते समय त्रुटि प्राप्त कर रहा हूँ

यह इसलिए होता है क्योंकि `spring-boot-devtools` का अपना `classloader` है और यह मेथड्स नहीं ढूंढ पा रहा है।

आपको `resources/META-INF/spring-devtools.properties` में जोड़ने की आवश्यकता है:

```properties
restart.include.generated=/eu.vendeli
```

### Ktor इंजन कैसे बदलें

यदि आप क्लाइंट द्वारा उपयोग किए जाने वाले इंजन को बदलना चाहते हैं तो आप [पैरामीटर](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/ktor-jvm-engine.html) को [प्लगइन सेटिंग्स](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/index.html) में बदल सकते हैं।

### मेरे पसंदीदा लॉगिंग प्रोवाइडर का उपयोग कैसे करें

लाइब्रेरी `slf4j-api` का उपयोग करती है और प्रोवाइडर का उपयोग करने के लिए आपको बस इसे डिपेंडेंसी में जोड़ने की आवश्यकता है।

लाइब्रेरी प्लगइन स्वचालित रूप से प्रोवाइडर के उपयोग का पता लगाता है, यदि प्रोवाइडर गायब है, तो डिफ़ॉल्ट रूप से `logback` का उपयोग किया जाएगा।

### लॉन्ग-पोलिंग हैंडलर के भीतर नेटवर्क अपवादों को पकड़ना

उदाहरण के लिए यदि आपके पास अस्थिर कनेक्शन है और इसके कारण त्रुटि को पकड़ने की आवश्यकता है, तो शायद यह दृष्टिकोण आपकी मदद करेगा:

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

आप देख सकते हैं कि [spring-starter](https://github.com/vendelieu/telegram-bot/blob/1584d40f9a94a8c31bba9e7614c0070155630a52/spring-ktgram-starter/src/jvmMain/kotlin/eu/vendeli/spring/starter/TelegramAutoConfiguration.kt#L53) में यह कैसे किया गया है।

---