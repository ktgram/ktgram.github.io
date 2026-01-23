---
title: Aide
---

############################################################################################################################# Aide Compiler Plugin [🔬]

_feature disabled by default, to use it enable in plugin parameters_

############################################################################################################################# Configuration  
Configure Aide in your `build.gradle.kts`:

```kotlin
ktGram {
    // Enable AIDE compiler extensions (Automatic .send() chaining)
    aideEnabled = true
    
}
```

---

############################################################################################################################# Usage Example

############################################################################################################################### Simple case
```kotlin
@CommandHandler
suspend fun handler(user: User, bot: TelegramBot) {
    // With aideAutoSend=true
    message {
        "Auto-sent message"
    } // ← Compiler adds .send(user, bot)
    
    // Explicit control
    message { 
        "Manual send"
    }.send(user, bot) // ← No auto-add when present
}
```

> [!CAUTION]
> Be aware that even if you do not use an explicit `send`, you still need to have `suspend` function keyword, otherwise you will get an error.

############################################################################################################################### Complex Case (Manual Handling Required)

```kotlin
@InputHandler
fun handleInput(user: User, bot: TelegramBot) {
    // Requires manual .send()
    val savedAction = message {
        "Stored action"
    }
    
    // Valid usage with explicit send
    savedAction.send(user, bot)
}
```

################################################################################################################################ Validation Rules

* Auto-Send Applies When:

    * Action is directly returned from handler
    * No intermediate variable assignment
    * No existing `.send()` call

---

############################################################################################################################# Feature Behavior

############################################################################################################################## When `aideEnabled=true`

```mermaid
graph TD
    A[Detect Action] --> B{Simple Call?}
    B -->|Yes| C{Has Send?}
    B -->|No| D[No send]
    C -->|No| E[Add Send]
    C -->|Yes| F[Keep]
    D --> G[Skip]
```

############################################################################################################################## Requirements

- Handler must declare parameters:
  - `User` for general actions (simple action require just `TelegramBot`)
  - `TelegramBot` for all actions
- Annotated with `@CommandHandler`, `@InputHandler`, etc (any supported annotation).

