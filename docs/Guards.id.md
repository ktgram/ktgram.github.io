---
---
title: Guards
---

### Pengantar
Guards adalah fitur penting bagi pengembang yang membuat bot. Guards ini berfungsi sebagai pemeriksaan pra-eksekusi yang menentukan apakah suatu perintah tertentu harus dipanggil. Dengan menerapkan pemeriksaan ini, pengembang dapat meningkatkan fungsionalitas, keamanan, dan pengalaman pengguna bot mereka.

### Tujuan Activity Guards
Tujuan utama activity guards adalah untuk memastikan bahwa hanya pengguna yang berwenang atau kondisi tertentu yang memicu suatu activity.

Hal ini dapat mencegah penyalahgunaan, menjaga integritas bot, dan merampingkan interaksi.

### Use Case Umum
1. Autentikasi dan Otorisasi: Memastikan hanya pengguna tertentu yang dapat mengakses perintah tertentu.
2. Pre-condition Checks: Memverifikasi bahwa kondisi tertentu terpenuhi sebelum mengeksekusi suatu activity (misalnya, memastikan pengguna berada dalam status atau konteks tertentu).
3. Contextual Guards: Membuat keputusan berdasarkan status chat atau pengguna saat ini.

### Strategi Implementasi
Mengimplementasikan Telegram Command Guards biasanya melibatkan penulisan fungsi atau metode yang mengenkapsulasi logika untuk setiap guard. Berikut adalah strategi umum:

1. User Role Check:
   - Memastikan pengguna memiliki peran yang diperlukan (misalnya, admin, moderator) sebelum mengeksekusi perintah.
      ```kotlin
       override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // Check if the user is an admin in the given chat
       }
      ```

2. State Verification:
   - Memeriksa status pengguna sebelum mengizinkan eksekusi perintah.
     ```kotlin
     override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        return bot.userData[user.id, "data"] == requiredState
     }
     ```

3. Custom Guards:
   - Membuat logika kustom berdasarkan persyaratan spesifik.
     ```kotlin
     override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // Custom logic to determine if the command should be executed
     }
     ```

### Mengintegrasikan Guards dengan Activities
Untuk mengintegrasikan guards ini dengan perintah bot Anda, Anda dapat membuat guard yang memeriksa kondisi-kondisi ini sebelum handler perintah dipanggil.

### Implementasi Contoh

```kotlin
// define somewhere your guard class that implements Guard interface
object YourGuard : Guard {
    override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // write your condition here
    }
}

// ...

@CommandHandler(["yourCommand"])
@Guard(YourGuard::class) // InputHandler also is supported
fun command(bot: TelegramBot) {
   // command body
}
```

### Praktik Terbaik

- Modularity: Jaga agar logika guard tetap modular dan terpisah dari activities.
- Reusability: Tulis fungsi guard yang dapat digunakan kembali yang dapat dengan mudah diterapkan di berbagai perintah/input.
- Efficiency: Optimalkan pemeriksaan guard untuk meminimalkan overhead kinerja.
- User Feedback: Berikan umpan balik yang jelas kepada pengguna ketika perintah diblokir oleh guard.

### Kesimpulan

Activity Guards adalah alat yang ampuh untuk mengelola eksekusi perintah/input bot.

Dengan mengimplementasikan mekanisme guard yang kuat, pengembang dapat memastikan bot mereka beroperasi secara aman dan efisien, memberikan pengalaman pengguna yang lebih baik.

### Lihat juga

* [Activities and Proccessors](Activites-and-Processors.md)
* [Update parsing](Update-parsing.md)
* [Actions](Actions.md)
* [Activity invocation](Activity-invocation.md)