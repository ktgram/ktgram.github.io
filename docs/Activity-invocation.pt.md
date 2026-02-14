---
---
title: Activity Invocation
---

Durante a invocação de atividade, é possível passar o contexto do bot, pois ele é declarado como um parâmetro nas funções de destino.

Os parâmetros que podem ser passados são:

* [`ProcessedUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processed-update/index.html) (e todas as suas subclasses) - atualização de processamento.
* [`ProcessingContext`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processing-context/index.html) - contexto de baixo nível do tratamento da atividade.
* [`User`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types/-user/index.html) - se presente.
* [`Chat`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.chat/-chat/index.html) - se presente.
* [`TelegramBot`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot/-telegram-bot/index.html) - instância atual do bot.

Também é possível adicionar um tipo personalizado para passagem.

Para fazer isso, adicione uma classe que implemente [`Autowiring<T>`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.marker/-autowiring/index.html) e marque-a com a anotação [`@Injectable`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-injectable/index.html).

Após implementar a interface `Autowiring` - `T` estará disponível para passagem nas funções de destino e será obtido através do método descrito na interface.

```kotlin
@Injectable
object UserResolver : Autowiring<UserRecord> {
    override suspend fun get(update: ProcessedUpdate, bot: TelegramBot): UserRecord? {
        return userRepository.getUserByTgId(update.user.id)
    }
}
```

Outros parâmetros declarados nas funções serão **buscados** nos parâmetros analisados.

Além disso, os parâmetros analisados durante a passagem podem ser convertidos para certos tipos, aqui está a lista:

- `String`
- `Integer`
- `Long`
- `Short`
- `Float`
- `Double`

Além disso, observe que se os parâmetros forem declarados e estiverem ausentes (ou nos parâmetros analisados ou, por exemplo, `User` estiver ausente em `Update`) ou o tipo declarado não se encaixar no parâmetro recebido na função, **`null`** será passado, então tenha cuidado.

Resumindo tudo, abaixo está um exemplo de como os parâmetros da função geralmente são formados:

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/3c1d7830-8e5d-45fb-82bb-ac63f08c3782" alt="Invokation process diagram" />
</p>

### Veja também

* [Update parsing](Update-parsing.md)
* [Activities & Processors](Activites-and-Processors.md)
---