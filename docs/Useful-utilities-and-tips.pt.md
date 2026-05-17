---
---
title: Useful Utilities And Tips
---


### Operando com ProcessedUpdate

O [`ProcessedUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processed-update/index.html) é uma classe genérica para updates que, dependendo dos dados originais, pode ser fornecida em diferentes tipos ([`MessageUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-message-update/index.html), [`CallbackQueryUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-callback-query-update/index.html), etc.)

Então você pode verificar o tipo dos dados recebidos e manipular determinados dados com smartcasts, por exemplo:

```kotlin
// ...
if (update !is MessageUpdate) {
    message { "Only messages are allowed" }.send(user, bot)
    return
}
// Further on, ProcessedUpdate will be perceived as MessageUpdate.
```

Também existe uma interface [`UserReference`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-user-reference/index.html) que permite determinar se há uma referência de usuário dentro, caso de uso exemplo:

```kotlin
val user = if(update is UserReference) update.user else null

```

Se necessário, dentro dela sempre há o [`update`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types/-update/index.html) original no parâmetro de update.


### Injeção de dependência

A biblioteca usa um mecanismo simples para inicializar classes onde seus métodos de processamento de update são anotados com as anotações fornecidas.

[`ClassManagerImpl`](https://github.com/vendelieu/telegram-bot/blob/master/telegram-bot/src/commonMain/kotlin/eu/vendeli/tgbot/implementations/ClassManagerImpl.kt) é usado por padrão para invocar métodos anotados.

Mas se você quiser usar outras bibliotecas para isso, pode redefinir a interface [`ClassManager`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-manager/index.html), <br/>usando o mecanismo de sua preferência e passá‑lo ao inicializar o bot.

```kotlin
fun main() = runBlocking {
    val bot = TelegramBot("BOT_TOKEN", "com.example.controllers") {
        classManager = ClassManagerImpl()
    }

    bot.handleUpdates()
}
```

### Filtrando updates

Se não houver condições complexas, você pode simplesmente filtrar alguns updates para não serem processados:

```kotlin
// function where updates filtering condition defined
fun filteringFun(update: Update): Boolean = update.message?.text.isNullOrBlank()

fun main() = runBlocking {
  val bot = TelegramBot("BOT_TOKEN")

  // setting more specific processing flow for updates
  bot.update.setListener {
    if(filteringFun(it)) return@setListener

    // so simply, if the listener left the scope before reaching the handler function, that it is filtering.
    // actually you can even write directly if-condition there with return@setListener or extend filtering to separate class.

    handle(it) // or manual handling way with block
  }
}
```

para incluir filtragem na correspondência de comandos ou excluir processo, dê uma olhada em guards ou `@CommonHandler`.

### Generalizar opções para diferentes métodos

Se você precisa aplicar os mesmos parâmetros opcionais com frequência, pode escrever uma função semelhante que atenda às suas necessidades e reduzir o código boilerplate :)

Algumas propriedades comuns são separadas em [diferentes interfaces](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.options/-options/index.html).

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


// ... and in your code

message { "test" }.markdownMode().send(to, via)

```


---