---
---
title: Guards
---

### Introduction
Guards são um recurso essencial para desenvolvedores que criam bots. Esses guards funcionam como verificações pré-execução que determinam se um determinado comando deve ser invocado. Ao implementar essas verificações, os desenvolvedores podem melhorar a funcionalidade, a segurança e a experiência do usuário de seus bots.

### Purpose of Activity Guards
O objetivo principal dos activity guards é garantir que apenas usuários autorizados ou condições específicas acionem uma atividade.

Isso pode prevenir uso indevido, manter a integridade do bot e simplificar as interações.

### Common Use Cases
1. Authentication and Authorization: Garantir que apenas certos usuários possam acessar comandos específicos.  
2. Pre-condition Checks: Verificar se certas condições são atendidas antes de executar uma atividade (por exemplo, garantir que um usuário esteja em um estado ou contexto específico).  
3. Contextual Guards: Tomar decisões com base no chat ou estado do usuário atual.

### Implementation Strategies
Implementar Telegram Command Guards tipicamente envolve escrever funções ou métodos que encapsulam a lógica para cada guard. Abaixo estão estratégias comuns:

1. User Role Check:
   - Garantindo que o usuário possua a role requerida (por exemplo, admin, moderator) antes de executar o comando.
      ```kotlin
       override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // Check if the user is an admin in the given chat
       }
      ```
   
2. State Verification:
   - Verificando o estado do usuário antes de permitir a execução do comando.
     ```kotlin
     override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        return bot.userData[user.id, "data"] == requiredState
     }
     ```
   
3. Custom Guards:
   - Criando lógica personalizada baseada em requisitos específicos.
     ```kotlin
     override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // Custom logic to determine if the command should be executed
     }
     ```
   
### Integrating Guards with Activities
Para integrar esses guards aos comandos do seu bot, você pode criar um guard que verifique essas condições antes que o manipulador de comando seja invocado.

### Implementing Example

```kotlin
// define somewhere your guard class that implements Guard interface
object YourGuard : Guard {
    override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // write your condition here
    }
}

// ...

@CommandHandler(["yourCommand"])
@Guard(YourGuard::class) // InputHandler also is supported
fun command(bot: TelegramBot) {
   // command body
}
```

### Best Practices

- Modularity: Mantenha a lógica do guard modular e separada das atividades.  
- Reusability: Escreva funções de guard reutilizáveis que possam ser aplicadas facilmente em diferentes comandos/entradas.  
- Efficiency: Otimize as verificações de guard para minimizar a sobrecarga de desempenho.  
- User Feedback: Forneça feedback claro aos usuários quando um comando for bloqueado por um guard.

### Conclusion

Activity Guards são uma ferramenta poderosa para gerenciar a execução de comandos/entradas de bot.

Ao implementar mecanismos de guard robustos, os desenvolvedores podem garantir que seus bots operem de forma segura e eficiente, proporcionando uma melhor experiência ao usuário.

### See also

* [Activities and Proccessors](Activites-and-Processors.md)
* [Update parsing](Update-parsing.md)
* [Actions](Actions.md)
* [Activity invocation](Activity-invocation.md)

---