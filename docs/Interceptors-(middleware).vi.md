---
---
title: Interceptors (Middleware)
---

### Interceptors: Cross-Cutting Logic for Your Bot

When building a Telegram bot, you often repeat setup, checks, or cleanup across handlers. Interceptors let you plug in shared logic around handlers, keeping handlers focused and maintainable.

Here’s how interceptors work in *telegram-bot* and how to use them.

### What Are Interceptors? (Simple Explanation)

Interceptors are functions that run at specific points in the update processing pipeline. They let you:
- Inspect and modify the processing context
- Add cross-cutting logic (logging, auth, metrics)
- Stop processing early if needed
- Clean up resources after processing

Think of interceptors as checkpoints that every update passes through before, during, and after handler execution.


### The Processing Pipeline

The bot processes updates through a pipeline with seven phases:

| Phase | When It Runs | What You Can Use It For |
|-------|--------------|-------------------------|
| **Setup** | As soon as the update arrives, before any processing | ✔ Global rate limiting<br>✔ Filter out spam or malformed updates<br>✔ Initial logging<br>✔ Setup shared context |
| **Parsing** | After setup, extracts command and parameters | ✔ Custom command parsing<br>✔ Enrich context with parsed data<br>✔ Validate update structure |
| **Match** | Finds the appropriate handler (Command/Input/Common) | ✔ Override handler selection<br>✔ Custom input handling logic<br>✔ Log matched handlers |
| **Validation** | After handler is found, before invocation | ✔ Handler-specific permissions<br>✔ Rate limiting per handler<br>✔ Guard checks<br>✔ Cancel processing if conditions aren't met |
| **PreInvoke** | Immediately before the handler runs | ✔ Last-minute checks<br>✔ Start timers/metrics<br>✔ Enrich context for handler<br>✔ Modify handler behavior |
| **Invoke** | The handler is executed here | ✔ Wrap handler execution<br>✔ Error handling<br>✔ Logging handler results |
| **PostInvoke** | After handler completes (success or failure) | ✔ Cleanup resources<br>✔ Log results<br>✔ Send fallback messages on errors<br>✔ Modify results before returning |


### Creating an Interceptor

An interceptor is a simple function that receives a `ProcessingContext`:

```kotlin
import eu.vendeli.tgbot.core.PipelineInterceptor
import eu.vendeli.tgbot.types.component.ProcessingContext

val myInterceptor: PipelineInterceptor = { context ->
    // Your logic here
    println("Processing update: ${context.update.updateId}")
}
```

Or using a lambda:

```kotlin
val loggingInterceptor = PipelineInterceptor { context ->
    val logger = context.bot.config.loggerFactory.get("MyInterceptor")
    logger.info("Processing update #${context.update.updateId}")
}
```


### Registering Interceptors

Register interceptors on the processing pipeline:

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

Example: a bot that requires authentication for certain commands, measures handler execution time, and logs all commands.

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

The `ProcessingContext` provides access to:

- **`update: ProcessedUpdate`** - The current update being processed
- **`bot: TelegramBot`** - The bot instance
- **`registry: ActivityRegistry`** - The activity registry
- **`parsedInput: String`** - The parsed command/input text
- **`parameters: Map<String, String>`** - Parsed command parameters
- **`activity: Activity?`** - The resolved handler (null until Match phase)
- **`shouldProceed: Boolean`** - Whether processing should continue
- **`additionalContext: AdditionalContext`** - Additional context data
- **`finish()`** - Stop processing early

#### Stopping Processing Early

Call `context.finish()` to stop processing:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.Validation) { context ->
    if (someCondition) {
        context.finish() // No further phases will execute
    }
}
```

#### Storing Custom Data

Use `additionalContext` to pass data between interceptors:

```kotlin
// In PreInvoke
context.additionalContext["userId"] = context.update.userOrNull?.id

// In PostInvoke
val userId = context.additionalContext["userId"] as? Long
```


### Multiple Interceptors

You can register multiple interceptors for the same phase. They execute in registration order:

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

If an interceptor calls `context.finish()`, subsequent interceptors in that phase are skipped, and later phases won't execute.


### Best Practices

#### 1. Use the Right Phase

- Setup: Global checks, filtering, initial setup
- Parsing: Custom parsing logic
- Match: Handler selection logic
- Validation: Permissions, rate limits, guards
- PreInvoke: Handler-specific preparation
- Invoke: Usually handled by the default interceptor
- PostInvoke: Cleanup, logging, error handling

#### 2. Keep Interceptors Focused

Each interceptor should do one thing:

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

Interceptors should not crash the bot:

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

If you open resources in `PreInvoke`, clean them up in `PostInvoke`:

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

Register interceptors in the order you want them to run:

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

Interceptors are ideal for:
- ✅ Authentication/authorization
- ✅ Logging
- ✅ Metrics/performance monitoring
- ✅ Rate limiting
- ✅ Error handling
- ✅ Request/response transformation

For handler-specific logic, keep it in the handler.


### Default Interceptors

The framework includes default interceptors for core functionality:

- **DefaultSetupInterceptor**: Global rate limiting
- **DefaultParsingInterceptor**: Command parsing
- **DefaultMatchInterceptor**: Handler matching (commands, inputs, common matchers)
- **DefaultValidationInterceptor**: Guard checks and per-handler rate limiting
- **DefaultInvokeInterceptor**: Handler execution and error handling

Your custom interceptors run alongside these defaults. You can add logic before or after the defaults, but you cannot remove the default interceptors.

---

### Advanced: Conditional Interceptors

You can make interceptors conditional:

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

Interceptors provide a clean way to add cross-cutting logic to your bot:

- ✅ **Seven phases** for different stages of processing
- ✅ **Simple API**: Just implement `PipelineInterceptor`
- ✅ **Flexible**: Register multiple interceptors per phase
- ✅ **Powerful**: Access to full processing context
- ✅ **Safe**: Can stop processing early with `context.finish()`

Use interceptors to keep your handlers focused on business logic while handling shared concerns like authentication, logging, and metrics in a centralized way.

---

### See also

* [Functional Handling DSL](Functional-handling-DSL.md) - Functional update processing
* [Guards](Guards.md) - Handler-level permission checks
---