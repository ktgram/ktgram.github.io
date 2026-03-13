---
---
title: فعال‌سازی فعالیت
---

در طول فعال‌سازی فعالیت، امکان گذراندن متن‌بات زمینه وجود دارد، زیرا به عنوان پارامتر در توابع هدف اعلام شده است.

پارامترهایی که می‌توان گذارد عبارتند از:

* [`ProcessedUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processed-update/index.html) (و تمام زیرکلاس‌های آن) - آپدیت در حال پردازش فعلی.
* [`ProcessingContext`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processing-context/index.html) - زمینه سطح پایین مدیریت فعالیت.
* [`User`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types/-user/index.html) - در صورت وجود.
* [`Chat`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.chat/-chat/index.html) - در صورت وجود.
* [`TelegramBot`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot/-telegram-bot/index.html) - نمونه فعلی متن‌بات.

همچنین امکان اضافه کردن نوع سفارشی برای گذراندن وجود دارد.

برای این کار، یک کلاس که از [`Autowiring<T>`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.interfaces.marker/-autowiring/index.html) پیاده‌سازی می‌کند اضافه کنید و آن را با کدکدن [`@Injectable`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-injectable/index.html) نشانه‌گذاری کنید.

پس از پیاده‌سازی رابط `Autowiring` - `T` برای گذراندن در توابع هدف در دسترس خواهد بود و از طریق متد توصیف‌شده در رابط به دست خواهد آمد.

```kotlin
@Injectable
object UserResolver : Autowiring<UserRecord> {
    override suspend fun get(update: ProcessedUpdate, bot: TelegramBot): UserRecord? {
        return userRepository.getUserByTgId(update.user.id)
    }
}
```


سایر پارامترهای اعلام شده در توابع **جستجو** خواهند شد در پارامترهای تجزیه‌شده.

علاوه بر این، پارامترهای تجزیه‌شده در طول گذراندن می‌توانند به انواع خاصی کست شوند، اینجا فهرست آنها است:

- `String`
- `Integer`
- `Long`
- `Short`
- `Float`
- `Double`

علاوه بر این، توجه داشته باشید که اگر پارامترها اعلام شده و موجود نباشند (یا در پارامترهای تجزیه‌شده یا به عنوان مثال `User` در `Update` موجود نباشد) یا نوع اعلام‌شده با پارامتر دریافتی در تابع تطبیق نداشته باشد، **`null`** گذارده خواهد شد پس مراقب باشید.

خلاصه‌بندی همه موارد، در زیر مثالی از چگونگی شکل‌گیری معمولی پارامترهای تابع وجود دارد:

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/3c1d7830-8e5d-45fb-82bb-ac63f08c3782" alt="نمودار فرآیند فراخوانی" />
</p>

### همچنین ببینید

* [تجزیه آپدیت](Update-parsing.md)
* [فعالیت‌ها و پردازنده‌ها](Activites-and-Processors.md)
---