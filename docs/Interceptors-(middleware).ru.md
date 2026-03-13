---
---
title: Перехватчики (Middleware)
---

### Перехватчики: сквозная логика для вашего бота

При создании Telegram-бота вы часто повторяете настройку, проверки или очистку между обработчиками. Перехватчики позволяют подключить общую логику вокруг обработчиков, сохраняя их сфокусированными и поддерживаемыми.

Вот как работают перехватчики в *telegram-bot* и как их использовать.

### Что такое перехватчики? (Простое объяснение)

Перехватчики — это функции, которые запускаются в определенные моменты конвейера обработки обновлений. Они позволяют вам:
- Инспектировать и модифицировать контекст обработки
- Добавлять сквозную логику (логирование, аутентификация, метрики)
- Останавливать обработку при необходимости
- Очищать ресурсы после обработки

Представьте перехватчики как контрольные точки, через которые проходит каждое обновление до, во время и после выполнения обработчика.


### Конвейер обработки

Бот обрабатывает обновления через конвейер с семью фазами:

| Фаза | Когда запускается | Для чего можно использовать |
|-------|--------------|-------------------------|
| **Setup** | Сразу после получения обновления, до начала обработки | ✔ Глобальное ограничение частоты<br>✔ Фильтрация спама или некорректных обновлений<br>✔ Начальное логирование<br>✔ Настройка общего контекста |
| **Parsing** | После Setup, извлекает команду и параметры | ✔ Пользовательский парсинг команд<br>✔ Обогащение контекста распарсенными данными<br>✔ Валидация структуры обновления |
| **Match** | Находит подходящий обработчик (Command/Input/Common) | ✔ Переопределение выбора обработчика<br>✔ Пользовательская логика обработки ввода<br>✔ Логирование найденных обработчиков |
| **Validation** | После нахождения обработчика, перед вызовом | ✔ Права конкретного обработчика<br>✔ Ограничение частоты на уровне обработчика<br>✔ Проверки guard<br>✔ Отмена обработки если условия не соблюдены |
| **PreInvoke** | Немедленно перед запуском обработчика | ✔ Последние проверки<br>✔ Запуск таймеров/метрик<br>✔ Обогащение контекста для обработчика<br>✔ Модификация поведения обработчика |
| **Invoke** | Здесь выполняется обработчик | ✔ Обертка выполнения обработчика<br>✔ Обработка ошибок<br>✔ Логирование результатов обработчика |
| **PostInvoke** | После завершения обработчика (успех или ошибка) | ✔ Очистка ресурсов<br>✔ Логирование результатов<br>✔ Отправка сообщений-заглушек при ошибках<br>✔ Модификация результатов перед возвратом |


### Создание перехватчика

Перехватчик — это простая функция, которая получает `ProcessingContext`:

```kotlin
import eu.vendeli.tgbot.core.PipelineInterceptor
import eu.vendeli.tgbot.types.component.ProcessingContext

val myInterceptor: PipelineInterceptor = { context ->
    // Ваша логика здесь
    println("Processing update: ${context.update.updateId}")
}
```

Или с использованием лямбды:

```kotlin
val loggingInterceptor = PipelineInterceptor { context ->
    val logger = context.bot.config.loggerFactory.get("MyInterceptor")
    logger.info("Processing update #${context.update.updateId}")
}
```


### Регистрация перехватчиков

Регистрируйте перехватчики в конвейере обработки:

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

    // Регистрация перехватчика для фазы Setup
    bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
        // Проверка забаненного пользователя
        val user = context.update.userOrNull
        if (user != null && isBanned(user.id)) {
            context.finish() // Остановка обработки
            return@intercept
        }
    }

    // Регистрация перехватчика для фазы PreInvoke
    bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
        val startTime = System.currentTimeMillis()
        // сохранение времени начала
    }

    // Регистрация перехватчика для фазы PostInvoke
    bot.update.pipeline.intercept(ProcessingPipePhase.PostInvoke) { context ->
        val startTime = // получение времени начала
        if (startTime != null) {
            val duration = System.currentTimeMillis() - startTime
            println("Handler took ${duration}ms")
        }
    }

    bot.handleUpdates()
}
```

### Реальный пример: Аутентификация и метрики

Пример: бот, который требует аутентификацию для определенных команд, измеряет время выполнения обработчиков и логирует все команды.

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

    // Фаза Setup: Проверка аутентификации пользователя
    bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
        val user = context.update.userOrNull ?: return@intercept

        if (!isAuthenticated(user.id)) {
            message { "Please authenticate first using /login" }
                .send(user, context.bot)
            context.finish()
        }
    }

    // Фаза PreInvoke: Запуск таймера и проверка прав
    bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
        val activity = context.activity ?: return@intercept
        val user = context.update.userOrNull ?: return@intercept

        // Проверка прав пользователя для этого конкретного обработчика
        if (!hasPermission(user.id, activity)) {
            message { "You don't have permission to use this command." }
                .send(user, context.bot)
            context.finish()
            return@intercept
        }

        // Запуск таймера
        // сохранение времени начала
    }

    // Фаза PostInvoke: Логирование и очистка
    bot.update.pipeline.intercept(ProcessingPipePhase.PostInvoke) { context ->
        val activity = context.activity ?: return@intercept
        val startTime = // получение времени начала

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

`ProcessingContext` предоставляет доступ к:

- **`update: ProcessedUpdate`** - Текущее обновление в процессе обработки
- **`bot: TelegramBot`** - Экземпляр бота
- **`registry: ActivityRegistry`** - Реестр активностей
- **`parsedInput: String`** - Распарсенный текст команды/ввода
- **`parameters: Map<String, String>`** - Параметры команды
- **`activity: Activity?`** - Найденный обработчик (null до фазы Match)
- **`shouldProceed: Boolean`** - Следует ли продолжать обработку
- **`additionalContext: AdditionalContext`** - Дополнительные данные контекста
- **`finish()`** - Остановка обработки раньше времени

#### Остановка обработки раньше времени

Вызовите `context.finish()` для остановки обработки:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.Validation) { context ->
    if (someCondition) {
        context.finish() // Дальнейшие фазы выполняться не будут
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

Вы можете зарегистрировать несколько перехватчиков для одной фазы. Они выполняются в порядке регистрации:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    println("First interceptor")
}

bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    println("Second interceptor")
}

// При обработке обновления:
// Вывод: "First interceptor"
// Вывод: "Second interceptor"
```

Если перехватчик вызывает `context.finish()`, последующие перехватчики в этой фазе пропускаются, и последующие фазы не выполняются.


### Лучшие практики

#### 1. Используйте правильную фазу

- Setup: Глобальные проверки, фильтрация, начальная настройка
- Parsing: Пользовательская логика парсинга
- Match: Логика выбора обработчика
- Validation: Права доступа, ограничение частоты, guard-проверки
- PreInvoke: Подготовка конкретного обработчика
- Invoke: Обычно обрабатывается перехватчиком по умолчанию
- PostInvoke: Очистка, логирование, обработка ошибок

#### 2. Делайте перехватчики сфокусированными

Каждый перехватчик должен делать одно действие:

```kotlin
// ✅ Хорошо - сфокусированный перехватчик
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    if (isBanned(context.update.userOrNull?.id)) {
        context.finish()
    }
}

// ❌ Избегайте - слишком много действий
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    // Аутентификация
    // Логирование
    // Метрики
    // Ограничение частоты
    // ... слишком много!
}
```

#### 3. Грамотно обрабатывайте ошибки

Перехватчики не должны крашить бота:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
    try {
        // Ваша логика
    } catch (e: Exception) {
        val logger = context.bot.config.loggerFactory.get("Interceptor")
        logger.error("Interceptor error", e)
        // Не вызывайте context.finish() если не хотите останавливать обработку
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

Регистрируйте перехватчики в том порядке, в котором хотите их запускать:

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
- ✅ Аутентификация/авторизация
- ✅ Логирование
- ✅ Мониторинг производительности
- ✅ Ограничение частоты
- ✅ Обработка ошибок
- ✅ Трансформация запросов/ответов

Для логики конкретного обработчика оставляйте в самом обработчике.


### Перехватчики по умолчанию

Фреймворк включает перехватчики по умолчанию для основной функциональности:

- **DefaultSetupInterceptor**: Глобальное ограничение частоты
- **DefaultParsingInterceptor**: Парсинг команд
- **DefaultMatchInterceptor**: Сопоставление обработчиков (команды, ввод, общие матчеры)
- **DefaultValidationInterceptor**: Guard-проверки и ограничение частоты на уровне обработчика
- **DefaultInvokeInterceptor**: Выполнение обработчика и обработка ошибок

Ваши пользовательские перехватчики работают вместе с этими перехватчиками по умолчанию. Вы можете добавить логику до или после перехватчиков по умолчанию, но вы не можете удалить перехватчики по умолчанию.

---

### Продвинутый: условные перехватчики

Вы можете делать перехватчики условными:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
    val activity = context.activity ?: return@intercept

    // Применять только к конкретным обработчикам
    if (activity::class.simpleName?.contains("Admin") == true) {
        // Логика для админ-обработчиков
        checkAdminPermissions(context)
    }
}
```


### Итог

Перехватчики предоставляют чистый способ добавить сквозную логику в ваш бот:

- ✅ **Семь фаз** для разных этапов обработки
- ✅ **Простой API**: Просто реализуйте `PipelineInterceptor`
- ✅ **Гибкие**: Регистрируйте несколько перехватчиков на фазу
- ✅ **Мощные**: Доступ ко всему контексту обработки
- ✅ **Безопасные**: Можно останавливать обработку раньше времени с `context.finish()`

Используйте перехватчики чтобы сохранять обработчики сфокусированными на бизнес-логике, пока сквозные задачи, такие как аутентификация, логирование и метрики, обрабатываются централизованно.

---

### См. также

* [Функциональный DSL обработки](Functional-handling-DSL.md) - Функциональная обработка обновлений
* [Guards](Guards.md) - Проверки прав доступа на уровне обработчика
---