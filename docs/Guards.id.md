---
---
title: Guards
---

### Introduction
Guards adalah fitur penting bagi pengembang yang membuat bot. Guard ini berfungsi sebagai pemeriksaan pra-eksekusi yang menentukan apakah suatu perintah tertentu harus dipanggil. Dengan menerapkan pemeriksaan ini, pengembang dapat meningkatkan fungsionalitas, keamanan, dan pengalaman pengguna bot mereka.

### Purpose of Activity Guards
Tujuan utama dari activity guard adalah memastikan hanya pengguna yang berwenang atau kondisi spesifik yang memicu suatu activity.

Hal ini dapat mencegah penyalahgunaan, menjaga integritas bot, dan menyederhanakan interaksi.

### Common Use Cases
1. Authentication and Authorization: Memastikan hanya pengguna tertentu yang dapat mengakses perintah spesifik.  
2. Pre-condition Checks: Memverifikasi bahwa kondisi tertentu terpenuhi sebelum mengeksekusi sebuah activity (mis., memastikan pengguna berada dalam keadaan atau konteks tertentu).  
3. Contextual Guards: Membuat keputusan berdasarkan keadaan chat atau pengguna saat ini.

### Implementation Strategies
Menerapkan Telegram Command Guard biasanya melibatkan penulisan fungsi atau metode yang mengenkapsulasi logika untuk setiap guard. Berikut adalah strategi umum:

1. User Role Check:
   - Memastikan pengguna memiliki peran yang diperlukan (mis., admin, moderator) sebelum mengeksekusi perintah.
      ```kotlin
       override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // Check if the user is an admin in the given chat
       }
      ```
   
2. State Verification:
   - Memeriksa keadaan pengguna sebelum mengizinkan eksekusi perintah.
     ```kotlin
     override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        return bot.userData[user.id, "data"] == requiredState
     }
     ```
   
3. Custom Guards:
   - Membuat logika khusus berdasarkan kebutuhan spesifik.
     ```kotlin
     override suspend fun condition(user: User?, update: ProcessedUpdate, bot: TelegramBot): Boolean {
        // Custom logic to determine if the command should be executed
     }
     ```
   
### Integrating Guards with Activities
Untuk mengintegrasikan guard ini dengan perintah bot Anda, Anda dapat membuat guard yang memeriksa kondisi tersebut sebelum handler perintah dipanggil.

### Implementing Example

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

### Best Practices

- Modularity: Jaga logika guard tetap modular dan terpisah dari activities.  
- Reusability: Tulis fungsi guard yang dapat digunakan kembali dan mudah diterapkan pada berbagai perintah/input.  
- Efficiency: Optimalkan pemeriksaan guard untuk meminimalkan beban kinerja.  
- User Feedback: Berikan umpan balik yang jelas kepada pengguna ketika sebuah perintah diblokir oleh guard.

### Conclusion

Activity Guards adalah alat yang kuat untuk mengelola eksekusi perintah/input bot.

Dengan menerapkan mekanisme guard yang kuat, pengembang dapat memastikan bot mereka beroperasi secara aman dan efisien, memberikan pengalaman pengguna yang lebih baik.

### See also

* [Activities and Proccessors](Activites-and-Processors.md)
* [Update parsing](Update-parsing.md)
* [Actions](Actions.md)
* [Activity invocation](Activity-invocation.md)

---