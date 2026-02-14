---
---
title: Fsm E Tratamento De Conversação
---

A biblioteca também suporta o mecanismo FSM, que é um mecanismo para processamento progressivo de entrada do usuário com tratamento de entrada incorreta.

> [!NOTE]
> TL;DR: Veja exemplo [lá](https://github.com/vendelieu/telegram-bot_template/tree/conversation).

### Na teoria

Vamos imaginar uma situação onde você precisa coletar uma pesquisa do usuário, você pode pedir todos os dados de uma pessoa em uma etapa, mas com entrada incorreta de um dos parâmetros, será difícil tanto para o usuário quanto para nós, e cada etapa pode ter uma diferença dependendo de certos dados de entrada.

Agora vamos imaginar entrada passo a passo dos dados, onde o bot entra em modo de diálogo com o usuário.

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/2e84fa00-e59c-4352-8665-83be3b971e7b" alt="Diagrama do processo de tratamento" />
</p>

As setas verdes indicam o processo de transição pelas etapas sem erros, as setas azuis significam salvar o estado atual e esperar por re-entrada (por exemplo, se o usuário indicou que ele tem -100 anos, deve pedir idade novamente), e as vermelhas mostram saída de todo o processo devido a qualquer comando ou qualquer outro cancelamento significativo.

### Na prática

O sistema Wizard permite interações de múltiplos passos em bots Telegram. Ele guia os usuários através de uma sequência de etapas, valida entrada, armazena estado e transita entre etapas.

**Principais Benefícios:**
- **Type-safe**: Verificação de tipo em tempo de compilação para acesso ao estado
- **Declarativo**: Defina etapas como classes/objeto aninhados
- **Flexível**: Suporte para transições condicionais, saltos e novas tentativas
- **Stateful**: Persistência automática de estado com backends de armazenamento plugáveis
- **Integrado**: Funciona com o sistema Activity existente

### Conceitos Principais

#### WizardStep

Um `WizardStep` representa uma única etapa no fluxo do wizard. Cada etapa deve implementar:

- **`onEntry(ctx: WizardContext)`**: Chamado quando o usuário entra nesta etapa. Use isso para solicitar ao usuário.
- **`onRetry(ctx: WizardContext)`**: Chamado quando a validação falha e a etapa deve tentar novamente. Use isso para mostrar mensagens de erro.
- **`validate(ctx: WizardContext): Transition`**: Valida a entrada atual e retorna uma `Transition` indicando o que acontece em seguida.
- **`store(ctx: WizardContext): Any?`** (opcional): Retorna o valor a persistir para esta etapa. Retorne `null` se a etapa não armazenar estado.

```kotlin
object NameStep : WizardStep(isInitial = true) {
    override suspend fun onEntry(ctx: WizardContext) {
        message { "Qual é o seu nome?" }.send(ctx.user, ctx.bot)
    }

    override suspend fun onRetry(ctx: WizardContext) {
        message { "Nome não pode estar vazio. Por favor, tente novamente." }.send(ctx.user, ctx.bot)
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
> Se alguma etapa não estiver marcada como inicial -> a primeira etapa declarada é considerada como.

#### Transition

Uma `Transition` determina o que acontece após a validação:

- **`Transition.Next`**: Vá para a próxima etapa na sequência
- **`Transition.JumpTo(step: KClass<out WizardStep>)`**: Salte para uma etapa específica
- **`Transition.Retry`**: Tente novamente a etapa atual (validação falhou)
- **`Transition.Finish`**: Termine o wizard

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
- **`update: ProcessedUpdate`**: A atualização atual
- **`bot: TelegramBot`**: A instância do bot
- **`userReference: UserChatReference`**: Referência de ID de usuário e chat para armazenamento de estado

Além de métodos de acesso a estado type-safe (gerados pelo KSP).

---

### Definindo um Wizard

#### Estrutura Básica

Um wizard é definido como uma classe ou objeto anotado com `@WizardHandler`:

```kotlin
@WizardHandler(trigger = ["/survey"])
object SurveyWizard {
    object NameStep : WizardStep(isInitial = true) {
        // ... implementação da etapa
    }

    object AgeStep : WizardStep {
        // ... implementação da etapa
    }

    object FinishStep : WizardStep {
        // ... implementação da etapa
    }
}
```

#### Parâmetros de Anotação

**`@WizardHandler`** aceita:
- **`trigger: Array<String>`**: Comandos que iniciam o wizard (e.g., `["/start", "/survey"]`)
- **`scope: Array<UpdateType>`**: Tipos de atualização para escutar (padrão: `[UpdateType.MESSAGE]`)
- **`stateManagers: Array<KClass<out WizardStateManager<*>>>`**: Classes de gerenciador de estado para armazenar dados de etapa

---

### Gerenciamento de Estado

#### WizardStateManager

O estado é armazenado usando implementações de `WizardStateManager<T>`. Cada gerenciador lida com um tipo específico:

```kotlin
interface WizardStateManager<T : Any> {
    suspend fun get(key: KClass<out WizardStep>, reference: UserChatReference): T?
    suspend fun set(key: KClass<out WizardStep>, reference: UserChatReference, value: T)
    suspend fun del(key: KClass<out WizardStep>, reference: UserChatReference)
}
```

Veja também: [MapStateManager<T>](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-state-manager/index.html), [MapStringStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-string-state-manager/index.html), [MapIntStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-int-state-manager/index.html), [MapLongStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-long-state-manager/index.html).

#### Correspondência Automática

KSP corresponde etapas a gerenciadores de estado baseado no tipo de retorno do `store()`:

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

#### Substituição Por Etapa

Substitua o gerenciador de estado para uma etapa específica usando `@WizardHandler.StateManager`:

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

### Acesso Type-Safe ao Estado

KSP gera funções de extensão type-safe em `WizardContext` para cada etapa que armazena estado.

#### Funções Geradas

Para uma etapa que armazena uma `String`:

```kotlin
// Gerado automaticamente pelo KSP
suspend inline fun <reified S : WizardStep> WizardContext.getState(): String?
suspend inline fun <reified S : WizardStep> WizardContext.setState(value: String)
suspend inline fun <reified S : WizardStep> WizardContext.delState()
```

#### Uso

```kotlin
object FinishStep : WizardStep {
    override suspend fun onEntry(ctx: WizardContext) {
        // Acesso type-safe - retorna String? (nulável)
        val name: String? = ctx.getState<NameStep>()

        // Acesso type-safe - retorna Int? (nulável)
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

Se os métodos type-safe não estiverem disponíveis, use os métodos de fallback:

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
            // Acesso type-safe ao estado
            val name: String? = ctx.getState<NameStep>()
            val age: Int? = ctx.getState<AgeStep>()

            val confirmation = buildString {
                appendLine("Por favor, confirme suas informações:")
                appendLine("Nome: $name")
                appendLine("Idade: $age")
                appendLine()
                appendLine("Responda 'sim' para confirmar ou 'não' para começar de novo.")
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
                "não" -> Transition.JumpTo(NameStep::class) // Começar de novo
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

#### Etapas Sem Estado

Etapas não precisam armazenar estado. Simplesmente retorne `null` do `store()` (ou mantenha como está):

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

1. **WizardActivity**: Uma implementação concreta estendendo `WizardActivity` com etapas hardcoded
2. **Start Activity**: Lida com o comando trigger e inicia o wizard
3. **Input Activity**: Lida com entrada do usuário durante o fluxo do wizard
4. **State Accessors**: Funções de extensão type-safe para acesso ao estado

#### Fluxo

1. Usuário envia `/register` → Start Activity é invocado
2. Start Activity cria `WizardContext` e chama `wizardActivity.start(ctx)`
3. `start()` entra na etapa inicial e define `inputListener` para rastrear a etapa atual
4. Usuário envia uma mensagem → Input Activity é invocado
5. Input Activity chama `wizardActivity.handleInput(ctx)`
6. `handleInput()` valida entrada, persiste estado e transita para a próxima etapa
7. Processo se repete até `Transition.Finish` ser retornado

#### Persistência de Estado

- Estado é persistido após validação bem-sucedida (antes da transição)
- O valor de retorno do `store()` de cada etapa é salvo usando o `WizardStateManager` correspondente
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

#### 2. Trate Erros de Validação Graciosamente

```kotlin
override suspend fun onRetry(ctx: WizardContext) {
    message {
        "Formato de email inválido. Por favor, tente novamente.\n" +
        "Exemplo: usuario@exemplo.com"
    }.send(ctx.user, ctx.bot)
}
```

#### 3. Use Acesso Type-Safe ao Estado

Prefira métodos type-safe gerados:

```kotlin
// ✅ Bom - type-safe
val name: String? = ctx.getState<NameStep>()

// ❌ Evite - perde type safety
val name = ctx.getState(NameStep::class) as? String
```

#### 4. Mantenha Etapas Focadas

Cada etapa deve ter uma única responsabilidade:

```kotlin
// ✅ Bom - etapa focada
object EmailStep : WizardStep {
    // Apenas lida com coleta de email
}

// ❌ Evite - lógica demais
object PersonalInfoStep : WizardStep {
    // Lida com nome, email, telefone, endereço...
}
```

#### 5. Use Nomes Significativos para Etapas

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
        // Limpar todo estado do wizard
        ctx.delState<NameStep>()
        ctx.delState<AgeStep>()

        message { "Registro cancelado." }.send(ctx.user, ctx.bot)
    }
}
```

---

### Resumo

O sistema Wizard fornece:
- ✅ **Type-safe** gerenciamento de estado com verificação em tempo de compilação
- ✅ **Declarativo** definições de etapas como classes aninhadas
- ✅ **Flexível** transições com lógica condicional
- ✅ **Automático** geração de código via KSP
- ✅ **Integrado** com o sistema Activity existente
- ✅ **Plugável** backends de armazenamento de estado

Comece a construir wizards anotando uma classe com `@WizardHandler` e definindo suas etapas como objetos `WizardStep` aninhados!
se você tiver alguma dúvida entre em contato conosco no chat, teremos prazer em ajudar :)
---