---
---
title: Bot Context
---

<p align="center">
  <img src="https://github.com/user-attachments/assets/60bb58ae-1806-4b8d-8550-833b09c2b606" alt="Bot context diagram" />
</p>

The bot can also provide the ability to remember some data through the `UserData` and `ClassData` interfaces.

- [`userData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-user-data/index.html) is a user-level data.
- [`classData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-data/index.html) is a class-level data, i.e. the data will be stored until the user moves to a command or input that is in a
  different class. (in function mode it will work like as user data)

By default, implementation is provided through [`ConcurrentHashMap`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.collections/java.util.concurrent.-concurrent-map/) but can be changed to your own through [`UserData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-user-data/index.html) and [`ClassData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-data/index.html) interfaces using
the data storage tools of your choice.


> [!CAUTION]
> Đừng quên chạy gradle `kspKotlin`/hoặc bất kỳ task ksp liên quan nào để làm cho các codegen bindings cần thiết có sẵn. 


Để thay đổi, tất cả những gì bạn cần làm là đặt annotation `@CtxProvider` dưới implementation của bạn và chạy gradle ksp task (hoặc build).

```kotlin
@CtxProvider
class MyRedis : UserData<String> {
    // ...
}

```

### See also

* [Home](https://github.com/vendelieu/telegram-bot/wiki)
* [Update parsing](Update-parsing.md)
---