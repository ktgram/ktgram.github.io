---
---
title: Fsm Dan Penanganan Percakapan
---

Perpustakaan ini juga mendukung mekanisme FSM, yang merupakan mekanisme untuk pemrosesan progresif input pengguna dengan penanganan input yang salah.

> [!NOTE]
> TL;DR: Lihat contoh [di sana](https://github.com/vendelieu/telegram-bot_template/tree/conversation).

### Secara Teori

Mari kita bayangkan situasi di mana Anda perlu mengumpulkan survei pengguna, Anda dapat meminta semua data seseorang dalam satu langkah, tetapi dengan input yang salah dari salah satu parameter, akan sulit baik untuk pengguna maupun untuk kita, dan setiap langkah mungkin berbeda tergantung pada data input tertentu.

Sekarang mari kita bayangkan input data secara bertahap, di mana bot memasuki mode dialog dengan pengguna.

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/2e84fa00-e59c-4352-8665-83be3b971e7b" alt="Diagram Proses Penanganan" />
</p>

Panah hijau menunjukkan proses transisi melalui langkah-langkah tanpa kesalahan, panah biru berarti menyimpan status saat ini dan menunggu input ulang (misalnya, jika pengguna menunjukkan bahwa dia berusia -100 tahun, itu harus meminta usia lagi), dan yang merah menunjukkan keluar dari seluruh proses karena ada perintah atau pembatalan makna lainnya.

### Secara Praktik

Sistem Wizard memungkinkan interaksi multi-langkah dengan pengguna di bot Telegram. Ini membimbing pengguna melalui urutan langkah-langkah, memvalidasi input, menyimpan status, dan beralih antar langkah.

**Manfaat Utama:**
- **Type-safe**: Pemeriksaan tipe waktu kompilasi untuk akses status
- **Declarative**: Tentukan langkah-langkah sebagai kelas/objek bersarang
- **Flexible**: Dukungan untuk transisi bersyarat, lompatan, dan retry
- **Stateful**: Persistensi status otomatis dengan backend penyimpanan yang dapat dihubungkan
- **Integrated**: Bekerja dengan sistem Activity yang ada

### Konsep Inti

#### WizardStep

`WizardStep` mewakili satu langkah dalam alur wizard. Setiap langkah harus mengimplementasikan:

- **`onEntry(ctx: WizardContext)`**: Dipanggil ketika pengguna memasuki langkah ini. Gunakan ini untuk meminta pengguna.
- **`onRetry(ctx: WizardContext)`**: Dipanggil ketika validasi gagal dan langkah harus retry. Gunakan ini untuk menampilkan pesan kesalahan.
- **`validate(ctx: WizardContext): Transition`**: Memvalidasi input saat ini dan mengembalikan `Transition` yang menunjukkan apa yang terjadi selanjutnya.
- **`store(ctx: WizardContext): Any?`** (opsional): Mengembalikan nilai yang akan disimpan untuk langkah ini. Kembalikan `null` jika langkah tidak menyimpan status.

```kotlin
object NameStep : WizardStep(isInitial = true) {
    override suspend fun onEntry(ctx: WizardContext) {
        message { "What is your name?" }.send(ctx.user, ctx.bot)
    }
    
    override suspend fun onRetry(ctx: WizardContext) {
        message { "Name cannot be empty. Please try again." }.send(ctx.user, ctx.bot)
    }
    
    override suspend fun validate(ctx: WizardContext): Transition {
        return if (ctx.update.text.isNullOrBlank()) {
            Transition.Retry
        } else {
            Transition.Next
        }
    }
    
    override suspend fun store(ctx: WizardContext): String {
        return ctx.update.text!!
    }
}
```

> [!NOTE]
> Jika beberapa langkah tidak ditandai sebagai initial -> langkah pertama yang dideklarasikan dianggap sebagai.

#### Transition

`Transition` menentukan apa yang terjadi setelah validasi:

- **`Transition.Next`**: Pindah ke langkah berikutnya dalam urutan
- **`Transition.JumpTo(step: KClass<out WizardStep>)`**: Lompat ke langkah tertentu
- **`Transition.Retry`**: Retry langkah saat ini (validasi gagal)
- **`Transition.Finish`**: Selesaikan wizard

```kotlin
// Lompatan bersyarat berdasarkan input
override suspend fun validate(ctx: WizardContext): Transition {
    val age = ctx.update.text?.toIntOrNull()
    return when {
        age == null -> Transition.Retry
        age < 18 -> Transition.JumpTo(UnderageStep::class)
        else -> Transition.Next
    }
}
```

#### WizardContext

`WizardContext` menyediakan akses ke:
- **`user: User`**: Pengguna saat ini
- **`update: ProcessedUpdate`**: Update saat ini
- **`bot: TelegramBot`**: Instance bot
- **`userReference: UserChatReference`**: Referensi ID pengguna dan chat untuk penyimpanan status

Plus metode akses status type-safe (dihasilkan oleh KSP).

---

### Mendefinisikan Wizard

#### Struktur Dasar

Wizard didefinisikan sebagai kelas atau objek yang dianotasi dengan `@WizardHandler`:

```kotlin
@WizardHandler(trigger = ["/survey"])
object SurveyWizard {
    object NameStep : WizardStep(isInitial = true) {
        // ... implementasi langkah
    }
    
    object AgeStep : WizardStep {
        // ... implementasi langkah
    }
    
    object FinishStep : WizardStep {
        // ... implementasi langkah
    }
}
```

#### Parameter Anotasi

**`@WizardHandler`** menerima:
- **`trigger: Array<String>`**: Perintah yang memulai wizard (misalnya, `["/start", "/survey"]`)
- **`scope: Array<UpdateType>`**: Tipe update yang akan didengarkan (default: `[UpdateType.MESSAGE]`)
- **`stateManagers: Array<KClass<out WizardStateManager<*>>>`**: Kelas state manager untuk menyimpan data langkah

---

### Manajemen Status

#### WizardStateManager

Status disimpan menggunakan implementasi `WizardStateManager<T>`. Setiap manager menangani tipe tertentu:

```kotlin
interface WizardStateManager<T : Any> {
    suspend fun get(key: KClass<out WizardStep>, reference: UserChatReference): T?
    suspend fun set(key: KClass<out WizardStep>, reference: UserChatReference, value: T)
    suspend fun del(key: KClass<out WizardStep>, reference: UserChatReference)
}
```

Lihat juga: [MapStateManager<T>](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-state-manager/index.html), [MapStringStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-string-state-manager/index.html), [MapIntStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-int-state-manager/index.html), [MapLongStateManager](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.implementations/-map-long-state-manager/index.html).

#### Pencocokan Otomatis

KSP mencocokkan langkah ke state manager berdasarkan tipe kembalian `store()`:

```kotlin
@WizardHandler(
    trigger = ["/survey"],
    stateManagers = [StringStateManager::class, IntStateManager::class]
)
object SurveyWizard {
    object NameStep : WizardStep(isInitial = true) {
        override suspend fun store(ctx: WizardContext): String {
            return ctx.update.text!! // Cocok dengan StringStateManager
        }
    }
    
    object AgeStep : WizardStep {
        override suspend fun store(ctx: WizardContext): Int {
            return ctx.update.text!!.toInt() // Cocok dengan IntStateManager
        }
    }
}
```

#### Override Per-Langkah

Override state manager untuk langkah tertentu menggunakan `@WizardHandler.StateManager`:

```kotlin
@WizardHandler(
    trigger = ["/survey"],
    stateManagers = [DefaultStateManager::class]
)
object SurveyWizard {
    object NameStep : WizardStep(isInitial = true) {
        // Menggunakan DefaultStateManager
    }
    
    @WizardHandler.StateManager(CustomStateManager::class)
    object AgeStep : WizardStep {
        // Menggunakan CustomStateManager sebagai gantinya
    }
}
```

---

### Akses Status Type-Safe

KSP menghasilkan fungsi ekstensi type-safe pada `WizardContext` untuk setiap langkah yang menyimpan status.

#### Fungsi yang Dihasilkan

Untuk langkah yang menyimpan `String`:

```kotlin
// Dihasilkan secara otomatis oleh KSP
suspend inline fun <reified S : WizardStep> WizardContext.getState(): String?
suspend inline fun <reified S : WizardStep> WizardContext.setState(value: String)
suspend inline fun <reified S : WizardStep> WizardContext.delState()
```

#### Penggunaan

```kotlin
object FinishStep : WizardStep {
    override suspend fun onEntry(ctx: WizardContext) {
        // Akses type-safe - mengembalikan String? (nullable)
        val name: String? = ctx.getState<NameStep>()
        
        // Akses type-safe - mengembalikan Int? (nullable)
        val age: Int? = ctx.getState<AgeStep>()
        
        val summary = buildString {
            appendLine("Name: $name")
            appendLine("Age: $age")
        }
        
        message { summary }.send(ctx.user, ctx.bot)
    }
    
    override suspend fun onRetry(ctx: WizardContext) = Unit
    
    override suspend fun validate(ctx: WizardContext): Transition {
        return Transition.Finish
    }
}
```

#### Metode Fallback

Jika metode type-safe tidak tersedia, gunakan metode fallback:

```kotlin
// Fallback - mengembalikan Any?
val name = ctx.getState(NameStep::class)

// Fallback - menerima Any?
ctx.setState(NameStep::class, "John")
ctx.delState(NameStep::class)
```

---

### Contoh Lengkap

#### User Registration Wizard

```kotlin
@WizardHandler(
    trigger = ["/register"],
    stateManagers = [StringStateManager::class, IntStateManager::class]
)
object RegistrationWizard {
    object NameStep : WizardStep(isInitial = true) {
        override suspend fun onEntry(ctx: WizardContext) {
            message { "What is your name?" }.send(ctx.user, ctx.bot)
        }
        
        override suspend fun onRetry(ctx: WizardContext) {
            message { "Please enter a valid name." }.send(ctx.user, ctx.bot)
        }
        
        override suspend fun validate(ctx: WizardContext): Transition {
            val name = ctx.update.text?.trim()
            return if (name.isNullOrBlank() || name.length < 2) {
                Transition.Retry
            } else {
                Transition.Next
            }
        }
        
        override suspend fun store(ctx: WizardContext): String {
            return ctx.update.text!!.trim()
        }
    }
    
    object AgeStep : WizardStep {
        override suspend fun onEntry(ctx: WizardContext) {
            message { "How old are you?" }.send(ctx.user, ctx.bot)
        }
        
        override suspend fun onRetry(ctx: WizardContext) {
            message { "Please enter a valid age (must be a number)." }.send(ctx.user, ctx.bot)
        }
        
        override suspend fun validate(ctx: WizardContext): Transition {
            val age = ctx.update.text?.toIntOrNull()
            return when {
                age == null -> Transition.Retry
                age < 0 || age > 150 -> Transition.Retry
                age < 18 -> Transition.JumpTo(UnderageStep::class)
                else -> Transition.Next
            }
        }
        
        override suspend fun store(ctx: WizardContext): Int {
            return ctx.update.text!!.toInt()
        }
    }
    
    object UnderageStep : WizardStep {
        override suspend fun onEntry(ctx: WizardContext) {
            message { 
                "Sorry, you must be 18 or older to register." 
            }.send(ctx.user, ctx.bot)
        }
        
        override suspend fun onRetry(ctx: WizardContext) = Unit
        
        override suspend fun validate(ctx: WizardContext): Transition {
            return Transition.Finish
        }
    }
    
    object ConfirmationStep : WizardStep {
        override suspend fun onEntry(ctx: WizardContext) {
            // Akses status type-safe
            val name: String? = ctx.getState<NameStep>()
            val age: Int? = ctx.getState<AgeStep>()
            
            val confirmation = buildString {
                appendLine("Please confirm your information:")
                appendLine("Name: $name")
                appendLine("Age: $age")
                appendLine()
                appendLine("Reply 'yes' to confirm or 'no' to start over.")
            }
            
            message { confirmation }.send(ctx.user, ctx.bot)
        }
        
        override suspend fun onRetry(ctx: WizardContext) {
            message { "Please reply 'yes' or 'no'." }.send(ctx.user, ctx.bot)
        }
        
        override suspend fun validate(ctx: WizardContext): Transition {
            val response = ctx.update.text?.lowercase()?.trim()
            return when (response) {
                "yes" -> Transition.Finish
                "no" -> Transition.JumpTo(NameStep::class) // Mulai ulang
                else -> Transition.Retry
            }
        }
    }
    
    object FinishStep : WizardStep {
        override suspend fun onEntry(ctx: WizardContext) {
            val name: String? = ctx.getState<NameStep>()
            val age: Int? = ctx.getState<AgeStep>()
            
            // Simpan ke database, kirim konfirmasi, dll.
            message { 
                "Registration complete! Welcome, $name (age $age)." 
            }.send(ctx.user, ctx.bot)
        }
        
        override suspend fun onRetry(ctx: WizardContext) = Unit
        
        override suspend fun validate(ctx: WizardContext): Transition {
            return Transition.Finish
        }
    }
}
```

---

### Fitur Lanjutan

#### Transisi Bersyarat

Gunakan `Transition.JumpTo` untuk alur bersyarat:

```kotlin
override suspend fun validate(ctx: WizardContext): Transition {
    val choice = ctx.update.text?.lowercase()
    return when (choice) {
        "premium" -> Transition.JumpTo(PremiumStep::class)
        "basic" -> Transition.JumpTo(BasicStep::class)
        else -> Transition.Retry
    }
}
```

#### Langkah Tanpa Status

Langkah tidak perlu menyimpan status. Cukup kembalikan `null` dari `store()` (atau biarkan seperti itu):

```kotlin
object ConfirmationStep : WizardStep {
    override suspend fun store(ctx: WizardContext): Any? = null
    // ... sisa implementasi
}
```

#### State Manager Kustom

Implementasikan `WizardStateManager<T>` untuk penyimpanan kustom (database, Redis, dll.):

```kotlin
class DatabaseStateManager : WizardStateManager<String> {
    override suspend fun get(
        key: KClass<out WizardStep>,
        reference: UserChatReference
    ): String? {
        // Muat dari database
        return database.getWizardState(reference.userId, key.qualifiedName)
    }
    
    override suspend fun set(
        key: KClass<out WizardStep>,
        reference: UserChatReference,
        value: String
    ) {
        // Simpan ke database
        database.saveWizardState(reference.userId, key.qualifiedName, value)
    }
    
    override suspend fun del(
        key: KClass<out WizardStep>,
        reference: UserChatReference
    ) {
        // Hapus dari database
        database.deleteWizardState(reference.userId, key.qualifiedName)
    }
}
```

---

### Cara Kerja Internal

#### Generasi Kode

KSP menghasilkan:

1. **WizardActivity**: Implementasi konkret yang memperluas `WizardActivity` dengan langkah-langkah yang di-hardcode
2. **Start Activity**: Menangani trigger perintah dan memulai wizard
3. **Input Activity**: Menangani input pengguna selama alur wizard
4. **State Accessors**: Fungsi ekstensi type-safe untuk akses status

#### Alur

1. Pengguna mengirim `/register` → Start Activity dipanggil
2. Start Activity membuat `WizardContext` dan memanggil `wizardActivity.start(ctx)`
3. `start()` memasuki langkah awal dan mengatur `inputListener` untuk melacak langkah saat ini
4. Pengguna mengirim pesan → Input Activity dipanggil
5. Input Activity memanggil `wizardActivity.handleInput(ctx)`
6. `handleInput()` memvalidasi input, menyimpan status, dan beralih ke langkah berikutnya
7. Proses berulang hingga `Transition.Finish` dikembalikan

#### Persistensi Status

- Status disimpan setelah validasi berhasil (sebelum transisi)
- Nilai kembalian `store()` dari setiap langkah disimpan menggunakan `WizardStateManager` yang cocok
- Status di-scope per pengguna dan chat (`UserChatReference`)

---

### Praktik Terbaik

#### 1. Selalu Berikan Prompt yang Jelas

```kotlin
override suspend fun onEntry(ctx: WizardContext) {
    message { 
        "Please enter your email address:\n" +
        "(Format: user@example.com)" 
    }.send(ctx.user, ctx.bot)
}
```

#### 2. Tangani Kesalahan Validasi dengan Baik

```kotlin
override suspend fun onRetry(ctx: WizardContext) {
    message { 
        "Invalid email format. Please try again.\n" +
        "Example: user@example.com" 
    }.send(ctx.user, ctx.bot)
}
```

#### 3. Gunakan Akses Status Type-Safe

Lebih suka metode type-safe yang dihasilkan:

```kotlin
// ✅ Bagus - type-safe
val name: String? = ctx.getState<NameStep>()

// ❌ Hindari - kehilangan type safety
val name = ctx.getState(NameStep::class) as? String
```

#### 4. Pertahankan Langkah yang Fokus

Setiap langkah harus memiliki tanggung jawab tunggal:

```kotlin
// ✅ Bagus - langkah fokus
object EmailStep : WizardStep {
    // Hanya menangani pengumpulan email
}

// ❌ Hindari - terlalu banyak logika
object PersonalInfoStep : WizardStep {
    // Menangani nama, email, telepon, alamat...
}
```

#### 5. Gunakan Nama Langkah yang Bermakna

```kotlin
// ✅ Bagus
object EmailVerificationStep : WizardStep

// ❌ Hindari
object Step2 : WizardStep
```

#### 6. Bersihkan Status Jika Diperlukan

Jika Anda perlu menghapus status secara manual:

```kotlin
object CancelStep : WizardStep {
    override suspend fun onEntry(ctx: WizardContext) {
        // Hapus semua status wizard
        ctx.delState<NameStep>()
        ctx.delState<AgeStep>()
        
        message { "Registration cancelled." }.send(ctx.user, ctx.bot)
    }
}
```

---

### Ringkasan

Sistem Wizard menyediakan:
- ✅ **Type-safe** manajemen status dengan pemeriksaan waktu kompilasi
- ✅ **Declarative** definisi langkah sebagai kelas bersarang
- ✅ **Flexible** transisi dengan logika bersyarat
- ✅ **Automatic** generasi kode via KSP
- ✅ **Integrated** dengan sistem Activity yang ada
- ✅ **Pluggable** backend penyimpanan status

Mulailah membangun wizard dengan menganotasi kelas dengan `@WizardHandler` dan mendefinisikan langkah-langkah Anda sebagai objek `WizardStep` bersarang!