---
---
title: Atividades e Processadores
---

### Introdução

`Activity` nesta biblioteca é a entidade abstrata que é uma generalização de entidades como `@CommandHandler`, `@InputHandler`, `@UnprocessedHandler` e `@CommonHandler`.

Também dê uma olhada no [artigo sobre handlers](Handlers.md).

### Coletando atividades

As atividades são coletadas e todo o contexto preparado em tempo de compilação (exceto aquelas definidas através do DSL funcional).

Se você quiser limitar a área em que o pacote será pesquisado, pode passar um parâmetro para o plugin:

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

note que nesse caso, para que as ações coletadas sejam processadas corretamente, você também deve especificar o pacote na própria instância.

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.mybot")

    bot.handleUpdates()
    // inicia o listener de long-polling
}
```

esta opção foi adicionada para poder executar múltiplas instâncias do bot:

```gradle
ktGram {
    packages = listOf("com.example.mybot", "com.example.mybot2")
}
```


ou se você não estiver usando plugin para especificar pacotes diferentes, precisa especificá-los com separador `;`:

```gradle
ksp {
    arg("package", "com.example.mybot;com.example.mybot2")
}
```

### Processamento

#### Webhooks

No seu controller (ou outro lugar onde o `webhook` é processado), você chama: [`bot.update.parseAndHandle(webhookString)`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.core/-tg-update-handler/index.html#706360827%2FFunctions%2F-880831646)

#### Long polling

Chame: `bot.handleUpdates()` ou através de `bot.update.setListener { handle(it) }`


### Veja também

* [Parsing de updates](Update-parsing.md)
* [Invocation de atividades](Activity-invocation.md)
* [Ações](Actions.md)