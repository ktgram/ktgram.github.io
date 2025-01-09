During activity invocation, it is possible to pass the bot context, as it is declared as a parameter in target functions. 

The parameters that can be passed are: 

* [`ProcessedUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.internal/-processed-update/index.html) (and all its subclasses) - current processing update.
* [`User`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types/-user/index.html) - if present.
* [`TelegramBot`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot/-telegram-bot/index.html) - current bot instance. 

It is also possible to add a custom type for passing. 

To do this, add a class that implements [`Autowiring<T>`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.marker/-autowiring/index.html) and mark it with the [`@Injectable`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-injectable/index.html) annotation. 

After implementing the `Autowiring` interface - `T` will be available for passing in target functions and will be obtained through the method described in the interface. 

```kotlin
@Injectable
object UserResolver : Autowiring<UserRecord> {
    override suspend fun get(update: ProcessedUpdate, bot: TelegramBot): UserRecord? {
        return userRepository.getUserByTgId(update.user.id)
    }
}
```


Other parameters declared in functions will be **searched** in parsed parameters. 

Additionally, parsed parameters during passing can be cast to certain types, here is their list: 

- `String`
- `Integer`
- `Long`
- `Short`
- `Float`
- `Double`

Moreover, note that if parameters are declared and missing (or in parsed parameters or for example `User` is missing in `Update`) or the declared type does not fit the received parameter in the function, **`null`** will be passed so be careful.

Summarizing everything, below here is an example of how function parameters are usually formed:

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/3c1d7830-8e5d-45fb-82bb-ac63f08c3782" alt="Invokation process diagram" />
</p>

# See also

* [Update parsing](https://github.com/vendelieu/telegram-bot/wiki/Update-parsing)
* [Activities & Processors](https://github.com/vendelieu/telegram-bot/wiki/Activites-and-Processors)