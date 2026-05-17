---
---
title: Interceptors (Middleware)
---

### Interceptors: Cross-Cutting Logic for Your Bot

Ao construir um bot no Telegram, você costuma repetir configuração, verificações ou limpeza em vários handlers. Os interceptors permitem conectar lógica compartilhada ao redor dos handlers, mantendo-os focados e mais fáceis de manter.

Veja como os interceptors funcionam no *telegram-bot* e como usá‑los.

### What Are Interceptors? (Simple Explanation)

Interceptores são funções que são executadas em pontos específicos do pipeline de processamento de updates. Eles permitem que você:
- Inspecione e modifique o contexto de processamento
- Adicione lógica transversal (log, autenticação, métricas)
- Interrompa o processamento antecipadamente, se necessário
- Libere recursos após o processamento

Pense nos interceptors como checkpoints pelos quais cada update passa antes, durante e depois da execução do handler.

### The Processing Pipeline

O bot processa updates através de um pipeline com sete fases:

| Phase | When It Runs | What You Can Use It For |
|-------|--------------|-------------------------|
| **Setup** | Assim que o update chega, antes de qualquer processamento | ✔ Limitação global de taxa<br>✔ Filtrar spam ou updates malformados<br>✔ Log inicial<br>✔ Configurar contexto compartilhado |
| **Parsing** | Após o setup, extrai comando e parâmetros | ✔ Parsing customizado de comandos<br>✔ Enriquecer o contexto com dados analisados<br>✔ Validar a estrutura do update |
| **Match** | Encontra o handler apropriado (Command/Input/Common) | ✔ Sobrescrever a seleção de handler<br>✔ Lógica customizada de tratamento de entrada<br>✔ Log dos handlers correspondidos |
| **Validation** | Depois que o handler é encontrado, antes da invocação | ✔ Permissões específicas do handler<br>✔ Limitação de taxa por handler<br>✔ Verificações de guardas<br>✔ Cancelar o processamento se as condições não forem atendidas |
| **PreInvoke** | Imediatamente antes do handler ser executado | ✔ Verificações de última hora<br>✔ Iniciar timers/métricas<br>✔ Enriquecer o contexto para o handler<br>✔ Modificar o comportamento do handler |
| **Invoke** | O handler é executado aqui | ✔ Envolver a execução do handler<br>✔ Tratamento de erros<br>✔ Log dos resultados do handler |
| **PostInvoke** | Após a conclusão do handler (sucesso ou falha) | ✔ Limpar recursos<br>✔ Log dos resultados<br>✔ Enviar mensagens de fallback em caso de erro<br>✔ Modificar resultados antes de retornar |

### Creating an Interceptor

Um interceptor é uma função simples que recebe um `ProcessingContext`:

```kotlin
import eu.vendeli.tgbot.core.PipelineInterceptor
import eu.vendeli.tgbot.types.component.ProcessingContext

val myInterceptor: PipelineInterceptor = { context ->
    // Your logic here
    println("Processing update: ${context.update.updateId}")
}
```

Ou usando uma lambda:

```kotlin
val loggingInterceptor = PipelineInterceptor { context ->
    val logger = context.bot.config.loggerFactory.get("MyInterceptor")
    logger.info("Processing update #${context.update.updateId}")
}
```

### Registering Interceptors

Registre interceptors no pipeline de processamento:

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")
    
    // Register an interceptor for the Setup phase
    bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
        // Check if user is banned
        val user = context.update.userOrNull
        if (user != null && isBanned(user.id)) {
            context.finish() // Stop processing
            return@intercept
        }
    }
    
    // Register an interceptor for the PreInvoke phase
    bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
        val startTime = System.currentTimeMillis()
        // store start time
    }
    
    // Register an interceptor for the PostInvoke phase
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

### Real-World Example: Authentication & Metrics

Exemplo: um bot que exige autenticação para certos comandos, mede o tempo de execução dos handlers e registra todos os comandos.

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")
    
    // Setup phase: Check if user is authenticated
    bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
        val user = context.update.userOrNull ?: return@intercept
        
        if (!isAuthenticated(user.id)) {
            message { "Please authenticate first using /login" }
                .send(user, context.bot)
            context.finish()
        }
    }
    
    // PreInvoke phase: Start timer and check permissions
    bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
        val activity = context.activity ?: return@intercept
        val user = context.update.userOrNull ?: return@intercept
        
        // Check if user has permission for this specific handler
        if (!hasPermission(user.id, activity)) {
            message { "You don't have permission to use this command." }
                .send(user, context.bot)
            context.finish()
            return@intercept
        }
        
        // Start timer
        // store start time
    }
    
    // PostInvoke phase: Log and cleanup
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
- **`registry: ActivityRegistry`** - O registro de activities
- **`parsedInput: String`** - O texto do comando/entrada analisado
- **`parameters: Map<String, String>`** - Parâmetros de comando analisados
- **`activity: Activity?`** - O handler resolvido (null até a fase Match)
- **`shouldProceed: Boolean`** - Se o processamento deve continuar
- **`additionalContext: AdditionalContext`** - Dados de contexto adicionais
- **`finish()`** - Interromper o processamento antecipadamente

#### Stopping Processing Early

Chame `context.finish()` para interromper o processamento:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.Validation) { context ->
    if (someCondition) {
        context.finish() // No further phases will execute
    }
}
```

#### Storing Custom Data

Use `additionalContext` para passar dados entre interceptors:

```kotlin
// In PreInvoke
context.additionalContext["userId"] = context.update.userOrNull?.id

// In PostInvoke
val userId = context.additionalContext["userId"] as? Long
```

### Multiple Interceptors

Você pode registrar vários interceptors para a mesma fase. Eles são executados na ordem de registro:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    println("First interceptor")
}

bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    println("Second interceptor")
}

// When an update is processed:
// Output: "First interceptor"
// Output: "Second interceptor"
```

Se um interceptor chamar `context.finish()`, os interceptors subsequentes naquela fase são pulados, e fases posteriores não serão executadas.

### Best Practices

#### 1. Use the Right Phase

- Setup: verificações globais, filtragem, configuração inicial
- Parsing: lógica customizada de parsing
- Match: lógica de seleção de handler
- Validation: permissões, limites de taxa, guardas
- PreInvoke: preparação específica do handler
- Invoke: normalmente tratado pelo interceptor padrão
- PostInvoke: limpeza, log, tratamento de erros

#### 2. Keep Interceptors Focused

Cada interceptor deve fazer uma única coisa:

```kotlin
// ✅ Good - focused interceptor
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    if (isBanned(context.update.userOrNull?.id)) {
        context.finish()
    }
}

// ❌ Avoid - doing too much
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    // Authentication
    // Logging
    // Metrics
    // Rate limiting
    // ... too much!
}
```

#### 3. Handle Errors Gracefully

Interceptores não devem travar o bot:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
    try {
        // Your logic
    } catch (e: Exception) {
        val logger = context.bot.config.loggerFactory.get("Interceptor")
        logger.error("Interceptor error", e)
        // Don't call context.finish() unless you want to stop processing
    }
}
```

#### 4. Clean Up Resources

Se você abrir recursos em `PreInvoke`, libere‑os em `PostInvoke`:

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

#### 5. Order Matters

Registre os interceptors na ordem que deseja que eles sejam executados:

```kotlin
// More general checks first
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { 
    // Global ban check
}

// More specific checks later
bot.update.pipeline.intercept(ProcessingPipePhase.Validation) { 
    // Handler-specific permission check
}
```

#### 6. Use Interceptors for Cross-Cutting Concerns

Interceptores são ideais para:
- ✅ Autenticação/autorização
- ✅ Log
- ✅ Métricas/monitoramento de performance
- ✅ Limitação de taxa
- ✅ Tratamento de erros
- ✅ Transformação de request/response

Para lógica específica de handler, mantenha‑a no próprio handler.

### Default Interceptors

O framework inclui interceptors padrão para funcionalidades centrais:

- **DefaultSetupInterceptor**: Limitação global de taxa
- **DefaultParsingInterceptor**: Parsing de comandos
- **DefaultMatchInterceptor**: Correspondência de handlers (commands, inputs, common matchers)
- **DefaultValidationInterceptor**: Verificações de guardas e limitação de taxa por handler
- **DefaultInvokeInterceptor**: Execução do handler e tratamento de erros

Seus interceptors customizados são executados junto com esses padrões. Você pode adicionar lógica antes ou depois dos padrões, mas não pode removê‑los.

---

### Advanced: Conditional Interceptors

Você pode tornar interceptors condicionais:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
    val activity = context.activity ?: return@intercept
    
    // Only apply to specific handlers
    if (activity::class.simpleName?.contains("Admin") == true) {
        // Admin-specific logic
        checkAdminPermissions(context)
    }
}
```

### Summary

Os interceptors fornecem uma forma limpa de adicionar lógica transversal ao seu bot:

- ✅ **Sete fases** para diferentes estágios de processamento
- ✅ **API simples**: basta implementar `PipelineInterceptor`
- ✅ **Flexível**: registre múltiplos interceptors por fase
- ✅ **Poderoso**: acesso total ao contexto de processamento
- ✅ **Seguro**: pode interromper o processamento antecipadamente com `context.finish()`

Use interceptors para manter seus handlers focados na lógica de negócio, tratando preocupações compartilhadas como autenticação, log e métricas de forma centralizada.

---

### See also

* [Handlers (incl. Functional DSL)](Handlers.md) - Annotation- and DSL-based handler definition
* [Sessions](Sessions.md) - Per-chat / per-user state &amp; message tracking
* [Guards](Guards.md) - Handler-level permission checks
---