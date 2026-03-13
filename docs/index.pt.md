---
---
title: Home
---

### Intro
Vamos ter uma ideia de como a biblioteca lida com atualizações em geral:

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/442cc5f1-0256-425a-9f25-185fdd49fe0a" alt="Diagrama do processo de manipulação" />
</p>

Após receber uma atualização, a biblioteca realiza três etapas principais, como podemos ver.

### Processamento

O processamento é empacotar novamente a atualização recebida na subclasse apropriada de [`ProcessedUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processed-update/index.html) dependendo da carga útil transportada.

Esta etapa é necessária para facilitar a operação da atualização e estender as capacidades de processamento.

### Manipulação

Em seguida vem a etapa principal, aqui chegamos à manipulação propriamente dita.

### RateLimiter Global

Se houver um usuário na atualização, verificamos o excedente do rate limiter global.

### Analisar texto

Em seguida, dependendo da carga útil, pegamos um componente de atualização específico contendo texto e o analisamos de acordo com a configuração.

Mais detalhes você pode ver no [artigo de análise de atualização](Update-parsing.md).

### Encontrar Atividade

Em seguida, de acordo com a prioridade de processamento:

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/6178c410-9b9e-4045-9f03-4791b3f49894" alt="Diagrama de prioridade de manipulação" />
</p>

Estamos procurando uma correspondência entre os dados analisados e as atividades nas quais estamos operando.
Como podemos ver no diagrama de prioridade, `Comandos` sempre vêm primeiro.

Ou seja, se a carga de texto na atualização corresponder a algum comando, a busca adicional por `Entradas`, `Comuns` e é claro a execução da ação `Não Processado` não será realizada.

A única coisa é que se houver `UpdateHandlers` será acionado em paralelo independentemente.

#### Comandos

Vamos dar uma olhada mais de perto nos comandos e seu processamento.

Como você pode ter notado, embora a anotação para processamento de comandos seja chamada [`CommandHandler`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-command-handler/index.html), ela é mais versátil do que o conceito clássico em Bots do Telegram.

##### Escopos

Isso porque tem uma gama mais ampla de possibilidades de processamento, ou seja, a função alvo pode ser definida não apenas dependendo da correspondência de texto, mas também do tipo de uma atualização adequada, este é o conceito de escopos.

Assim, cada comando pode ter diferentes manipuladores para uma lista diferente de escopos, ou vice-versa, um comando para vários.

Abaixo você pode ver como o mapeamento por carga útil de texto e escopo é feito:

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/c870027e-750e-4bb8-a2ed-45ad93a55875" alt="Diagrama de escopo de comando" />
</p>

#### Entradas

Em seguida, se a carga útil de texto não corresponder a nenhum comando, os pontos de entrada são pesquisados.

O conceito é muito semelhante à espera de entrada em aplicativos de linha de comando, você coloca no contexto do bot para um usuário específico um ponto que irá lidar com sua próxima entrada, não importa o que contenha, o importante é que a próxima atualização tenha um `Usuário` para poder relacioná-lo ao ponto de espera de entrada definido.

Abaixo você pode ver um exemplo de processamento de uma atualização quando não há correspondência em `Comandos`.

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/925d3e05-0985-43d5-8d6f-b3f2786ff212" alt="Diagrama de exemplo de prioridade" />
</p>

#### Comuns

Se o manipulador não encontrar `comandos` ou `entradas`, ele verifica a carga de texto contra manipuladores `comuns`.

Aconselhamos usar com moderação, pois verifica iterando sobre todas as entradas.

#### Não Processado

E a etapa final, se o manipulador não encontrar nenhuma atividade correspondente ([`UpdateHandler`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-update-handler/index.html) funciona completamente em paralelo e não conta como atividade usual), então o [`UnprocessedHandler`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-unprocessed-handler/index.html) entra em ação, se estiver definido, ele lidará com este caso, pode ser útil avisar o usuário que algo deu errado.

Mais detalhes leia no [artigo Manipuladores](Handlers.md).

### RateLimiter de Atividade

Após encontrar uma atividade, também verifica os limites de taxa do usuário sobre ela, de acordo com os parâmetros especificados nos parâmetros da atividade.

### Atividade

Atividade refere-se aos diferentes tipos de manipuladores que a biblioteca de bots do telegram pode manipular, incluindo Comandos, Entradas, Expressões Regulares e o manipulador Não Processado.

### Invocação

A etapa final de processamento é a invocação da atividade encontrada.

Mais detalhes podem ser encontrados no [artigo de invocação](Activity-invocation.md).

### Veja também

* [Análise de atualização](Update-parsing.md)
* [Invocação de atividade](Activity-invocation.md)
* [Manipuladores](Handlers.md)
* [Configuração do bot](Bot-configuration.md)
* [Iniciadores Web (Spring, Ktor)](Web-starters-(Spring-and-Ktor.md))
---