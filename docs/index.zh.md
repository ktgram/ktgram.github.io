---
---
title: 首页
---

### 简介
让我们了解一下库如何处理更新的一般情况：

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/442cc5f1-0256-425a-9f25-185fdd49fe0a" alt="处理流程图" />
</p>

如我们所见，在收到更新后，库执行三个主要步骤。

### 处理

处理是将收到的更新重新打包为[`ProcessedUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processed-update/index.html)的相应子类的过程，具体取决于所携带的负载。

这一步是为了更容易操作更新并扩展处理能力而需要的。

### 处理

接下来是主要步骤，这里我们进入处理本身。

### 全局速率限制器

如果更新中有用户，我们检查是否超过了全局速率限制器。

### 解析文本

接下来，根据负载，我们获取包含文本的特定更新组件，并根据配置对其进行解析。

更详细的内容可以在[更新解析文章](Update-parsing.md)中查看。

### 查找活动

接下来，根据处理优先级：

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/6178c410-9b9e-4045-9f03-4791b3f49894" alt="处理优先级图" />
</p>

我们在解析数据和我们正在操作的活动之间寻找对应关系。
正如我们在优先级图中看到的，`Commands`始终排在第一位。

也就是说，如果更新中的文本负载与任何命令相对应，则不会执行对`Inputs`、`Common`的进一步搜索，当然也不会执行`Unprocessed`操作。

唯一需要注意的是，如果有`UpdateHandlers`将并行触发，而不管这些。

#### 命令

让我们更详细地了解命令及其处理。

正如您可能已经注意到的，虽然用于处理命令的注解称为[`CommandHandler`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-command-handler/index.html)，但它比电报机器人中的经典概念更通用。

##### 作用域

这是因为它的处理可能性范围更广，即目标函数不仅可以根据文本匹配来定义，还可以根据相应更新的类型来定义，这就是作用域的概念。

因此，每个命令可以根据不同的作用域列表具有不同的处理程序，或者反过来，一个命令对应多个处理程序。

下面您可以看到如何通过文本负载和作用域进行映射：

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/c870027e-750e-4bb8-a2ed-45ad93a55875" alt="命令作用域图" />
</p>

#### 输入

接下来，如果文本负载与任何命令都不匹配，则搜索输入点。

这个概念与命令行应用程序中的输入等待非常相似，您在机器人上下文中为特定用户设置一个点，该点将处理他的下一个输入，无论它包含什么，主要的是下一个更新有一个`User`以便能够将其与设置的输入等待点关联起来。

下面您可以看到当在`Commands`上没有匹配时处理更新的示例。

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/925d3e05-0985-43d5-8d6f-b3f2786ff212" alt="优先级示例图" />
</p>

#### 通用

如果处理程序找不到`commands`或`inputs`，它会检查文本负载与`common`处理程序的匹配。

我们建议不要滥用它，因为它需要遍历所有条目。

#### 未处理

最后一步，如果处理程序找不到任何匹配的活动（[`UpdateHandler`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-update-handler/index.html)完全并行工作，不算作常规活动），则[`UnprocessedHandler`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-unprocessed-handler/index.html)开始发挥作用，如果设置了它，它将处理这种情况，警告用户出了问题的做法可能很有用。

在[Handlers文章](Handlers.md)中可以阅读更多详细信息。

### 活动速率限制器

找到活动后，它也会根据活动参数中指定的参数检查用户的速率限制。

### 活动

活动是指电报机器人库可以处理的各种类型的处理程序，包括命令、输入、正则表达式和未处理处理程序。

### 调用

最后的处理步骤是调用找到的活动。

更多详细信息可以在[调用文章](Activity-invocation.md)中找到。

### 另请参阅

* [更新解析](Update-parsing.md)
* [活动调用](Activity-invocation.md)
* [处理程序](Handlers.md)
* [机器人配置](Bot-configuration.md)
* [Web启动器（Spring、Ktor）](Web-starters-(Spring-and-Ktor.md))
---