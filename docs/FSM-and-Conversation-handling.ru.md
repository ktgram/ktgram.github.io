---
---
title: FSM и обработка диалогов
---

Библиотека также поддерживает механизм FSM, который представляет собой механизм пошаговой обработки пользовательского ввода с обработкой некорректного ввода.

> [!NOTE]
> TL;DR: См. пример [тут](https://github.com/vendelieu/telegram-bot_template/tree/conversation).

### В теории

Представим ситуацию, когда вам нужно собрать опрос у пользователя, можно запросить все данные человека за один шаг, но при некорректном вводе одного из параметров, это будет сложно и для пользователя, и для нас, и каждый шаг может отличаться в зависимости от определенных входных данных.

Теперь представим пошаговый ввод данных, когда бот переходит в режим диалога с пользователем.

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/2e84fa00-e59c-4352-8665-83be3b971e7b" alt="Схема процесса обработки" />
</p>

Зеленые стрелки указывают процесс перехода через шаги без ошибок, синие стрелки означают сохранение текущего состояния и ожидание повторного ввода (например, если пользователь указал, что ему -100 лет, нужно снова спросить возраст), а красные показывают выход из всего процесса из-за любой команды или отмены по любому другому значению.

### На практике

Система Wizard (волшебник) обеспечивает многошаговые взаимодействия с пользователем в ботах Telegram. Она проводит пользователей через последовательность шагов, проверяет ввод, сохраняет состояние и переходит между шагами.

**Основные преимущества:**
- **Type-safe**: Проверка типов на этапе компиляции для доступа к состоянию
- **Декларативный**: Определение шагов как вложенных классов/объектов
- **Гибкий**: Поддержка условных переходов, переходов и повторных попыток
- **Сохраняющий состояние**: Автоматическое сохранение состояния с подключаемыми бэкендами хранения
- **Интегрированный**: Работает с существующей системой Activity

### Основные концепции

#### WizardStep

`WizardStep` представляет собой отдельный шаг в потоке волшебника. Каждый шаг должен реализовывать:

- **`onEntry(ctx: WizardContext)`**: Вызывается, когда пользователь входит на этот шаг. Используйте это для запроса у пользователя.
- **`onRetry(ctx: WizardContext)`**: Вызывается при сбое валидации и необходимости повторной попытки. Используйте это для показа сообщений об ошибках.
- **`validate(ctx: WizardContext): Transition`**: Проверяет текущий ввод и возвращает `Transition`, указывающий, что происходит дальше.
- **`store(ctx: WizardContext): Any?`** (опционально): Возвращает значение для сохранения для этого шага. Верните `null`, если шаг не сохраняет состояние.

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
> Если какой-то шаг не помечен как начальный -> первый объявленный шаг считается таковым.

#### Transition

`Transition` определяет, что происходит после валидации:

- **`Transition.Next`**: Переход к следующему шагу в последовательности
- **`Transition.JumpTo(step: KClass<out WizardStep>)`**: Переход к конкретному шагу
- **`Transition.Retry`**: Повторная попытка текущего шага (валидация не прошла)
- **`Transition.Finish`**: Завершение волшебника

```kotlin
// Условный переход на основе ввода
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

`WizardContext` предоставляет доступ к:
- **`user: User`**: Текущий пользователь
- **`update: ProcessedUpdate`**: Текущее обновление
- **`bot: TelegramBot`**: Экземпляр бота
- **`userReference: UserChatReference`**: Ссылка на ID пользователя и чата для хранения состояния

Плюс методы типа-безопасного доступа к состоянию (генерируются KSP).

---

### Определение волшебника

#### Базовая структура

Волшебник определяется как класс или объект, аннотированный `@WizardHandler`:

```kotlin
@WizardHandler(trigger = ["/survey"])
object SurveyWizard {
    object NameStep : WizardStep(isInitial = true) {
        // ... реализация шага
    }
    
    object AgeStep : WizardStep {
        // ... реализация шага
    }
    
    object FinishStep : WizardStep {
        // ... реализация шага
    }
}
```

#### Параметры аннотации

**`@WizardHandler`** принимает:
- **`trigger: Array<String>`**: Команды, запускающие волшебника (например, `["/start", "/survey"]`)
- **`scope: Array<UpdateType>`**: Типы обновлений для прослушивания (по умолчанию: `[UpdateType.MESSAGE]`)
- **`stateManagers: Array<KClass<out WizardStateManager<*>>>`**: Классы менеджеров состояния для хранения данных шагов

---

### Управление состоянием

#### WizardStateManager

Состояние хранится с использованием реализаций `WizardStateManager<T>`. Каждый менеджер обрабатывает определенный тип:

```kotlin
interface WizardStateManager<T : Any> {
    suspend fun get(key: KClass<out WizardStep>, reference: UserChatReference): T?
    suspend fun set(key: KClass<out WizardStep>, reference: UserChatReference, value: T)
    suspend fun del(key: KClass<out WizardStep>, reference: UserChatReference)
}
```

См. также: [MapStateManager<T>](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-state-manager/index.html), [MapStringStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-string-state-manager/index.html), [MapIntStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-int-state-manager/index.html), [MapLongStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-long-state-manager/index.html).

#### Автоматическое сопоставление

KSP сопоставляет шаги с менеджерами состояния на основе возвращаемого типа `store()`:

```kotlin
@WizardHandler(
    trigger = ["/survey"],
    stateManagers = [StringStateManager::class, IntStateManager::class]
)
object SurveyWizard {
    object NameStep : WizardStep(isInitial = true) {
        override suspend fun store(ctx: WizardContext): String {
            return ctx.update.text!! // Соответствует StringStateManager
        }
    }
    
    object AgeStep : WizardStep {
        override suspend fun store(ctx: WizardContext): Int {
            return ctx.update.text!!.toInt() // Соответствует IntStateManager
        }
    }
}
```

#### Переопределение на уровне шага

Переопределите менеджер состояния для конкретного шага, используя `@WizardHandler.StateManager`:

```kotlin
@WizardHandler(
    trigger = ["/survey"],
    stateManagers = [DefaultStateManager::class]
)
object SurveyWizard {
    object NameStep : WizardStep(isInitial = true) {
        // Использует DefaultStateManager
    }
    
    @WizardHandler.StateManager(CustomStateManager::class)
    object AgeStep : WizardStep {
        // Использует CustomStateManager вместо
    }
}
```

---

### Тип-безопасный доступ к состоянию

KSP генерирует тип-безопасные функции расширения на `WizardContext` для каждого шага, который сохраняет состояние.

#### Сгенерированные функции

Для шага, сохраняющего `String`:

```kotlin
// Генерируется автоматически KSP
suspend inline fun <reified S : WizardStep> WizardContext.getState(): String?
suspend inline fun <reified S : WizardStep> WizardContext.setState(value: String)
suspend inline fun <reified S : WizardStep> WizardContext.delState()
```

#### Использование

```kotlin
object FinishStep : WizardStep {
    override suspend fun onEntry(ctx: WizardContext) {
        // Тип-безопасный доступ - возвращает String? (nullable)
        val name: String? = ctx.getState<NameStep>()
        
        // Тип-безопасный доступ - возвращает Int? (nullable)
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

#### Методы резервного доступа

Если тип-безопасные методы недоступны, используйте методы резервного доступа:

```kotlin
// Резервный метод - возвращает Any?
val name = ctx.getState(NameStep::class)

// Резервный метод - принимает Any?
ctx.setState(NameStep::class, "John")
ctx.delState(NameStep::class)
```

---

### Полный пример

#### Волшебник регистрации пользователя

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
            // Тип-безопасный доступ к состоянию
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
                "no" -> Transition.JumpTo(NameStep::class) // Начать заново
                else -> Transition.Retry
            }
        }
    }
    
    object FinishStep : WizardStep {
        override suspend fun onEntry(ctx: WizardContext) {
            val name: String? = ctx.getState<NameStep>()
            val age: Int? = ctx.getState<AgeStep>()
            
            // Сохранить в базу данных, отправить подтверждение и т.д.
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

### Продвинутые возможности

#### Условные переходы

Используйте `Transition.JumpTo` для условных потоков:

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

#### Шаги без состояния

Шаги не обязаны сохранять состояние. Просто верните `null` из `store()` (или оставьте как есть):

```kotlin
object ConfirmationStep : WizardStep {
    override suspend fun store(ctx: WizardContext): Any? = null
    // ... остальная реализация
}
```

#### Кастомные менеджеры состояния

Реализуйте `WizardStateManager<T>` для кастомного хранения (база данных, Redis и т.д.):

```kotlin
class DatabaseStateManager : WizardStateManager<String> {
    override suspend fun get(
        key: KClass<out WizardStep>,
        reference: UserChatReference
    ): String? {
        // Загрузить из базы данных
        return database.getWizardState(reference.userId, key.qualifiedName)
    }
    
    override suspend fun set(
        key: KClass<out WizardStep>,
        reference: UserChatReference,
        value: String
    ) {
        // Сохранить в базу данных
        database.saveWizardState(reference.userId, key.qualifiedName, value)
    }
    
    override suspend fun del(
        key: KClass<out WizardStep>,
        reference: UserChatReference
    ) {
        // Удалить из базы данных
        database.deleteWizardState(reference.userId, key.qualifiedName)
    }
}
```

---

### Как это работает внутри

#### Генерация кода

KSP генерирует:

1. **WizardActivity**: Конкретная реализация, расширяющая `WizardActivity` с захардкоженными шагами
2. **Start Activity**: Обрабатывает команду-триггер и запускает волшебника
3. **Input Activity**: Обрабатывает пользовательский ввод во время потока волшебника
4. **State Accessors**: Тип-безопасные функции расширения для доступа к состоянию

#### Поток

1. Пользователь отправляет `/register` → вызывается Start Activity
2. Start Activity создает `WizardContext` и вызывает `wizardActivity.start(ctx)`
3. `start()` входит на начальный шаг и устанавливает `inputListener` для отслеживания текущего шага
4. Пользователь отправляет сообщение → вызывается Input Activity
5. Input Activity вызывает `wizardActivity.handleInput(ctx)`
6. `handleInput()` проверяет ввод, сохраняет состояние и переходит к следующему шагу
7. Процесс повторяется до возврата `Transition.Finish`

#### Сохранение состояния

- Состояние сохраняется после успешной валидации (перед переходом)
- Возвращаемое значение `store()` каждого шага сохраняется с использованием соответствующего `WizardStateManager`
- Состояние ограничено по пользователю и чату (`UserChatReference`)

---

### Рекомендации

#### 1. Всегда предоставляйте понятные подсказки

```kotlin
override suspend fun onEntry(ctx: WizardContext) {
    message { 
        "Please enter your email address:\n" +
        "(Format: user@example.com)" 
    }.send(ctx.user, ctx.bot)
}
```

#### 2. Обрабатывайте ошибки валидации корректно

```kotlin
override suspend fun onRetry(ctx: WizardContext) {
    message { 
        "Invalid email format. Please try again.\n" +
        "Example: user@example.com" 
    }.send(ctx.user, ctx.bot)
}
```

#### 3. Используйте тип-безопасный доступ к состоянию

Предпочитайте сгенерированные тип-безопасные методы:

```kotlin
// ✅ Хорошо - тип-безопасный
val name: String? = ctx.getState<NameStep>()

// ❌ Избегайте - теряется тип-безопасность
val name = ctx.getState(NameStep::class) as? String
```

#### 4. Делайте шаги сфокусированными

Каждый шаг должен иметь единственную ответственность:

```kotlin
// ✅ Хорошо - сфокусированный шаг
object EmailStep : WizardStep {
    // Только обрабатывает сбор email
}

// ❌ Избегайте - слишком много логики
object PersonalInfoStep : WizardStep {
    // Обрабатывает имя, email, телефон, адрес...
}
```

#### 5. Используйте осмысленные имена шагов

```kotlin
// ✅ Хорошо
object EmailVerificationStep : WizardStep

// ❌ Избегайте
object Step2 : WizardStep
```

#### 6. Очищайте состояние при необходимости

Если нужно очистить состояние вручную:

```kotlin
object CancelStep : WizardStep {
    override suspend fun onEntry(ctx: WizardContext) {
        // Очистить все состояние волшебника
        ctx.delState<NameStep>()
        ctx.delState<AgeStep>()
        
        message { "Registration cancelled." }.send(ctx.user, ctx.bot)
    }
}
```

---

### Резюме

Система Wizard предоставляет:
- ✅ **Тип-безопасное** управление состоянием с проверкой на этапе компиляции
- ✅ **Декларативное** определение шагов как вложенных классов
- ✅ **Гибкие** переходы с условной логикой
- ✅ **Автоматическую** генерацию кода через KSP
- ✅ **Интеграцию** с существующей системой Activity
- ✅ **Подключаемые** бэкенды хранения состояния

Начните создавать волшебников, аннотируя класс с помощью `@WizardHandler` и определяя шаги как вложенные объекты `WizardStep`!
если у вас есть вопросы, свяжитесь с нами в чате, мы будем рады помочь :)
---