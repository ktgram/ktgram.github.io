---
---
title: Contexto do Bot
---

<p align="center">
  <img src="https://github.com/user-attachments/assets/60bb58ae-1806-4b8d-8550-833b09c2b606" alt="Diagrama de contexto do bot" />
</p>

O bot também pode fornecer a capacidade de lembrar alguns dados através das interfaces `UserData` e `ClassData`.

- [`userData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-user-data/index.html) é um dado em nível de usuário.
- [`classData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-data/index.html) é um dado em nível de classe, ou seja, os dados serão armazenados até que o usuário se mova para um comando ou entrada que esteja em uma
  classe diferente. (no modo função funcionará como dado de usuário)

Por padrão, a implementação é fornecida através de [`ConcurrentHashMap`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.collections/java.util.concurrent.-concurrent-map/) mas pode ser alterada para a sua própria através das interfaces [`UserData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-user-data/index.html) e [`ClassData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-data/index.html) usando
as ferramentas de armazenamento de dados de sua escolha.


> [!CAUTION]
> Não se esqueça de executar a tarefa gradle `kspKotlin`/ou qualquer tarefa ksp relevante para tornar as vinculações de codegen necessárias disponíveis. 


Para alterar, tudo o que você precisa fazer é colocar sob sua implementação a anotação `@CtxProvider` e executar a tarefa gradle ksp (ou build).

```kotlin
@CtxProvider
class MyRedis : UserData<String> {
    // ...
}
```

### Veja também

* [Home](https://github.com/vendelieu/telegram-bot/wiki)
* [Parsing de atualização](Update-parsing.md)
---