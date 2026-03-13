---
---
title: زمینه بات
---

<p align="center">
  <img src="https://github.com/user-attachments/assets/60bb58ae-1806-4b8d-8550-833b09c2b606" alt="Bot context diagram" />
</p>

بات همچنین می‌تواند توانایی به خاطر سپردن برخی داده‌ها از طریق رابط‌های `UserData` و `ClassData` را فراهم کند.

- [`userData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-user-data/index.html) داده‌ای در سطح کاربر است.
- [`classData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-data/index.html) داده‌ای در سطح کلاس است، یعنی داده تا زمانی که کاربر به دستور یا ورودی در کلاس متفاوتی منتقل شود، ذخیره می‌شود. (در حالت تابع مانند داده کاربر عمل می‌کند)

به طور پیش‌فرض، پیاده‌سازی از طریق [`ConcurrentHashMap`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.collections/java.util.concurrent.-concurrent-map/) ارائه می‌شود اما می‌تواند با استفاده از رابط‌های [`UserData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-user-data/index.html) و [`ClassData`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.ctx/-class-data/index.html) با ابزار ذخیره‌سازی داده‌ای که انتخاب می‌کنید تغییر کند.


> [!CAUTION]
> فراموش نکنید تا وظیفه gradle `kspKotlin`/یا هر وظیفه ksp مرتبط را برای در دسترس قرار دادن کدگنری مورد نیاز اجرا کنید.


برای تغییر، تنها کاری که باید انجام دهید قرار دادن `@CtxProvider` روی پیاده‌سازی خود و اجرای وظیفه gradle ksp (یا ساخت) است.

```kotlin
@CtxProvider
class MyRedis : UserData<String> {
    // ...
}
```

### همچنین ببینید

* [خانه](https://github.com/vendelieu/telegram-bot/wiki)
* [Parsing به روز رسانی](Update-parsing.md)
---