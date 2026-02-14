---
---
title: Functional Dsl
---

### Para ~~infinito~~ functional dsl e além!

O bot suporta configuração de contexto baseada em anotações e functional dsl. Você pode combinar ambas as abordagens.

### Functional DSL

Functional DSL é apenas uma forma diferente de definir o contexto do bot.

Exemplo:

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

### Comandos e Entradas

Você pode lidar com ambos `comandos` e `entradas` usando o functional DSL.

#### Comandos

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

    bot.setFunctionality {
        // Comando regular
        onCommand("/start") {
            message { "Hello" }.send(user, bot)
        }
        
        // Correspondência de comando baseada em regex
        onCommand("""(red|green|blue)""".toRegex()) {
            message { "you typed ${update.text} color" }.send(user, bot)
        }
    }
}
```

Em `onCommand`, os parâmetros analisados estão disponíveis como `Map<String, String>` com base na sua configuração.

#### Entradas

Você pode usar entradas via [`bot.inputListener`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot/-telegram-bot/input-listener.html).

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

    bot.setFunctionality {
        onCommand("/start") {
            message { "Hello, what's your name?" }.send(user, bot)
            bot.inputListener[user] = "testInput"
        }
        
        onInput("testInput") {
            message { "Hey, nice to meet you, ${update.text}" }.send(user, bot)
        }
    }
}
```

#### Cadeias de Entrada

Para fluxos de entrada de vários passos, use `inputChain`:

```kotlin
bot.setFunctionality {
    inputChain("conversation") {
        message { "Nice to meet you, ${update.text}" }.send(user, bot)
        message { "What is your favorite food?" }.send(user, bot)
    }.breakIf({ update.text == "peanut butter" }) { // condição de quebra da cadeia
        message { "Oh, too bad, I'm allergic to it." }.send(user, bot)
        // ação que será aplicada quando a condição corresponder
    }.andThen {
        // próximo ponto de entrada se a condição de quebra não corresponder
        message { "Great choice!" }.send(user, bot)
    }
}
```

A cadeia avança automaticamente para a próxima etapa, a menos que uma condição de quebra seja atendida. Se uma condição de quebra corresponder e `repeat` for `true` (padrão), o usuário permanece no passo atual.

#### Manipuladores de Tipo de Atualização

Manipule tipos específicos de atualização diretamente:

```kotlin
bot.setFunctionality {
    onUpdate(UpdateType.MESSAGE, UpdateType.CALLBACK_QUERY) {
        // Manipula atualizações de mensagem e callback query
        println("Received update: ${update.type}")
    }
}
```

#### Correspondências Comuns

Corresponda conteúdo de texto (não apenas comandos) usando `common`:

```kotlin
bot.setFunctionality {
    // Correspondência de string
    common("hello") {
        message { "Hi there!" }.send(user, bot)
    }
    
    // Correspondência de regex
    common("""\d+""".toRegex()) {
        message { "You sent a number!" }.send(user, bot)
    }
}
```

#### Manipulador de Fallback

Manipule atualizações que não foram processadas por nenhum manipulador:

```kotlin
bot.setFunctionality {
    whenNotHandled {
        message { "I didn't understand that." }.send(user, bot)
    }
}
```

### Configuração Avançada

#### Rate Limiting

Aplique limites de taxa a qualquer manipulador:

```kotlin
bot.setFunctionality {
    onCommand("/expensive", rateLimits = RateLimits(5, 60)) {
        // Este comando só pode ser chamado 5 vezes por 60 segundos
        message { "Processing..." }.send(user, bot)
    }
}
```

#### Guards

Use guards para adicionar lógica de validação personalizada:

```kotlin
bot.setFunctionality {
    onCommand("/admin", guard = AdminGuard::class) {
        message { "Admin command executed" }.send(user, bot)
    }
}
```

#### Análise de Argumentos

Personalize como os argumentos de comando são analisados:

```kotlin
bot.setFunctionality {
    onCommand("/custom", argParser = CustomArgParser::class) {
        // os parâmetros serão analisados usando CustomArgParser
        message { "Parameters: $parameters" }.send(user, bot)
    }
}
```

### Combinando Functional e Annotation-Based setting

Você pode usar ambas as abordagens no mesmo bot:

```kotlin
// Manipulador baseado em anotação
@CommandHandler(["/register"])
suspend fun register(ctx: CommandContext) {
    message { "Registration started" }.send(ctx.user, ctx.bot)
}

// Manipulador functional
bot.setFunctionality {
    onCommand("/help") {
        message { "Available commands: /register, /help" }.send(user, bot)
    }
}
```

Ambos os manipuladores são registrados no mesmo `ActivityRegistry` e funcionam perfeitamente juntos.

### Consulte também

* [Action](Actions.md)
* [Useful utilities](Useful-utilities-and-tips.md)
---