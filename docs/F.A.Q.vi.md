---
---
title: F.A.Q
---

### `AbstractMethodError` exception

Nếu bạn gặp ngoại lệ này khi khởi động ứng dụng của mình:

```kotlin
Exception in thread "DefaultDispatcher-worker-1" java.lang.AbstractMethodError: 'kotlinx.serialization.KSerializer[] kotlinx.serialization.internal.GeneratedSerializer.typeParametersSerializers()'
	at eu.vendeli.tgbot.types.options.GetUpdatesOptions$$serializer.typeParametersSerializers(GetUpdatesOptions.kt:6)
```

Điều này xảy ra vì hệ thống build của bạn đang giải quyết phiên bản cũ của thư viện serialization có cơ chế nội bộ khác nhau.  
Để giải quyết, bạn nên sử dụng phiên bản mới hơn, ví dụ bằng cách thêm đoạn này vào script build của bạn:

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

(Nếu nó đã được mô tả chi tiết trong changelog, tôi sẽ không nâng cấp nó vì tôi nhận được quá nhiều báo cáo về vấn đề này)

### How do I get the method's response?

Để nhận phản hồi và có thể thao tác với nó, bạn cần dùng `sendReturning` ở cuối phương thức thay vì `send`.

Trong trường hợp này lớp `Response` sẽ được trả về, chứa phản hồi, thành công hoặc thất bại; sau đó bạn cần xử lý thất bại hoặc chỉ gọi `getOrNull()`.

Có phần hướng dẫn về: [Processing responses](https://github.com/vendelieu/telegram-bot#processing-responses).

### I'm getting error while using `spring-boot-devtools`

Điều này xảy ra vì `spring-boot-devtools` có `classloader` riêng và không tìm thấy các phương thức.

Bạn cần thêm vào `resources/META-INF/spring-devtools.properties`:

```properties
restart.include.generated=/eu.vendeli
```

### How to change ktor engine

Nếu muốn thay đổi engine mà client sử dụng, bạn chỉ cần thay đổi [parameter](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/ktor-jvm-engine.html) trong [plugin settings](https://vendelieu.github.io/telegram-bot/ktgram-gradle-plugin/eu.vendeli.ktgram.gradle/-kt-gram-ext/index.html).

### How to use my favorite logging provider

Thư viện sử dụng `slf4j-api` và để dùng provider bạn chỉ cần thêm nó vào các dependency.

Plugin của thư viện tự động phát hiện việc sử dụng provider; nếu thiếu provider, `logback` sẽ được dùng mặc định.

### Catch network exceptions within long-polling handler

Ví dụ nếu bạn có kết nối không ổn định và cần bắt lỗi vì lý do này, có thể cách này sẽ hữu ích:

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

---