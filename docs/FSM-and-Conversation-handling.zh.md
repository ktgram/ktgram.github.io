---
title: FSM 和对话处理
---

该库还支持 FSM 机制，这是一种逐步处理用户输入的机制，具有错误输入处理功能。

### 理论上

让我们想象一个需要收集用户调查的情况，您可以在一个步骤中询问一个人的所有数据，但如果其中一个参数输入不正确，对用户和我们来说都会很困难，并且每个步骤可能会根据某些输入数据有所不同。

现在让我们想象逐步输入数据的过程，机器人与用户进入对话模式。

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/2e84fa00-e59c-4352-8665-83be3b971e7b" alt="处理过程图" />
</p>

绿色箭头表示无错误地通过步骤的过程，蓝色箭头表示保存当前状态并等待重新输入（例如，如果用户表示他是 -100 岁，应该再次询问年龄），红色箭头则显示由于任何命令或其他含义的取消而退出整个过程。

### 实践中

这样的机制可以通过一个简单的类在库中实现，该类实现特定接口并用特定注解 `@InputChain` 标记。

```kotlin
@InputChain
object ConversationChain {
    object Name : BaseStatefulLink() {
        override val breakCondition = BreakCondition { _, update, _ -> update.text.isBlank() }
        override suspend fun breakAction(user: User, update: ProcessedUpdate, bot: TelegramBot) {
            message {
                "请告诉我你的名字，因为这就是有礼貌的人所做的 :)"
            }.send(user, bot)
        }

        override suspend fun action(user: User, update: ProcessedUpdate, bot: TelegramBot): String {
            message { "哦，${update.text}，你好" }.send(user, bot)
            message { "你多大了？" }.send(user, bot)

            return update.text
        }
    }

    object Age : BaseStatefulLink() {
        override val breakCondition = BreakCondition { _, update, _ -> update.text.toIntOrNull() == null }
        override suspend fun breakAction(user: User, update: ProcessedUpdate, bot: TelegramBot) {
            message {
                "也许问你的年龄不太礼貌，但也许你可以告诉我。"
            }.send(user, bot)
        }

        override suspend fun action(user: User, update: ProcessedUpdate, bot: TelegramBot): String {
            message { "很高兴见到你！" }.send(user, bot)

            return update.text
        }
    }

    object Final : ChainLink() {
        override suspend fun action(user: User, update: ProcessedUpdate, bot: TelegramBot) {
            val state = user.getAllState(ConversationChain)

            message {
                "我记性不好，但我记住了你！ " +
                        "你叫 ${state.Name}，你 ${state.Age} 岁。"
            }.send(user, bot)
        }
    }
}
```

在我们描述了启动处理的机制后，我们只需调用方法并指定初始步骤，然后库将自动遵循顺序。

```kotlin
bot.inputListener.setChain(user, Conversation.Name)
```

### 链接细节

所有链接都有相同的基础，并实现 [`Link<T>`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.internal.chain/-link/index.html) 接口，该接口具有以下属性：

关键属性：

* afterAction：在主要操作后执行的可选操作。
* beforeAction：在主要操作前执行的可选操作。
* breakCondition：如果满足，将触发链中断的条件。
* chainingStrategy：定义如何确定下一个链接。
* retryAfterBreak：指示在满足中断条件后是否重试操作。

关键函数：

* action：这是一个抽象函数，必须实现以定义链接的主要行为。
* breakAction：可选函数，可以重写以定义在满足中断条件时的行为。

有两种类型的链接，它们按状态区分，无状态和有状态：

### 无状态链接

无状态链接由抽象类 [`ChainLink`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.internal/-chain-link/index.html) 表示。此类作为创建不在用户交互之间维护任何状态信息的链接的基础。

### 有状态链接

`InputChain` 机制，特别是在使用 `StatefulLink` 及其各种实现时，提供了一种复杂的方法来管理应用程序中的对话状态，例如聊天机器人。该系统自动存 储与每个状态相关联的 `action` 函数的结果，将其直接链接到参与交互的用户（或其他选定的关键）。

#### 关键特性

##### 自动状态存储

- 默认情况下，在 `StatefulLink` 中执行的 `action` 函数的结果会自动存储。此存储与用户相关联，确保基于过去的交流进行个性化交互。

##### 可定制的键

- 开发人员可以灵活地覆盖基本实现，以指定用于状态关联的自定义键。这可以是唯一标识聊天会话的标识符，也可以是适合应用程序需求的任何其他相关属性。

##### 数据类型和键的利用

- 基础实现 `BaseStatefulLink` 将数据分类为 `String` 类型，使用 `User .id` 作为状态关联的主键。这种方法简化了数据管理和检索过程。

##### 统一访问状态

- 如果所有 `Link` 对象在 InputChain 中使用相同的键，系统会生成函数以便于统一访问所有状态。这一增强显著简化了在应用程序不同部分检索和管理状态信息的过程。

#### 使用示例

##### 检索所有状态

要访问与特定链关联的给定用户的所有状态，可以使用以下语法：
```kotlin
user.getAllState(MyChain).LinkName
```
此命令检索与指定的 `LinkName` 相关联的数据，提供用户交互历史的全面概述。

##### 直接状态访问

或者，为了更细粒度的控制，可以通过链接本身直接访问状态：
```kotlin
Chain.LinkName.state.get(key)
```
或者，如果在当前链中查询状态，可以省略 `Chain.LinkName`，简化调用为：
```kotlin
state.get(key)
```

#### 优势

这种方法使得数据管理协议更加严格，提供快速便捷的存储状态访问。它提高了状态检索和操作的效率，促进了更流畅的用户体验。

默认的 `BaseStatefulLink` 实现使用 `ConcurrentHashMap`，但对于严肃的项目，建议使用其他解决方案 :)

### 总结

可以使用所提出的工具与不同的变体创建相当灵活的交互，如果您有任何问题，请在聊天中与我们联系，我们将很高兴提供帮助 :)