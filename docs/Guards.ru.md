---
---
title: Guards
---

### Introduction
Guards — это важная функция для разработчиков, создающих ботов. Эти охранники выступают в роли проверок перед выполнением, определяя, следует ли вызывать конкретную команду. Реализуя такие проверки, разработчики могут улучшить функциональность, безопасность и пользовательский опыт своих ботов.

### Purpose of Activity Guards
Основная цель охранников активности — гарантировать, что только уполномоченные пользователи или определённые условия вызывают активность.

Это может предотвратить злоупотребления, поддерживать целостность бота и упорядочить взаимодействия.

### Common Use Cases
1. Authentication and Authorization: Обеспечение доступа к определённым командам только для определённых пользователей.  
2. Pre-condition Checks: Проверка, что выполнены необходимые условия перед выполнением активности (например, пользователь находится в определённом состоянии или контексте).  
3. Contextual Guards: Принятие решений на основе текущего чата или состояния пользователя.

### Implementation Strategies
Реализация охранников команд Telegram обычно включает написание функций или методов, инкапсулирующих логику для каждого охранника. Ниже представлены распространённые стратегии:

1. User Role Check:
   - Проверка, что у пользователя есть требуемая роль (например, администратор, модератор) перед выполнением команды.
      ```kotlin
       override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // Check if the user is an admin in the given chat
       }
      ```
   
2. State Verification:
   - Проверка состояния пользователя перед разрешением выполнения команды.
     ```kotlin
     override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        return bot.userData[user.id, "data"] == requiredState
     }
     ```
   
3. Custom Guards:
   - Создание пользовательской логики на основе конкретных требований.
     ```kotlin
     override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // Custom logic to determine if the command should be executed
     }
     ```
   
### Integrating Guards with Activities
Чтобы интегрировать эти охранники с командами бота, можно создать охранник, который проверяет условия до вызова обработчика команды.

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

- Modularity: Держите логику охранников модульной и отделённой от активностей.  
- Reusability: Пишите переиспользуемые функции охранников, которые можно легко применять к разным командам/вводам.  
- Efficiency: Оптимизируйте проверки охранников, чтобы минимизировать нагрузку на производительность.  
- User Feedback: Предоставляйте понятную обратную связь пользователям, когда команда блокируется охранником.

### Conclusion

Охранники активности — мощный инструмент управления выполнением команд/вводов бота.

Реализуя надёжные механизмы охранников, разработчики могут обеспечить безопасную и эффективную работу ботов, улучшая пользовательский опыт.

### See also

* [Activities and Proccessors](Activites-and-Processors.md)
* [Update parsing](Update-parsing.md)
* [Actions](Actions.md)
* [Activity invocation](Activity-invocation.md)

---