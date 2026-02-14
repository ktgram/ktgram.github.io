---
---
عنوان: Fsm And Conversation Handling
---

کتابخانه همچنین از مکانیزم FSM پشتیبانی می‌کند، که مکانیزمی برای پردازش تدریجی ورودی کاربر با مدیریت ورودی نادرست است.

> [!NOTE]
> TL;DR: نمونه را [در اینجا](https://github.com/vendelieu/telegram-bot_template/tree/conversation) ببینید.

### در تئوری

بیایید یک موقعیت را تصور کنیم که شما نیاز به جمع‌آوری یک نظرسنجی از کاربر دارید، می‌توانید تمام داده‌های یک شخص را در یک مرحله بپرسید، اما با ورودی نادرست یکی از پارامترها، هم برای کاربر و هم برای ما دشوار خواهد بود، و هر مرحله ممکن است متفاوت باشد بسته به داده‌های ورودی خاص.

حال بیایید ورودی گام‌به‌گام داده‌ها را تصور کنیم، جایی که ربات وضعیت گفت‌وگو با کاربر را وارد می‌کند.

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/2e84fa00-e59c-4352-8665-83be3b971e7b" alt="نمودار فرآیند مدیریت" />
</p>

پیکان‌های سبز فرآیند گذار از مرحله به مرحله بدون خطا را نشان می‌دهند، پیکان‌های آبی به معنای ذخیره وضعیت فعلی و منتظر ورودی مجدد است (برای مثال اگر کاربر اشاره کرد که سن او -100 سال است، باید دوباره از سن بپرسد)، و قرمزها خروج از کل فرآیند به دلیل هر دستوری یا هر معنای لغو دیگری را نشان می‌دهند.

### در عمل

سیستم Wizard تعامل‌های چندمرحله‌ای کاربر را در ربات‌های تلگرام فعال می‌کند. کاربران را از طریق یک توالی مراحل راهنمایی می‌کند، ورودی را تأیید می‌کند، وضعیت را ذخیره می‌کند و بین مراحل گذار می‌کند.

**مزایای کلیدی:**
- **تایپ ایمن**: بررسی تایپ در زمان کامپایل برای دسترسی به وضعیت
- **اعلامی**: مراحل را به عنوان کلاس‌های تو در تو تعریف کنید
- **انعطاف‌پذیر**: پشتیبانی از گذارهای شرطی، پرش‌ها و تلاش مجدد
- **وضعیت‌دار**: پایداری خودکار وضعیت با ذخیره‌سازی backend قابل plug-in
- **یکپارچه**: با سیستم فعالیت موجود کار می‌کند

### مفاهیم پایه

#### WizardStep

یک `WizardStep` یک مرحله منفرد در جریان wizard را نشان می‌دهد. هر مرحله باید پیاده‌سازی کند:

- **`onEntry(ctx: WizardContext)`**: زمانی که کاربر وارد این مرحله می‌شود فراخوانی می‌شود. از این برای درخواست از کاربر استفاده کنید.
- **`onRetry(ctx: WizardContext)`**: زمانی که تأیید ناموفق بوده و مرحله باید تلاش مجدد کند فراخوانی می‌شود. از این برای نمایش پیام‌های خطا استفاده کنید.
- **`validate(ctx: WizardContext): Transition`**: ورودی فعلی را تأیید می‌کند و یک `Transition` باز می‌گرداند که نشان می‌دهد چه اتفاقی بعد از آن می‌افتد.
- **`store(ctx: WizardContext): Any?`** (اختیاری): مقداری را باز می‌گرداند که باید برای این مرحله ذخیره شود. `null` بازگردانید اگر مرحله وضعیتی ذخیره نکند.

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
> اگر برخی از مراحل به عنوان اولیه مشخص نشده باشند -> اولین مرحله اعلام شده به عنوان اولیه در نظر گرفته می‌شود.

#### Transition

یک `Transition` تعیین می‌کند چه اتفاقی بعد از تأیید می‌افتد:

- **`Transition.Next`**: به مرحله بعدی در توالی برو
- **`Transition.JumpTo(step: KClass<out WizardStep>)`**: به یک مرحله خاص پرش کن
- **`Transition.Retry`**: مرحله فعلی را تلاش مجدد کن (تأیید ناموفق بود)
- **`Transition.Finish`**: wizard را به پایان برسان

```kotlin
// پرش شرطی بر اساس ورودی
override suspend fun validate(ctx: WizardContext): Transition {
    val age = ctx.update.text?.toIntOrNull()
    return when {
        age == null -> Transition.Retry
        age < 18 -> Transition.JumpTo(UnderageStep::class)
        else -> Transition.Next
    }
}
```

#### WizardContext

`WizardContext` دسترسی به:
- **`user: User`**: کاربر فعلی
- **`update: ProcessedUpdate`**: آپدیت فعلی
- **`bot: TelegramBot`**: نمونه ربات
- **`userReference: UserChatReference`**: مرجع شناسه کاربر و چت برای ذخیره‌سازی وضعیت

علاوه بر متدهای دسترسی به وضعیت تایپ ایمن (توسط KSP تولید می‌شود).

---

### تعریف یک Wizard

#### ساختار پایه

یک wizard به عنوان یک کلاس یا شی با کامنت `@WizardHandler` تعریف می‌شود:

```kotlin
@WizardHandler(trigger = ["/survey"])
object SurveyWizard {
    object NameStep : WizardStep(isInitial = true) {
        // ... پیاده‌سازی مرحله
    }
    
    object AgeStep : WizardStep {
        // ... پیاده‌سازی مرحله
    }
    
    object FinishStep : WizardStep {
        // ... پیاده‌سازی مرحله
    }
}
```

#### پارامترهای کامنت

**`@WizardHandler`** پذیرفته می‌کند:
- **`trigger: Array<String>`**: دستوراتی که wizard را شروع می‌کنند (مثلاً `["/start", "/survey"]`)
- **`scope: Array<UpdateType>`**: انواع آپدیت‌هایی که گوش می‌کند (پیش‌فرض: `[UpdateType.MESSAGE]`)
- **`stateManagers: Array<KClass<out WizardStateManager<*>>>`**: کلاس‌های مدیر وضعیت برای ذخیره‌سازی داده مراحل

---

### مدیریت وضعیت

#### WizardStateManager

وضعیت با استفاده از پیاده‌سازی‌های `WizardStateManager<T>` ذخیره می‌شود. هر مدیر یک نوع خاص را مدیریت می‌کند:

```kotlin
interface WizardStateManager<T : Any> {
    suspend fun get(key: KClass<out WizardStep>, reference: UserChatReference): T?
    suspend fun set(key: KClass<out WizardStep>, reference: UserChatReference, value: T)
    suspend fun del(key: KClass<out WizardStep>, reference: UserChatReference)
}
```

همچنین ببینید: [MapStateManager<T>](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-state-manager/index.html)، [MapStringStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-string-state-manager/index.html)، [MapIntStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-int-state-manager/index.html)، [MapLongStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-long-state-manager/index.html).

#### تطبیق خودکار

KSP مراحل را با مدیران وضعیت بر اساس نوع بازگشتی `store()` تطبیق می‌دهد:

```kotlin
@WizardHandler(
    trigger = ["/survey"],
    stateManagers = [StringStateManager::class, IntStateManager::class]
)
object SurveyWizard {
    object NameStep : WizardStep(isInitial = true) {
        override suspend fun store(ctx: WizardContext): String {
            return ctx.update.text!! // با StringStateManager تطبیق می‌خورد
        }
    }
    
    object AgeStep : WizardStep {
        override suspend fun store(ctx: WizardContext): Int {
            return ctx.update.text!!.toInt() // با IntStateManager تطبیق می‌خورد
        }
    }
}
```

#### بازنویسی تک مرحله‌ای

برای بازنویسی مدیر وضعیت برای یک مرحله خاص از `@WizardHandler.StateManager` استفاده کنید:

```kotlin
@WizardHandler(
    trigger = ["/survey"],
    stateManagers = [DefaultStateManager::class]
)
object SurveyWizard {
    object NameStep : WizardStep(isInitial = true) {
        // از DefaultStateManager استفاده می‌کند
    }
    
    @WizardHandler.StateManager(CustomStateManager::class)
    object AgeStep : WizardStep {
        // به جای آن از CustomStateManager استفاده می‌کند
    }
}
```

---

### دسترسی به وضعیت تایپ ایمن

KSP توابع گسترش تایپ ایمن برای `WizardContext` برای هر مرحله‌ای که وضعیت ذخیره می‌کند تولید می‌کند.

#### توابع تولید شده

برای یک مرحله که یک `String` ذخیره می‌کند:

```kotlin
// به صورت خودکار توسط KSP تولید می‌شود
suspend inline fun <reified S : WizardStep> WizardContext.getState(): String?
suspend inline fun <reified S : WizardStep> WizardContext.setState(value: String)
suspend inline fun <reified S : WizardStep> WizardContext.delState()
```

#### استفاده

```kotlin
object FinishStep : WizardStep {
    override suspend fun onEntry(ctx: WizardContext) {
        // دسترسی تایپ ایمن - String? (nullable) باز می‌گرداند
        val name: String? = ctx.getState<NameStep>()
        
        // دسترسی تایپ ایمن - Int? (nullable) باز می‌گرداند
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

#### متدهای fallback

اگر متدهای تایپ ایمن در دسترس نباشند، از متدهای fallback استفاده کنید:

```kotlin
// Fallback - Any? باز می‌گرداند
val name = ctx.getState(NameStep::class)

// Fallback - Any? می‌پذیرد
ctx.setState(NameStep::class, "John")
ctx.delState(NameStep::class)
```

---

### نمونه کامل

#### wizard ثبت‌نام کاربر

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
            // دسترسی تایپ ایمن به وضعیت
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
                "no" -> Transition.JumpTo(NameStep::class) // از نو شروع کن
                else -> Transition.Retry
            }
        }
    }
    
    object FinishStep : WizardStep {
        override suspend fun onEntry(ctx: WizardContext) {
            val name: String? = ctx.getState<NameStep>()
            val age: Int? = ctx.getState<AgeStep>()
            
            // ذخیره در دیتابیس، ارسال تأیید، و غیره.
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

### ویژگی‌های پیشرفته

#### گذارهای شرطی

برای جریان‌های شرطی از `Transition.JumpTo` استفاده کنید:

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

#### مراحل بدون وضعیت

مراحل نیازی به ذخیره وضعیت ندارند. ببسید `null` از `store()` بازگردانید (یا همانطور که هست بگذارید):

```kotlin
object ConfirmationStep : WizardStep {
    override suspend fun store(ctx: WizardContext): Any? = null
    // ... بقیه پیاده‌سازی
}
```

#### مدیران وضعیت سفارشی

`WizardStateManager<T>` را برای ذخیره‌سازی سفارشی (دیتابیس، Redis و غیره) پیاده‌سازی کنید:

```kotlin
class DatabaseStateManager : WizardStateManager<String> {
    override suspend fun get(
        key: KClass<out WizardStep>,
        reference: UserChatReference
    ): String? {
        // از دیتابیس بارگذاری کن
        return database.getWizardState(reference.userId, key.qualifiedName)
    }
    
    override suspend fun set(
        key: KClass<out WizardStep>,
        reference: UserChatReference,
        value: String
    ) {
        // در دیتابیس ذخیره کن
        database.saveWizardState(reference.userId, key.qualifiedName, value)
    }
    
    override suspend fun del(
        key: KClass<out WizardStep>,
        reference: UserChatReference
    ) {
        // از دیتابیس حذف کن
        database.deleteWizardState(reference.userId, key.qualifiedName)
    }
}
```

---

### چگونه در درون کار می‌کند

#### تولید کد

KSP تولید می‌کند:

1. **WizardActivity**: یک پیاده‌سازی ملموس که از `WizardActivity` ارث می‌برد با مراحل hardcoded
2. **Start Activity**: دستور trigger را مدیریت کرده و wizard را شروع می‌کند
3. **Input Activity**: ورودی کاربر را در جریان wizard مدیریت می‌کند
4. **State Accessors**: توابع گسترش تایپ ایمن برای دسترسی به وضعیت

#### جریان

1. کاربر `/register` را ارسال می‌کند → Start Activity فراخوانی می‌شود
2. Start Activity یک `WizardContext` می‌سازد و `wizardActivity.start(ctx)` را فراخوانی می‌کند
3. `start()` وارد مرحله اولیه می‌شود و `inputListener` را برای ردیابی مرحله فعلی تنظیم می‌کند
4. کاربر یک پیام ارسال می‌کند → Input Activity فراخوانی می‌شود
5. Input Activity `wizardActivity.handleInput(ctx)` را فراخوانی می‌کند
6. `handleInput()` ورودی را تأیید می‌کند، وضعیت را ذخیره می‌کند و به مرحله بعدی گذار می‌کند
7. فرآیند تا زمانی که `Transition.Finish` بازگردانده شود تکرار می‌شود

#### پایداری وضعیت

- وضعیت بعد از تأیید موفق (قبل از گذار) ذخیره می‌شود
- مقدار بازگشتی `store()` هر مرحله با استفاده از `WizardStateManager` مطابق ذخیره می‌شود
- وضعیت در هر کاربر و چت (`UserChatReference`) scoped است

---

### بهترین شیوه‌ها

#### 1. همیشه پیام‌های روشن ارائه دهید

```kotlin
override suspend fun onEntry(ctx: WizardContext) {
    message { 
        "Please enter your email address:\n" +
        "(Format: user@example.com)" 
    }.send(ctx.user, ctx.bot)
}
```

#### 2. خطاهای تأیید را با مهربانی مدیریت کنید

```kotlin
override suspend fun onRetry(ctx: WizardContext) {
    message { 
        "Invalid email format. Please try again.\n" +
        "Example: user@example.com" 
    }.send(ctx.user, ctx.bot)
}
```

#### 3. از دسترسی تایپ ایمن به وضعیت استفاده کنید

ترجیحاً از متدهای تایپ ایمن تولید شده استفاده کنید:

```kotlin
// ✅ خوب - تایپ ایمن
val name: String? = ctx.getState<NameStep>()

// ❌ اجتناب کنید - تایپ ایمنی از دست می‌دهد
val name = ctx.getState(NameStep::class) as? String
```

#### 4. مراحل را متمرکز نگه دارید

هر مرحله باید یک مسئولیت واحد داشته باشد:

```kotlin
// ✅ خوب - مرحله متمرکز
object EmailStep : WizardStep {
    // فقط جمع‌آوری ایمیل را مدیریت می‌کند
}

// ❌ اجتناب کنید - منطق زیاد
object PersonalInfoStep : WizardStep {
    // نام، ایمیل، تلفن، آدرس را مدیریت می‌کند...
}
```

#### 5. از نام‌های معنی‌دار مرحله استفاده کنید

```kotlin
// ✅ خوب
object EmailVerificationStep : WizardStep

// ❌ اجتناب کنید
object Step2 : WizardStep
```

#### 6. وضعیت را هنگام نیاز پاک کنید

اگر نیاز به پاک کردن دستی وضعیت دارید:

```kotlin
object CancelStep : WizardStep {
    override suspend fun onEntry(ctx: WizardContext) {
        // تمام وضعیت wizard را پاک کن
        ctx.delState<NameStep>()
        ctx.delState<AgeStep>()
        
        message { "Registration cancelled." }.send(ctx.user, ctx.bot)
    }
}
```

---

### خلاصه

سیستم Wizard ارائه می‌دهد:
- ✅ **تایپ ایمن** مدیریت وضعیت با بررسی در زمان کامپایل
- ✅ **اعلامی** تعریف مراحل به عنوان کلاس‌های تو در تو
- ✅ **انعطاف‌پذیر** گذارها با منطق شرطی
- ✅ **خودکار** تولید کد توسط KSP
- ✅ **یکپارچه** با سیستم فعالیت موجود
- ✅ **قابل plug-in** backend‌های ذخیره‌سازی وضعیت

شروع به ساختن wizardها با کامنت کردن یک کلاس با `@WizardHandler` و تعریف مراحل خود به عنوان اشیای `WizardStep` تو در تو کنید!
اگر سوالی دارید با ما در چت تماس بگیرید، ما خوشحالیم که کمک کنیم :)
---