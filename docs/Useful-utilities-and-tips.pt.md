---
---
title: Utilitários Úteis e Dicas
---


### Operando com ProcessedUpdate

A [`ProcessedUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processed-update/index.html) é uma classe genérica para atualizações que, dependendo dos dados originais, podem ser fornecidas em diferentes tipos ([`MessageUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-message-update/index.html), [`CallbackQueryUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-callback-query-update/index.html), etc.)

Assim você pode verificar o tipo de dados de entrada e manipular posteriormente certos dados com smartcasts, por exemplo:

```kotlin
// ...
if (update !is MessageUpdate) {
    message { "Only messages are allowed" }.send(user, bot)
    return
}
// Posteriormente, ProcessedUpdate será percebido como MessageUpdate.
```

Também existe uma interface [`UserReference`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-user-reference/index.html) dentro que permite determinar se há uma referência de usuário dentro, exemplo de caso de uso:

```kotlin
val user = if(update is UserReference) update.user else null

```

Se necessário, dentro há sempre a original [`update`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types/-update/index.html) no parâmetro de atualização.


### Injeção de dependência

A biblioteca usa um mecanismo simples para inicializar classes onde seus métodos de processamento de atualização são anotados com as anotações fornecidas.

[`ClassManagerImpl`](https://github.com/vendelieu/telegram-bot/blob/master/telegram-bot/src/commonMain/kotlin/eu/vendeli/tgbot/implementations/ClassManagerImpl.kt) é usado por padrão para invocar métodos anotados.

Mas se você quiser usar algumas outras bibliotecas para isso, você pode redefinir a interface [`ClassManager`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-manager/index.html), <br/>usando seu mecanismo preferido e passá-lo ao inicializar o bot.

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.controllers") {
        classManager = ClassManagerImpl()
    }

    bot.handleUpdates()
}
```

### Filtrando atualizações

Se não houver condições complexas, você pode simplesmente filtrar algumas atualizações para serem processadas:

```kotlin
// função onde a condição de filtragem de atualizações é definida
fun filteringFun(update: Update): Boolean = update.message?.text.isNullOrBlank()

fun main() = runBlocking {
  val bot = TelegramBot("BOT_TOKEN")

  // definindo um fluxo de processamento mais específico para atualizações
  bot.update.setListener {
    if(filteringFun(it)) return@setListener

    // então simplesmente, se o listener saiu do escopo antes de alcançar a função handler, ele está filtrando.
    // na verdade você pode até escrever diretamente a condição if lá com return@setListener ou estender o filtro para uma classe separada.

    handle(it) // ou maneira manual de manipulação com bloco
  }
}
```

para incluir filtragem no seu processo de correspondência ou exclusão de comando, dê uma olhada nos guards ou `@CommonHandler`.

### Generalizar opções para diferentes métodos

Se você tiver que aplicar os mesmos parâmetros opcionais com frequência, você pode escrever uma função similar que atenda você e aliviar o código boilerplate :)

Algumas propriedades comuns são separadas para [diferentes interfaces](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.options/-options/index.html).

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


// ... e no seu código

message { "test" }.markdownMode().send(to, via)

```