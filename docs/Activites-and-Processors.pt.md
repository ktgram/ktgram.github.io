---
---
title: Atividades e Processadores
---

### Introdução

`Activity` nos termos desta biblioteca é a entidade abstrata que é uma generalização de entidades como `@CommandHandler`, `@InputHandler`, `@UnprocessedHandler` e `@CommonHandler`.

Além disso, dê uma olhada no [artigo sobre handlers](Handlers.md).

### Coletando atividades

As atividades são coletadas e preparadas todo o contexto em tempo de compilação (exceto aquelas definidas através de DSL funcional).

Se você quiser limitar a área na qual o pacote será pesquisado, você pode passar um parâmetro para o plugin:

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

esta opção foi adicionada para poder executar múltiplas instâncias de bot:

```gradle
ktGram {
    packages = listOf("com.example.mybot", "com.example.mybot2")
}
```


ou se você não estiver usando plugin para especificar pacotes diferentes, você precisa especificá-los com o separador `;`:

```gradle
ksp {
    arg("package", "com.example.mybot;com.example.mybot2")
}
```

### Processamento

#### Webhooks

No seu controlador (ou outro lugar onde o `webhook` é processado), você chama: [`bot.update.parseAndHandle(webhookString)`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.core/-tg-update-handler/index.html#706360827%2FFunctions%2F-880831646)

#### Long polling

Chame: `bot.handleUpdates()` ou através de `bot.update.setListener { handle(it) }`


### Veja também

* [Parsing de atualizações](Update-parsing.md)
* [Invocação de atividade](Activity-invocation.md)
* [Ações](Actions.md)

---