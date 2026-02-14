---
---
title: Guards
---

### Introdução
Guards são um recurso essencial para desenvolvedores que criam bots. Esses guards funcionam como verificações pré-execução que determinam se um determinado comando deve ser invocado. Ao implementar essas verificações, os desenvolvedores podem aprimorar a funcionalidade, segurança e experiência do usuário de seus bots.

### Propósito dos Activity Guards
O propósito principal dos activity guards é garantir que apenas usuários autorizados ou condições específicas disparem uma atividade.

Isso pode prevenir o uso indevido, manter a integridade do bot e agilizar as interações.

### Casos de Uso Comuns
1. Autenticação e Autorização: Garantir que apenas certos usuários possam acessar comandos específicos.
2. Verificações de Pré-condição: Verificar se certas condições são atendidas antes de executar uma atividade (por exemplo, garantir que um usuário esteja em um estado ou contexto específico).
3. Guards Contextuais: Tomar decisões com base no estado atual do chat ou usuário.

### Estratégias de Implementação
A implementação de Telegram Command Guards normalmente envolve escrever funções ou métodos que encapsulam a lógica para cada guard. Abaixo estão estratégias comuns:

1. Verificação de Função do Usuário:
   - Garantir que o usuário tenha a função necessária (por exemplo, admin, moderador) antes de executar o comando.
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
Para integrar esses guards com seus comandos de bot, você pode criar um guard que verifica essas condições antes que o manipulador de comandos seja invocado.

### Exemplo de Implementação

```kotlin
// defina em algum lugar sua classe guard que implementa a interface Guard
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
- Reutilização: Escreva funções de guard reutilizáveis que possam ser facilmente aplicadas em diferentes comandos/entradas.
- Eficiência: Otimize as verificações do guard para minimizar sobrecarga de desempenho.
- Feedback do Usuário: Forneça feedback claro aos usuários quando um comando for bloqueado por um guard.

### Conclusão

Activity Guards são uma ferramenta poderosa para gerenciar a execução de comandos/entradas de bot.

Ao implementar mecanismos robustos de guard, os desenvolvedores podem garantir que seus bots operem de forma segura e eficiente, proporcionando uma melhor experiência ao usuário.

### Veja também

* [Activities and Proccessors](Activites-and-Processors.md)
* [Update parsing](Update-parsing.md)
* [Actions](Actions.md)
* [Activity invocation](Activity-invocation.md)