# Introduction
Guards are an essential feature for developers creating bots. These guards function as pre-execution checks that determine whether a particular command should be invoked. By implementing these checks, developers can enhance the functionality, security, and user experience of their bots.

# Purpose of Activity Guards
The primary purpose of activity guards is to ensure that only authorized users or specific conditions trigger a activity. 

This can prevent misuse, maintain the bot's integrity, and streamline interactions.

# Common Use Cases
1. Authentication and Authorization: Ensuring only certain users can access specific commands.
2. Pre-condition Checks: Verifying that certain conditions are met before executing a activity (e.g., ensuring a user is in a particular state or context).
3. Contextual Guards: Making decisions based on the current chat or user state.

# Implementation Strategies
Implementing Telegram Command Guards typically involves writing functions or methods that encapsulate the logic for each guard. Below are common strategies:

1. User Role Check:
   - Ensuring the user has the required role (e.g., admin, moderator) before executing the command.
      ```kotlin
       override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // Check if the user is an admin in the given chat
       }
      ```
   
2. State Verification:
   - Checking the user's state before allowing command execution.
     ```kotlin
     override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        return bot.userData[user.id, "data"] == requiredState
     }
     ```
   
3. Custom Guards:
   - Creating custom logic based on specific requirements.
     ```kotlin
     override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // Custom logic to determine if the command should be executed
     }
     ```
   
# Integrating Guards with Activities
To integrate these guards with your bot commands, you can create a guard that checks these conditions before the command handler is invoked.

## Implementing Example

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

# Best Practices

- Modularity: Keep guard logic modular and separate from activities.
- Reusability: Write reusable guard functions that can be easily applied across different commands/inputs.
- Efficiency: Optimize guard checks to minimize performance overhead.
- User Feedback: Provide clear feedback to users when a command is blocked by a guard.

# Conclusion

Activity Guards are a powerful tool for managing bot command/input execution. 

By implementing robust guard mechanisms, developers can ensure their bots operate securely and efficiently, providing a better user experience.

# See also

* [Activities and Proccessors](Activites-and-Processors)
* [Update parsing](Update-parsing)
* [Actions](Actions)
* [Activity invocation](Activity-invocation)
