---
---
title: Guards
---

### Introdução
Guards são um recurso essencial para desenvolvedores criando bots. Estes guards funcionam como verificações pré-execução que determinam se um comando específico deve ser invocado. Ao implementar estas verificações, os desenvolvedores podem aprimorar a funcionalidade, segurança e experiência do usuário de seus bots.

### Propósito dos Activity Guards
O propósito principal dos activity guards é garantir que apenas usuários autorizados ou condições específicas disparem uma atividade.

Isso pode prevenir o uso indevido, manter a integridade do bot e agilizar as interações.

### Casos de Uso Comuns
1. Autenticação e Autorização: Garantir que apenas certos usuários possam acessar comandos específicos.
2. Verificações de Pré-condição: Verificar se certas condições são atendidas antes de executar uma atividade (por exemplo, garantindo que um usuário esteja em um estado ou contexto específico).
3. Guards Contextuais: Tomar decisões baseadas no estado atual do chat ou usuário.

### Estratégias de Implementação
Implementar Telegram Command Guards normalmente envolve escrever funções ou métodos que encapsulam a lógica para cada guard. Abaixo estão estratégias comuns:

1. Verificação de Papel do Usuário:
   - Garantir que o usuário tenha o papel necessário (por exemplo, admin, moderador) antes de executar o comando.
      ```kotlin
       override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // Verificar se o usuário é um admin no chat dado
       }
      ```

2. Verificação de Estado:
   - Verificar o estado do usuário antes de permitir a execução do comando.
     ```kotlin
     override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        return bot.userData[user.id, "data"] == requiredState
     }
     ```

3. Guards Personalizados:
   - Criar lógica personalizada baseada em requisitos específicos.
     ```kotlin
     override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // Lógica personalizada para determinar se o comando deve ser executado
     }
     ```

### Integrando Guards com Activities
Para integrar estes guards com seus comandos de bot, você pode criar um guard que verifica estas condições antes que o manipulador de comando seja invocado.

### Implementando Exemplo

```kotlin
// definir em algum lugar sua classe guard que implementa a interface Guard
object YourGuard : Guard {
    override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // escreva sua condição aqui
    }
}

// ...

@CommandHandler(["yourCommand"])
@Guard(YourGuard::class) // InputHandler também é suportado
fun command(bot: TelegramBot) {
   // corpo do comando
}
```

### Melhores Práticas

- Modularidade: Mantenha a lógica do guard modular e separada das activities.
- Reutilização: Escreva funções de guard reutilizáveis que possam ser facilmente aplicadas em diferentes comandos/inputs.
- Eficiência: Otimize as verificações de guard para minimizar overhead de desempenho.
- Feedback do Usuário: Forneça feedback claro aos usuários quando um comando é bloqueado por um guard.

### Conclusão

Activity Guards são uma ferramenta poderosa para gerenciar a execução de comandos/inputs de bot.

Ao implementar mecanismos robustos de guard, os desenvolvedores podem garantir que seus bots operem de forma segura e eficiente, proporcionando uma melhor experiência do usuário.

### Veja também

* [Activities and Proccessors](Activites-and-Processors.md)
* [Update parsing](Update-parsing.md)
* [Actions](Actions.md)
* [Activity invocation](Activity-invocation.md)