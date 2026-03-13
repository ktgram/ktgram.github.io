---
---
title: Interceptors (Middleware)
---

### Interceptors: Cross-Cutting Logic untuk Bot Anda

Saat membangun bot Telegram, Anda sering mengulangi setup, pengecekan, atau pembersihan di berbagai handler. Interceptors memungkinkan Anda menyisipkan logika bersama di sekitar handler, menjaga handler tetap fokus dan mudah dipelihara.

Inilah cara interceptors bekerja di *telegram-bot* dan cara menggunakannya.

### Apa Itu Interceptors? (Penjelasan Sederhana)

Interceptors adalah fungsi yang berjalan pada titik-titik tertentu dalam pipeline pemrosesan update. Mereka memungkinkan Anda:
- Memeriksa dan memodifikasi konteks pemrosesan
- Menambahkan logika cross-cutting (logging, auth, metrics)
- Menghentikan pemrosesan lebih awal jika diperlukan
- Membersihkan sumber daya setelah pemrosesan

Bayangkan interceptors sebagai checkpoint yang setiap update lalui sebelum, selama, dan setelah eksekusi handler.


### Pipeline Pemrosesan

Bot memproses update melalui pipeline dengan tujuh fase:

| Fase | Kapan Dijalankan | Apa yang Bisa Anda Gunakan |
|-------|--------------|-------------------------|
| **Setup** | Segera setelah update tiba, sebelum pemrosesan | ✔ Pembatasan laju global<br>✔ Filter spam atau update yang salah format<br>✔ Logging awal<br>✔ Setup konteks bersama |
| **Parsing** | Setelah setup, mengekstrak command dan parameter | ✔ Custom command parsing<br>✔ Enrich konteks dengan data yang telah diparsing<br>✔ Validasi struktur update |
| **Match** | Mencari handler yang sesuai (Command/Input/Common) | ✔ Override pemilihan handler<br>✔ Custom logic penanganan input<br>✔ Log handler yang cocok |
| **Validation** | Setelah handler ditemukan, sebelum invokasi | ✔ Permissions spesifik handler<br>✔ Pembatasan laju per handler<br>✔ Guard checks<br>✔ Batalkan pemrosesan jika kondisi tidak terpenuhi |
| **PreInvoke** | Segera sebelum handler berjalan | ✔ Pengecekan menit terakhir<br>✔ Mulai timer/metrics<br>✔ Enrich konteks untuk handler<br>✔ Modifikasi perilaku handler |
| **Invoke** | Handler dieksekusi di sini | ✔ Wrap eksekusi handler<br>✔ Error handling<br>✔ Logging hasil handler |
| **PostInvoke** | Setelah handler selesai (sukses atau gagal) | ✔ Cleanup sumber daya<br>✔ Log hasil<br>✔ Kirim pesan fallback saat error<br>✔ Modifikasi hasil sebelum dikembalikan |


### Membuat Interceptor

Interceptor adalah fungsi sederhana yang menerima `ProcessingContext`:

```kotlin
import eu.vendeli.tgbot.core.PipelineInterceptor
import eu.vendeli.tgbot.types.component.ProcessingContext

val myInterceptor: PipelineInterceptor = { context ->
    // Your logic here
    println("Processing update: ${context.update.updateId}")
}
```

Atau menggunakan lambda:

```kotlin
val loggingInterceptor = PipelineInterceptor { context ->
    val logger = context.bot.config.loggerFactory.get("MyInterceptor")
    logger.info("Processing update #${context.update.updateId}")
}
```


### Mendaftarkan Interceptors

Daftarkan interceptors pada pipeline pemrosesan:

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

    // Register an interceptor for the Setup phase
    bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
        // Check if user is banned
        val user = context.update.userOrNull
        if (user != null && isBanned(user.id)) {
            context.finish() // Stop processing
            return@intercept
        }
    }

    // Register an interceptor for the PreInvoke phase
    bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
        val startTime = System.currentTimeMillis()
        // store start time
    }

    // Register an interceptor for the PostInvoke phase
    bot.update.pipeline.intercept(ProcessingPipePhase.PostInvoke) { context ->
        val startTime = // get start time
        if (startTime != null) {
            val duration = System.currentTimeMillis() - startTime
            println("Handler took ${duration}ms")
        }
    }

    bot.handleUpdates()
}
```

### Contoh Nyata: Authentication & Metrics

Contoh: bot yang memerlukan autentikasi untuk command tertentu, mengukur waktu eksekusi handler, dan melog semua command.

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")

    // Setup phase: Check if user is authenticated
    bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
        val user = context.update.userOrNull ?: return@intercept

        if (!isAuthenticated(user.id)) {
            message { "Please authenticate first using /login" }
                .send(user, context.bot)
            context.finish()
        }
    }

    // PreInvoke phase: Start timer and check permissions
    bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
        val activity = context.activity ?: return@intercept
        val user = context.update.userOrNull ?: return@intercept

        // Check if user has permission for this specific handler
        if (!hasPermission(user.id, activity)) {
            message { "You don't have permission to use this command." }
                .send(user, context.bot)
            context.finish()
            return@intercept
        }

        // Start timer
        // store start time
    }

    // PostInvoke phase: Log and cleanup
    bot.update.pipeline.intercept(ProcessingPipePhase.PostInvoke) { context ->
        val activity = context.activity ?: return@intercept
        val startTime = // get start time

        if (startTime != null) {
            val duration = System.currentTimeMillis() - startTime
            val logger = context.bot.config.loggerFactory.get("Metrics")
            logger.info(
                "Handler ${activity::class.simpleName} took ${duration}ms " +
                "for user ${context.update.userOrNull?.id}"
            )
        }
    }

    bot.handleUpdates()
}
```


### ProcessingContext

`ProcessingContext` menyediakan akses ke:

- **`update: ProcessedUpdate`** - Update yang sedang diproses
- **`bot: TelegramBot`** - Bot instance
- **`registry: ActivityRegistry`** - Activity registry
- **`parsedInput: String`** - Text command/input yang telah diparsing
- **`parameters: Map<String, String>`** - Parameter command yang telah diparsing
- **`activity: Activity?`** - Handler yang telah diresolusi (null sampai fase Match)
- **`shouldProceed: Boolean`** - Apakah pemrosesan harus dilanjutkan
- **`additionalContext: AdditionalContext`** - Data konteks tambahan
- **`finish()`** - Stop pemrosesan lebih awal

#### Menghentikan Pemrosesan Lebih Awal

Panggil `context.finish()` untuk menghentikan pemrosesan:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.Validation) { context ->
    if (someCondition) {
        context.finish() // Tidak ada fase selanjutnya yang akan dieksekusi
    }
}
```

#### Menyimpan Data Custom

Gunakan `additionalContext` untuk mengirim data antar interceptors:

```kotlin
// In PreInvoke
context.additionalContext["userId"] = context.update.userOrNull?.id

// In PostInvoke
val userId = context.additionalContext["userId"] as? Long
```


### Multiple Interceptors

Anda dapat mendaftarkan multiple interceptors untuk fase yang sama. Mereka dieksekusi dalam urutan pendaftaran:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    println("First interceptor")
}

bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    println("Second interceptor")
}

// When an update is processed:
// Output: "First interceptor"
// Output: "Second interceptor"
```

Jika interceptor memanggil `context.finish()`, interceptors selanjutnya pada fase tersebut akan dilewati, dan fase selanjutnya tidak akan dieksekusi.


### Best Practices

#### 1. Gunakan Fase yang Tepat

- Setup: Global checks, filtering, initial setup
- Parsing: Custom parsing logic
- Match: Handler selection logic
- Validation: Permissions, rate limits, guards
- PreInvoke: Handler-specific preparation
- Invoke: Biasanya ditangani oleh interceptor default
- PostInvoke: Cleanup, logging, error handling

#### 2. Keep Interceptors Focused

Setiap interceptor seharusnya melakukan satu hal:

```kotlin
// ✅ Good - focused interceptor
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    if (isBanned(context.update.userOrNull?.id)) {
        context.finish()
    }
}

// ❌ Avoid - doing too much
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    // Authentication
    // Logging
    // Metrics
    // Rate limiting
    // ... too much!
}
```

#### 3. Handle Errors Gracefully

Interceptors seharusnya tidak crash bot:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
    try {
        // Your logic
    } catch (e: Exception) {
        val logger = context.bot.config.loggerFactory.get("Interceptor")
        logger.error("Interceptor error", e)
        // Don't call context.finish() unless you want to stop processing
    }
}
```

#### 4. Clean Up Resources

Jika Anda membuka sumber daya di `PreInvoke`, bersihkan di `PostInvoke`:

```kotlin
var timer: Timer? = null

bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
    timer = Timer()
    context.additionalContext["timer"] = timer
}

bot.update.pipeline.intercept(ProcessingPipePhase.PostInvoke) { context ->
    val timer = context.additionalContext["timer"] as? Timer
    timer?.stop()
}
```

#### 5. Order Matters

Daftarkan interceptors dalam urutan yang Anda inginkan untuk dieksekusi:

```kotlin
// More general checks first
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) {
    // Global ban check
}

// More specific checks later
bot.update.pipeline.intercept(ProcessingPipePhase.Validation) {
    // Handler-specific permission check
}
```

#### 6. Use Interceptors for Cross-Cutting Concerns

Interceptors ideal untuk:
- ✅ Authentication/authorization
- ✅ Logging
- ✅ Metrics/performance monitoring
- ✅ Rate limiting
- ✅ Error handling
- ✅ Request/response transformation

Untuk logic spesifik handler, simpan di handler.


### Default Interceptors

Framework menyertakan default interceptors untuk fungsionalitas inti:

- **DefaultSetupInterceptor**: Global rate limiting
- **DefaultParsingInterceptor**: Command parsing
- **DefaultMatchInterceptor**: Handler matching (commands, inputs, common matchers)
- **DefaultValidationInterceptor**: Guard checks dan per-handler rate limiting
- **DefaultInvokeInterceptor**: Handler execution dan error handling

Custom interceptors Anda berjalan bersama default ini. Anda bisa menambahkan logic sebelum atau sesudah default, tapi Anda tidak bisa menghapus default interceptors.

---

### Advanced: Conditional Interceptors

Anda bisa membuat interceptors kondisional:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
    val activity = context.activity ?: return@intercept

    // Only apply to specific handlers
    if (activity::class.simpleName?.contains("Admin") == true) {
        // Admin-specific logic
        checkAdminPermissions(context)
    }
}
```


### Summary

Interceptors menyediakan cara bersih untuk menambahkan logika cross-cutting ke bot Anda:

- ✅ **Tujuh fase** untuk tahapan pemrosesan yang berbeda
- ✅ **API sederhana**: Cukup implementasikan `PipelineInterceptor`
- ✅ **Fleksibel**: Daftarkan multiple interceptors per fase
- ✅ **Powerful**: Akses ke full processing context
- ✅ **Aman**: Bisa stop pemrosesan lebih awal dengan `context.finish()`

Gunakan interceptors untuk menjaga handler Anda fokus pada business logic sambil menangani concerns bersama seperti authentication, logging, dan metrics secara terpusat.

---

### Lihat juga

* [Functional Handling DSL](Functional-handling-DSL.md) - Functional update processing
* [Guards](Guards.md) - Handler-level permission checks
---