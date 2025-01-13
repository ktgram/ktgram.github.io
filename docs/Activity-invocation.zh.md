---
title: 活动调用
---

在活动调用期间，可以传递机器人上下文，因为它被声明为目标函数中的一个参数。

可以传递的参数有：

* [`ProcessedUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.internal/-processed-update/index.html)（及其所有子类） - 当前处理的更新。
* [`User `](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types/-user/index.html) - 如果存在。
* [`TelegramBot`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot/-telegram-bot/index.html) - 当前的机器人实例。

还可以添加自定义类型进行传递。

为此，添加一个实现 [`Autowiring<T>`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.marker/-autowiring/index.html) 的类，并用 [`@Injectable`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-injectable/index.html) 注解标记它。

在实现 `Autowiring` 接口后，`T` 将可以在目标函数中传递，并通过接口中描述的方法获取。

```kotlin
@Injectable
object UserResolver : Autowiring<UserRecord> {
    override suspend fun get(update: ProcessedUpdate, bot: TelegramBot): UserRecord? {
        return userRepository.getUser ByTgId(update.user.id)
    }
}
```

在函数中声明的其他参数将**在解析的参数中被搜索**。

此外，在传递时，解析的参数可以被转换为某些类型，以下是它们的列表：

- `String`
- `Integer`
- `Long`
- `Short`
- `Float`
- `Double`

此外，请注意，如果参数被声明但缺失（例如在解析的参数中或 `Update` 中缺少 `User `），或者声明的类型与函数中接收到的参数不匹配，**`null`** 将被传递，因此请小心。

总结一下，下面是函数参数通常是如何形成的示例：

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/3c1d7830-8e5d-45fb-82bb-ac63f08c3782" alt="调用过程图" />
</p>

### 另请参见

* [更新解析](Update-parsing.md)
* [活动与处理器](Activites-and-Processors.md)