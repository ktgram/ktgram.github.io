---
---
title: Interceptores (Middleware)
---

### Interceptores: Lógica de Corte Transversal para seu Bot

Ao construir um bot do Telegram, você frequentemente repete configuração, verificações ou limpeza entre manipuladores. Os interceptores permitem que você insira lógica compartilhada ao redor dos manipuladores, mantendo-os focados e manuteníveis.

Aqui está como os interceptores funcionam no *telegram-bot* e como usá-los.

### O que são Interceptores? (Explicação Simples)

Interceptores são funções que executam em pontos específicos no pipeline de processamento de atualizações. Eles permitem que você:
- Inspecione e modifique o contexto de processamento
- Adicione lógica de corte transversal (log, autenticação, métricas)
- Pare o processamento antecipadamente se necessário
- Limpe recursos após o processamento

Pense nos interceptores como checkpoints que toda atualização passa antes, durante e após a execução do manipulador.


### O Pipeline de Processamento

O bot processa atualizações através de um pipeline com sete fases:

| Fase | Quando Executa | Para que Você Pode Usá-lo |
|-------|--------------|-------------------------|
| **Setup** | Assim que a atualização chega, antes de qualquer processamento | ✔ Rate limiting global<br>✔ Filtrar spam ou atualizações malformadas<br>✔ Log inicial<br>✔ Configurar contexto compartilhado |
| **Parsing** | Após o setup, extrai comando e parâmetros | ✔ Parsing personalizado de comandos<br>✔ Enriquecer contexto com dados parseados<br>✔ Validar estrutura da atualização |
| **Match** | Encontra o manipulador apropriado (Command/Input/Common) | ✔ Sobrescrever seleção de manipulador<br>✔ Lógica personalizada de manipulação de entrada<br>✔ Log de manipuladores correspondidos |
| **Validation** | Após o manipulador ser encontrado, antes da invocação | ✔ Permissões específicas do manipulador<br>✔ Rate limiting por manipulador<br>✔ Verificações de guarda<br>✔ Cancelar processamento se condições não forem atendidas |
| **PreInvoke** | Imediatamente antes do manipulador executar | ✔ Últimas verificações<br>✔ Iniciar temporizadores/métricas<br>✔ Enriquecer contexto para o manipulador<br>✔ Modificar comportamento do manipulador |
| **Invoke** | O manipulador é executado aqui | ✔ Envolve execução do manipulador<br>✔ Tratamento de erros<br>✔ Log de resultados do manipulador |
| **PostInvoke** | Após o manipulador completar (sucesso ou falha) | ✔ Limpar recursos<br>✔ Log de resultados<br>✔ Enviar mensagens de fallback em erros<br>✔ Modificar resultados antes de retornar |


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

Ou usando uma lambda:

```kotlin
val loggingInterceptor = PipelineInterceptor { context ->
    val logger = context.bot.config.loggerFactory.get("MyInterceptor")
    logger.info("Processing update #${context.update.updateId}")
}
```


### Registrando Interceptores

Registre interceptores no pipeline de processamento:

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
        // armazenar tempo inicial
    }

    // Registra um interceptor para a fase PostInvoke
    bot.update.pipeline.intercept(ProcessingPipePhase.PostInvoke) { context ->
        val startTime = // obter tempo inicial
        if (startTime != null) {
            val duration = System.currentTimeMillis() - startTime
            println("Handler took ${duration}ms")
        }
    }

    bot.handleUpdates()
}
```

### Exemplo Real: Autenticação & Métricas

Exemplo: um bot que requer autenticação para certos comandos, mede tempo de execução do manipulador e loga todos os comandos.

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

    // Fase PreInvoke: Iniciar temporizador e verificar permissões
    bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
        val activity = context.activity ?: return@intercept
        val user = context.update.userOrNull ?: return@intercept

        // Verifica se usuário tem permissão para este manipulador específico
        if (!hasPermission(user.id, activity)) {
            message { "You don't have permission to use this command." }
                .send(user, context.bot)
            context.finish()
            return@intercept
        }

        // Iniciar temporizador
        // armazenar tempo inicial
    }

    // Fase PostInvoke: Log e limpeza
    bot.update.pipeline.intercept(ProcessingPipePhase.PostInvoke) { context ->
        val activity = context.activity ?: return@intercept
        val startTime = // obter tempo inicial

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

- **`update: ProcessedUpdate`** - A atualização atual sendo processada
- **`bot: TelegramBot`** - A instância do bot
- **`registry: ActivityRegistry`** - O registry de atividades
- **`parsedInput: String`** - O texto do comando/entrada parseado
- **`parameters: Map<String, String>`** - Parâmetros do comando parseados
- **`activity: Activity?`** - O manipulador resolvido (nulo até a fase Match)
- **`shouldProceed: Boolean`** - Se o processamento deve continuar
- **`additionalContext: AdditionalContext`** - Dados de contexto adicionais
- **`finish()`** - Para processamento antecipadamente

#### Parando Processamento Antecipadamente

Chame `context.finish()` para parar processamento:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.Validation) { context ->
    if (someCondition) {
        context.finish() // Nenhuma fase subsequente executará
    }
}
```

#### Armazenando Dados Personalizados

Use `additionalContext` para passar dados entre interceptores:

```kotlin
// Em PreInvoke
context.additionalContext["userId"] = context.update.userOrNull?.id

// Em PostInvoke
val userId = context.additionalContext["userId"] as? Long
```


### Múltiplos Interceptores

Você pode registrar múltiplos interceptores para a mesma fase. Eles executam na ordem de registro:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    println("First interceptor")
}

bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    println("Second interceptor")
}

// Quando uma atualização é processada:
// Output: "First interceptor"
// Output: "Second interceptor"
```

Se um interceptor chamar `context.finish()`, os interceptores subsequentes naquela fase são pulados, e fases posteriores não executarão.


### Melhores Práticas

#### 1. Use a Fase Correta

- Setup: Verificações globais, filtragem, configuração inicial
- Parsing: Lógica personalizada de parsing
- Match: Lógica de seleção de manipulador
- Validation: Permissões, rate limits, verificações de guarda
- PreInvoke: Preparação específica do manipulador
- Invoke: Geralmente tratado pelo interceptor padrão
- PostInvoke: Limpeza, log, tratamento de erros

#### 2. Mantenha Interceptores Focados

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
    // Log
    // Métricas
    // Rate limiting
    // ... muito!
}
```

#### 3. Trate Erros Graciosamente

Interceptores não devem travar o bot:

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

Se você abrir recursos em `PreInvoke`, limpe-os em `PostInvoke`:

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

Registre interceptores na ordem que você quer que executem:

```kotlin
// Verificações mais gerais primeiro
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) {
    // Verificação global de ban
}

// Verificações mais específicas depois
bot.update.pipeline.intercept(ProcessingPipePhase.Validation) {
    // Verificação de permissão específica do manipulador
}
```

#### 6. Use Interceptores para Preocupações de Corte Transversal

Interceptores são ideais para:
- ✅ Autenticação/autorização
- ✅ Log
- ✅ Monitoramento de métricas/desempenho
- ✅ Rate limiting
- ✅ Tratamento de erros
- ✅ Transformação de requisição/resposta

Para lógica específica do manipulador, mantenha no manipulador.


### Interceptores Padrão

O framework inclui interceptores padrão para funcionalidade core:

- **DefaultSetupInterceptor**: Rate limiting global
- **DefaultParsingInterceptor**: Parsing de comandos
- **DefaultMatchInterceptor**: Correspondência de manipuladores (comandos, entradas, matchers comuns)
- **DefaultValidationInterceptor**: Verificações de guarda e rate limiting por manipulador
- **DefaultInvokeInterceptor**: Execução de manipulador e tratamento de erros

Seus interceptores personalizados executam ao lado desses padrões. Você pode adicionar lógica antes ou depois dos padrões, mas não pode remover os interceptores padrão.

---

### Avançado: Interceptores Condicionais

Você pode tornar interceptores condicionais:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
    val activity = context.activity ?: return@intercept

    // Aplicar apenas a manipuladores específicos
    if (activity::class.simpleName?.contains("Admin") == true) {
        // Lógica específica de admin
        checkAdminPermissions(context)
    }
}
```


### Resumo

Interceptores fornecem uma maneira limpa de adicionar lógica de corte transversal ao seu bot:

- ✅ **Sete fases** para diferentes estágios de processamento
- ✅ **API simples**: Basta implementar `PipelineInterceptor`
- ✅ **Flexível**: Registre múltiplos interceptores por fase
- ✅ **Poderoso**: Acesso ao contexto completo de processamento
- ✅ **Seguro**: Pode parar processamento antecipadamente com `context.finish()`

Use interceptores para manter seus manipuladores focados na lógica de negócio enquanto lida com preocupações compartilhadas como autenticação, log e métricas de forma centralizada.

---

### Veja também

* [Functional Handling DSL](Functional-handling-DSL.md) - Processamento funcional de atualizações
* [Guards](Guards.md) - Verificações de permissão em nível de manipulador
---