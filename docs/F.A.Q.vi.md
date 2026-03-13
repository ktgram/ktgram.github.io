---
---
title: F.A.Q
---

### Ngoại lệ `AbstractMethodError`

Nếu bạn gặp ngoại lệ này khi khởi động ứng dụng:

```kotlin
Exception in thread "DefaultDispatcher-worker-1" java.lang.AbstractMethodError: 'kotlinx.serialization.KSerializer[] kotlinx.serialization.internal.GeneratedSerializer.typeParametersSerializers()'
	at eu.vendeli.tgbot.types.options.GetUpdatesOptions$$serializer.typeParametersSerializers(GetUpdatesOptions.kt:6)
```

Điều này xảy ra vì hệ thống build của bạn đang sử dụng thư viện serialization cũ với cơ chế nội tại khác biệt.
Để giải quyết, bạn cần buộc nó sử dụng phiên bản mới hơn, ví dụ bằng cách thêm đoạn này vào buildscript:

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

(Nếu điều này được mô tả rõ trong changelog thì tôi đã không bao giờ nâng cấp nó vì tôi nhận được quá nhiều báo cáo về vấn đề này)

### Làm thế nào để lấy response của phương thức?

Để lấy response và có thể thao tác với nó, bạn cần sử dụng `sendReturning` ở cuối phương thức thay vì `send`.

Trong trường hợp này, lớp `Response` sẽ được trả về, chứa response, thành công hoặc thất bại, sau đó bạn cần hoặc xử lý thất bại hoặc đơn giản gọi `getOrNull()`.

Có một phần về: [Xử lý responses](https://github.com/vendelieu/telegram-bot#processing-responses).

### Tôi gặp lỗi khi sử dụng `spring-boot-devtools`

Điều này xảy ra vì `spring-boot-devtools` có `classloader` riêng và không tìm thấy các phương thức.

Bạn cần thêm vào `resources/META-INF/spring-devtools.properties`:

```properties
restart.include.generated=/eu.vendeli
```

### Làm thế nào để thay đổi ktor engine

Nếu bạn muốn thay đổi engine được client sử dụng, bạn có thể đơn giản thay đổi [parameter](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/ktor-jvm-engine.html) trong [plugin settings](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/index.html).

### Làm thế nào để sử dụng nhà cung cấp logging yêu thích

Thư viện sử dụng `slf4j-api` và để sử dụng nhà cung cấp, bạn chỉ cần thêm nó vào dependencies.

Plugin thư viện tự động phát hiện việc sử dụng nhà cung cấp, nếu nhà cung cấp bị thiếu, `logback` sẽ được sử dụng mặc định.

### Bắt ngoại lệ mạng trong long-polling handler

Ví dụ nếu bạn có kết nối không ổn định và cần bắt lỗi do điều này, có lẽ cách tiếp cận này sẽ giúp bạn:

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

Bạn cũng có thể xem cách thực hiện trong [spring-starter](https://github.com/vendelieu/telegram-bot/blob/1584d40f9a94a8c31bba9e7614c0070155630a52/spring-ktgram-starter/src/jvmMain/kotlin/eu/vendeli/spring/starter/TelegramAutoConfiguration.kt#L53).