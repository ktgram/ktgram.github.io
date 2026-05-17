---
---
title: Activites And Processors
---

### Introduction

`Activity` nos termos desta biblioteca é a entidade abstrata que generaliza entidades como `@CommandHandler`, `@InputHandler`, `@UnprocessedHandler`, `@CommonHandler`, `@UpdateHandler` e `@WizardHandler`.

Também dê uma olhada no [artigo sobre handlers](Handlers.md).

### Collecting activities

As activities são descobertas e conectadas em **tempo de compilação** pelo processador KSP **ktnip**. O [Functional DSL](Handlers#functional-dsl.md) é a única exceção — handlers definidos através de `bot.setFunctionality { ... }` são registrados em tempo de execução.

Se você quiser limitar a área em que o pacote será pesquisado, pode passar um parâmetro ao plugin:

```gradle
ktGram {
    packages = listOf("com.example.mybot")
}
```

ou sem plugin através do ksp:

```gradle
ksp {
    arg("package", "com.example.mybot")
}
```

note que, nesse caso, para que as ações coletadas sejam processadas corretamente, você também deve especificar o pacote na própria instância.

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.mybot")

    bot.handleUpdates()
    // start long-polling listener
}
```

essa opção foi adicionada para permitir a execução de múltiplas instâncias de bot:

```gradle
ktGram {
    packages = listOf("com.example.mybot", "com.example.mybot2")
}
```


ou, se você não estiver usando o plugin, para especificar pacotes diferentes você precisa declará-los com o separador `;`:

```gradle
ksp {
    arg("package", "com.example.mybot;com.example.mybot2")
}
```

### Processing

#### Webhooks

No seu controller (ou outro local onde o `webhook` é processado), você chama: [`bot.update.parseAndHandle(webhookString)`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.core/-tg-update-handler/index.html#706360827%2FFunctions%2F-880831646)

#### Long polling

Chame: `bot.handleUpdates()` ou através de `bot.update.setListener { handle(it) }`


### See also

* [Update parsing](Update-parsing.md)
* [Activity invocation](Activity-invocation.md)
* [Actions](Actions.md)

---