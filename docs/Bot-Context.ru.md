---
---
title: Контекст бота
---

<p align="center">
  <img src="https://github.com/user-attachments/assets/60bb58ae-1806-4b8d-8550-833b09c2b606" alt="Диаграмма контекста бота" />
</p>

Бот также может предоставлять возможность запоминать некоторые данные через интерфейсы `UserData` и `ClassData`.

- [`userData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-user-data/index.html) - это данные уровня пользователя.
- [`classData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-data/index.html) - это данные уровня класса, т.е. данные будут храниться до тех пор, пока пользователь не перейдет к команде или вводу, которые находятся в
  другом классе. (в режиме функций он будет работать как данные пользователя)

По умолчанию реализация предоставляется через [`ConcurrentHashMap`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.collections/java.util.concurrent.-concurrent-map/), но может быть изменена на вашу собственную через интерфейсы [`UserData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-user-data/index.html) и [`ClassData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-data/index.html) с использованием
инструментов хранения данных по вашему выбору.


> [!CAUTION]
> Не забудьте выполнить gradle `kspKotlin`/или любую соответствующую задачу ksp, чтобы сделать доступными необходимые привязки codegen.


Чтобы изменить, все что вам нужно сделать - это поместить под вашей реализацией аннотацию `@CtxProvider` и запустить задачу gradle ksp (или сборку).

```kotlin
@CtxProvider
class MyRedis : UserData<String> {
    // ...
}
```

### См. также

* [Домой](https://github.com/vendelieu/telegram-bot/wiki)
* [Разбор обновлений](Update-parsing.md)
---