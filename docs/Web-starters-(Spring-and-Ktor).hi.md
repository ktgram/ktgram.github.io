---
---
title: Web Starters (Spring And Ktor)
---

### Spring starter

Spring Starter मॉड्यूल लाइब्रेरी के लिए एक ऑटो‑कॉन्फ़िगरेशन मॉड्यूल है जो Telegram बॉट कार्यक्षमताओं को Spring Boot एप्लिकेशन में एकीकृत करता है। यह Spring Boot की डिपेंडेंसी इंजेक्शन और कॉन्फ़िगरेशन प्रॉपर्टीज़ की शक्ति का उपयोग करके प्रदान किए गए कॉन्फ़िगरेशन के आधार पर स्वचालित रूप से Telegram बॉट को कॉन्फ़िगर करता है। यह लाइब्रेरी उन डेवलपर्स के लिए विशेष रूप से उपयोगी है जो Kotlin और Spring Boot का उपयोग करके Telegram बॉट बनाना चाहते हैं, बॉट विकास और प्रबंधन के लिए एक सुव्यवस्थित दृष्टिकोण प्रदान करती है।

### Key Features

- **Auto-Configuration**: लाइब्रेरी प्रदान किए गए कॉन्फ़िगरेशन प्रॉपर्टीज़ के आधार पर Telegram बॉट को स्वचालित रूप से कॉन्फ़िगर करती है, जिससे मैन्युअल सेटअप की आवश्यकता समाप्त हो जाती है।
- **Configuration Properties**: यह बॉट सेटिंग्स जैसे बॉट टोकन, पैकेज नाम, और आइडेंटिफायर को आसान कस्टमाइज़ेशन के लिए कॉन्फ़िगरेशन प्रॉपर्टीज़ का समर्थन करता है।
- **Spring Integration**: Spring इकोसिस्टम के साथ सहजता से इंटीग्रेट करता है, बॉट इंस्टेंस को मैनेज करने के लिए Spring की डिपेंडेंसी इंजेक्शन और एप्लिकेशन कॉन्टेक्स्ट का उपयोग करता है।
- **Coroutine Support**: असिंक्रोनस बॉट ऑपरेशन्स के लिए Kotlin कोरोटीन का लाभ उठाता है, जिससे प्रभावी और नॉन‑ब्लॉकिंग निष्पादन सुनिश्चित होता है।

### Getting Started

Telegram बॉट्स के लिए Spring Starter लाइब्रेरी का उपयोग करने के लिए, आपको इसे अपने Spring Boot प्रोजेक्ट में एक डिपेंडेंसी के रूप में शामिल करना होगा। लाइब्रेरी Spring Boot एप्लिकेशन के साथ कार्य करने के लिए डिज़ाइन की गई है और इसे कार्य करने के लिए Spring Boot फ्रेमवर्क की आवश्यकता होती है।

#### Dependency

अपने `build.gradle` या `pom.xml` फ़ाइल में निम्नलिखित डिपेंडेंसी जोड़ें:

```gradle
dependencies {
    implementation 'eu.vendeli:spring-starter:<version>'
}
```

`<version>` को लाइब्रेरी के नवीनतम संस्करण से बदलें।

#### Configuration

लाइब्रेरी कॉन्फ़िगरेशन प्रॉपर्टीज़ को बाइंड करने के लिए Spring Boot की `@ConfigurationProperties` का उपयोग करती है। आप अपने बॉट कॉन्फ़िगरेशन `application.properties` या `application.yml` फ़ाइल में परिभाषित कर सकते हैं।

```yaml
ktgram:
 autoStartPolling: true
 shareHttpClient: true
 bot:
    - token: YOUR_BOT_TOKEN
      pckg: com.example.bot
      identifier: MyBot
```

#### Usage

एक बार लाइब्रेरी शामिल और कॉन्फ़िगर हो जाने पर, यह प्रदान किए गए कॉन्फ़िगरेशन के आधार पर स्वचालित रूप से Telegram बॉट इंस्टेंस बनाता और कॉन्फ़िगर करता है।

यह कई बॉट इंस्टेंस का भी समर्थन करता है; कई बॉट आरंभ करने के लिए बस बॉट सेक्शन में नया प्रविष्टि जोड़ें:

```yaml
ktgram:
 bot:
    - token: YOUR_BOT_TOKEN
    - token: SECOND_BOT_TOKEN
```

### Advanced Configuration

और अधिक उन्नत कॉन्फ़िगरेशन के लिए, जैसे बॉट व्यवहार को कस्टमाइज़ करना या अन्य Spring कंपोनेंट्स के साथ इंटीग्रेट करना, आप `BotConfiguration` क्लास को एक्सटेंड कर सकते हैं और उसके `applyCfg` मेथड के माध्यम से बॉट कॉन्फ़िगरेशन बदल सकते हैं; उदाहरण के लिए आप [यहाँ](https://github.com/vendelieu/telegram-bot_template/blob/spring-bot/src/main/kotlin/com/example/springbot/configuration/BotConfig.kt) देख सकते हैं।

> [!TIP]
> प्रत्येक आरंभित इंस्टेंस को कस्टम कॉन्फ़िगरेशन के साथ कॉन्फ़िगर करने के लिए, उन्हें उनके आइडेंटिफायर द्वारा अलग पहचानें (BotConfiguration क्लास में भी एक आइडेंटिफायर होता है)।

### Ktor

यह मॉड्यूल Telegram बॉट्स के लिए वेबहूक सर्वर बनाने में सुविधा प्रदान करने के लिए डिज़ाइन किया गया है। यह डेवलपर्स को सर्वर, जिसमें SSL/TLS सेटिंग्स शामिल हैं, को कॉन्फ़िगर करने और कस्टम कॉन्फ़िगरेशन के साथ कई Telegram बॉट्स को घोषित करने की अनुमति देता है। सेटअप प्रक्रिया लचीली है, जिससे डेवलपर्स अपनी विशिष्ट आवश्यकताओं के अनुसार सर्वर को अनुकूलित कर सकते हैं।

### Installation

ktor starter स्थापित करने के लिए मुख्य डिपेंडेंसी में अतिरिक्त जोड़ें:

```gradle
dependencies {
    implementation("eu.vendeli:ktor-starter:x.y.z") // there
    // change x.y.z to current library version
}
```

### Key Components

`serveWebhook` Function

`serveWebhook` फ़ंक्शन लाइब्रेरी का कोर है। यह Telegram बॉट्स के लिए वेबहूक सर्वर सेट अप करता और शुरू करता है। यह दो पैरामीटर लेता है:

- `wait`: एक बूलियन जो दर्शाता है कि सर्वर को एप्लिकेशन के बंद होने का इंतज़ार करना चाहिए या नहीं। डिफ़ॉल्ट रूप से true।
- `serverBuilder`: एक लैम्ब्डा फ़ंक्शन जो सर्वर को कॉन्फ़िगर करता है। डिफ़ॉल्ट रूप से खाली लैम्ब्डा।

### Configuration

* `WEBHOOK_PREFIX`: यह पैरामीटर वेबहूक लिस्नर रूट के पते के प्रीफ़िक्स के लिए उपयोग किया जाता है। (डिफ़ॉल्ट "/")

#### Server Setup

- `server`: EnvConfiguration या ManualConfiguration में से किसी का उपयोग करके सर्वर कॉन्फ़िगरेशन सेट करने की विधि।
- `engine`: Netty एप्लिकेशन इंजन को कॉन्फ़िगर करने की विधि।
- `ktorModule`: एप्लिकेशन में Ktor मॉड्यूल जोड़ने की विधि।

लाइब्रेरी सर्वर के लिए होस्ट, पोर्ट, SSL सेटिंग्स आदि जैसे कई कॉन्फ़िगरेबल पैरामीटर प्रदान करती है। इसे कॉन्फ़िगर करने के दो ठोस विकल्प हैं:

* `EnvConfiguration`: `KTGRAM_` प्रीफ़िक्स के साथ पर्यावरण से कॉन्फ़िगरेशन वैल्यू पढ़ता है।
* `ManualConfiguration`: `server {}` फ़ंक्शन में पैरामीटर मैन्युअल रूप से सेट करने की अनुमति देता है।

सेट किए जा सकने वाले पैरामीटर की सूची:

- `HOST`: सर्वर के होस्टनाम या IP पता।
- `PORT`: सर्वर का पोर्ट नंबर।
- `SSL_PORT`: SSL/TLS कनेक्शन के लिए पोर्ट नंबर।
- `PEM_PRIVATE_KEY_PATH`: PEM प्राइवेट की फ़ाइल का पाथ।
- `PEM_CHAIN_PATH`: PEM सर्टिफ़िकेट चेन फ़ाइल का पाथ।
- `PEM_PRIVATE_KEY`: PEM प्राइवेट की का पासवर्ड कैरेक्टर एरे रूप में।
- `KEYSTORE_PATH`: Java KeyStore फ़ाइल का पाथ।
- `KEYSTORE_PASSWORD`: KeyStore का पासवर्ड।
- `KEY_ALIAS`: KeyStore में की का एलियास।
- `SSL_ON`: एक बूलियन जो दर्शाता है कि SSL/TLS सक्षम होना चाहिए या नहीं। डिफ़ॉल्ट true।

> [!TIP]
> यदि PEM सर्टिफ़िकेट मौजूद हैं, तो मॉड्यूल स्वयं निर्दिष्ट पाथ पर उनसे एक jks स्टोरेज बनाएगा।

#### Bot Configuration:

बॉट को कॉन्फ़िगर करने के लिए `declareBot {}` कॉल करें जिसमें निम्न पैरामीटर होते हैं:

- `token`: बॉट टोकन।
- `pckg`: बॉट का पैकेज नाम।
- `configuration`: बॉट को कॉन्फ़िगर करने के लिए लैम्ब्डा फ़ंक्शन।
- `handlingBehaviour`: बॉट के हैंडलिंग व्यवहार को सेट करने के लिए लैम्ब्डा फ़ंक्शन।
- `onInit`: बॉट के इनिशियलाइज़ होने पर चलने वाला लैम्ब्डा फ़ंक्शन।

### Example Usage

इस मॉड्यूल का उपयोग करने के लिए `serveWebhook` फ़ंक्शन कॉल करें, इसे अपनी वांछित सेटिंग्स के साथ कॉन्फ़िगर करें, और अपने बॉट्स को घोषित करें। यहाँ एक सरल उदाहरण है:

```kotlin
fun main() = runBlocking {
    serveWebhook {
        server {
            HOST = "0.0.0.0"
            PORT = 8080
            SSL_PORT = 8443

            PEM_PRIVATE_KEY_PATH = "/etc/letsencrypt/live/example.com/privkey.pem"
            PEM_CHAIN_PATH = "/etc/letsencrypt/live/example.com/fullchain.pem"
            PEM_PRIVATE_KEY = "pem_changeit".toCharArray()

            KEYSTORE_PATH = "/etc/ssl/certs/java/cacerts/bot_keystore.jks"
            KEYSTORE_PASSWORD = "changeit".toCharArray()
            // Set other configuration parameters as needed
        }
        declareBot {
            token = "YOUR_BOT_TOKEN"
            // Configure other bot settings
        }
        // Add more bots or set other parameters if needed
    }
}
```

> [!CAUTION]
> सब कुछ काम करने के लिए वेबहूक सेट करना न भूलें। :)

डिफ़ॉल्ट रूप से मॉड्यूल वेबहूक लिस्निंग एन्डपॉइंट `host/BOT_TOKEN` के रूप में सर्व करेगा


---