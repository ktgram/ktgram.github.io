---
---
title: Trang chủ
---

### Giới thiệu
Hãy cùng tìm hiểu ý tưởng về cách thư viện xử lý các bản cập nhật nói chung:

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/442cc5f1-0256-425a-9f25-185fdd49fe0a" alt="Sơ đồ quy trình xử lý" />
</p>

Sau khi nhận được bản cập nhật, thư viện thực hiện ba bước chính, như chúng ta có thể thấy.

### Xử lý

Xử lý là đóng gói lại bản cập nhật nhận được vào lớp con phù hợp của [`ProcessedUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.component/-processed-update/index.html) tùy thuộc vào tải trọng được mang theo.

Bước này cần thiết để dễ dàng vận hành bản cập nhật và mở rộng khả năng xử lý.

### Xử lý

Tiếp theo là bước chính, ở đây chúng ta đi vào xử lý thực tế.

### Global RateLimiter

Nếu có người dùng trong bản cập nhật, chúng ta kiểm tra việc vượt quá giới hạn tốc độ toàn cầu.

### Phân tích văn bản

Tiếp theo, tùy thuộc vào tải trọng, chúng ta lấy một thành phần bản cập nhật cụ thể chứa văn bản và phân tích nó theo cấu hình.

Bạn có thể xem chi tiết hơn trong [bài viết phân tích bản cập nhật](Update-parsing.md).

### Tìm Hoạt động

Tiếp theo, theo thứ tự ưu tiên xử lý:

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/6178c410-9b9e-4045-9f03-4791b3f49894" alt="Sơ đồ ưu tiên xử lý" />
</p>

Chúng ta đang tìm kiếm sự tương ứng giữa dữ liệu đã phân tích và các hoạt động chúng ta đang vận hành.
Như chúng ta có thể thấy trên sơ đồ ưu tiên, `Commands` luôn đứng đầu tiên.

Tức là nếu tải văn bản trong bản cập nhật tương ứng với bất kỳ lệnh nào, việc tìm kiếm tiếp theo cho `Inputs`, `Common` và tất nhiên việc thực thi hành động `Unprocessed` sẽ không được thực hiện.

Điều duy nhất là nếu có `UpdateHandlers` sẽ được kích hoạt song song bất kể.

#### Commands

Hãy cùng xem kỹ hơn về các lệnh và cách xử lý chúng.

Như bạn có thể đã nhận thấy, mặc dù annotation để xử lý lệnh được gọi là [`CommandHandler`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-command-handler/index.html), nó linh hoạt hơn khái niệm cổ điển trong Telegram Bots.

##### Scopes

Điều này là do nó có phạm vi xử lý rộng hơn, tức là hàm mục tiêu có thể được định nghĩa không chỉ tùy thuộc vào việc khớp văn bản, mà còn dựa trên loại bản cập nhật phù hợp, đây là khái niệm về scopes.

Tương ứng, mỗi lệnh có thể có các trình xử lý khác nhau cho danh sách scopes khác nhau, hoặc ngược lại, một lệnh cho nhiều scopes.

Bạn có thể thấy bên dưới cách ánh xạ theo tải trọng văn bản và scope được thực hiện:

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/c870027e-750e-4bb8-a2ed-45ad93a55875" alt="Sơ đồ scope lệnh" />
</p>

#### Inputs

Tiếp theo, nếu tải văn bản không khớp với bất kỳ lệnh nào, các điểm input sẽ được tìm kiếm.

Khái niệm này rất giống với việc chờ input trong các ứng dụng dòng lệnh, bạn đặt trong ngữ cảnh bot cho một người dùng cụ thể một điểm sẽ xử lý input tiếp theo của anh ta, không quan trọng nó chứa gì, điều chính là bản cập nhật tiếp theo có `User` để có thể liên hệ nó với điểm chờ input đã đặt.

Bạn có thể thấy bên dưới một ví dụ về xử lý bản cập nhật khi không có khớp với `Commands`.

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/925d3e05-0985-43d5-8d6f-b3f2786ff212" alt="Sơ đồ ví dụ ưu tiên" />
</p>

#### Commons

Nếu trình xử lý không tìm thấy `commands` hoặc `inputs`, nó kiểm tra tải văn bản với các trình xử lý `common`.

Chúng tôi khuyên không nên lạm dụng nó, vì nó kiểm tra bằng cách lặp qua tất cả các mục.

#### Unprocessed

Và bước cuối cùng, nếu trình xử lý không tìm thấy bất kỳ hoạt động nào khớp ([`UpdateHandler`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-update-handler/index.html) hoạt động hoàn toàn song song và không được tính là hoạt động thông thường), thì [`UnprocessedHandler`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-unprocessed-handler/index.html) sẽ được kích hoạt, nếu được đặt, nó sẽ xử lý trường hợp này, có thể hữu ích để cảnh báo người dùng rằng có gì đó đã xảy ra sai.

Đọc chi tiết hơn trong [bài viết Handlers](Handlers.md).

### Activity RateLimiter

Sau khi tìm thấy một hoạt động, nó cũng kiểm tra giới hạn tốc độ của người dùng trên nó, theo các tham số được chỉ định trong tham số hoạt động.

### Activity

Activity đề cập đến các loại trình xử lý khác nhau mà thư viện bot telegram có thể xử lý, bao gồm Commands, Inputs, Regexes, và trình xử lý Unprocessed.

### Invocation

Bước xử lý cuối cùng là việc gọi hoạt động đã tìm thấy.

Chi tiết hơn có thể tìm thấy trong [bài viết invocation](Activity-invocation.md).

### Xem thêm

* [Phân tích bản cập nhật](Update-parsing.md)
* [Invocation hoạt động](Activity-invocation.md)
* [Handlers](Handlers.md)
* [Cấu hình bot](Bot-configuration.md)
* [Web starters (Spring, Ktor)](Web-starters-(Spring-and-Ktor.md))
---