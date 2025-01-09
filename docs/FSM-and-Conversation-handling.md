---
title: Fsm-And-Conversation-Handling
---

The library also supports the FSM mechanism, which is a mechanism for progressive processing of user input with incorrect input handling.

# In theory

Let's imagine a situation where you need to collect a user survey, you can ask for all the data of a person at one step, but with incorrect input of one of the parameters, it will be difficult both for the user and for us, and each step may have a difference depending on certain input data.

Now let's imagine step-by-step input of data, where the bot enters dialogue mode with the user.

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/2e84fa00-e59c-4352-8665-83be3b971e7b" alt="Handling process diagram" />
</p>

Green arrows indicate the process of transitioning through steps without errors, blue arrows mean saving the current state and waiting for re-input (for example, if the user indicated that he is -100 years old, it should ask for age again), and red ones show exit from the entire process due to any command or any other meaning cancellation.

# In practice

Such a mechanism can be implemented in the library through a simple class that implements a certain interface and marked with a specific annotation `@InputChain`.


```kotlin
@InputChain
object ConversationChain {
    object Name : BaseStatefulLink() {
        override val breakCondition = BreakCondition { _, update, _ -> update.text.isBlank() }
        override suspend fun breakAction(user: User, update: ProcessedUpdate, bot: TelegramBot) {
            message {
                "Please say your name, because that's what well-mannered people do :)"
            }.send(user, bot)
        }

        override suspend fun action(user: User, update: ProcessedUpdate, bot: TelegramBot): String {
            message { "Oh, ${update.text}, hey there" }.send(user, bot)
            message { "How old are you?" }.send(user, bot)

            return update.text
        }
    }

    object Age : BaseStatefulLink() {
        override val breakCondition = BreakCondition { _, update, _ -> update.text.toIntOrNull() == null }
        override suspend fun breakAction(user: User, update: ProcessedUpdate, bot: TelegramBot) {
            message {
                "Perhaps it's not nice to ask your age, but maybe you can tell me anyway."
            }.send(user, bot)
        }

        override suspend fun action(user: User, update: ProcessedUpdate, bot: TelegramBot): String {
            message { "Pleased to meet you!" }.send(user, bot)

            return update.text
        }
    }

    object Final : ChainLink() {
        override suspend fun action(user: User, update: ProcessedUpdate, bot: TelegramBot) {
            val state = user.getAllState(ConversationChain)

            message {
                "I'm not good at remembering, but I remembered you! " +
                        "You're ${state.Name} and you're ${state.Age} years old."
            }.send(user, bot)
        }
    }
}
```

And after we described the mechanism to start the processing, we just need to call the method and specify the initial step, then the library itself will follow the sequence.

```kotlin
bot.inputListener.setChain(user, Conversation.Name)
```

# Links details

All links have the same foundation and implementing [`Link<T>`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.internal.chain/-link/index.html) interface, which have such properties:

Key Properties:

* afterAction: An optional action to execute after the main action.
* beforeAction: An optional action to execute before the main action.
* breakCondition: A condition that, if met, will trigger a break in the chain.
* chainingStrategy: Defines how the next link is determined.
* retryAfterBreak: Indicates whether to retry the action after a break condition is met.

Key Functions:

* action: This is an abstract function that must be implemented to define the primary behavior of the link.
* breakAction: An optional function that can be overridden to define behavior when a break condition is met.


There are two types of links they are differentiated by state, stateless and stateful:

## Stateless Links

Stateless links are represented by the abstract class [`ChainLink`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.internal/-chain-link/index.html). This class serves as the foundation for creating links that do not maintain any state information between user interactions.

## Stateful Links

The `InputChain` mechanism, particularly when employing `StatefulLink` and its various implementations, offers a sophisticated approach to managing conversational states within applications, such as chatbots. This system automatically stores the result of the `action` function associated with each state, linking it directly to the user involved in the interaction (or other selected key).

### Key Features

#### Automatic State Storage

- By default, the outcome of the `action` function executed within a `StatefulLink` is automatically stored. This storage is linked to the user, ensuring personalized interactions based on past exchanges.
  
#### Customizable Keys

- Developers have the flexibility to override the base implementation to specify custom keys for state association. This could range from identifiers unique to a chat session to any other relevant attribute that suits the application's requirements.

#### Data Typing and Key Utilization

- The foundational implementation, `BaseStatefulLink`, categorizes data as `String` types, utilizing `User.id` as the primary key for state association. This approach streamlines data management and retrieval processes.

#### Unified Access to States

- Should all `Link` objects within the InputChain utilize identical keys, the system generates functions that facilitate unified access to all states. This enhancement significantly simplifies the process of retrieving and managing state information across different parts of the application.

### Usage Examples

#### Retrieving All States

To access all states associated with a particular chain for a given user, the following syntax can be employed:
```kotlin
user.getAllState(MyChain).LinkName
```
This command retrieves the data linked to the specified `LinkName` within `MyChain`, providing a comprehensive overview of the user's interaction history.

#### Direct State Access

Alternatively, for more granular control, states can be accessed directly through the links themselves:
```kotlin
Chain.LinkName.state.get(key)
```
Or, if querying the state within the current chain, `Chain.LinkName` may be omitted, simplifying the call to:
```kotlin
state.get(key)
```

### Benefits

This methodology enables stricter data management protocols, offering rapid and convenient access to stored states. It enhances the efficiency of state retrieval and manipulation, contributing to a more seamless user experience.

Default `BaseStatefulLink` implementation uses `ConcurrentHashMap`, but for serious projects it is recommended to use other solutions :)

## Summarizing

It is possible to use the proposed tools with different variations to create quite flexible interaction, if you have any questions contact us in chat, we will be glad to help :)
