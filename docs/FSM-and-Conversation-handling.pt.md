---
---
title: Fsm E Tratamento De Conversação
---

A biblioteca também suporta o mecanismo FSM, que é um mecanismo para processamento progressivo de entrada do usuário com tratamento de entrada incorreta.

> [!NOTE]
> TL;DR: Veja exemplo [lá](https://github.com/vendelieu/telegram-bot_template/tree/conversation).

### Na teoria

Vamos imaginar uma situação onde você precisa coletar uma pesquisa do usuário, você pode pedir todos os dados de uma pessoa em um único passo, mas com entrada incorreta de um dos parâmetros, será difícil tanto para o usuário quanto para nós, e cada passo pode ter uma diferença dependendo de certos dados de entrada.

Agora vamos imaginar entrada de dados passo a passo, onde o bot entra no modo de diálogo com o usuário.

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/2e84fa00-e59c-4352-8665-83be3b971e7b" alt="Diagrama do processo de tratamento" />
</p>

Setas verdes indicam o processo de transição através dos passos sem erros, setas azuis significam salvar o estado atual e aguardar nova entrada (por exemplo, se o usuário indicou que tem -100 anos, deve pedir idade novamente), e vermelhas mostram saída de todo o processo devido a qualquer comando ou qualquer outra cancelamento significativo.

### Na prática

O sistema Wizard permite interações multi-passos com usuários em bots Telegram. Ele guia usuários através de uma sequência de passos, valida entrada, armazena estado e transita entre passos.

**Benefícios Principais:**
- **Type-safe**: Verificação de tipo em tempo de compilação para acesso a estado
- **Declarativo**: Defina passos como classes/objeto aninhados
- **Flexível**: Suporte para transições condicionais, saltos e novas tentativas
- **Stateful**: Persistência automática de estado com backends de armazenamento plugáveis
- **Integrado**: Funciona com o sistema Activity existente

### Conceitos Principais

#### WizardStep

Um `WizardStep` representa um único passo no fluxo wizard. Cada passo deve implementar:

- **`onEntry(ctx: WizardContext)`**: Chamado quando o usuário entra neste passo. Use isso para solicitar ao usuário.
- **`onRetry(ctx: WizardContext)`**: Chamado quando validação falha e o passo deve tentar novamente. Use isso para mostrar mensagens de erro.
- **`validate(ctx: WizardContext): Transition`**: Valida a entrada atual e retorna uma `Transition` indicando o que acontece em seguida.
- **`store(ctx: WizardContext): Any?`** (opcional): Retorna o valor a persistir para este passo. Retorne `null` se o passo não armazenar estado.

```kotlin
object NameStep : WizardStep(isInitial = true) {
    override suspend fun onEntry(ctx: WizardContext) {
        message { "Qual é o seu nome?" }.send(ctx.user, ctx.bot)
    }

    override suspend fun onRetry(ctx: WizardContext) {
        message { "Nome não pode ser vazio. Por favor, tente novamente." }.send(ctx.user, ctx.bot)
    }

    override suspend fun validate(ctx: WizardContext): Transition {
        return if (ctx.update.text.isNullOrBlank()) {
            Transition.Retry
        } else {
            Transition.Next
        }
    }

    override suspend fun store(ctx: WizardContext): String {
        return ctx.update.text!!
    }
}
```

> [!NOTE]
> Se algum passo não estiver marcado como inicial -> o primeiro passo declarado é considerado como.

#### Transition

Uma `Transition` determina o que acontece após validação:

- **`Transition.Next`**: Vai para o próximo passo na sequência
- **`Transition.JumpTo(step: KClass<out WizardStep>)`**: Salta para um passo específico
- **`Transition.Retry`**: Tenta novamente o passo atual (validação falhou)
- **`Transition.Finish`**: Finaliza o wizard

```kotlin
// Salto condicional baseado na entrada
override suspend fun validate(ctx: WizardContext): Transition {
    val age = ctx.update.text?.toIntOrNull()
    return when {
        age == null -> Transition.Retry
        age < 18 -> Transition.JumpTo(UnderageStep::class)
        else -> Transition.Next
    }
}
```

#### WizardContext

`WizardContext` fornece acesso a:
- **`user: User`**: O usuário atual
- **`update: ProcessedUpdate`**: O update atual
- **`bot: TelegramBot`**: A instância do bot
- **`userReference: UserChatReference`**: Referência de ID de usuário e chat para armazenamento de estado

Além de métodos de acesso a estado type-safe (gerados por KSP).

---

### Definindo um Wizard

#### Estrutura Básica

Um wizard é definido como uma classe ou objeto anotado com `@WizardHandler`:

```kotlin
@WizardHandler(trigger = ["/survey"])
object SurveyWizard {
    object NameStep : WizardStep(isInitial = true) {
        // ... implementação do passo
    }

    object AgeStep : WizardStep {
        // ... implementação do passo
    }

    object FinishStep : WizardStep {
        // ... implementação do passo
    }
}
```

#### Parâmetros de Anotação

**`@WizardHandler`** aceita:
- **`trigger: Array<String>`**: Comandos que iniciam o wizard (ex: `["/start", "/survey"]`)
- **`scope: Array<UpdateType>`**: Tipos de update para escutar (padrão: `[UpdateType.MESSAGE]`)
- **`stateManagers: Array<KClass<out WizardStateManager<*>>>`**: Classes de gerenciador de estado para armazenar dados de passo

---

### Gerenciamento de Estado

#### WizardStateManager

Estado é armazenado usando implementações de `WizardStateManager<T>`. Cada gerenciador lida com um tipo específico:

```kotlin
interface WizardStateManager<T : Any> {
    suspend fun get(key: KClass<out WizardStep>, reference: UserChatReference): T?
    suspend fun set(key: KClass<out WizardStep>, reference: UserChatReference, value: T)
    suspend fun del(key: KClass<out WizardStep>, reference: UserChatReference)
}
```

Veja também: [MapStateManager<T>](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-state-manager/index.html), [MapStringStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-string-state-manager/index.html), [MapIntStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-int-state-manager/index.html), [MapLongStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-long-state-manager/index.html).

#### Correspondência Automática

KSP corresponde passos a gerenciadores de estado baseado no tipo de retorno de `store()`:

```kotlin
@WizardHandler(
    trigger = ["/survey"],
    stateManagers = [StringStateManager::class, IntStateManager::class]
)
object SurveyWizard {
    object NameStep : WizardStep(isInitial = true) {
        override suspend fun store(ctx: WizardContext): String {
            return ctx.update.text!! // Corresponde a StringStateManager
        }
    }

    object AgeStep : WizardStep {
        override suspend fun store(ctx: WizardContext): Int {
            return ctx.update.text!!.toInt() // Corresponde a IntStateManager
        }
    }
}
```

#### Substituição por Passo

Substitua o gerenciador de estado para um passo específico usando `@WizardHandler.StateManager`:

```kotlin
@WizardHandler(
    trigger = ["/survey"],
    stateManagers = [DefaultStateManager::class]
)
object SurveyWizard {
    object NameStep : WizardStep(isInitial = true) {
        // Usa DefaultStateManager
    }

    @WizardHandler.StateManager(CustomStateManager::class)
    object AgeStep : WizardStep {
        // Usa CustomStateManager em vez disso
    }
}
```

---

### Acesso Type-Safe a Estado

KSP gera funções de extensão type-safe em `WizardContext` para cada passo que armazena estado.

#### Funções Geradas

Para um passo que armazena uma `String`:

```kotlin
// Gerado automaticamente por KSP
suspend inline fun <reified S : WizardStep> WizardContext.getState(): String?
suspend inline fun <reified S : WizardStep> WizardContext.setState(value: String)
suspend inline fun <reified S : WizardStep> WizardContext.delState()
```

#### Uso

```kotlin
object FinishStep : WizardStep {
    override suspend fun onEntry(ctx: WizardContext) {
        // Acesso type-safe - retorna String? (nuloável)
        val name: String? = ctx.getState<NameStep>()

        // Acesso type-safe - retorna Int? (nuloável)
        val age: Int? = ctx.getState<AgeStep>()

        val summary = buildString {
            appendLine("Nome: $name")
            appendLine("Idade: $age")
        }

        message { summary }.send(ctx.user, ctx.bot)
    }

    override suspend fun onRetry(ctx: WizardContext) = Unit

    override suspend fun validate(ctx: WizardContext): Transition {
        return Transition.Finish
    }
}
```

#### Métodos de Fallback

Se métodos type-safe não estiverem disponíveis, use os métodos de fallback:

```kotlin
// Fallback - retorna Any?
val name = ctx.getState(NameStep::class)

// Fallback - aceita Any?
ctx.setState(NameStep::class, "John")
ctx.delState(NameStep::class)
```

---

### Exemplo Completo

#### Wizard de Registro de Usuário

```kotlin
@WizardHandler(
    trigger = ["/register"],
    stateManagers = [StringStateManager::class, IntStateManager::class]
)
object RegistrationWizard {
    object NameStep : WizardStep(isInitial = true) {
        override suspend fun onEntry(ctx: WizardContext) {
            message { "Qual é o seu nome?" }.send(ctx.user, ctx.bot)
        }

        override suspend fun onRetry(ctx: WizardContext) {
            message { "Por favor, insira um nome válido." }.send(ctx.user, ctx.bot)
        }

        override suspend fun validate(ctx: WizardContext): Transition {
            val name = ctx.update.text?.trim()
            return if (name.isNullOrBlank() || name.length < 2) {
                Transition.Retry
            } else {
                Transition.Next
            }
        }

        override suspend fun store(ctx: WizardContext): String {
            return ctx.update.text!!.trim()
        }
    }

    object AgeStep : WizardStep {
        override suspend fun onEntry(ctx: WizardContext) {
            message { "Quantos anos você tem?" }.send(ctx.user, ctx.bot)
        }

        override suspend fun onRetry(ctx: WizardContext) {
            message { "Por favor, insira uma idade válida (deve ser um número)." }.send(ctx.user, ctx.bot)
        }

        override suspend fun validate(ctx: WizardContext): Transition {
            val age = ctx.update.text?.toIntOrNull()
            return when {
                age == null -> Transition.Retry
                age < 0 || age > 150 -> Transition.Retry
                age < 18 -> Transition.JumpTo(UnderageStep::class)
                else -> Transition.Next
            }
        }

        override suspend fun store(ctx: WizardContext): Int {
            return ctx.update.text!!.toInt()
        }
    }

    object UnderageStep : WizardStep {
        override suspend fun onEntry(ctx: WizardContext) {
            message {
                "Desculpe, você deve ter 18 anos ou mais para se registrar."
            }.send(ctx.user, ctx.bot)
        }

        override suspend fun onRetry(ctx: WizardContext) = Unit

        override suspend fun validate(ctx: WizardContext): Transition {
            return Transition.Finish
        }
    }

    object ConfirmationStep : WizardStep {
        override suspend fun onEntry(ctx: WizardContext) {
            // Acesso type-safe a estado
            val name: String? = ctx.getState<NameStep>()
            val age: Int? = ctx.getState<AgeStep>()

            val confirmation = buildString {
                appendLine("Por favor, confirme suas informações:")
                appendLine("Nome: $name")
                appendLine("Idade: $age")
                appendLine()
                appendLine("Responda 'sim' para confirmar ou 'não' para recomeçar.")
            }

            message { confirmation }.send(ctx.user, ctx.bot)
        }

        override suspend fun onRetry(ctx: WizardContext) {
            message { "Por favor, responda 'sim' ou 'não'." }.send(ctx.user, ctx.bot)
        }

        override suspend fun validate(ctx: WizardContext): Transition {
            val response = ctx.update.text?.lowercase()?.trim()
            return when (response) {
                "sim" -> Transition.Finish
                "não" -> Transition.JumpTo(NameStep::class) // Recomeçar
                else -> Transition.Retry
            }
        }
    }

    object FinishStep : WizardStep {
        override suspend fun onEntry(ctx: WizardContext) {
            val name: String? = ctx.getState<NameStep>()
            val age: Int? = ctx.getState<AgeStep>()

            // Salvar no banco de dados, enviar confirmação, etc.
            message {
                "Registro completo! Bem-vindo, $name (idade $age)."
            }.send(ctx.user, ctx.bot)
        }

        override suspend fun onRetry(ctx: WizardContext) = Unit

        override suspend fun validate(ctx: WizardContext): Transition {
            return Transition.Finish
        }
    }
}
```

---

### Recursos Avançados

#### Transições Condicionais

Use `Transition.JumpTo` para fluxos condicionais:

```kotlin
override suspend fun validate(ctx: WizardContext): Transition {
    val choice = ctx.update.text?.lowercase()
    return when (choice) {
        "premium" -> Transition.JumpTo(PremiumStep::class)
        "basic" -> Transition.JumpTo(BasicStep::class)
        else -> Transition.Retry
    }
}
```

#### Passos Stateless

Passos não precisam armazenar estado. Simplesmente retorne `null` de `store()` (ou mantenha como está):

```kotlin
object ConfirmationStep : WizardStep {
    override suspend fun store(ctx: WizardContext): Any? = null
    // ... resto da implementação
}
```

#### Gerenciadores de Estado Personalizados

Implemente `WizardStateManager<T>` para armazenamento personalizado (banco de dados, Redis, etc.):

```kotlin
class DatabaseStateManager : WizardStateManager<String> {
    override suspend fun get(
        key: KClass<out WizardStep>,
        reference: UserChatReference
    ): String? {
        // Carregar do banco de dados
        return database.getWizardState(reference.userId, key.qualifiedName)
    }

    override suspend fun set(
        key: KClass<out WizardStep>,
        reference: UserChatReference,
        value: String
    ) {
        // Salvar no banco de dados
        database.saveWizardState(reference.userId, key.qualifiedName, value)
    }

    override suspend fun del(
        key: KClass<out WizardStep>,
        reference: UserChatReference
    ) {
        // Deletar do banco de dados
        database.deleteWizardState(reference.userId, key.qualifiedName)
    }
}
```

---

### Como Funciona Internamente

#### Geração de Código

KSP gera:

1. **WizardActivity**: Uma implementação concreta estendendo `WizardActivity` com passos hardcoded
2. **Start Activity**: Lida com o trigger de comando e inicia o wizard
3. **Input Activity**: Lida com entrada do usuário durante o fluxo wizard
4. **State Accessors**: Funções de extensão type-safe para acesso a estado

#### Fluxo

1. Usuário envia `/register` → Start Activity é invocada
2. Start Activity cria `WizardContext` e chama `wizardActivity.start(ctx)`
3. `start()` entra no passo inicial e define `inputListener` para rastrear o passo atual
4. Usuário envia uma mensagem → Input Activity é invocada
5. Input Activity chama `wizardActivity.handleInput(ctx)`
6. `handleInput()` valida entrada, persiste estado e transita para o próximo passo
7. Processo se repete até `Transition.Finish` ser retornado

#### Persistência de Estado

- Estado é persistido após validação bem-sucedida (antes da transição)
- O valor de retorno de `store()` de cada passo é salvo usando o `WizardStateManager` correspondente
- Estado é escopo por usuário e chat (`UserChatReference`)

---

### Melhores Práticas

#### 1. Sempre Forneça Prompts Claros

```kotlin
override suspend fun onEntry(ctx: WizardContext) {
    message {
        "Por favor, insira seu endereço de email:\n" +
        "(Formato: usuario@exemplo.com)"
    }.send(ctx.user, ctx.bot)
}
```

#### 2. Trate Erros de Validação com Elegância

```kotlin
override suspend fun onRetry(ctx: WizardContext) {
    message {
        "Formato de email inválido. Por favor, tente novamente.\n" +
        "Exemplo: usuario@exemplo.com"
    }.send(ctx.user, ctx.bot)
}
```

#### 3. Use Acesso Type-Safe a Estado

Prefira métodos type-safe gerados:

```kotlin
// ✅ Bom - type-safe
val name: String? = ctx.getState<NameStep>()

// ❌ Evite - perde type safety
val name = ctx.getState(NameStep::class) as? String
```

#### 4. Mantenha Passos Focados

Cada passo deve ter uma única responsabilidade:

```kotlin
// ✅ Bom - passo focado
object EmailStep : WizardStep {
    // Apenas lida com coleta de email
}

// ❌ Evite - muita lógica
object PersonalInfoStep : WizardStep {
    // Lida com nome, email, telefone, endereço...
}
```

#### 5. Use Nomes Significativos para Passos

```kotlin
// ✅ Bom
object EmailVerificationStep : WizardStep

// ❌ Evite
object Step2 : WizardStep
```

#### 6. Limpe Estado Quando Necessário

Se precisar limpar estado manualmente:

```kotlin
object CancelStep : WizardStep {
    override suspend fun onEntry(ctx: WizardContext) {
        // Limpar todo estado wizard
        ctx.delState<NameStep>()
        ctx.delState<AgeStep>()

        message { "Cadastro cancelado." }.send(ctx.user, ctx.bot)
    }
}
```

---

### Resumo

O sistema Wizard fornece:
- ✅ **Gerenciamento type-safe** de estado com verificação em tempo de compilação
- ✅ **Definições declarativas** de passos como classes aninhadas
- ✅ **Transições flexíveis** com lógica condicional
- ✅ **Geração automática** de código via KSP
- ✅ **Integração** com o sistema Activity existente
- ✅ **Backends de armazenamento** plugáveis

Comece a construir wizards anotando uma classe com `@WizardHandler` e definindo seus passos como objetos `WizardStep` aninhados!
se você tiver alguma dúvida entre em contato conosco no chat, ficaremos felizes em ajudar :)
---