---
---
title: Контекст бота
---

<p align="center">
  <img src="https://github.com/user-attachments/assets/60bb58ae-1806-4b8d-8550-833b09c2b606" alt="Схема контекста бота" />
</p>

Бот также может предоставлять возможность запоминать некоторые данные через интерфейсы `UserData` и `ClassData`.

- [`userData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-user-data/index.html) — это данные уровня пользователя.
- [`classData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-data/index.html) — это данные уровня класса, то есть данные будут сохраняться до тех пор, пока пользователь не перейдет к команде или вводу, который находится
  в другом классе. (в режиме функции это будет работать как данные пользователя)

По умолчанию реализация предоставляется через [`ConcurrentHashMap`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.collections/java.util.concurrent.-concurrent-map/) но может быть изменена на вашу собственную через интерфейсы [`UserData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-user-data/index.html) и [`ClassData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-data/index.html) используя
инструменты хранения данных на ваш выбор.


> [!CAUTION]
> Не забудьте выполнить gradle задачу `kspKotlin`/или любую соответствующую ksp задачу для создания необходимых привязок кода.

Для изменения вам нужно всего лишь поместить вашу реализацию под аннотацию `@CtxProvider` и запустить gradle задачу ksp (или сборку).

```kotlin
@CtxProvider
class MyRedis : UserData<String> {
    // ...
}
```

### См. также

* [Домашняя страница](https://github.com/vendelieu/telegram-bot/wiki)
* [Разбор обновлений](Update-parsing.md)
---