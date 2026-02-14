---
---
title: Перехватчики (Middleware)
---

### Перехватчики: сквозная логика для вашего бота

При создании Telegram-бота вы часто повторяете настройку, проверки или очистку в обработчиках. Перехватчики позволяют подключать общую логику вокруг обработчиков, сохраняя их сфокусированными и поддерживаемыми.

Вот как работают перехватчики в *telegram-bot* и как их использовать.

### Что такое Перехватчики? (Простое объяснение)

Перехватчики — это функции, которые выполняются на определенных этапах конвейера обработки обновлений. Они позволяют вам:
- Инспектировать и модифицировать контекст обработки
- Добавлять сквозную логику (логирование, аутентификация, метрики)
- Прерывать обработку при необходимости
- Очищать ресурсы после обработки

Представьте перехватчики как контрольные точки, через которые проходит каждое обновление до, во время и после выполнения обработчика.


### Конвейер обработки

Бот обрабатывает обновления через конвейер с семью этапами:

| Этап | Когда выполняется | Для чего можно использовать |
|-------|--------------|-------------------------|
| **Setup** | Сразу после поступления обновления, до начала обработки | ✔ Глобальное ограничение частоты<br>✔ Фильтрация спама или некорректных обновлений<br>✔ Начальное логирование<br>✔ Настройка общего контекста |
| **Parsing** | После Setup, извлекает команду и параметры | ✔ Пользовательский разбор команд<br>✔ Обогащение контекста распарсенными данными<br>✔ Валидация структуры обновления |
| **Match** | Находит подходящий обработчик (Command/Input/Common) | ✔ Переопределение выбора обработчика<br>✔ Пользовательская логика обработки ввода<br>✔ Логирование найденных обработчиков |
| **Validation** | После нахождения обработчика, перед вызовом | ✔ Права конкретного обработчика<br>✔ Ограничение частоты для каждого обработчика<br>✔ Проверки<br>✔ Отмена обработки если условия не выполнены |
| **PreInvoke** | Немедленно перед запуском обработчика | ✔ Последние проверки<br>✔ Запуск таймеров/метрик<br>✔ Обогащение контекста для обработчика<br>✔ Модификация поведения обработчика |
| **Invoke** | Здесь выполняется обработчик | ✔ Обертка выполнения обработчика<br>✔ Обработка ошибок<br>✔ Логирование результатов обработчика |
| **PostInvoke** | После завершения обработчика (успех или неудача) | ✔ Очистка ресурсов<br>✔ Логирование результатов<br>✔ Отправка сообщений-заглушек при ошибках<br>✔ Модификация результатов перед возвратом |


### Создание перехватчика

Перехватчик — это простая функция, которая получает `ProcessingContext`:

```kotlin
import eu.vendeli.tgbot.core.PipelineInterceptor
import eu.vendeli.tgbot.types.component.ProcessingContext

val myInterceptor: PipelineInterceptor = { context ->
    // Ваша логика здесь
    println("Обработка обновления: ${context.update.updateId}")
}
```

Или через лямбду:

```kotlin
val loggingInterceptor = PipelineInterceptor { context ->
    val logger = context.bot.config.loggerFactory.get("MyInterceptor")
    logger.info("Обработка обновления #${context.update.updateId}")
}
```


### Регистрация перехватчиков

Регистрируйте перехватчики в конвейере обработки:

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

    // Регистрация перехватчика для этапа Setup
    bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
        // Проверка забанен ли пользователь
        val user = context.update.userOrNull
        if (user != null && isBanned(user.id)) {
            context.finish() // Прерываем обработку
            return@intercept
        }
    }

    // Регистрация перехватчика для этапа PreInvoke
    bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
        val startTime = System.currentTimeMillis()
        // сохранить время начала
    }

    // Регистрация перехватчика для этапа PostInvoke
    bot.update.pipeline.intercept(ProcessingPipePhase.PostInvoke) { context ->
        val startTime = // получить время начала
        if (startTime != null) {
            val duration = System.currentTimeMillis() - startTime
            println("Обработчик занял ${duration}ms")
        }
    }

    bot.handleUpdates()
}
```

### Реальный пример: Аутентификация и метрики

Пример: бот, требующий аутентификацию для определенных команд, измеряющий время выполнения обработчиков и логирующий все команды.

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

    // Этап Setup: Проверка аутентификации пользователя
    bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
        val user = context.update.userOrNull ?: return@intercept

        if (!isAuthenticated(user.id)) {
            message { "Пожалуйста, сначала пройдите аутентификацию через /login" }
                .send(user, context.bot)
            context.finish()
        }
    }

    // Этап PreInvoke: Запуск таймера и проверка прав
    bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
        val activity = context.activity ?: return@intercept
        val user = context.update.userOrNull ?: return@intercept

        // Проверка прав пользователя для этого конкретного обработчика
        if (!hasPermission(user.id, activity)) {
            message { "У вас нет прав для использования этой команды." }
                .send(user, context.bot)
            context.finish()
            return@intercept
        }

        // Запуск таймера
        // сохранить время начала
    }

    // Этап PostInvoke: Логирование и очистка
    bot.update.pipeline.intercept(ProcessingPipePhase.PostInvoke) { context ->
        val activity = context.activity ?: return@intercept
        val startTime = // получить время начала

        if (startTime != null) {
            val duration = System.currentTimeMillis() - startTime
            val logger = context.bot.config.loggerFactory.get("Metrics")
            logger.info(
                "Обработчик ${activity::class.simpleName} занял ${duration}ms " +
                "для пользователя ${context.update.userOrNull?.id}"
            )
        }
    }

    bot.handleUpdates()
}
```


### ProcessingContext

`ProcessingContext` предоставляет доступ к:

- **`update: ProcessedUpdate`** - Текущее обновление, которое обрабатывается
- **`bot: TelegramBot`** - Экземпляр бота
- **`registry: ActivityRegistry`** - Реестр активностей
- **`parsedInput: String`** - Распарсенный текст команды/ввода
- **`parameters: Map<String, String>`** - Параметры команды
- **`activity: Activity?`** - Найденный обработчик (null до этапа Match)
- **`shouldProceed: Boolean`** - Должна ли продолжаться обработка
- **`additionalContext: AdditionalContext`** - Дополнительные данные контекста
- **`finish()`** - Прервать обработку раньше

#### Прерывание обработки раньше

Вызовите `context.finish()` чтобы прервать обработку:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.Validation) { context ->
    if (someCondition) {
        context.finish() // Дальнейшие этапы выполняться не будут
    }
}
```

#### Хранение пользовательских данных

Используйте `additionalContext` для передачи данных между перехватчиками:

```kotlin
// В PreInvoke
context.additionalContext["userId"] = context.update.userOrNull?.id

// В PostInvoke
val userId = context.additionalContext["userId"] as? Long
```


### Несколько перехватчиков

Вы можете зарегистрировать несколько перехватчиков для одного этапа. Они выполняются в порядке регистрации:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    println("Первый перехватчик")
}

bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    println("Второй перехватчик")
}

// Когда обновление обрабатывается:
// Вывод: "Первый перехватчик"
// Вывод: "Второй перехватчик"
```

Если перехватчик вызывает `context.finish()`, последующие перехватчики на этом этапе пропускаются, и дальнейшие этапы не выполняются.


### Best Practices

#### 1. Используйте правильный этап

- Setup: Глобальные проверки, фильтрация, начальная настройка
- Parsing: Пользовательская логика разбора
- Match: Логика выбора обработчика
- Validation: Права, ограничение частоты, проверки
- PreInvoke: Подготовка к запуску обработчика
- Invoke: Обычно обрабатывается перехватчиком по умолчанию
- PostInvoke: Очистка, логирование, обработка ошибок

#### 2. Держите перехватчики сфокусированными

Каждый перехватчик должен делать одну вещь:

```kotlin
// ✅ Хорошо - сфокусированный перехватчик
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    if (isBanned(context.update.userOrNull?.id)) {
        context.finish()
    }
}

// ❌ Избегайте - слишком много дел
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    // Аутентификация
    // Логирование
    // Метрики
    // Ограничение частоты
    // ... слишком много!
}
```

#### 3. Грациозно обрабатывайте ошибки

Перехватчики не должны крашить бота:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
    try {
        // Ваша логика
    } catch (e: Exception) {
        val logger = context.bot.config.loggerFactory.get("Interceptor")
        logger.error("Ошибка перехватчика", e)
        // Не вызывайте context.finish() если не хотите прервать обработку
    }
}
```

#### 4. Очищайте ресурсы

Если вы открываете ресурсы в `PreInvoke`, очищайте их в `PostInvoke`:

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

#### 5. Порядок имеет значение

Регистрируйте перехватчики в том порядке, в котором хотите чтобы они выполнялись:

```kotlin
// Более общие проверки сначала
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) {
    // Глобальная проверка бана
}

// Более специфичные проверки позже
bot.update.pipeline.intercept(ProcessingPipePhase.Validation) {
    // Проверка прав конкретного обработчика
}
```

#### 6. Используйте перехватчики для сквозных задач

Перехватчики идеальны для:
- ✅ Аутентификации/авторизации
- ✅ Логирования
- ✅ Метрик/мониторинга производительности
- ✅ Ограничения частоты
- ✅ Обработки ошибок
- ✅ Трансформации запросов/ответов

Для логики конкретного обработчика оставьте это в обработчике.


### Перехватчики по умолчанию

Фреймворк включает перехватчики по умолчанию для основной функциональности:

- **DefaultSetupInterceptor**: Глобальное ограничение частоты
- **DefaultParsingInterceptor**: Разбор команд
- **DefaultMatchInterceptor**: Сопоставление обработчиков (команды, ввод, общие матчеры)
- **DefaultValidationInterceptor**: Проверки и ограничение частоты для каждого обработчика
- **DefaultInvokeInterceptor**: Выполнение обработчика и обработка ошибок

Ваши пользовательские перехватчики работают вместе с этими перехватчиками по умолчанию. Вы можете добавить логику до или после перехватчиков по умолчанию, но вы не можете удалить перехватчики по умолчанию.

---

### Продвинутый: Условные перехватчики

Вы можете делать перехватчики условными:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
    val activity = context.activity ?: return@intercept

    // Применять только к конкретным обработчикам
    if (activity::class.simpleName?.contains("Admin") == true) {
        // Логика для админов
        checkAdminPermissions(context)
    }
}
```


### Итог

Перехватчики предоставляют чистый способ добавления сквозной логики в ваш бот:

- ✅ **Семь этапов** для разных стадий обработки
- ✅ **Простой API**: Просто реализуйте `PipelineInterceptor`
- ✅ **Гибкие**: Регистрируйте несколько перехватчиков на этап
- ✅ **Мощные**: Доступ к полному контексту обработки
- ✅ **Безопасные**: Можно прервать обработку раньше с `context.finish()`

Используйте перехватчики чтобы держать ваши обработчики сфокусированными на бизнес-логике, в то время как сквозные задачи, такие как аутентификация, логирование и метрики, обрабатываются централизованно.

---

### См. также

* [Functional Handling DSL](Functional-handling-DSL.md) - Функциональная обработка обновлений
* [Guards](Guards.md) - Проверки прав на уровне обработчика
---