---
---
title: Ações
---

### Todas as requisições são Ações
Todas as requisições da API do Telegram são diferentes tipos de interfaces [`TgAction`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.action/-tg-action/index.html) que implementam diferentes métodos como [`SendMessageAction`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.api.message/-send-message-action/index.html), <br/>que foram encapsulados na forma de funções do tipo [`message()`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.api.message/message.html) para a conveniência da interface da biblioteca.

<p align="center">
    <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/2d097d60-1907-4ca1-8ad3-3ee8d223f8eb" alt="Diagrama de Ações" />
</p>

Cada `Action` pode ter seus próprios métodos possíveis, dependendo das [`Feature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-feature/index.html) disponíveis.

### Recursos

Diferentes ações podem ter diferentes [`Features`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-feature/index.html) dependendo da API do Bot do Telegram, como:
[`OptionsFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-options-feature/index.html),
[`MarkupFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-markup-feature/index.html)
[`EntitiesFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-entities-feature/index.html)
[`CaptionFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-caption-feature/index.html).

Vamos dar uma olhada mais de perto neles:

### Opções
Por exemplo, [`OptionsFeature`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.features/-options-feature/index.html) é usado para passar parâmetros opcionais.

Cada ação tem seu próprio tipo de opções, que você pode ver na própria `Action` no parâmetro `options`, na seção de propriedades. <br/>Por exemplo, `sendMessage` que contém uma classe de dados [`MessageOptions`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.options/-message-options/index.html) com diferentes parâmetros como opções.

Exemplo de uso:

```kotlin
message{ "*Test*" }.options {
    parseMode = ParseMode.Markdown
}.send(user, bot)
```
### Markup

Também há um método para enviar markups que suporta todos os tipos de [teclados](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.marker/-keyboard/index.html): <br/>[`ReplyKeyboardMarkup`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-reply-keyboard-markup/index.html), [`InlineKeyboardMarkup`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-inline-keyboard-markup/index.html), [`ForceReply`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-force-reply/index.html), [`ReplyKeyboardRemove`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.keyboard/-reply-keyboard-remove/index.html).

#### Inline Keyboard Markup

Este construtor permite que você construa botões inline com qualquer combinação de parâmetros.

```kotlin
message{ "Test" }.inlineKeyboardMarkup {
    "name" callback "callbackData"         //
    "buttonName" url "https://google.com"  //--- estes dois botões estarão na mesma linha.
    newLine() // ou br()
    "otherButton" webAppInfo "data"       // este estará em outra linha

    // você também pode usar um estilo diferente dentro do construtor:
    callbackData("buttonName") { "callbackData" }
}.send(user, bot)

```

Mais detalhes podem ser vistos na documentação do construtor [documentation](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.builders/-inline-keyboard-markup-builder/index.html).

#### Reply Keyboard Markup

Este construtor permite que você construa botões de menu.

```kotlin
message{ "Test" }.replyKeyboardMarkup {
  + "Menu button"     // você pode adicionar botões usando o operador de soma unário
  + "Menu button 2"
  br() // vá para a segunda linha
  "Send polls 👀" requestPoll true   // botão com parâmetro

  options {
    resizeKeyboard = true
  }
}.send(user, bot)
```

Opções adicionais aplicáveis ao teclado podem ser vistas em [`ReplyKeyboardMarkupOptions`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.options/-reply-keyboard-markup-options/index.html).

Veja a documentação do construtor [documentation](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.builders/-reply-keyboard-markup-builder/index.html) para mais detalhes sobre os métodos.

É geralmente conveniente usar dsl para coletar markup do teclado, mas se necessário, você também pode adicionar markup manualmente.

```kotlin
message{ "*Test*" }.markup {
    InlineKeyboardMarkup(
        InlineKeyboardButton("test", callbackData = "testCallback")
    )
}.send(user, bot)

```

```kotlin
message{ "*Test*" }.markup {
    ReplyKeyboardMarkup(
        KeyboardButton("Test menu button")
    )
}.send(user, bot)
```

### Entities
Também há um método para enviar [`MessageEntity`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.msg/-message-entity/index.html).

Exemplo de uso:

```kotlin
message{ "Test \$hello" }.replyKeyboardMarkup {
    +"Test menu button"
}.entities {
    5 to 15 url "https://google.com" // adicione TextLink
    entity(EntityType.Bold, 0, 4)
    entity(EntityType.Cashtag, 5, 5) // a contrabarra não conta (porque é usada para o compilador)
}.send(user, bot)
```

#### Entities contextuais.

Entities também podem ser adicionadas através do contexto de algumas construções, elas são rotuladas com uma interface específica [EntitiesContextBuilder](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.utils.builders/-entities-ctx-builder/index.html), que também está presente no recurso de legenda.

Exemplo de uso:

```kotlin
message { "usual text " - bold { "this is bold text" } - " continue usual" }.send(user, bot)
```

Todos os tipos de [entity types](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.msg/-entity-type/index.html) são suportados.

### Caption
Também, o método `caption` pode ser usado para adicionar legendas a arquivos de mídia.

Exemplo de uso:

```kotlin
photo { "FILE_ID" }.caption { "Test caption" }.send(user, bot)
```


### Veja também

* [Bot context](Bot-Context.md)
* [FSM | Conversation handling](FSM-and-Conversation-handling.md)