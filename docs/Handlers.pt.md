---
---
title: Handlers
---


### Variedade de Handlers

No desenvolvimento de bots, particularmente em sistemas envolvendo interações com usuários, é crucial gerenciar e processar comandos e eventos de forma eficiente.

Estas anotações marcam funções projetadas para processar comandos, entradas ou atualizações específicas e fornecem metadados como palavras-chave de comando, escopos e guardas.

### Visão Geral das Anotações

#### CommandHandler

A anotação `CommandHandler` é usada para marcar funções que processam comandos específicos. Esta anotação inclui propriedades que definem as palavras-chave e escopos do comando.

-   **value**: Especifica as palavras-chave associadas ao comando.
-   **scope**: Determina o contexto ou escopo em que o comando será verificado.

```kotlin
@CommandHandler(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommandHandler.CallbackQuery

Uma versão especializada da anotação `CommandHandler` projetada especificamente para lidar com callback queries. Ela inclui propriedades semelhantes ao `CommandHandler`, com foco em comandos relacionados a callbacks.

_É, na verdade, a mesma coisa que apenas `@CommandHandler` com um escopo `UpdateType.CALLBACK_QUERY` pré-configurado_.

-   **value**: Especifica as palavras-chave associadas ao comando.
-   **autoAnswer**: Responde à `callbackQuery` automaticamente (chama `answerCallbackQuery` antes de processar).


```kotlin
@CommandHandler.CallbackQuery(["text"])
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### CommonHandler

A anotação `CommonHandler` destina-se a funções que processam comandos com prioridade menor em comparação com `CommandHandler` e `InputHandler`. Ela é usada no nível da fonte e fornece uma maneira flexível de definir handlers de comandos comuns.

**Esteja ciente de que a prioridade funciona apenas dentro dos próprios `@CommonHandler` (ou seja, não afeta outros handlers).**

##### CommonHandler.Text

Esta anotação especifica correspondência de texto contra atualizações. Ela inclui propriedades para definir o texto de correspondência, condições de filtragem, prioridade e escopo.

-   **value**: O texto a ser correspondido contra atualizações recebidas.
-   **filter**: Uma classe que define condições usadas no processo de correspondência.
-   **priority**: O nível de prioridade do handler, onde 0 é a prioridade mais alta.
-   **scope**: O contexto ou escopo em que a correspondência de texto será verificada.

```kotlin
@CommonHandler.Text(["text"], filter = isNewUserFilter::class, priority = 10)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

##### CommonHandler.Regex

Semelhante ao `CommonHandler.Text`, esta anotação é usada para corresponder atualizações com base em expressões regulares. Ela inclui propriedades para definir o padrão regex, opções, condições de filtragem, prioridade e escopo.

-   **value**: O padrão regex usado para correspondência.
-   **options**: Opções regex que modificam o comportamento do padrão regex.
-   **filter**: Uma classe que define condições usadas no processo de correspondência.
-   **priority**: O nível de prioridade do handler, onde 0 é a prioridade mais alta.
-   **scope**: O contexto ou escopo em que a correspondência regex será verificada.

```kotlin
@CommonHandler.Regex("^\d+$", scope = [UpdateType.EDITED_MESSAGE])
suspend fun test(update: EditedMessageUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### InputHandler

A anotação `InputHandler` marca funções que processam eventos de entrada específicos. Ela destina-se a funções que manipulam entradas em tempo de execução e inclui propriedades para definir palavras-chave de entrada e escopos.

-   **value**: Especifica as palavras-chave associadas ao evento de entrada.

```kotlin
@InputHandler("text")
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UnprocessedHandler

A anotação `UnprocessedHandler` é usada para marcar funções que lidam com atualizações não processadas por outros handlers. Ela garante que quaisquer atualizações não processadas sejam gerenciadas adequadamente, com apenas um ponto de processamento possível para este tipo de handler.

```kotlin
@UnprocessedHandler
suspend fun test(update: ProcessedUpdate, user: User, bot: TelegramBot) {
    //...
}
```

#### UpdateHandler

A anotação `UpdateHandler` marca funções que lidam com tipos específicos de atualizações recebidas. Ela fornece uma maneira de categorizar e processar diferentes tipos de atualizações de forma sistemática.

-   **type**: Especifica os tipos de atualizações que a função handler processará.

```kotlin
@UpdateHandler([UpdateType.PRE_CHECKOUT_QUERY])
suspend fun test(update: PreCheckoutQueryUpdate, user: User, bot: TelegramBot) {
    //...
}
```
### Anotações Companheiras de Handler

Também existem anotações adicionais que são opcionais para os handlers, complementando o comportamento opcional dos próprios handlers.

Elas podem ser colocadas tanto em funções para as quais um handler é aplicado quanto em classes, neste último caso elas serão automaticamente aplicadas a todos os handlers naquela classe, mas se houver necessidade é possível ter comportamento separado para algumas funções.

Ou seja, a aplicação tem tal prioridade: `Função` > `Classe`, onde a função tem prioridade mais alta.

#### Rate Limiting

Além disso, vamos também divulgar o mecanismo de rate limiting descrito nas anotações.

Você pode definir limites gerais para cada usuário:

```kotlin
// ...
val bot = TelegramBot("BOT_TOKEN") {
    rateLimiter { // limites gerais
        limits = RateLimits(period = 10000, rate = 5)
    }
}
```

###### Específico do Handler

Limites em certas ações podem ser definidos usando a anotação `RateLimits`, suportada por `@CommandHandler`, `@CommandHandler.CallbackQuery`, `@InputHandler`, `@CommonHandler`.

```kotlin
@CommandHandler(["/start"])
@RateLimits(period = 1000L, rate = 1L)
suspend fun start(user: User, bot: TelegramBot) {
    // ...
}
```

#### Guard

Você pode definir guardas separadamente para controlar o acesso aos handlers, suportado por `@CommandHandler`, `@CommandHandler.CallbackQuery`, `@InputHandler` :

```kotlin
@CommandHandler(["text"])
@Guard(isAdminGuard::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

#### ArgParser

Você pode definir um parser de argumentos personalizado separadamente para alterar o comportamento de análise de parâmetros para handlers, suportado por `@CommandHandler`, `@CommandHandler.CallbackQuery`, `@CommonHandler`:

```kotlin
@CommandHandler(["text"])
@ArgParser(SpaceArgParser::class)
suspend fun test(user: User, bot: TelegramBot) {
    //...
}
```

**veja também [`defaultArgParser`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.common/default-arg-parser.html)**

### Conclusão

Estas anotações fornecem ferramentas robustas e flexíveis para lidar com comandos, entradas e eventos, permitindo configurações separadas de rate limits e guardas, melhorando a estrutura geral e a manutenibilidade do desenvolvimento de bots.

### Veja também

* [Activities & Processors](Activites-and-Processors.md)
* [Activity invocation](Activity-invocation.md)
* [FSM and Conversation handling](FSM-and-Conversation-handling.md)
* [Update parsing](Update-parsing.md)
* [Aide](Aide.md)

---

MODO DE INTEGRIDADE ESTRUTURAL:

Você deve produzir uma saída que seja estruturalmente compatível em bytes com o Markdown de entrada.

Regras:
- O número de blocos de código deve corresponder exatamente.
- O número de headings deve corresponder exatamente.
- Todos os blocos de código delimitados devem permanecer inalterados.
- Todas as URLs devem permanecer idênticas.
- Todas as spans de código inline devem permanecer idênticas.
- Não mesclar ou dividir parágrafos.
- Não normalizar espaçamento.