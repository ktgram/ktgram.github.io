---
---
title: Interceptors (Middleware)
---

### Interceptors: Lógica Cross-Cutting para seu Bot

Ao construir um bot Telegram, você frequentemente repete configuração, verificações ou limpeza entre handlers. Os interceptors permitem que você insira lógica compartilhada ao redor dos handlers, mantendo-os focados e manuteníveis.

Aqui está como os interceptors funcionam no *telegram-bot* e como usá-los.

### O que são Interceptors? (Explicação Simples)

Interceptors são funções que executam em pontos específicos do pipeline de processamento de updates. Eles permitem que você:
- Inspecione e modifique o contexto de processamento
- Adicione lógica cross-cutting (logging, auth, métricas)
- Pare o processamento antecipadamente se necessário
- Limpe recursos após o processamento

Pense nos interceptors como checkpoints que todo update passa antes, durante e após a execução do handler.


### O Pipeline de Processamento

O bot processa updates através de um pipeline com sete fases:

| Fase | Quando é executado | Para que você pode usá-lo |
|-------|--------------|-------------------------|
| **Setup** | Assim que o update chega, antes de qualquer processamento | ✔ Rate limiting global<br>✔ Filtrar spam ou updates malformados<br>✔ Logging inicial<br>✔ Configurar contexto compartilhado |
| **Parsing** | Após o setup, extrai comando e parâmetros | ✔ Parsing de comandos customizado<br>✔ Enriquecer contexto com dados parseados<br>✔ Validar estrutura do update |
| **Match** | Encontra o handler apropriado (Command/Input/Common) | ✔ Sobrescrever seleção de handler<br>✔ Lógica customizada de input handling<br>✔ Log de handlers correspondidos |
| **Validation** | Após o handler ser encontrado, antes da invocação | ✔ Permissões específicas do handler<br>✔ Rate limiting por handler<br>✔ Guard checks<br>✔ Cancelar processamento se condições não forem atendidas |
| **PreInvoke** | Imediatamente antes do handler rodar | ✔ Últimas verificações<br>✔ Iniciar timers/métricas<br>✔ Enriquecer contexto para o handler<br>✔ Modificar comportamento do handler |
| **Invoke** | O handler é executado aqui | ✔ Wrapper na execução do handler<br>✔ Tratamento de erros<br>✔ Logging de resultados do handler |
| **PostInvoke** | Após o handler completar (sucesso ou falha) | ✔ Limpar recursos<br>✔ Log de resultados<br>✔ Enviar mensagens de fallback em erros<br>✔ Modificar resultados antes de retornar |


### Criando um Interceptor

Um interceptor é uma função simples que recebe um `ProcessingContext`:

```kotlin
import eu.vendeli.tgbot.core.PipelineInterceptor
import eu.vendeli.tgbot.types.component.ProcessingContext

val myInterceptor: PipelineInterceptor = { context ->
    // Sua lógica aqui
    println("Processing update: ${context.update.updateId}")
}
```

Ou usando lambda:

```kotlin
val loggingInterceptor = PipelineInterceptor { context ->
    val logger = context.bot.config.loggerFactory.get("MyInterceptor")
    logger.info("Processing update #${context.update.updateId}")
}
```


### Registrando Interceptors

Registre interceptors no pipeline de processamento:

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

    // Registra um interceptor para a fase Setup
    bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
        // Verifica se usuário está banido
        val user = context.update.userOrNull
        if (user != null && isBanned(user.id)) {
            context.finish() // Para processamento
            return@intercept
        }
    }

    // Registra um interceptor para a fase PreInvoke
    bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
        val startTime = System.currentTimeMillis()
        // store start time
    }

    // Registra um interceptor para a fase PostInvoke
    bot.update.pipeline.intercept(ProcessingPipePhase.PostInvoke) { context ->
        val startTime = // get start time
        if (startTime != null) {
            val duration = System.currentTimeMillis() - startTime
            println("Handler took ${duration}ms")
        }
    }

    bot.handleUpdates()
}
```

### Exemplo Real: Autenticação & Métricas

Exemplo: um bot que requer autenticação para certos comandos, mede tempo de execução dos handlers e loga todos os comandos.

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

    // Fase Setup: Verifica se usuário está autenticado
    bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
        val user = context.update.userOrNull ?: return@intercept

        if (!isAuthenticated(user.id)) {
            message { "Please authenticate first using /login" }
                .send(user, context.bot)
            context.finish()
        }
    }

    // Fase PreInvoke: Inicia timer e verifica permissões
    bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
        val activity = context.activity ?: return@intercept
        val user = context.update.userOrNull ?: return@intercept

        // Verifica se usuário tem permissão para este handler específico
        if (!hasPermission(user.id, activity)) {
            message { "You don't have permission to use this command." }
                .send(user, context.bot)
            context.finish()
            return@intercept
        }

        // Iniciar timer
        // store start time
    }

    // Fase PostInvoke: Log e cleanup
    bot.update.pipeline.intercept(ProcessingPipePhase.PostInvoke) { context ->
        val activity = context.activity ?: return@intercept
        val startTime = // get start time

        if (startTime != null) {
            val duration = System.currentTimeMillis() - startTime
            val logger = context.bot.config.loggerFactory.get("Metrics")
            logger.info(
                "Handler ${activity::class.simpleName} took ${duration}ms " +
                "for user ${context.update.userOrNull?.id}"
            )
        }
    }

    bot.handleUpdates()
}
```


### ProcessingContext

O `ProcessingContext` fornece acesso a:

- **`update: ProcessedUpdate`** - O update atual sendo processado
- **`bot: TelegramBot`** - A instância do bot
- **`registry: ActivityRegistry`** - O registry de activities
- **`parsedInput: String`** - O texto parseado de comando/input
- **`parameters: Map<String, String>`** - Parâmetros do comando parseados
- **`activity: Activity?`** - O handler resolvido (null até a fase Match)
- **`shouldProceed: Boolean`** - Se o processamento deve continuar
- **`additionalContext: AdditionalContext`** - Dados de contexto adicionais
- **`finish()`** - Para processamento antecipadamente

#### Parando Processamento Antecipadamente

Chame `context.finish()` para parar processamento:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.Validation) { context ->
    if (someCondition) {
        context.finish() // Nenhuma fase posterior será executada
    }
}
```

#### Armazenando Dados Customizados

Use `additionalContext` para passar dados entre interceptors:

```kotlin
// No PreInvoke
context.additionalContext["userId"] = context.update.userOrNull?.id

// No PostInvoke
val userId = context.additionalContext["userId"] as? Long
```


### Múltiplos Interceptors

Você pode registrar múltiplos interceptors para a mesma fase. Eles executam na ordem de registro:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    println("First interceptor")
}

bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    println("Second interceptor")
}

// Quando um update é processado:
// Output: "First interceptor"
// Output: "Second interceptor"
```

Se um interceptor chama `context.finish()`, interceptors subsequentes naquela fase são pulados, e fases posteriores não serão executadas.


### Boas Práticas

#### 1. Use a Fase Correta

- Setup: Verificações globais, filtragem, configuração inicial
- Parsing: Lógica de parsing customizada
- Match: Lógica de seleção de handler
- Validation: Permissões, rate limits, guards
- PreInvoke: Preparação específica do handler
- Invoke: Geralmente manipulado pelo interceptor padrão
- PostInvoke: Cleanup, logging, tratamento de erros

#### 2. Mantenha Interceptors Focados

Cada interceptor deve fazer uma coisa:

```kotlin
// ✅ Bom - interceptor focado
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    if (isBanned(context.update.userOrNull?.id)) {
        context.finish()
    }
}

// ❌ Evite - fazendo muito
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    // Autenticação
    // Logging
    // Métricas
    // Rate limiting
    // ... muito!
}
```

#### 3. Trate Erros Graciosamente

Interceptors não devem quebrar o bot:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
    try {
        // Sua lógica
    } catch (e: Exception) {
        val logger = context.bot.config.loggerFactory.get("Interceptor")
        logger.error("Interceptor error", e)
        // Não chame context.finish() a menos que queira parar processamento
    }
}
```

#### 4. Limpe Recursos

Se você abre recursos no `PreInvoke`, limpe-os no `PostInvoke`:

```kotlin
var timer: Timer? = null

bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
    timer = Timer()
    context.additionalContext["timer"] = timer
}

bot.update.pipeline.intercept(ProcessingPipePhase.PostInvoke) { context ->
    val timer = context.additionalContext["timer"] as? Timer
    timer?.stop()
}
```

#### 5. Ordem Importa

Registre interceptors na ordem que você quer que eles executem:

```kotlin
// Verificações mais gerais primeiro
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) {
    // Verificação global de ban
}

// Verificações mais específicas depois
bot.update.pipeline.intercept(ProcessingPipePhase.Validation) {
    // Verificação de permissão específica do handler
}
```

#### 6. Use Interceptors para Cross-Cutting Concerns

Interceptors são ideais para:
- ✅ Autenticação/autorização
- ✅ Logging
- ✅ Monitoramento de métricas/performance
- ✅ Rate limiting
- ✅ Tratamento de erros
- ✅ Transformação de request/response

Para lógica específica do handler, mantenha no handler.


### Interceptors Padrão

O framework inclui interceptors padrão para funcionalidade core:

- **DefaultSetupInterceptor**: Rate limiting global
- **DefaultParsingInterceptor**: Parsing de comandos
- **DefaultMatchInterceptor**: Matching de handlers (commands, inputs, common matchers)
- **DefaultValidationInterceptor**: Guard checks e rate limiting por handler
- **DefaultInvokeInterceptor**: Execução de handler e tratamento de erros

Seus interceptors customizados rodam ao lado desses defaults. Você pode adicionar lógica antes ou depois dos defaults, mas não pode remover os interceptors padrão.

---

### Avançado: Interceptors Condicionais

Você pode tornar interceptors condicionais:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
    val activity = context.activity ?: return@intercept

    // Apenas aplicar a handlers específicos
    if (activity::class.simpleName?.contains("Admin") == true) {
        // Lógica específica de admin
        checkAdminPermissions(context)
    }
}
```


### Resumo

Interceptors fornecem uma maneira limpa de adicionar lógica cross-cutting ao seu bot:

- ✅ **Sete fases** para diferentes estágios de processamento
- ✅ **API simples**: Basta implementar `PipelineInterceptor`
- ✅ **Flexível**: Registre múltiplos interceptors por fase
- ✅ **Poderoso**: Acesso ao contexto completo de processamento
- ✅ **Seguro**: Pode parar processamento antecipadamente com `context.finish()`

Use interceptors para manter seus handlers focados na lógica de negócio enquanto lida com preocupações compartilhadas como autenticação, logging e métricas de forma centralizada.

---

### Veja também

* [Functional Handling DSL](Functional-handling-DSL.md) - Processamento de updates funcional
* [Guards](Guards.md) - Verificações de permissão no nível do handler
---