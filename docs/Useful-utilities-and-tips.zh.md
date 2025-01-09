---
title: 有用的工具和提示
---

### 操作 ProcessedUpdate

[`ProcessedUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.internal/-processed-update/index.html) 是一个通用类，用于更新，根据原始数据，可以提供不同类型（[`MessageUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.internal/-message-update/index.html)、[`CallbackQueryUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.internal/-callback-query-update/index.html) 等）。

因此，您可以检查传入数据的类型，并使用智能类型转换进一步操作某些数据，例如：

```kotlin
// ...
if (update !is MessageUpdate) {
    message { "只允许消息" }.send(user, bot)
    return
}
// 进一步处理时，ProcessedUpdate 将被视为 MessageUpdate。
```

内部还有一个 [`User Reference`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.internal/-user-reference/index.html) 接口，可以让您确定是否存在用户引用，示例用例：

```kotlin
val user = if(update is UserReference) update.user else null
```

如果需要，更新参数中始终有原始的 [`update`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types/-update/index.html)。

### 依赖注入

该库使用简单机制来初始化类，其中您的更新处理方法用提供的注解标记。

默认情况下使用 [`ClassManagerImpl`](https://github.com/vendelieu/telegram-bot/blob/master/telegram-bot/src/commonMain/kotlin/eu/vendeli/tgbot/implementations/ClassManagerImpl.kt) 来调用注解方法。

但如果您想使用其他库，可以重新定义 [`ClassManager`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-manager/index.html) 接口，<br/>
使用您首选的机制并在初始化机器人时传递它。

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.controllers") {
        classManager = ClassManagerImpl()
    }

    bot.handleUpdates()
}
```

### 过滤更新

如果没有复杂条件，您可以简单地过滤一些更新以进行处理：

```kotlin
// 定义更新过滤条件的函数
fun filteringFun(update: Update): Boolean = update.message?.text.isNullOrBlank()

fun main() = runBlocking {
  val bot = TelegramBot("BOT_TOKEN")

  // 为更新设置更具体的处理流程
  bot.update.setListener {
    if(filteringFun(it)) return@setListener

    // 因此，如果监听器在到达处理函数之前离开了作用域，则它正在过滤。
    // 实际上，您甚至可以直接在此处编写 if 条件，使用 return@setListener 或将过滤扩展到单独的类。

    handle(it) // 或使用块的手动处理方式
  }
}
```

要在命令匹配或排除过程中包含过滤，请查看保护机制或 `@CommonHandler`。

### 为不同方法通用化选项

如果您需要经常应用相同的可选参数，可以编写一个适合您的类似函数，以减轻样板代码的负担 :)

一些常见属性被分离到 [不同接口](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.internal.options/-options/index.html)。

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


// ... 在您的代码中

message { "test" }.markdownMode().send(to, via)

```