---
title: 处理器
---

### 处理器的多样性

在机器人开发中，特别是在涉及用户交互的系统中，有效地管理和处理命令和事件至关重要。

这些注解标记了旨在处理特定命令、输入或更新的函数，并提供了诸如命令关键字、作用域和保护机制等元数据。

### 注解概述

#### CommandHandler

`CommandHandler` 注解用于标记处理特定命令的函数。此注解包括定义命令关键字和作用域的属性。

-   **value**：指定与命令相关联的关键字。
-   **scope**：确定检查命令的上下文或作用域。

```kotlin
@CommandHandler(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommandHandler.CallbackQuery

`CommandHandler` 注解的一个专用版本，专门用于处理回调查询。它包括与 `CommandHandler` 相似的属性，重点关注与回调相关的命令。

_实际上，它与仅使用 `@CommandHandler` 并预设 `UpdateType.CALLBACK_QUERY` 作用域是相同的_。

-   **value**：指定与命令相关联的关键字。
-   **autoAnswer**：自动回复 `callbackQuery`（在处理之前调用 `answerCallbackQuery`）。

```kotlin
@CommandHandler.CallbackQuery(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### CommonHandler

`CommonHandler` 注解旨在处理优先级低于 `CommandHandler` 和 `InputHandler` 的命令的函数。它在源级别使用，并提供了一种灵活的方式来定义常见命令处理器。

**请注意，优先级仅在 `@CommonHandler` 内部有效（即不影响其他处理器）。**

##### CommonHandler.Text

此注解指定与更新匹配的文本。它包括定义匹配文本、过滤条件、优先级和作用域的属性。

-   **value**：要与传入更新匹配的文本。
-   **filter**：定义在匹配过程中使用的条件的类。
-   **priority**：处理器的优先级级别，0 为最高优先级。
-   **scope**：检查文本匹配的上下文或作用域。

```kotlin
@CommonHandler.Text(["text"], filter = isNewUser Filter::class, priority = 10)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommonHandler.Regex

与 `CommonHandler.Text` 类似，此注解用于基于正则表达式匹配更新。它包括定义正则表达式模式、选项、过滤条件、优先级和作用域的属性。

-   **value**：用于匹配的正则表达式模式。
-   **options**：修改正则表达式模式行为的正则表达式选项。
-   **filter**：定义在匹配过程中使用的条件的类。
-   **priority**：处理器的优先级级别，0 为最高优先级。
-   **scope**：检查正则表达式匹配的上下文或作用域。

```kotlin
@CommonHandler.Regex("^<br/>d+$", scope = [UpdateType.EDITED_MESSAGE])
suspend fun test(update: EditedMessageUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### InputHandler

`InputHandler` 注解标记处理特定输入事件的函数。它旨在处理运行时的输入，并包括定义输入关键字和作用域的属性。

-   **value**：指定与输入事件相关联的关键字。

```kotlin
@InputHandler("text")
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UnprocessedHandler

`UnprocessedHandler` 注解用于标记处理未被其他处理器处理的更新的函数。它确保任何未处理的更新都得到适当管理，并且此处理器类型仅允许一个处理点。

```kotlin
@UnprocessedHandler
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UpdateHandler

`UpdateHandler` 注解标记处理特定类型的传入更新的函数。它提供了一种系统化地分类和处理不同更新类型的方法。

-   **type**：指定处理器函数将处理的更新类型。

```kotlin
@UpdateHandler([UpdateType.PRE_CHECKOUT_QUERY])
suspend fun test(update: PreCheckoutQueryUpdate, user: User, bot: TelegramBot) {
    //...
}
```

### 处理器伴随注解

还有一些附加注解是可选的，补充了处理器本身的可选行为。

它们可以放置在应用处理器的函数上，也可以放置在类上，在后者的情况下，它们将自动应用于该类中的所有处理器，但如果需要，可以为某些函数具有单独的行为。

即，应用的优先级为 `Function` > `Class`，其中函数具有更高的优先级。

#### 速率限制

此外，让我们还披露在注解中描述的速率限制机制。

您可以为每个用户设置一般限制：

```kotlin
// ...
val bot = TelegramBot("BOT_TOKEN") {
    rateLimiter { // 一般限制
        limits = RateLimits(period = 10000, rate = 5)
    }
}
```

###### 处理器特定

可以使用 `RateLimits` 注解定义某些操作的限制，支持 `@CommandHandler`、`@CommandHandler.CallbackQuery`、`@InputHandler`、`@CommonHandler`。

```kotlin
@CommandHandler(["/start"])
@RateLimits(period = 1000L, rate = 1L)
suspend fun start(user: User, bot: TelegramBot) {
    // ...
}
```

#### 保护机制

您可以单独定义保护机制以控制对处理器的访问，支持 `@CommandHandler`、`@CommandHandler.CallbackQuery`、`@InputHandler`：

```kotlin
@CommandHandler(["text"])
@Guard(isAdminGuard::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### 参数解析器

您可以单独定义自定义参数解析器，以更改处理器的参数解析行为，支持 `@CommandHandler`、`@CommandHandler.CallbackQuery`、`@CommonHandler`：

```kotlin
@CommandHandler(["text"])
@ArgParser(SpaceArgParser::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

**另请参见 [`defaultArgParser`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils/default-arg-parser.html)**

### 结论

这些注解为处理命令、输入和事件提供了强大而灵活的工具，同时允许单独配置速率限制和保护机制，增强了机器人开发的整体结构和可维护性。

### 另请参见

* [活动与处理器](Activites-and-Processors.md)
* [活动调用](Activity-invocation.md)
* [有限状态机和对话处理](FSM-and-Conversation-handling.md)
* [更新解析](Update-parsing.md)