---
---
title: F.A.Q
---

### `AbstractMethodError` exception

Se você está recebendo essa exceção na inicialização da sua aplicação:

```kotlin
Exception in thread "DefaultDispatcher-worker-1" java.lang.AbstractMethodError: 'kotlinx.serialization.KSerializer[] kotlinx.serialization.internal.GeneratedSerializer.typeParametersSerializers()'
	at eu.vendeli.tgbot.types.options.GetUpdatesOptions$$serializer.typeParametersSerializers(GetUpdatesOptions.kt:6)
```

Isso acontece porque o seu sistema de build está resolvendo uma biblioteca de serialização antiga, cuja mecânica interna difere.  
Para resolver, faça com que ele use uma versão mais nova, por exemplo adicionando isto ao seu buildscript:

```kotlin
configurations.all {
    resolutionStrategy.eachDependency {
        val serdeVer = "x.x.x" // should be >= 1.8.0
        when(requested.module.toString()) {
            // json serialiazaton
            "org.jetbrains.kotlinx:kotlinx-serialization-json" -> useVersion(serdeVer)
            "org.jetbrains.kotlinx:kotlinx-serialization-json-jvm" -> useVersion(serdeVer)
            "org.jetbrains.kotlinx:kotlinx-serialization-core" -> useVersion(serdeVer)
            "org.jetbrains.kotlinx:kotlinx-serialization-core-jvm" -> useVersion(serdeVer)
            "org.jetbrains.kotlinx:kotlinx-serialization-bom" -> useVersion(serdeVer)
        }
    }
}
```

(Se estivesse bem descrito no changelog, eu nunca teria atualizado porque recebo muitos relatórios sobre esse problema)

### How do I get the method's response?

Para obter uma resposta e poder operá‑la, você precisa usar `sendReturning` ao final do método ao invés de `send`.

Nesse caso a classe `Response` é retornada, contendo a resposta, sucesso ou falha; então você deve tratar a falha ou simplesmente chamar `getOrNull()`.

Há uma seção sobre: [Processing responses](https://github.com/vendelieu/telegram-bot#processing-responses).

### I'm getting error while using `spring-boot-devtools`

Isso ocorre porque o `spring-boot-devtools` tem seu próprio `classloader` e não encontra os métodos.

Você precisa adicionar em `resources/META-INF/spring-devtools.properties`:

```properties
restart.include.generated=/eu.vendeli
```

### How to change ktor engine

Se você quiser mudar o engine usado pelo cliente, basta alterar o [parâmetro](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/ktor-jvm-engine.html) nas [configurações do plugin](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/index.html).

### How to use my favorite logging provider

A biblioteca usa `slf4j-api` e, para usar o provedor, basta adicioná‑lo nas dependências.

O plugin da biblioteca detecta automaticamente o uso do provedor; se o provedor estiver ausente, `logback` será usado por padrão.

### Catch network exceptions within long-polling handler

Por exemplo, se você tem uma conexão instável e precisa capturar um erro por causa disso, talvez esta abordagem ajude:

```kotlin
fun main() {
    val bot = TelegramBot("TOKEN")

    try {
        bot.handleUpdates()
    } catch (e: Exception) {
        // handle if needed
        
        bot.update.stopListener()
        bot.handleUpdates()
    }
}
```

Também pode ver como isso é feito no [spring-starter](https://github.com/vendelieu/telegram-bot/blob/1584d40f9a94a8c31bba9e7614c0070155630a52/spring-ktgram-starter/src/jvmMain/kotlin/eu/vendeli/spring/starter/TelegramAutoConfiguration.kt#L53).

---