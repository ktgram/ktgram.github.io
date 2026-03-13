---
---
title: Beranda
---

### Intro
Mari kita lihat bagaimana library menangani pembaruan secara umum:

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/442cc5f1-0256-425a-9f25-185fdd49fe0a" alt="Diagram proses penanganan" />
</p>

Setelah menerima pembaruan, library melakukan tiga langkah utama, seperti yang bisa kita lihat.

### Processing

Processing adalah untuk mengemas ulang pembaruan yang diterima ke dalam subclass yang sesuai dari [`ProcessedUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processed-update/index.html) tergantung pada payload yang dibawa.

Langkah ini diperlukan untuk memudahkan operasi pembaruan dan memperluas kemampuan pemrosesan.

### Handling

Selanjutnya adalah langkah utama, di sini kita sampai ke penanganan itu sendiri.

### Global RateLimiter

Jika ada pengguna dalam pembaruan, kita memeriksa apakah melebihi batas rate limiter global.

### Parse text

Selanjutnya, tergantung pada payload, kita mengambil komponen pembaruan tertentu yang berisi teks dan memparse-nya sesuai konfigurasi.

Lebih detail bisa dilihat di [artikel parsing pembaruan](Update-parsing.md).

### Find Activity

Selanjutnya, sesuai prioritas pemrosesan:

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/6178c410-9b9e-4045-9f03-4791b3f49894" alt="Diagram prioritas penanganan" />
</p>

Kita mencari kesesuaian antara data yang diparse dan aktivitas yang kita operasikan.
Seperti yang bisa kita lihat pada diagram prioritas, `Commands` selalu datang pertama.

Artinya jika teks dalam pembaruan sesuai dengan command apapun, pencarian lebih lanjut untuk `Inputs`, `Common` dan tentu saja eksekusi action `Unprocessed` tidak akan dilakukan.

Satu-satunya hal adalah bahwa jika ada `UpdateHandlers` akan dipicu secara paralel tanpa memandang.

#### Commands

Mari kita lihat lebih dekat command dan pemrosesannya.

Seperti yang mungkin Anda perhatikan, meskipun anotasi untuk memproses command disebut [`CommandHandler`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-command-handler/index.html), ini lebih serbaguna daripada konsep klasik di Telegram Bots.

##### Scopes

Ini karena memiliki jangkauan kemungkinan pemrosesan yang lebih luas, yaitu fungsi target dapat didefinisikan tidak hanya tergantung pada pencocokan teks, tetapi juga pada tipe update yang sesuai, ini adalah konsep scopes.

Sesuai, setiap command dapat memiliki handler yang berbeda untuk daftar scopes yang berbeda, atau sebaliknya, satu command untuk beberapa.

Di bawah ini Anda bisa melihat bagaimana pemetaan dilakukan berdasarkan teks payload dan scope:

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/c870027e-750e-4bb8-a2ed-45ad93a55875" alt="Diagram scope command" />
</p>

#### Inputs

Selanjutnya, jika teks payload tidak cocok dengan command apapun, titik input dicari.

Konsep ini sangat mirip dengan menunggu input di aplikasi command line, Anda menaruh di konteks bot untuk pengguna tertentu sebuah titik yang akan menangani input berikutnya, tidak masalah apa yang berisi, yang penting adalah bahwa update berikutnya memiliki `User` agar bisa menghubungkannya dengan titik menunggu input yang ditetapkan.

Di bawah ini Anda bisa melihat contoh pemrosesan update ketika tidak ada kecocokan pada `Commands`.

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/925d3e05-0985-43d5-8d6f-b3f2786ff212" alt="Diagram contoh prioritas" />
</p>

#### Commons

Jika handler tidak menemukan `commands` atau `inputs`, ia memeriksa teks payload terhadap handler `common`.

Kami menyarankan untuk menggunakannya tanpa berlebihan, karena memeriksa dengan iterasi melalui semua entri.

#### Unprocessed

Dan langkah terakhir, jika handler tidak menemukan aktivitas yang cocok ([`UpdateHandler`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-update-handler/index.html) bekerja sepenuhnya secara paralel dan tidak dihitung sebagai aktivitas biasa), maka [`UnprocessedHandler`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-unprocessed-handler/index.html) berperan, jika diatur, akan menangani kasus ini, mungkin berguna untuk memperingatkan pengguna bahwa ada yang salah.

Lebih detail baca di [artikel Handlers](Handlers.md).

### Activity RateLimiter

Setelah menemukan aktivitas, juga memeriksa batas rate limit pengguna pada aktivitas tersebut, sesuai parameter yang ditentukan dalam parameter aktivitas.

### Activity

Activity mengacu pada berbagai jenis handler yang dapat ditangani oleh library telegram bot, termasuk Commands, Inputs, Regexes, dan handler Unprocessed.

### Invocation

Langkah pemrosesan terakhir adalah invokasi aktivitas yang ditemukan.

Detail lebih lanjut dapat ditemukan di [artikel invocation](Activity-invocation.md).

### See also

* [Update parsing](Update-parsing.md)
* [Activity invocation](Activity-invocation.md)
* [Handlers](Handlers.md)
* [Bot configuration](Bot-configuration.md)
* [Web starters (Spring, Ktor)](Web-starters-(Spring-and-Ktor.md))
---