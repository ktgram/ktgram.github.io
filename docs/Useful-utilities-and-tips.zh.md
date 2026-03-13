---
---
title: 实用工具和技巧
---


### 处理 ProcessedUpdate

[`ProcessedUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processed-update/index.html) 是一个通用类，用于更新，根据原始数据，可以以不同类型提供（[`MessageUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-message-update/index.html)、[`CallbackQueryUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-callback-query-update/index.html) 等）

因此，你可以检查传入数据的类型，并通过智能转换进一步操作特定数据，例如：

```kotlin
// ...
if (update !is MessageUpdate) {
    message { "Only messages are allowed" }.send(user, bot)
    return
}
// 进一步，ProcessedUpdate 将被视为 MessageUpdate。
```

还有一个 [`UserReference`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-user-reference/index.html) 接口，允许你确定其中是否包含用户引用，使用示例：

```kotlin
val user = if(update is UserReference) update.user else null

```

如果需要，更新参数中始终有原始的 [`update`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types/-update/index.html)。


### 依赖注入

库使用简单的机制来初始化类，其中你的更新处理方法使用提供的注解进行标注。

[`ClassManagerImpl`](https://github.com/vendelieu/telegram-bot/blob/master/telegram-bot/src/commonMain/kotlin/eu/vendeli/tgbot/implementations/ClassManagerImpl.kt) 默认用于调用注解方法。

但如果你想使用其他库来实现，你可以重新定义 [`ClassManager`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-manager/index.html) 接口，<br/>使用你偏好的机制，并在初始化机器人时传入。

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.controllers") {
        classManager = ClassManagerImpl()
    }

    bot.handleUpdates()
}
```

### 过滤更新

如果没有复杂的条件，你可以简单地过滤某些更新以进行处理：

```kotlin
// 定义更新过滤条件的函数
fun filteringFun(update: Update): Boolean = update.message?.text.isNullOrBlank()

fun main() = runBlocking {
  val bot = TelegramBot("BOT_TOKEN")

  // 为更新设置更具体的处理流程
  bot.update.setListener {
    if(filteringFun(it)) return@setListener

    // 所以，如果监听器在到达处理程序函数之前离开作用域，那就是过滤。
    // 实际上你甚至可以直接在那里写 if 条件，使用 return@setListener，或者将过滤扩展到单独的类。

    handle(it) // 或使用块进行手动处理
  }
}
```

要在命令匹配或排除过程中包含过滤，请查看 guards 或 `@CommonHandler`。

### 为不同方法通用化选项

如果你经常需要应用相同的可选参数，你可以编写类似的函数来满足你的需求，并简化样板代码 :)

一些通用属性被分离到[不同的接口](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.options/-options/index.html)中。

```kotlin
@Suppress("NOTHING_TO_INLINE")
inline fun <T, R, O> T.markdownMode(crossinline block: O.() -> Unit = {}): T
        where               T : TgAction<R>,
                            T : OptionsFeature<T, O>,
                            O : Options,
                            O : OptionsParseMode =
    options {
        parseMode = ParseMode.Markdown
        block()
    }


// ... 在你的代码中

message { "test" }.markdownMode().send(to, via)

```