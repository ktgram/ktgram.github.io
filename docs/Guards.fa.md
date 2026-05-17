---
---
title: Guards
---

### Introduction
Guards یک ویژگی اساسی برای توسعه‌دهندگانی هستند که ربات می‌سازند. این گاردها به‌عنوان بررسی‌های پیش از اجرا عمل می‌کنند تا تعیین کنند آیا یک دستور خاص باید فراخوانی شود یا نه. با پیاده‌سازی این بررسی‌ها، توسعه‌دهندگان می‌توانند کارکرد، امنیت و تجربه کاربری ربات‌های خود را بهبود بخشند.

### Purpose of Activity Guards
هدف اصلی گاردهای فعالیت این است که تنها کاربران مجاز یا شرایط خاصی یک فعالیت را تحریک کنند.

این می‌تواند از سوءاستفاده جلوگیری کند، یکپارچگی ربات را حفظ کند و تعاملات را به‌صورت کارآمدتری مدیریت نماید.

### Common Use Cases
1. Authentication and Authorization: اطمینان از این که تنها کاربران مشخصی می‌توانند به دستورات خاص دسترسی داشته باشند.  
2. Pre-condition Checks: تأیید اینکه شرایط خاصی پیش از اجرای یک فعالیت برآورده شده‌اند (مثلاً اطمینان از اینکه کاربر در حالت یا زمینه خاصی قرار دارد).  
3. Contextual Guards: اتخاذ تصمیم بر اساس وضعیت جاری چت یا کاربر.

### Implementation Strategies
پیاده‌سازی Guardهای دستور تلگرام معمولاً شامل نوشتن توابع یا روش‌هایی است که منطق هر گارد را در بر می‌گیرد. در زیر برخی استراتژی‌های رایج آمده است:

1. User Role Check:
   - اطمینان از این که کاربر نقش مورد نیاز (مثلاً admin، moderator) را قبل از اجرای دستور دارد.
      ```kotlin
       override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // Check if the user is an admin in the given chat
       }
      ```
   
2. State Verification:
   - بررسی وضعیت کاربر قبل از اجازه به اجرای دستور.
     ```kotlin
     override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        return bot.userData[user.id, "data"] == requiredState
     }
     ```
   
3. Custom Guards:
   - ایجاد منطق سفارشی بر پایه نیازمندی‌های خاص.
     ```kotlin
     override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // Custom logic to determine if the command should be executed
     }
     ```
   
### Integrating Guards with Activities
برای یکپارچه‌سازی این گاردها با دستورات ربات خود، می‌توانید گاردی ایجاد کنید که این شرایط را قبل از فراخوانی هندلر دستور بررسی کند.

### Implementing Example

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

### Best Practices

- Modularity: منطق گاردها را ماژولار و جدا از فعالیت‌ها نگه دارید.  
- Reusability: توابع گارد قابل استفاده مجدد بنویسید تا به‌راحتی در دستورات/ورودی‌های مختلف به کار رود.  
- Efficiency: بررسی‌های گارد را به‌گونه‌ای بهینه کنید که بار عملکردی کمی داشته باشد.  
- User Feedback: هنگام مسدود شدن یک دستور توسط گارد، بازخورد واضحی به کاربر ارائه دهید.

### Conclusion

Guardهای فعالیت ابزار قدرتمندی برای مدیریت اجرای دستورات/ورودی‌های ربات هستند.

با پیاده‌سازی سازوکارهای گارد قوی، توسعه‌دهندگان می‌توانند اطمینان حاصل کنند ربات‌هایشان به‌صورت ایمن و کارآمد عمل می‌کند و تجربه کاربری بهتری را فراهم می‌آورد.

### See also

* [Activities and Proccessors](Activites-and-Processors.md)
* [Update parsing](Update-parsing.md)
* [Actions](Actions.md)
* [Activity invocation](Activity-invocation.md)

---