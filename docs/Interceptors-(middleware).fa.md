---
---
title: Interceptors (Middleware)
---

### Interceptors: Cross-Cutting Logic for Your Bot

هنگام ساخت یک ربات تلگرام، معمولاً تنظیمات، بررسی‌ها یا پاک‌سازی‌ها را در چندین هندلر تکرار می‌کنید. Interceptors به شما امکان می‌دهند منطق مشترک را در اطراف هندلرها وصل کنید و هندلرها را متمرکز و قابل نگهداری نگه دارید.

در اینجا نحوه کار Interceptorها در *telegram-bot* و چگونگی استفاده از آن‌ها آورده شده است.

### What Are Interceptors? (Simple Explanation)

Interceptorها توابعی هستند که در نقاط مشخصی از مسیر پردازش آپدیت اجرا می‌شوند. آن‌ها به شما اجازه می‌دهند:
- بافت پردازش را بررسی و اصلاح کنید
- منطق مشترک (logging, auth, metrics) اضافه کنید
- در صورت نیاز پردازش را زودتر متوقف کنید
- منابع را پس از پردازش پاک‌سازی کنید

Interceptorها را می‌توان به‌عنوان نقطه‌های بررسی در نظر گرفت که هر آپدیت قبل، حین و پس از اجرای هندلر از آن‌ها عبور می‌کند.


### The Processing Pipeline

ربات آپدیت‌ها را از طریق یک خط لوله با هفت فاز پردازش می‌کند:

| Phase | When It Runs | What You Can Use It For |
|-------|--------------|-------------------------|
| **Setup** | به محض رسیدن آپدیت، قبل از هر پردازشی | ✔ محدودیت نرخ Global<br>✔ فیلتر کردن اسپم یا آپدیت‌های خراب<br>✔ لاگ‌گیری اولیه<br>✔ تنظیم بافت مشترک |
| **Parsing** | پس از Setup، استخراج فرمان و پارامترها | ✔ پارسینگ سفارشی فرمان<br>✔ غنی‌سازی بافت با داده‌های پارس‌شده<br>✔ اعتبارسنجی ساختار آپدیت |
| **Match** | پیدا کردن هندلر مناسب (Command/Input/Common) | ✔ بازنویسی انتخاب هندلر<br>✔ منطق سفارشی برای ورودی<br>✔ لاگ‌گیری هندلرهای منطبق |
| **Validation** | پس از یافتن هندلر، قبل از فراخوانی | ✔ مجوزهای خاص هندلر<br>✔ محدودیت نرخ برای هر هندلر<br>✔ بررسی‌های Guard<br>✔ لغو پردازش در صورت عدم برآورده شدن شرایط |
| **PreInvoke** | بلافاصله قبل از اجرا شدن هندلر | ✔ بررسی‌های لحظه آخر<br>✔ شروع تایمر/متریک<br>✔ غنی‌سازی بافت برای هندلر<br>✔ تغییر رفتار هندلر |
| **Invoke** | اجرا شدن هندلر در اینجا | ✔ پوشش اجرای هندلر<br>✔ مدیریت خطا<br>✔ لاگ‌گیری نتایج هندلر |
| **PostInvoke** | پس از اتمام هندلر (موفق یا ناموفق) | ✔ پاک‌سازی منابع<br>✔ لاگ‌گیری نتایج<br>✔ ارسال پیام‌های fallback در صورت خطا<br>✔ اصلاح نتایج پیش از بازگشت |


### Creating an Interceptor

یک Interceptor تابع ساده‌ای است که یک `ProcessingContext` دریافت می‌کند:

```kotlin
import eu.vendeli.tgbot.core.PipelineInterceptor
import eu.vendeli.tgbot.types.component.ProcessingContext

val myInterceptor: PipelineInterceptor = { context ->
    // Your logic here
    println("Processing update: ${context.update.updateId}")
}
```

یا با استفاده از lambda:

```kotlin
val loggingInterceptor = PipelineInterceptor { context ->
    val logger = context.bot.config.loggerFactory.get("MyInterceptor")
    logger.info("Processing update #${context.update.updateId}")
}
```


### Registering Interceptors

Interceptorها را در خط لوله پردازش ثبت کنید:

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

مثال: رباتی که برای برخی فرمان‌ها نیاز به احراز هویت دارد، زمان اجرای هندلر را اندازه می‌گیرد و تمام فرمان‌ها را لاگ می‌کند.

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

`ProcessingContext` دسترسی به موارد زیر را فراهم می‌کند:

- **`update: ProcessedUpdate`** - آپدیت جاری که در حال پردازش است
- **`bot: TelegramBot`** - نمونه ربات
- **`registry: ActivityRegistry`** - رجیستری اکتیویتی‌ها
- **`parsedInput: String`** - متن فرمان/ورودی پارس‌شده
- **`parameters: Map<String, String>`** - پارامترهای فرمان پارس‌شده
- **`activity: Activity?`** - هندلر حل‌شده (تا فاز Match مقدار null است)
- **`shouldProceed: Boolean`** - آیا پردازش باید ادامه یابد
- **`additionalContext: AdditionalContext`** - داده‌های بافت اضافی
- **`finish()`** - توقف زودتر پردازش

#### Stopping Processing Early

برای توقف زودتر پردازش `context.finish()` را فراخوانی کنید:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.Validation) { context ->
    if (someCondition) {
        context.finish() // No further phases will execute
    }
}
```

#### Storing Custom Data

از `additionalContext` برای انتقال داده بین Interceptorها استفاده کنید:

```kotlin
// In PreInvoke
context.additionalContext["userId"] = context.update.userOrNull?.id

// In PostInvoke
val userId = context.additionalContext["userId"] as? Long
```


### Multiple Interceptors

می‌توانید چندین Interceptor برای همان فاز ثبت کنید. آن‌ها به ترتیب ثبت اجرا می‌شوند:

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

اگر یک Interceptor `context.finish()` را صدا بزند، Interceptorهای بعدی در همان فاز رد می‌شوند و فازهای بعدی اجرا نخواهند شد.


### Best Practices

#### 1. Use the Right Phase

- Setup: بررسی‌های کلی، فیلتر کردن، تنظیم اولیه
- Parsing: منطق پارسینگ سفارشی
- Match: منطق انتخاب هندلر
- Validation: مجوزها، محدودیت نرخ، Guardها
- PreInvoke: آماده‌سازی خاص هندلر
- Invoke: معمولاً توسط Interceptor پیش‌فرض مدیریت می‌شود
- PostInvoke: پاک‌سازی، لاگ‌گیری، مدیریت خطا

#### 2. Keep Interceptors Focused

هر Interceptor باید یک کار انجام دهد:

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

Interceptorها نباید ربات را سقوط دهند:

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

اگر در `PreInvoke` منبعی باز کردید، در `PostInvoke` آن را پاک‌سازی کنید:

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

Interceptorها را به ترتیبی ثبت کنید که می‌خواهید اجرا شوند:

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

Interceptorها برای موارد زیر ایده‌آل هستند:
- ✅ احراز هویت/مجوز
- ✅ لاگ‌گیری
- ✅ متریک/نظارت عملکرد
- ✅ محدودیت نرخ
- ✅ مدیریت خطا
- ✅ تبدیل درخواست/پاسخ

برای منطق خاص هندلر، آن را در خود هندلر نگه دارید.


### Default Interceptors

چارچوب Interceptorهای پیش‌فرض برای عملکرد هسته‌ای شامل می‌شود:

- **DefaultSetupInterceptor**: محدودیت نرخ سراسری
- **DefaultParsingInterceptor**: پارس فرمان
- **DefaultMatchInterceptor**: تطبیق هندلر (دستورات، ورودی‌ها، matcherهای عمومی)
- **DefaultValidationInterceptor**: بررسی Guardها و محدودیت نرخ برای هر هندلر
- **DefaultInvokeInterceptor**: اجرای هندلر و مدیریت خطا

Interceptorهای سفارشی شما همراه با این پیش‌فرض‌ها اجرا می‌شوند. می‌توانید قبل یا بعد از پیش‌فرض‌ها منطق اضافه کنید، اما نمی‌توانید Interceptorهای پیش‌فرض را حذف کنید.

---

### Advanced: Conditional Interceptors

می‌توانید Interceptorها را شرطی کنید:

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

Interceptorها روشی تمیز برای افزودن منطق مشترک به ربات شما ارائه می‌دهند:

- ✅ **هفت فاز** برای مراحل مختلف پردازش
- ✅ **API ساده**: فقط `PipelineInterceptor` را پیاده‌سازی کنید
- ✅ **قابل انعطاف**: می‌توانید چندین Interceptor برای هر فاز ثبت کنید
- ✅ **قوی**: دسترسی به بافت پردازش کامل
- ✅ **ایمن**: می‌توانید پردازش را زودتر با `context.finish()` متوقف کنید

از Interceptorها برای حفظ تمرکز هندلرها بر منطق کسب‌وکار استفاده کنید و نگرانی‌های مشترک مانند احراز هویت، لاگ‌گیری و متریک‌ها را به‌صورت مرکزی مدیریت کنید.

---

### See also

* [Handlers (incl. Functional DSL)](Handlers.md) - تعریف هندلرها به‌صورت Annotation و DSL
* [Sessions](Sessions.md) - حالت per‑chat / per‑user و ردیابی پیام
* [Guards](Guards.md) - بررسی‌های مجوز سطح هندلر
---