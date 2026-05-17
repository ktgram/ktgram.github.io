---
---
title: Interceptors (Middleware)
---

### Interceptors: Cross-Cutting Logic for Your Bot

Saat membangun bot Telegram, Anda sering mengulang-ulang setup, pengecekan, atau pembersihan di berbagai handler. Interceptors memungkinkan Anda menyisipkan logika bersama di sekitar handler, sehingga handler tetap fokus dan mudah dipelihara.

Berikut cara kerja interceptors di *telegram-bot* dan cara menggunakannya.

### What Are Interceptors? (Simple Explanation)

Interceptors adalah fungsi yang dijalankan pada titik tertentu dalam pipeline pemrosesan update. Mereka memungkinkan Anda:
- Memeriksa dan memodifikasi konteks pemrosesan
- Menambahkan logika lintas‑bagian (logging, auth, metrics)
- Menghentikan pemrosesan lebih awal bila diperlukan
- Membersihkan sumber daya setelah pemrosesan

Anggap interceptors sebagai titik pemeriksaan yang dilalui setiap update sebelum, selama, dan setelah eksekusi handler.


### The Processing Pipeline

Bot memproses update melalui pipeline dengan tujuh fase:

| Phase | When It Runs | What You Can Use It For |
|-------|--------------|-------------------------|
| **Setup** | Segera setelah update tiba, sebelum ada pemrosesan | ✔ Global rate limiting<br>✔ Filter spam atau update yang malformed<br>✔ Logging awal<br>✔ Setup konteks bersama |
| **Parsing** | Setelah setup, mengekstrak perintah dan parameter | ✔ Parsing perintah khusus<br>✔ Memperkaya konteks dengan data yang diparse<br>✔ Validasi struktur update |
| **Match** | Menemukan handler yang tepat (Command/Input/Common) | ✔ Menimpa pemilihan handler<br>✔ Logika penanganan input khusus<br>✔ Log handler yang cocok |
| **Validation** | Setelah handler ditemukan, sebelum dipanggil | ✔ Izin khusus handler<br>✔ Rate limiting per handler<br>✔ Guard checks<br>✔ Membatalkan pemrosesan bila kondisi tidak terpenuhi |
| **PreInvoke** | Tepat sebelum handler dijalankan | ✔ Pemeriksaan menit terakhir<br>✔ Mulai timer/metrics<br>✔ Memperkaya konteks untuk handler<br>✔ Memodifikasi perilaku handler |
| **Invoke** | Handler dieksekusi di sini | ✔ Membungkus eksekusi handler<br>✔ Penanganan error<br>✔ Logging hasil handler |
| **PostInvoke** | Setelah handler selesai (sukses atau gagal) | ✔ Pembersihan sumber daya<br>✔ Log hasil<br>✔ Mengirim pesan fallback saat error<br>✔ Memodifikasi hasil sebelum dikembalikan |


### Creating an Interceptor

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


### Registering Interceptors

Daftarkan interceptor pada pipeline pemrosesan:

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

### Real-World Example: Authentication & Metrics

Contoh: bot yang memerlukan autentikasi untuk perintah tertentu, mengukur waktu eksekusi handler, dan mencatat semua perintah.

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
- **`bot: TelegramBot`** - Instance bot
- **`registry: ActivityRegistry`** - Registry aktivitas
- **`parsedInput: String`** - Teks perintah/input yang diparse
- **`parameters: Map<String, String>`** - Parameter perintah yang diparse
- **`activity: Activity?`** - Handler yang terdeteksi (null sampai fase Match)
- **`shouldProceed: Boolean`** - Apakah pemrosesan harus dilanjutkan
- **`additionalContext: AdditionalContext`** - Data konteks tambahan
- **`finish()`** - Hentikan pemrosesan lebih awal

#### Stopping Processing Early

Panggil `context.finish()` untuk menghentikan pemrosesan:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.Validation) { context ->
    if (someCondition) {
        context.finish() // No further phases will execute
    }
}
```

#### Storing Custom Data

Gunakan `additionalContext` untuk meneruskan data antar interceptor:

```kotlin
// In PreInvoke
context.additionalContext["userId"] = context.update.userOrNull?.id

// In PostInvoke
val userId = context.additionalContext["userId"] as? Long
```


### Multiple Interceptors

Anda dapat mendaftarkan beberapa interceptor untuk fase yang sama. Mereka dijalankan sesuai urutan pendaftaran:

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

Jika sebuah interceptor memanggil `context.finish()`, interceptor selanjutnya pada fase itu akan dilewati, dan fase berikutnya tidak akan dijalankan.


### Best Practices

#### 1. Use the Right Phase

- Setup: Pemeriksaan global, penyaringan, setup awal
- Parsing: Logika parsing khusus
- Match: Logika pemilihan handler
- Validation: Izin, rate limit, guard
- PreInvoke: Persiapan khusus handler
- Invoke: Biasanya ditangani oleh interceptor default
- PostInvoke: Pembersihan, logging, penanganan error

#### 2. Keep Interceptors Focused

Setiap interceptor harus melakukan satu hal:

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
    // ... terlalu banyak!
}
```

#### 3. Handle Errors Gracefully

Interceptor tidak boleh membuat bot crash:

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

Daftarkan interceptor dalam urutan yang Anda inginkan mereka berjalan:

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

Interceptor ideal untuk:
- ✅ Autentikasi/otorisasi
- ✅ Logging
- ✅ Metrics/pemantauan performa
- ✅ Rate limiting
- ✅ Penanganan error
- ✅ Transformasi request/response

Untuk logika khusus handler, simpan di dalam handler.


### Default Interceptors

Framework menyediakan interceptor default untuk fungsi inti:

- **DefaultSetupInterceptor**: Global rate limiting
- **DefaultParsingInterceptor**: Parsing perintah
- **DefaultMatchInterceptor**: Pencocokan handler (commands, inputs, common matchers)
- **DefaultValidationInterceptor**: Guard checks dan rate limiting per handler
- **DefaultInvokeInterceptor**: Eksekusi handler dan penanganan error

Interceptor kustom Anda berjalan bersamaan dengan default ini. Anda dapat menambahkan logika sebelum atau sesudah default, tetapi tidak dapat menghapus interceptor default.

---

### Advanced: Conditional Interceptors

Anda dapat membuat interceptor bersifat kondisional:

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

Interceptor menyediakan cara bersih untuk menambahkan logika lintas‑bagian ke bot Anda:

- ✅ **Seven phases** untuk berbagai tahap pemrosesan
- ✅ **Simple API**: Cukup implementasikan `PipelineInterceptor`
- ✅ **Flexible**: Daftarkan banyak interceptor per fase
- ✅ **Powerful**: Akses penuh ke konteks pemrosesan
- ✅ **Safe**: Dapat menghentikan pemrosesan lebih awal dengan `context.finish()`

Gunakan interceptor untuk menjaga handler Anda fokus pada logika bisnis sementara concern bersama seperti autentikasi, logging, dan metrics ditangani secara terpusat.

---

### See also

* [Handlers (incl. Functional DSL)](Handlers.md) - Annotation- and DSL-based handler definition
* [Sessions](Sessions.md) - Per-chat / per-user state &amp; message tracking
* [Guards](Guards.md) - Handler-level permission checks
---