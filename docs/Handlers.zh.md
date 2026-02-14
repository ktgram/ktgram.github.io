---
---
title: 处理程序
---

### 处理程序种类

在机器人开发中，特别是在涉及用户交互的系统中，高效地管理和处理命令和事件至关重要。

这些注解标记了设计用于处理特定命令、输入或更新的函数，并提供元数据，如命令关键字、作用域和保护。

### 注解概述

#### CommandHandler

`CommandHandler` 注解用于标记处理特定命令的函数。此注解包含定义命令关键字和作用域的属性。

-   **value**: 指定与命令关联的关键字。
-   **scope**: 确定将检查命令的上下文或作用域。

```kotlin
@CommandHandler(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommandHandler.CallbackQuery

`CommandHandler` 注解的专门版本，专门用于处理回调查询。它包含与 `CommandHandler` 类似的属性，但专注于回调相关的命令。

_它实际上与预设 `UpdateType.CALLBACK_QUERY` 作用域的 `@CommandHandler` 相同_。

-   **value**: 指定与命令关联的关键字。
-   **autoAnswer**: 自动回复 `callbackQuery`（在处理之前调用 `answerCallbackQuery`）。


```kotlin
@CommandHandler.CallbackQuery(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### CommonHandler

`CommonHandler` 注解用于处理优先级低于 `CommandHandler` 和 `InputHandler` 的命令的函数。它在源级别使用，并提供了一种灵活的方式来定义通用命令处理程序。

**请注意，优先级仅在 `@CommonHandler` 本身内起作用（即不影响其他处理程序）。**

##### CommonHandler.Text

此注解指定针对更新的文本匹配。它包含定义匹配文本、筛选条件、优先级和作用域的属性。

-   **value**: 要与传入更新匹配的文本。
-   **filter**: 定义匹配过程中使用的条件的类。
-   **priority**: 处理程序的优先级级别，0 为最高优先级。
-   **scope**: 将检查文本匹配的上下文或作用域。

```kotlin
@CommonHandler.Text(["text"], filter = isNewUserFilter::class, priority = 10)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommonHandler.Regex

与 `CommonHandler.Text` 类似，此注解用于基于正则表达式匹配更新。它包含定义正则表达式模式、选项、筛选条件、优先级和作用域的属性。

-   **value**: 用于匹配的正则表达式模式。
-   **options**: 修改正则表达式模式行为的正则表达式选项。
-   **filter**: 定义匹配过程中使用的条件的类。
-   **priority**: 处理程序的优先级级别，0 为最高优先级。
-   **scope**: 将检查正则表达式匹配的上下文或作用域。

```kotlin
@CommonHandler.Regex("^\d+$", scope = [UpdateType.EDITED_MESSAGE])
suspend fun test(update: EditedMessageUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### InputHandler

`InputHandler` 注解标记处理特定输入事件的函数。它用于在运行时处理输入的函数，并包含定义输入关键字和作用域的属性。

-   **value**: 指定与输入事件关联的关键字。

```kotlin
@InputHandler("text")
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UnprocessedHandler

`UnprocessedHandler` 注解用于标记处理未被其他处理程序处理的更新的函数。它确保任何未处理的更新都能得到适当管理，这种处理程序类型只有一个处理点。

```kotlin
@UnprocessedHandler
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UpdateHandler

`UpdateHandler` 注解标记处理特定类型传入更新的函数。它提供了一种系统地分类和处理不同更新类型的方法。

-   **type**: 指定处理程序函数将处理的更新类型。

```kotlin
@UpdateHandler([UpdateType.PRE_CHECKOUT_QUERY])
suspend fun test(update: PreCheckoutQueryUpdate, user: User, bot: TelegramBot) {
    //...
}
```

### 处理程序伴随注解

还有一些额外的注解是处理程序的可选注解，补充了处理程序本身的可选行为。

它们可以同时放置在应用处理程序的函数和类上，在后一种情况下，它们将自动应用于该类中的所有处理程序，但如果需要，可以为某些函数设置单独的行为。

即，应用的优先级为 `Function` > `Class`，其中函数具有更高的优先级。

#### 速率限制

此外，让我们还披露注解中描述的速率限制机制。

您可以为每个用户设置一般限制：

```kotlin
// ...
val bot = TelegramBot("BOT_TOKEN") {
    rateLimiter { // 一般限制
        limits = RateLimits(period = 10000, rate = 5)
    }
}
```

###### 特定处理程序的速率限制

可以使用 `RateLimits` 注解定义某些操作的限制，支持 `@CommandHandler`、`@CommandHandler.CallbackQuery`、`@InputHandler`、`@CommonHandler`。

```kotlin
@CommandHandler(["/start"])
@RateLimits(period = 1000L, rate = 1L)
suspend fun start(user: User, bot: TelegramBot) {
    // ...
}
```

#### 保护

您可以单独定义保护来控制对处理程序的访问，支持 `@CommandHandler`、`@CommandHandler.CallbackQuery`、`@InputHandler`：

```kotlin
@CommandHandler(["text"])
@Guard(isAdminGuard::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### 参数解析器

您可以单独定义自定义参数解析器来更改处理程序的参数解析行为，支持 `@CommandHandler`、`@CommandHandler.CallbackQuery`、`@CommonHandler`：

```kotlin
@CommandHandler(["text"])
@ArgParser(SpaceArgParser::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

**另请参阅 [`defaultArgParser`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.common/default-arg-parser.html)**

### 结论

这些注解为处理命令、输入和事件提供了强大而灵活的工具，同时允许单独配置速率限制和保护，增强了机器人开发的整体结构和可维护性。

### 另请参阅

* [活动和处理器](Activites-and-Processors.md)
* [活动调用](Activity-invocation.md)
* [FSM 和会话处理](FSM-and-Conversation-handling.md)
* [更新解析](Update-parsing.md)
* [助手](Aide.md)