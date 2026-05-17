---
---
title: Guards
---

### परिचय
Guards बॉट बनाने वाले डेवलपर्स के लिए एक आवश्यक सुविधा है। ये गार्ड्स प्री-एक्ज़िक्यूशन चेक्स के रूप में काम करते हैं जो निर्धारित करते हैं कि कोई विशेष कमांड 실행 किया जाना चाहिए या नहीं। इन चेक्स को लागू करके, डेवलपर्स अपने बॉट की कार्यक्षमता, सुरक्षा और उपयोगकर्ता अनुभव को बेहतर बना सकते हैं।

### Activity Guards का उद्देश्य
Activity गार्ड्स का मुख्य उद्देश्य यह सुनिश्चित करना है कि केवल अधिकृत उपयोगकर्ता या विशिष्ट स्थितियों में ही कोई activity ट्रिगर हो।

इससे दुरुपयोग को रोका जा सकता है, बॉट की अखंडता बनी रहती है, और इंटरैक्शन को सहज बनाया जा सकता है।

### सामान्य उपयोग के मामले
1. प्रमाणीकरण और प्राधिकरण: यह सुनिश्चित करना कि केवल कुछ उपयोगकर्ता ही विशिष्ट कमांड्स तक पहुंच सकें।  
2. प्री-कंडीशन चेक्स: यह सत्यापित करना कि activity को निष्पादित करने से पहले कुछ शर्तें पूरी हुई हैं (उदा., उपयोगकर्ता एक विशेष स्थिति या संदर्भ में है)।  
3. संदर्भ गार्ड्स: वर्तमान चैट या उपयोगकर्ता की स्थिति के आधार पर निर्णय लेना।

### कार्यान्वयन रणनीतियाँ
Telegram Command Guards को लागू करने में आमतौर पर प्रत्येक गार्ड की लॉजिक को समाहित करने वाले फ़ंक्शन या मेथड लिखे जाते हैं। नीचे सामान्य रणनीतियाँ दी गई हैं:

1. यूज़र रोल चेक:
   - कमांड चलाने से पहले यह सुनिश्चित करना कि उपयोगकर्ता के पास आवश्यक भूमिका है (जैसे, admin, moderator)।
      ```kotlin
       override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // Check if the user is an admin in the given chat
       }
      ```
   
2. स्टेट वैरिफिकेशन:
   - कमांड निष्पादन की अनुमति देने से पहले उपयोगकर्ता की स्थिति की जाँच करना।
     ```kotlin
     override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        return bot.userData[user.id, "data"] == requiredState
     }
     ```
   
3. कस्टम गार्ड्स:
   - विशिष्ट आवश्यकताओं के आधार पर कस्टम लॉजिक बनाना।
     ```kotlin
     override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // Custom logic to determine if the command should be executed
     }
     ```
   
### गार्ड्स को Activities के साथ एकीकृत करना
इन गार्ड्स को आपके बॉट कमांड्स के साथ एकीकृत करने के लिए, आप एक गार्ड बना सकते हैं जो कमांड हैंडलर के बुलाए जाने से पहले इन शर्तों की जाँच करता है।

### कार्यान्वयन उदाहरण

```kotlin
// define somewhere your guard class that implements Guard interface
object YourGuard : Guard {
    override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // write your condition here
    }
}

// ...

@CommandHandler(["yourCommand"])
@Guard(YourGuard::class) // InputHandler also is supported
fun command(bot: TelegramBot) {
   // command body
}
```

### सर्वोत्तम प्रथाएँ

- मॉड्युलैरिटी: गार्ड लॉजिक को मॉड्यूलर रखें और activities से अलग रखें।  
- पुन: उपयोगिता: पुनः उपयोग योग्य गार्ड फ़ंक्शन लिखें जिन्हें विभिन्न कमांड/इनपुट्स में आसानी से लागू किया जा सके।  
- दक्षता: प्रदर्शन ओवरहेड को न्यूनतम करने के लिए गार्ड चेक्स को ऑप्टिमाइज़ करें।  
- उपयोगकर्ता प्रतिक्रिया: जब कोई कमांड गार्ड द्वारा ब्लॉक किया जाए तो उपयोगकर्ता को स्पष्ट प्रतिक्रिया प्रदान करें।

### निष्कर्ष

Activity Guards बॉट कमांड/इनपुट निष्पादन को प्रबंधित करने के लिए एक शक्तिशाली उपकरण हैं।

मजबूत गार्ड मैकेनिज़्म लागू करके, डेवलपर्स सुनिश्चित कर सकते हैं कि उनके बॉट सुरक्षित और कुशलता से कार्य करें, और बेहतर उपयोगकर्ता अनुभव प्रदान करें।

### देखें भी

* [Activities and Proccessors](Activites-and-Processors.md)
* [Update parsing](Update-parsing.md)
* [Actions](Actions.md)
* [Activity invocation](Activity-invocation.md)

---