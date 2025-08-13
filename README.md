# HỆ THỐNG GIAO DỊCH RSI SÀN FLIPSTER TỰ ĐỘNG

Một hệ thống bot giao dịch tự động 99% trên sàn Flipster, sử dụng chiến lược dựa trên chỉ báo RSI (Relative Strength Index) để mở và đóng lệnh.

## 🌟 Giới thiệu
Dự án này là một bot giao dịch tiền điện tử tự động được thiết kế để hoạt động trên sàn giao dịch Flipster. Bot sử dụng thư viện `selenium` và `undetected_chromedriver` để tự động hóa các thao tác trên trình duyệt, kết hợp với dữ liệu giá từ Binance để tính toán chỉ báo **RSI**.

Bot sẽ tự động mở lệnh **LONG** hoặc **SHORT** khi RSI chạm các ngưỡng quá mua/quá bán và quản lý vị thế bằng cách đóng lệnh khi có lời hoặc trung bình giá (DCA) khi thị trường đi ngược lại.

## ✨ Tính năng nổi bật
  * **Giao dịch tự động**: Tự động mở và đóng lệnh dựa trên chiến lược RSI.
  * **Hỗ trợ sàn Flipster**: Tích hợp và tự động hóa thao tác trên trang web của sàn Flipster.
  * **Quản lý vị thế thông minh**: Tự động trung bình giá (DCA) khi cần thiết.
  * **Xử lý lỗi mạnh mẽ**: Tích hợp các hàm xử lý popup, alert và retry các thao tác bị lỗi để tăng độ ổn định.
  * **Giao diện dòng lệnh thân thiện**: Hiển thị thông tin giao dịch, PnL, và các trạng thái hệ thống một cách rõ ràng trên terminal.
  * **Giao dịch an toàn**: Hạn chế số lần DCA để kiểm soát rủi ro.

## 🛠️ Yêu cầu cài đặt

Để chạy bot, bạn cần cài đặt các thư viện Python sau:
```bash
pip install -r requirements.txt
```

Nội dung của file `requirements.txt` nên bao gồm:
```
binance-client
numpy
selenium
undetected-chromedriver
```

Ngoài ra, bạn cũng cần có:

  * **Git**: Đã được cài đặt trên máy tính của bạn.
  * **Trình duyệt Chrome**: Cần thiết để `undetected-chromedriver` hoạt động.

## 🚀 Hướng dẫn sử dụng

### 1\. Cấu hình ban đầu

  * **Đăng nhập tài khoản Flipster**: Mở file code và thay đổi thông tin đăng nhập trong phần `driver.get("https://flipster.io/en/login")`.
      * Sửa `email_input.send_keys("tranvietthang2994@gmail.com")`
      * Sửa `password_input.send_keys("Thang2994!")`
  * **Giải mã captcha**: Khi chạy lần đầu, bot sẽ dừng lại để bạn tự giải captcha. Sau khi đăng nhập thành công, bạn có thể chạy lại để bot hoạt động bình thường.
  * **Cấu hình tham số**: Bạn có thể tùy chỉnh các tham số sau trong code:
      * `leverage_default`: Mức đòn bẩy mặc định.
      * `margin_default`: Số tiền ký quỹ mặc định cho mỗi lệnh ban đầu.
      * `coin_used`: Cặp giao dịch, ví dụ `ETHUSDT` hoặc `BTCUSDT`.

### 2\. Chạy bot

Mở terminal hoặc command prompt, điều hướng đến thư mục chứa file code và chạy lệnh:
```bash
python your_bot_file.py
```

*Lưu ý: Tên file có thể khác tùy thuộc vào cách bạn lưu.*

### 3\. Quy trình hoạt động

1.  Bot sẽ mở trình duyệt Chrome ẩn danh và truy cập trang đăng nhập Flipster.
2.  Sau khi đăng nhập và giải captcha, bot sẽ chuyển đến trang giao dịch đã cấu hình.
3.  Bot sẽ tạo một "lệnh ảo" và yêu cầu bạn bấm `Close all` để vượt qua các cảnh báo ban đầu của sàn.
4.  Sau khi hoàn tất bước trên, bot sẽ bắt đầu vòng lặp giao dịch chính, liên tục kiểm tra RSI và giá để thực hiện lệnh.

## ⚠️ Cảnh báo & Lưu ý
  * Đây là một bot giao dịch tự động. **Hãy sử dụng cẩn thận và hiểu rõ rủi ro liên quan đến giao dịch tiền điện tử.**
  * Hãy bắt đầu với số tiền nhỏ và giám sát hoạt động của bot thường xuyên.
  * Mặc dù bot có các cơ chế xử lý lỗi, nhưng không thể đảm bảo 100% hoạt động liên tục trong mọi tình huống.

-----

### Tác giả

**WinTradeCoi** - Telegram: `@dutbeo`
