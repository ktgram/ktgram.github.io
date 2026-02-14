---
---
title: F.A.Q
---

### Exceção `AbstractMethodError`

Se você está obtendo essa exceção ao iniciar seu aplicativo:

```kotlin
Exception in thread "DefaultDispatcher-worker-1" java.lang.AbstractMethodError: 'kotlinx.serialization.KSerializer[] kotlinx.serialization.internal.GeneratedSerializer.typeParametersSerializers()'
	at eu.vendeli.tgbot.types.options.GetUpdatesOptions$$serializer.typeParametersSerializers(GetUpdatesOptions.kt:6)
```

Isso acontece porque seu sistema de build está resolvendo uma biblioteca de serialização antiga cuja mecânica interna difere.
Para resolver isso você deve fazer com que use uma versão mais recente, por exemplo adicionando isso ao seu buildscript:

```kotlin
configurations.all {
    resolutionStrategy.eachDependency {
        val serdeVer = "x.x.x" // deve ser >= 1.8.0
        when(requested.module.toString()) {
            // serialização json
            "org.jetbrains.kotlinx:kotlinx-serialization-json" -> useVersion(serdeVer)
            "org.jetbrains.kotlinx:kotlinx-serialization-json-jvm" -> useVersion(serdeVer)
            "org.jetbrains.kotlinx:kotlinx-serialization-core" -> useVersion(serdeVer)
            "org.jetbrains.kotlinx:kotlinx-serialization-core-jvm" -> useVersion(serdeVer)
            "org.jetbrains.kotlinx:kotlinx-serialization-bom" -> useVersion(serdeVer)
        }
    }
}
```

(Se estivesse bem descrito no changelog eu nunca teria atualizado, pois estou recebendo tantos relatórios sobre este problema)

### Como obter a resposta do método?

Para obter uma resposta e poder operar sobre ela, você precisa usar `sendReturning` no final do método em vez de `send`.

Neste caso a classe `Response` é retornada, que contém a resposta, sucesso ou falha, posteriormente você precisa ou tratar a falha ou simplesmente chamar `getOrNull()`.

Há uma seção sobre: [Processando respostas](https://github.com/vendelieu/telegram-bot#processing-responses).

### Estou obtendo erro ao usar `spring-boot-devtools`

Isso acontece porque `spring-boot-devtools` tem seu próprio `classloader` e não encontra os métodos.

Você precisa adicionar ao `resources/META-INF/spring-devtools.properties`:

```properties
restart.include.generated=/eu.vendeli
```

### Como mudar o motor ktor

Se você quiser mudar o motor usado pelo cliente você pode simplesmente mudar o [parâmetro](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/ktor-jvm-engine.html) nas [configurações do plugin](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/index.html).

### Como usar meu provedor de logging favorito

A biblioteca usa `slf4j-api` e para usar o provedor você só precisa adicioná-lo às dependências.

O plugin da biblioteca detecta automaticamente o uso do provedor, se o provedor estiver ausente, `logback` será usado por padrão.

### Capturar exceções de rede dentro do manipulador de long-polling

Por exemplo, se você tem uma conexão instável e precisa capturar um erro por causa disso, talvez esta abordagem ajude você:

```kotlin
fun main() {
    val bot = TelegramBot("TOKEN")

    try {
        bot.handleUpdates()
    } catch (e: Exception) {
        // tratar se necessário
        
        bot.update.stopListener()
        bot.handleUpdates()
    }
}
```

Você também pode dar uma olhada em como é feito no [spring-starter](https://github.com/vendelieu/telegram-bot/blob/1584d40f9a94a8c31bba9e7614c0070155630a52/spring-ktgram-starter/src/jvmMain/kotlin/eu/vendeli/spring/starter/TelegramAutoConfiguration.kt#L53).

---