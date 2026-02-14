---
---
title: FSM и Обработка Диалогов
---

Библиотека также поддерживает механизм FSM, который представляет собой механизм прогрессивной обработки пользовательского ввода с обработкой некорректного ввода.

> [!NOTE]
> TL;DR: Смотрите пример [тут](https://github.com/vendelieu/telegram-bot_template/tree/conversation).

### В теории

Представим ситуацию, когда вам нужно собрать опрос пользователя, вы можете запросить все данные человека за один шаг, но при некорректном вводе одного из параметров, это будет сложно и для пользователя, и для нас, и каждый шаг может отличаться в зависимости от определенных входных данных.

Теперь представим пошаговый ввод данных, где бот входит в режим диалога с пользователем.

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/2e84fa00-e59c-4352-8665-83be3b971e7b" alt="Схема процесса обработки" />
</p>

Зеленые стрелки указывают процесс перехода через шаги без ошибок, синие стрелки означают сохранение текущего состояния и ожидание повторного ввода (например, если пользователь указал, что ему -100 лет, нужно спросить возраст еще раз), а красные показывают выход из всего процесса из-за любой команды или любого другого значения отмены.

### На практике

Система Wizard обеспечивает многошаговые взаимодействия с пользователем в ботах Telegram. Она направляет пользователей через последовательность шагов, проверяет ввод, сохраняет состояние и переходит между шагами.

**Ключевые Преимущества:**
- **Type-safe**: Проверка типов на этапе компиляции для доступа к состоянию
- **Декларативный**: Определяйте шаги как вложенные классы/объекты
- **Гибкий**: Поддержка условных переходов, прыжков и повторных попыток
- **Сохраняющий состояние**: Автоматическое сохранение состояния с подключаемыми бэкендами хранения
- **Интегрированный**: Работает с существующей системой Activity

### Основные Концепции

#### WizardStep

`WizardStep` представляет собой отдельный шаг в потоке мастера. Каждый шаг должен реализовать:

- **`onEntry(ctx: WizardContext)`**: Вызывается, когда пользователь входит на этот шаг. Используйте это для запроса у пользователя.
- **`onRetry(ctx: WizardContext)`**: Вызывается при сбое проверки и необходимости повторной попытки. Используйте это для показа сообщений об ошибках.
- **`validate(ctx: WizardContext): Transition`**: Проверяет текущий ввод и возвращает `Transition`, указывающий, что происходит дальше.
- **`store(ctx: WizardContext): Any?`** (необязательно): Возвращает значение для сохранения для этого шага. Верните `null`, если шаг не сохраняет состояние.

```kotlin
object NameStep : WizardStep(isInitial = true) {
    override suspend fun onEntry(ctx: WizardContext) {
        message { "Как вас зовут?" }.send(ctx.user, ctx.bot)
    }
    
    override suspend fun onRetry(ctx: WizardContext) {
        message { "Имя не может быть пустым. Пожалуйста, попробуйте еще раз." }.send(ctx.user, ctx.bot)
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

`Transition` определяет, что происходит после проверки:

- **`Transition.Next`**: Перейти к следующему шагу в последовательности
- **`Transition.JumpTo(step: KClass<out WizardStep>)`**: Перейти к конкретному шагу
- **`Transition.Retry`**: Повторить текущий шаг (проверка не удалась)
- **`Transition.Finish`**: Завершить мастера

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

Плюс методы доступа к состоянию с проверкой типов (сгенерированы KSP).

---

### Определение Мастера

#### Базовая Структура

Мастер определяется как класс или объект, аннотированный `@WizardHandler`:

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

#### Параметры Аннотации

**`@WizardHandler`** принимает:
- **`trigger: Array<String>`**: Команды, которые запускают мастера (например, `["/start", "/survey"]`)
- **`scope: Array<UpdateType>`**: Типы обновлений для прослушивания (по умолчанию: `[UpdateType.MESSAGE]`)
- **`stateManagers: Array<KClass<out WizardStateManager<*>>>`**: Классы менеджеров состояния для хранения данных шагов

---

### Управление Состоянием

#### WizardStateManager

Состояние хранится с использованием реализаций `WizardStateManager<T>`. Каждый менеджер обрабатывает конкретный тип:

```kotlin
interface WizardStateManager<T : Any> {
    suspend fun get(key: KClass<out WizardStep>, reference: UserChatReference): T?
    suspend fun set(key: KClass<out WizardStep>, reference: UserChatReference, value: T)
    suspend fun del(key: KClass<out WizardStep>, reference: UserChatReference)
}
```

См. также: [MapStateManager<T>](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-state-manager/index.html), [MapStringStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-string-state-manager/index.html), [MapIntStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-int-state-manager/index.html), [MapLongStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-long-state-manager/index.html).

#### Автоматическое Сопоставление

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

#### Переопределение На Уровне Шага

Переопределите менеджер состояния для конкретного шага с помощью `@WizardHandler.StateManager`:

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

### Type-Safe Доступ к Состоянию

KSP генерирует type-safe функции-расширения для `WizardContext` для каждого шага, который сохраняет состояние.

#### Сгенерированные Функции

Для шага, который сохраняет `String`:

```kotlin
// Сгенерировано автоматически KSP
suspend inline fun <reified S : WizardStep> WizardContext.getState(): String?
suspend inline fun <reified S : WizardStep> WizardContext.setState(value: String)
suspend inline fun <reified S : WizardStep> WizardContext.delState()
```

#### Использование

```kotlin
object FinishStep : WizardStep {
    override suspend fun onEntry(ctx: WizardContext) {
        // Type-safe доступ - возвращает String? (nullable)
        val name: String? = ctx.getState<NameStep>()
        
        // Type-safe доступ - возвращает Int? (nullable)
        val age: Int? = ctx.getState<AgeStep>()
        
        val summary = buildString {
            appendLine("Имя: $name")
            appendLine("Возраст: $age")
        }
        
        message { summary }.send(ctx.user, ctx.bot)
    }
    
    override suspend fun onRetry(ctx: WizardContext) = Unit
    
    override suspend fun validate(ctx: WizardContext): Transition {
        return Transition.Finish
    }
}
```

#### Методы Fallback

Если type-safe методы недоступны, используйте методы fallback:

```kotlin
// Fallback - возвращает Any?
val name = ctx.getState(NameStep::class)

// Fallback - принимает Any?
ctx.setState(NameStep::class, "John")
ctx.delState(NameStep::class)
```

---

### Полный Пример

#### Мастер Регистрации Пользователя

```kotlin
@WizardHandler(
    trigger = ["/register"],
    stateManagers = [StringStateManager::class, IntStateManager::class]
)
object RegistrationWizard {
    object NameStep : WizardStep(isInitial = true) {
        override suspend fun onEntry(ctx: WizardContext) {
            message { "Как вас зовут?" }.send(ctx.user, ctx.bot)
        }
        
        override suspend fun onRetry(ctx: WizardContext) {
            message { "Пожалуйста, введите корректное имя." }.send(ctx.user, ctx.bot)
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
            message { "Сколько вам лет?" }.send(ctx.user, ctx.bot)
        }
        
        override suspend fun onRetry(ctx: WizardContext) {
            message { "Пожалуйста, введите корректный возраст (должно быть числом)." }.send(ctx.user, ctx.bot)
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
                "Извините, вам должно быть 18 лет или больше для регистрации." 
            }.send(ctx.user, ctx.bot)
        }
        
        override suspend fun onRetry(ctx: WizardContext) = Unit
        
        override suspend fun validate(ctx: WizardContext): Transition {
            return Transition.Finish
        }
    }
    
    object ConfirmationStep : WizardStep {
        override suspend fun onEntry(ctx: WizardContext) {
            // Type-safe доступ к состоянию
            val name: String? = ctx.getState<NameStep>()
            val age: Int? = ctx.getState<AgeStep>()
            
            val confirmation = buildString {
                appendLine("Пожалуйста, подтвердите вашу информацию:")
                appendLine("Имя: $name")
                appendLine("Возраст: $age")
                appendLine()
                appendLine("Ответьте 'да' для подтверждения или 'нет' для начала заново.")
            }
            
            message { confirmation }.send(ctx.user, ctx.bot)
        }
        
        override suspend fun onRetry(ctx: WizardContext) {
            message { "Пожалуйста, ответьте 'да' или 'нет'." }.send(ctx.user, ctx.bot)
        }
        
        override suspend fun validate(ctx: WizardContext): Transition {
            val response = ctx.update.text?.lowercase()?.trim()
            return when (response) {
                "да" -> Transition.Finish
                "нет" -> Transition.JumpTo(NameStep::class) // Начать заново
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
                "Регистрация завершена! Добро пожаловать, $name (возраст $age)." 
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

### Продвинутые Функции

#### Условные Переходы

Используйте `Transition.JumpTo` для условных потоков:

```kotlin
override suspend fun validate(ctx: WizardContext): Transition {
    val choice = ctx.update.text?.lowercase()
    return when (choice) {
        "премиум" -> Transition.JumpTo(PremiumStep::class)
        "базовый" -> Transition.JumpTo(BasicStep::class)
        else -> Transition.Retry
    }
}
```

#### Шаги Без Состояния

Шаги не обязаны сохранять состояние. Просто верните `null` из `store()` (или оставьте как есть):

```kotlin
object ConfirmationStep : WizardStep {
    override suspend fun store(ctx: WizardContext): Any? = null
    // ... остальная реализация
}
```

#### Кастомные Менеджеры Состояния

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

### Как Это Работает Внутри

#### Генерация Кода

KSP генерирует:

1. **WizardActivity**: Конкретная реализация, расширяющая `WizardActivity` с захардкоженными шагами
2. **Start Activity**: Обрабатывает команду-триггер и запускает мастера
3. **Input Activity**: Обрабатывает пользовательский ввод во время потока мастера
4. **State Accessors**: Type-safe функции-расширения для доступа к состоянию

#### Поток

1. Пользователь отправляет `/register` → Вызывается Start Activity
2. Start Activity создает `WizardContext` и вызывает `wizardActivity.start(ctx)`
3. `start()` входит в начальный шаг и устанавливает `inputListener` для отслеживания текущего шага
4. Пользователь отправляет сообщение → Вызывается Input Activity
5. Input Activity вызывает `wizardActivity.handleInput(ctx)`
6. `handleInput()` проверяет ввод, сохраняет состояние и переходит к следующему шагу
7. Процесс повторяется до тех пор, пока не будет возвращен `Transition.Finish`

#### Сохранение Состояния

- Состояние сохраняется после успешной проверки (перед переходом)
- Возвращаемое значение `store()` каждого шага сохраняется с использованием соответствующего `WizardStateManager`
- Состояние ограничено по пользователю и чату (`UserChatReference`)

---

### Best Practices

#### 1. Всегда Предоставляйте Ясные Подсказки

```kotlin
override suspend fun onEntry(ctx: WizardContext) {
    message { 
        "Пожалуйста, введите ваш адрес электронной почты:\n" +
        "(Формат: user@example.com)" 
    }.send(ctx.user, ctx.bot)
}
```

#### 2. Грациозно Обрабатывайте Ошибки Проверки

```kotlin
override suspend fun onRetry(ctx: WizardContext) {
    message { 
        "Некорректный формат электронной почты. Пожалуйста, попробуйте еще раз.\n" +
        "Пример: user@example.com" 
    }.send(ctx.user, ctx.bot)
}
```

#### 3. Используйте Type-Safe Доступ к Состоянию

Предпочитайте сгенерированные type-safe методы:

```kotlin
// ✅ Хорошо - type-safe
val name: String? = ctx.getState<NameStep>()

// ❌ Избегайте - теряется type safety
val name = ctx.getState(NameStep::class) as? String
```

#### 4. Держите Шаги Сосредоточенными

Каждый шаг должен иметь единственную ответственность:

```kotlin
// ✅ Хорошо - сосредоточенный шаг
object EmailStep : WizardStep {
    // Только обрабатывает сбор электронной почты
}

// ❌ Избегайте - слишком много логики
object PersonalInfoStep : WizardStep {
    // Обрабатывает имя, электронную почту, телефон, адрес...
}
```

#### 5. Используйте Значимые Имена Шагов

```kotlin
// ✅ Хорошо
object EmailVerificationStep : WizardStep

// ❌ Избегайте
object Step2 : WizardStep
```

#### 6. Очищайте Состояние При Необходимости

Если вам нужно вручную очистить состояние:

```kotlin
object CancelStep : WizardStep {
    override suspend fun onEntry(ctx: WizardContext) {
        // Очистить все состояние мастера
        ctx.delState<NameStep>()
        ctx.delState<AgeStep>()
        
        message { "Регистрация отменена." }.send(ctx.user, ctx.bot)
    }
}
```

---

### Summary

Система Wizard предоставляет:
- ✅ **Type-safe** управление состоянием с проверкой на этапе компиляции
- ✅ **Декларативное** определение шагов как вложенные классы
- ✅ **Гибкие** переходы с условной логикой
- ✅ **Автоматическую** генерацию кода через KSP
- ✅ **Интегрированную** с существующей системой Activity
- ✅ **Подключаемые** бэкенды хранения состояния

Начните создавать мастера, аннотируя класс с `@WizardHandler` и определяя ваши шаги как вложенные объекты `WizardStep`!