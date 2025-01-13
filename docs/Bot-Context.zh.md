---
title: 机器人上下文
---

<p align="center">
  <img src="https://github.com/user-attachments/assets/60bb58ae-1806-4b8d-8550-833b09c2b606" alt="机器人上下文图" />
</p>

机器人还可以通过 `User Data` 和 `ClassData` 接口提供记住一些数据的能力。

- [`userData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-user-data/index.html) 是用户级别的数据。
- [`classData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-data/index.html) 是类级别的数据，即数据将被存储，直到用户移动到不同类中的命令或输入。（在函数模式下，它将像用户数据一样工作）

默认情况下，提供的实现是通过 [`ConcurrentHashMap`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.collections/java.util.concurrent.-concurrent-map/) 进行的，但可以通过 [`User Data`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-user-data/index.html) 和 [`ClassData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-data/index.html) 接口使用您选择的数据存储工具进行更改。

> [!CAUTION]
> 不要忘记运行 gradle `kspKotlin`/或任何相关的 ksp 任务，以使所需的代码生成绑定可用。

要更改，您只需在您的实现下放置 `@CtxProvider` 注解并运行 gradle ksp 任务（或构建）。

```kotlin
@CtxProvider
class MyRedis : UserData<String> {
    // ...
}

```

### 另请参见

* [首页](https://github.com/vendelieu/telegram-bot/wiki)
* [更新解析](Update-parsing.md)