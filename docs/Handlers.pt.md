---
---
title: Handlers
---


### Variety of Handlers

No desenvolvimento de bots, especialmente em sistemas que envolvem interações com usuários, é crucial gerenciar e processar comandos e eventos de forma eficiente.

Essas anotações marcam funções projetadas para processar comandos, entradas ou atualizações específicas e fornecem metadados como palavras‑chave de comando, escopos e guardas.

### Annotations Overview

#### CommandHandler

A anotação `CommandHandler` é usada para marcar funções que processam comandos específicos. Esta anotação inclui propriedades que definem as palavras‑chave e os escopos do comando.

-   **value**: Especifica as palavras‑chave associadas ao comando.
-   **scope**: Determina o contexto ou escopo no qual o comando será verificado.

```kotlin
@CommandHandler(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommandHandler.CallbackQuery

Uma versão especializada da anotação `CommandHandler` projetada especificamente para lidar com consultas de callback. Inclui propriedades semelhantes às de `CommandHandler`, com foco em comandos relacionados a callbacks.

_É na verdade o mesmo que apenas `@CommandHandler` com um escopo pré‑definido `UpdateType.CALLBACK_QUERY`._

-   **value**: Especifica as palavras‑chave associadas ao comando.
-   **autoAnswer**: Responde ao `callbackQuery` automaticamente (chama `answerCallbackQuery` antes de processar).


```kotlin
@CommandHandler.CallbackQuery(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### CommonHandler

A anotação `CommonHandler` destina‑se a funções que processam comandos com prioridade menor em comparação com `CommandHandler` e `InputHandler`. É usada ao nível de fonte e oferece uma forma flexível de definir manipuladores de comando comuns.

**Esteja ciente de que a prioridade funciona apenas dentro de `@CommonHandler` (ou seja, não afeta outros manipuladores).**

##### CommonHandler.Text

Esta anotação especifica correspondência de texto contra atualizações. Inclui propriedades para definir o texto a ser correspondido, condições de filtragem, prioridade e escopo.

-   **value**: O texto a ser correspondido contra as atualizações recebidas.
-   **filter**: Uma classe que define condições usadas no processo de correspondência.
-   **priority**: O nível de prioridade do manipulador, onde 0 é a prioridade mais alta.
-   **scope**: O contexto ou escopo no qual a correspondência de texto será verificada.

```kotlin
@CommonHandler.Text(["text"], filter = isNewUserFilter::class, priority = 10)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommonHandler.Regex

Semelhante ao `CommonHandler.Text`, esta anotação é usada para corresponder atualizações com base em expressões regulares. Inclui propriedades para definir o padrão regex, opções, condições de filtragem, prioridade e escopo.

-   **value**: O padrão regex usado para correspondência.
-   **options**: Opções de regex que modificam o comportamento do padrão.
-   **filter**: Uma classe que define condições usadas no processo de correspondência.
-   **priority**: O nível de prioridade do manipulador, onde 0 é a prioridade mais alta.
-   **scope**: O contexto ou escopo no qual a correspondência regex será verificada.

```kotlin
@CommonHandler.Regex("^\d+$", scope = [UpdateType.EDITED_MESSAGE])
suspend fun test(update: EditedMessageUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### InputHandler

A anotação `InputHandler` marca funções que processam eventos de entrada específicos. Destina‑se a funções que tratam entradas em tempo de execução e inclui propriedades para definir palavras‑chave de entrada e escopos.

-   **value**: Especifica as palavras‑chave associadas ao evento de entrada.

```kotlin
@InputHandler("text")
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UnprocessedHandler

A anotação `UnprocessedHandler` é usada para marcar funções que tratam atualizações não processadas por outros manipuladores. Garante que quaisquer atualizações não processadas sejam gerenciadas adequadamente, com apenas um ponto de processamento possível para esse tipo de manipulador.

```kotlin
@UnprocessedHandler
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UpdateHandler

A anotação `UpdateHandler` marca funções que tratam tipos específicos de atualizações recebidas. Ela fornece uma maneira de categorizar e processar diferentes tipos de atualização de forma sistemática.

-   **type**: Especifica os tipos de atualizações que a função manipuladora processará.
-   **messageKind** *(added in 9.5)*: Conjunto opcional de [`MessageKind`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-message-kind/index.html)s que restringem o despacho a atualizações que contenham mensagem cujo tipo detectado corresponda. Vazio (padrão) significa que qualquer tipo corresponde.

```kotlin
@UpdateHandler([UpdateType.PRE_CHECKOUT_QUERY])
suspend fun test(update: PreCheckoutQueryUpdate, user: User, bot: TelegramBot) {
    //...
}
```

##### Filtering by `MessageKind`

Use o parâmetro `messageKind` para reagir apenas a um subconjunto específico de atualizações de mensagem (fotos, texto, eventos de serviço, …) em vez de inspecionar campos opcionais manualmente:

```kotlin
@UpdateHandler(type = [UpdateType.MESSAGE], messageKind = [MessageKind.PHOTO])
suspend fun onPhoto(update: MessageUpdate, bot: TelegramBot) {
    //...
}
```
### Handler Companion Annotations

Existem também anotações adicionais que são opcionais para os manipuladores, complementando o comportamento opcional dos próprios manipuladores.

Elas podem ser colocadas tanto em funções às quais um manipulador é aplicado quanto em classes; neste último caso serão aplicadas automaticamente a todos os manipuladores da classe, mas se necessário é possível ter comportamento separado para algumas funções.

Ou seja, a aplicação tem essa prioridade, `Function` > `Class`, onde a função tem prioridade mais alta.

#### Rate Limiting

Além disso, vamos também expor o mecanismo de limitação de taxa descrito nas anotações.

Você pode definir limites gerais para cada usuário:

```kotlin
// ...
val bot = TelegramBot("BOT_TOKEN") {
    rateLimiter { // general limits
        limits = RateLimits(period = 10000, rate = 5)
    }
}
```

###### Handler specific

Limites em determinadas ações podem ser definidos usando a anotação `RateLimits`, suportada por `@CommandHandler`, `@CommandHandler.CallbackQuery`, `@InputHandler`, `@CommonHandler`.

```kotlin
@CommandHandler(["/start"])
@RateLimits(period = 1000L, rate = 1L)
suspend fun start(user: User, bot: TelegramBot) {
    // ...
}
```

#### Guard

Você pode definir guardas separadamente para controlar o acesso aos manipuladores, suportado por `@CommandHandler`, `@CommandHandler.CallbackQuery`, `@InputHandler` :

```kotlin
@CommandHandler(["text"])
@Guard(isAdminGuard::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### ArgParser

Você pode definir um analisador de argumentos personalizado separadamente para mudar o comportamento da análise de parâmetros para os manipuladores, suportado por `@CommandHandler`, `@CommandHandler.CallbackQuery`, `@CommonHandler`:

```kotlin
@CommandHandler(["text"])
@ArgParser(SpaceArgParser::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

**see also [`defaultArgParser`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.common/default-arg-parser.html)**

### Functional DSL

Cada anotação acima tem um equivalente na **Functional DSL**, uma forma alternativa de declarar manipuladores em tempo de execução via `bot.setFunctionality { … }`. Ambas abordagens compartilham o mesmo `ActivityRegistry` e podem ser combinadas livremente no mesmo bot.

| Annotation | DSL counterpart |
|------------|-----------------|
| `@CommandHandler` | `onCommand(...)` |
| `@CommandHandler.CallbackQuery` | `onCommand(..., scope = [UpdateType.CALLBACK_QUERY])` |
| `@InputHandler` / input chains | `onInput(...)` / `inputChain(...)` |
| `@CommonHandler` | `common(...)` |
| `@UpdateHandler` | `onUpdate(...)` |
| `@UnprocessedHandler` | `whenNotHandled { ... }` |

Exemplo mínimo:

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

    bot.setFunctionality {
        onChosenInlineResult {
            println("got a result ${update.chosenInlineResult.resultId} from ${update.user}")
        }
    }
}
```

### Commands

```kotlin
bot.setFunctionality {
    // Regular command
    onCommand("/start") {
        message { "Hello" }.send(user, bot)
    }

    // Regex-based command matching
    onCommand("""(red|green|blue)""".toRegex()) {
        message { "you typed ${update.text} color" }.send(user, bot)
    }
}
```

Dentro de um bloco `onCommand`, os parâmetros analisados estão disponíveis como `Map<String, String>` configurados pela configuração ativa `commandParsing`.

### Inputs

```kotlin
bot.setFunctionality {
    onCommand("/start") {
        message { "Hello, what's your name?" }.send(user, bot)
        bot.inputListener[user] = "testInput"
    }

    onInput("testInput") {
        message { "Hey, nice to meet you, ${update.text}" }.send(user, bot)
    }
}
```

Veja [`bot.inputListener`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot/-telegram-bot/input-listener.html) para a API de armazenamento.

#### Input chains

Para fluxos de entrada de múltiplas etapas use `inputChain`:

```kotlin
bot.setFunctionality {
    inputChain("conversation") {
        message { "Nice to meet you, ${update.text}" }.send(user, bot)
        message { "What is your favorite food?" }.send(user, bot)
    }.breakIf({ update.text == "peanut butter" }) {     // chain break condition
        message { "Oh, too bad, I'm allergic to it." }.send(user, bot)
    }.andThen {
        // next step when the break condition didn't match
        message { "Great choice!" }.send(user, bot)
    }
}
```

A cadeia avança automaticamente a menos que uma condição de interrupção seja correspondida; quando `repeat = true` (padrão), uma interrupção correspondida mantém o usuário na etapa atual.

> For richer multi-step flows with typed state and validation, prefer the [`@WizardHandler`](FSM-and-Conversation-handling.md) instead.

### Update type handlers

```kotlin
bot.setFunctionality {
    onUpdate(UpdateType.MESSAGE, UpdateType.CALLBACK_QUERY) {
        println("Received update: ${update.type}")
    }
}
```

### Common matchers

```kotlin
bot.setFunctionality {
    common("hello") {
        message { "Hi there!" }.send(user, bot)
    }

    common("""\d+""".toRegex()) {
        message { "You sent a number!" }.send(user, bot)
    }
}
```

### Fallback handler

```kotlin
bot.setFunctionality {
    whenNotHandled {
        message { "I didn't understand that." }.send(user, bot)
    }
}
```

### Companion options

Limites de taxa, guardas e analisadores de argumentos são passados diretamente como parâmetros nomeados em vez de anotações separadas:

```kotlin
bot.setFunctionality {
    onCommand("/expensive", rateLimits = RateLimits(rate = 5, period = 60_000)) {
        message { "Processing..." }.send(user, bot)
    }

    onCommand("/admin", guard = AdminGuard::class) {
        message { "Admin command executed" }.send(user, bot)
    }

    onCommand("/custom", argParser = CustomArgParser::class) {
        message { "Parameters: $parameters" }.send(user, bot)
    }
}
```

### Combining DSL and annotations

Os dois estilos coexistem — registram da mesma forma, despacham da mesma forma:

```kotlin
@CommandHandler(["/register"])
suspend fun register(user: User, bot: TelegramBot) {
    message { "Registration started" }.send(user, bot)
}

bot.setFunctionality {
    onCommand("/help") {
        message { "Available commands: /register, /help" }.send(user, bot)
    }
}
```

### Conclusion

Essas anotações fornecem ferramentas robustas e flexíveis para lidar com comandos, entradas e eventos, permitindo configurações separadas de limites de taxa e guardas, aprimorando a estrutura geral e a manutenibilidade do desenvolvimento de bots.

### See also

* [Activities & Processors](Activites-and-Processors.md)
* [Activity invocation](Activity-invocation.md)
* [FSM and Conversation handling](FSM-and-Conversation-handling.md)
* [Sessions](Sessions.md)
* [Update parsing](Update-parsing.md)

---