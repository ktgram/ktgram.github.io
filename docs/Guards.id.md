---
---
title: Guards
---

### Pengantar
Guards adalah fitur penting bagi pengembang yang membuat bot. Guards ini berfungsi sebagai pemeriksaan pra-eksekusi yang menentukan apakah perintah tertentu harus dipanggil. Dengan menerapkan pemeriksaan ini, pengembang dapat meningkatkan fungsionalitas, keamanan, dan pengalaman pengguna bot mereka.

### Tujuan Activity Guards
Tujuan utama activity guards adalah untuk memastikan bahwa hanya pengguna yang berwenang atau kondisi tertentu yang memicu sebuah activity.

Hal ini dapat mencegah penyalahgunaan, menjaga integritas bot, dan merampingkan interaksi.

### Kasus Penggunaan Umum
1. Otentikasi dan Otorisasi: Memastikan hanya pengguna tertentu yang dapat mengakses perintah tertentu.
2. Pemeriksaan Pra-kondisi: Memverifikasi bahwa kondisi tertentu terpenuhi sebelum mengeksekusi sebuah activity (misalnya, memastikan pengguna berada dalam status atau konteks tertentu).
3. Guards Kontekstual: Membuat keputusan berdasarkan status obrolan atau pengguna saat ini.

### Strategi Implementasi
Menerapkan Telegram Command Guards biasanya melibatkan penulisan fungsi atau metode yang mengenkapsulasi logika untuk setiap guard. Berikut adalah strategi umum:

1. Pemeriksaan Peran Pengguna:
   - Memastikan pengguna memiliki peran yang diperlukan (misalnya, admin, moderator) sebelum mengeksekusi perintah.
      ```kotlin
       override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // Periksa apakah pengguna adalah admin dalam obrolan yang diberikan
       }
      ```

2. Verifikasi Status:
   - Memeriksa status pengguna sebelum mengizinkan eksekusi perintah.
     ```kotlin
     override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        return bot.userData[user.id, "data"] == requiredState
     }
     ```

3. Guards Kustom:
   - Membuat logika kustom berdasarkan persyaratan spesifik.
     ```kotlin
     override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // Logika kustom untuk menentukan apakah perintah harus dieksekusi
     }
     ```

### Mengintegrasikan Guards dengan Activities
Untuk mengintegrasikan guards ini dengan perintah bot Anda, Anda dapat membuat guard yang memeriksa kondisi-kondisi ini sebelum handler perintah dipanggil.

### Contoh Implementasi

```kotlin
// definisikan di suatu tempat kelas guard Anda yang mengimplementasikan interface Guard
object YourGuard : Guard {
    override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // tulis kondisi Anda di sini
    }
}

// ...

@CommandHandler(["yourCommand"])
@Guard(YourGuard::class) // InputHandler juga didukung
fun command(bot: TelegramBot) {
   // tubuh perintah
}
```

### Praktik Terbaik

- Modularitas: Jaga agar logika guard tetap modular dan terpisah dari activities.
- Reusability: Tulis fungsi guard yang dapat digunakan kembali yang dapat dengan mudah diterapkan di berbagai perintah/input.
- Efisiensi: Optimalkan pemeriksaan guard untuk meminimalkan overhead kinerja.
- Umpan Balik Pengguna: Berikan umpan balik yang jelas kepada pengguna ketika perintah diblokir oleh guard.

### Kesimpulan

Activity Guards adalah alat yang ampuh untuk mengelola eksekusi perintah/input bot.

Dengan menerapkan mekanisme guard yang kuat, pengembang dapat memastikan bot mereka beroperasi secara aman dan efisien, memberikan pengalaman pengguna yang lebih baik.

### Lihat juga

* [Activities and Proccessors](Activites-and-Processors.md)
* [Update parsing](Update-parsing.md)
* [Actions](Actions.md)
* [Activity invocation](Activity-invocation.md)