---
title: 首页
---

### 介绍
让我们了解一下库如何处理更新的总体情况：

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/442cc5f1-0256-425a-9f25-185fdd49fe0a" alt="处理过程图" />
</p>

在接收到更新后，库执行三个主要步骤，如我们所见。

### 处理

处理是将接收到的更新重新打包为适当的 [`ProcessedUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.internal/-processed-update/index.html) 子类，具体取决于所携带的有效负载。

此步骤的目的是使操作更新更容易，并扩展处理能力。

### 处理

接下来是主要步骤，这里我们进入处理本身。

### 全局速率限制器

如果更新中有用户，我们会检查是否超过了全局速率限制器。

### 解析文本

接下来，根据有效负载，我们获取包含文本的特定更新组件，并根据配置进行解析。

更详细的信息可以在 [更新解析文章](Update-parsing.md) 中查看。

### 查找活动

接下来，根据处理优先级：

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/6178c410-9b9e-4045-9f03-4791b3f49894" alt="处理优先级图" />
</p>

我们在解析的数据与我们正在操作的活动之间寻找对应关系。
如优先级图所示，`Commands` 总是优先。

即，如果更新中的文本负载对应于任何命令，则不会进一步搜索 `Inputs`、`Common`，当然也不会执行 `Unprocessed` 操作。

唯一的例外是，如果存在 `UpdateHandlers`，则会并行触发。

#### 命令

让我们更详细地了解命令及其处理。

正如您可能注意到的，尽管处理命令的注解称为 [`CommandHandler`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-command-handler/index.html)，但它比 Telegram 机器人的经典概念更为通用。

##### 作用域

这是因为它具有更广泛的处理可能性，即目标函数不仅可以根据文本匹配来定义，还可以根据适当更新的类型来定义，这就是作用域的概念。

因此，每个命令可以针对不同的作用域具有不同的处理器，反之亦然，一个命令可以对应多个作用域。

下面您可以看到如何通过文本负载和作用域进行映射：

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/c870027e-750e-4bb8-a2ed-45ad93a55875" alt="命令作用域图" />
</p>

#### 输入

接下来，如果文本负载与任何命令不匹配，则会搜索输入点。

该概念与命令行应用程序中的输入等待非常相似，您为特定用户在机器人上下文中设置一个点，该点将处理他的下一个输入，无论它包含什么，主要是下一个更新必须有一个 `User ` 以便能够将其与设置的输入等待点关联。

下面您可以看到在没有匹配 `Commands` 时处理更新的示例。

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/925d3e05-0985-43d5-8d6f-b3f2786ff212" alt="优先级示例图" />
</p>

#### 常规

如果处理器未找到 `commands` 或 `inputs`，则会检查文本负载与 `common` 处理器的匹配。

我们建议在不滥用的情况下使用它，因为它会对所有条目进行迭代检查。

#### 未处理

最后一步，如果处理器未找到任何匹配的活动（[`UpdateHandler`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-update-handler/index.html) 完全并行工作，不算作常规活动），则会调用 [`UnprocessedHandler`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-unprocessed-handler/index.html)，如果设置了它，将处理此情况，这可能有助于警告用户某些事情出错了 ```markdown
。

更详细的信息可以在 [处理器文章](Handlers.md) 中查看。

### 活动速率限制器

在找到活动后，它还会根据活动参数中指定的参数检查用户的速率限制。

### 活动

活动是指 Telegram 机器人库可以处理的不同类型的处理器，包括命令、输入、正则表达式和未处理的处理器。

### 调用

最后的处理步骤是调用找到的活动。

更多详细信息可以在 [调用文章](Activity-invocation.md) 中找到。

### 另请参见

* [更新解析](Update-parsing.md)
* [活动调用](Activity-invocation.md)
* [处理器](Handlers.md)
* [机器人配置](Bot-configuration.md)
* [Web 启动器（Spring、Ktor）](Web-starters-(Spring-and-Ktor).md)