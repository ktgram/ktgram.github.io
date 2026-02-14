---
---
title: Interceptors (Middleware)
---

### Interceptors: Logika Lintas-Kepentingan untuk Bot Anda

Saat membangun bot Telegram, Anda sering mengulang setup, pengecekan, atau pembersihan di seluruh handler. Interceptors memungkinkan Anda memasang logika bersama di sekitar handler, menjaga handler tetap fokus dan mudah dikelola.

Inilah cara interceptors bekerja di *telegram-bot* dan cara menggunakannya.

### Apa Itu Interceptors? (Penjelasan Sederhana)

Interceptors adalah fungsi yang berjalan pada titik-titik tertentu dalam pipeline pemrosesan update. Mereka memungkinkan Anda:
- Memeriksa dan memodifikasi konteks pemrosesan
- Menambahkan logika lintas-kepentingan (logging, auth, metrik)
- Menghentikan pemrosesan lebih awal jika diperlukan
- Membersihkan sumber daya setelah pemrosesan

Bayangkan interceptors sebagai pos pemeriksaan yang dilewati setiap update sebelum, selama, dan setelah eksekusi handler.


### Pipeline Pemrosesan

Bot memproses update melalui pipeline dengan tujuh fase:

| Fase | Kapan Dijalankan | Apa yang Dapat Digunakan |
|-------|--------------|-------------------------|
| **Setup** | Segera setelah update tiba, sebelum pemrosesan | ✔ Pembatasan laju global<br>✔ Filter spam atau update tidak valid<br>✔ Logging awal<br>✔ Setup konteks bersama |
| **Parsing** | Setelah setup, mengekstrak perintah dan parameter | ✔ Parsing perintah kustom<br>✔ Perkaya konteks dengan data yang diparsing<br>✔ Validasi struktur update |
| **Match** | Menemukan handler yang sesuai (Command/Input/Common) | ✔ Override pemilihan handler<br>✔ Logika penanganan input kustom<br>✔ Log handler yang cocok |
| **Validation** | Setelah handler ditemukan, sebelum dipanggil | ✔ Izin khusus handler<br>✔ Pembatasan laju per handler<br>✔ Pengecekan guard<br>✔ Batalkan pemrosesan jika kondisi tidak terpenuhi |
| **PreInvoke** | Segera sebelum handler berjalan | ✔ Pengecekan menit terakhir<br>✔ Mulai timer/metrik<br>✔ Perkaya konteks untuk handler<br>✔ Modifikasi perilaku handler |
| **Invoke** | Handler dieksekusi di sini | ✔ Bungkus eksekusi handler<br>✔ Penanganan error<br>✔ Logging hasil handler |
| **PostInvoke** | Setelah handler selesai (berhasil atau gagal) | ✔ Bersihkan sumber daya<br>✔ Log hasil<br>✔ Kirim pesan fallback pada error<br>✔ Modifikasi hasil sebelum dikembalikan |


### Membuat Interceptor

Interceptor adalah fungsi sederhana yang menerima `ProcessingContext`:

```kotlin
import eu.vendeli.tgbot.core.PipelineInterceptor
import eu.vendeli.tgbot.types.component.ProcessingContext

val myInterceptor: PipelineInterceptor = { context ->
    // Logika Anda di sini
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
    
    // Daftarkan interceptor untuk fase Setup
    bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
        // Cek apakah user diblokir
        val user = context.update.userOrNull
        if (user != null && isBanned(user.id)) {
            context.finish() // Hentikan pemrosesan
            return@intercept
        }
    }
    
    // Daftarkan interceptor untuk fase PreInvoke
    bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
        val startTime = System.currentTimeMillis()
        // simpan waktu mulai
    }
    
    // Daftarkan interceptor untuk fase PostInvoke
    bot.update.pipeline.intercept(ProcessingPipePhase.PostInvoke) { context ->
        val startTime = // dapatkan waktu mulai
        if (startTime != null) {
            val duration = System.currentTimeMillis() - startTime
            println("Handler took ${duration}ms")
        }
    }
    
    bot.handleUpdates()
}
```

### Contoh Dunia Nyata: Authentication & Metrics

Contoh: bot yang memerlukan autentikasi untuk perintah tertentu, mengukur waktu eksekusi handler, dan melog semua perintah.

```kotlin
suspend fun main() {
    val bot = TelegramBot("BOT_TOKEN")
    
    // Fase Setup: Cek apakah user terautentikasi
    bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
        val user = context.update.userOrNull ?: return@intercept
        
        if (!isAuthenticated(user.id)) {
            message { "Please authenticate first using /login" }
                .send(user, context.bot)
            context.finish()
        }
    }
    
    // Fase PreInvoke: Mulai timer dan cek izin
    bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
        val activity = context.activity ?: return@intercept
        val user = context.update.userOrNull ?: return@intercept
        
        // Cek apakah user memiliki izin untuk handler spesifik ini
        if (!hasPermission(user.id, activity)) {
            message { "You don't have permission to use this command." }
                .send(user, context.bot)
            context.finish()
            return@intercept
        }
        
        // Mulai timer
        // simpan waktu mulai
    }
    
    // Fase PostInvoke: Log dan cleanup
    bot.update.pipeline.intercept(ProcessingPipePhase.PostInvoke) { context ->
        val activity = context.activity ?: return@intercept
        val startTime = // dapatkan waktu mulai
        
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
- **`parsedInput: String`** - Teks input/perintah yang diparsing
- **`parameters: Map<String, String>`** - Parameter perintah yang diparsing
- **`activity: Activity?`** - Handler yang diresolusi (null hingga fase Match)
- **`shouldProceed: Boolean`** - Apakah pemrosesan harus dilanjutkan
- **`additionalContext: AdditionalContext`** - Data konteks tambahan
- **`finish()`** - Hentikan pemrosesan lebih awal

#### Menghentikan Pemrosesan Lebih Awal

Panggil `context.finish()` untuk menghentikan pemrosesan:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.Validation) { context ->
    if (someCondition) {
        context.finish() // Tidak ada fase selanjutnya yang akan dieksekusi
    }
}
```

#### Menyimpan Data Kustom

Gunakan `additionalContext` untuk mengirim data antar interceptors:

```kotlin
// Di PreInvoke
context.additionalContext["userId"] = context.update.userOrNull?.id

// Di PostInvoke
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

// Saat update diproses:
// Output: "First interceptor"
// Output: "Second interceptor"
```

Jika interceptor memanggil `context.finish()`, interceptors selanjutnya di fase tersebut akan dilewati, dan fase selanjutnya tidak akan dieksekusi.


### Best Practices

#### 1. Gunakan Fase yang Tepat

- Setup: Pengecekan global, filtering, setup awal
- Parsing: Logika parsing kustom
- Match: Logika pemilihan handler
- Validation: Izin, pembatasan laju, guard
- PreInvoke: Persiapan khusus handler
- Invoke: Biasanya ditangani oleh interceptor default
- PostInvoke: Cleanup, logging, penanganan error

#### 2. Jaga Interceptors Tetap Fokus

Setiap interceptor harus melakukan satu hal:

```kotlin
// ✅ Baik - interceptor fokus
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    if (isBanned(context.update.userOrNull?.id)) {
        context.finish()
    }
}

// ❌ Hindari - melakukan terlalu banyak
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { context ->
    // Authentication
    // Logging
    // Metrics
    // Rate limiting
    // ... terlalu banyak!
}
```

#### 3. Tangani Error dengan Elegan

Interceptors tidak boleh crash bot:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
    try {
        // Logika Anda
    } catch (e: Exception) {
        val logger = context.bot.config.loggerFactory.get("Interceptor")
        logger.error("Interceptor error", e)
        // Jangan panggil context.finish() kecuali Anda ingin menghentikan pemrosesan
    }
}
```

#### 4. Bersihkan Sumber Daya

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

#### 5. Urutan Penting

Daftarkan interceptors dalam urutan yang Anda inginkan:

```kotlin
// Pengecekan umum lebih dulu
bot.update.pipeline.intercept(ProcessingPipePhase.Setup) { 
    // Pengecekan ban global
}

// Pengecekan spesifik kemudian
bot.update.pipeline.intercept(ProcessingPipePhase.Validation) { 
    // Pengecekan izin khusus handler
}
```

#### 6. Gunakan Interceptors untuk Cross-Cutting Concerns

Interceptors ideal untuk:
- ✅ Authentication/authorization
- ✅ Logging
- ✅ Metrics/performance monitoring
- ✅ Rate limiting
- ✅ Error handling
- ✅ Request/response transformation

Untuk logika khusus handler, simpan di handler.


### Default Interceptors

Framework menyertakan default interceptors untuk fungsionalitas inti:

- **DefaultSetupInterceptor**: Pembatasan laju global
- **DefaultParsingInterceptor**: Parsing perintah
- **DefaultMatchInterceptor**: Pematching handler (commands, inputs, common matchers)
- **DefaultValidationInterceptor**: Guard checks dan pembatasan laju per-handler
- **DefaultInvokeInterceptor**: Eksekusi handler dan penanganan error

Custom interceptors Anda berjalan bersama default ini. Anda dapat menambahkan logika sebelum atau sesudah default, tetapi Anda tidak dapat menghapus default interceptors.

---

### Advanced: Conditional Interceptors

Anda dapat membuat interceptors kondisional:

```kotlin
bot.update.pipeline.intercept(ProcessingPipePhase.PreInvoke) { context ->
    val activity = context.activity ?: return@intercept
    
    // Hanya terapkan ke handler spesifik
    if (activity::class.simpleName?.contains("Admin") == true) {
        // Logika khusus admin
        checkAdminPermissions(context)
    }
}
```


### Summary

Interceptors menyediakan cara bersih untuk menambahkan logika lintas-kepentingan ke bot Anda:

- ✅ **Tujuh fase** untuk tahap pemrosesan berbeda
- ✅ **API sederhana**: Cukup implementasikan `PipelineInterceptor`
- ✅ **Fleksibel**: Daftarkan multiple interceptors per fase
- ✅ **Kuat**: Akses ke konteks pemrosesan lengkap
- ✅ **Aman**: Dapat menghentikan pemrosesan lebih awal dengan `context.finish()`

Gunakan interceptors untuk menjaga handler fokus pada logika bisnis sambil menangani kepentingan bersama seperti authentication, logging, dan metrics secara terpusat.

---

### See also

* [Functional Handling DSL](Functional-handling-DSL.md) - Pemrosesan update fungsional
* [Guards](Guards.md) - Pengecekan izin level handler
---