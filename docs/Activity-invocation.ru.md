---
---
title: Вызов Activity
---

При вызове activity можно передать контекст бота, так как он объявлен как параметр в целевых функциях.

Параметры, которые можно передать:

* [`ProcessedUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processed-update/index.html) (и все его подклассы) - текущий обрабатываемый update.
* [`ProcessingContext`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processing-context/index.html) - низкоуровневый контекст обработки activity.
* [`User`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types/-user/index.html) - если присутствует.
* [`Chat`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.chat/-chat/index.html) - если присутствует.
* [`TelegramBot`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot/-telegram-bot/index.html) - текущий экземпляр бота.

Также возможно добавить пользовательский тип для передачи.

Для этого добавьте класс, реализующий интерфейс [`Autowiring<T>`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.marker/-autowiring/index.html) и пометьте его аннотацией [`@Injectable`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-injectable/index.html).

После реализации интерфейса `Autowiring` - `T` станет доступен для передачи в целевые функции и будет получен через метод, описанный в интерфейсе.

```kotlin
@Injectable
object UserResolver : Autowiring<UserRecord> {
    override suspend fun get(update: ProcessedUpdate, bot: TelegramBot): UserRecord? {
        return userRepository.getUserByTgId(update.user.id)
    }
}
```

Другие параметры, объявленные в функциях, будут **искаться** в распарсенных параметрах.

Дополнительно, распарсенные параметры при передаче могут приводиться к определенным типам, вот их список:

- `String`
- `Integer`
- `Long`
- `Short`
- `Float`
- `Double`

Более того, обратите внимание, что если параметры объявлены и отсутствуют (или в распарсенных параметрах или например `User` отсутствует в `Update`) или объявленный тип не соответствует полученному параметру в функции, будет передано **`null`**, так что будьте внимательны.

Подводя итог всему, ниже приведен пример того, как обычно формируются параметры функции:

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/3c1d7830-8e5d-45fb-82bb-ac63f08c3782" alt="Схема процесса вызова" />
</p>

### См. также

* [Парсинг Update](Update-parsing.md)
* [Activities & Processors](Activites-and-Processors.md)
---