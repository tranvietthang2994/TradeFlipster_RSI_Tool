import os
import time
import datetime
import random
from binance.client import Client
import numpy as np
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    ElementClickInterceptedException, 
    TimeoutException, 
    NoSuchElementException,
    StaleElementReferenceException,
    WebDriverException
)
import undetected_chromedriver as uc  

# Tắt log của TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
print("+-------------------------------------------------------------+")
print("|      HỆ THỐNG GIAO DỊCH RSI SÀN FLIPSTER TỰ ĐỘNG 99%        |")
print("|                          Author: WinTradeCoi - Tele: @dutbeo|")
print("|                                     Version 2.2 - 09/06/2025|")
print("+-------------------------------------------------------------+")
print("\nUpdated: Xử lý lỗi popup/alert và cải thiện độ ổn định hệ thống")

# Khởi tạo client Binance
client = Client()

# Cấu hình Chrome Options
chrome_options = uc.ChromeOptions()
chrome_options.add_argument("--guest")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")

# Khởi tạo webdriver với undetected-chromedriver
driver = None
try:
    driver = uc.Chrome(options=chrome_options)
except Exception as e:
    print(f"Lỗi khởi tạo WebDriver: {e}")
    exit(1)

# Hàm xử lý popup/alert
def handle_popups_and_alerts():
    """Xử lý các popup và alert có thể xuất hiện"""
    try:
        # Tìm và đóng các popup thông báo
        popups = driver.find_elements(By.CSS_SELECTOR, ".alert_wrapper__IXkZU, .modal, .popup, [role='dialog']")
        for popup in popups:
            try:
                # Tìm nút đóng trong popup
                close_buttons = popup.find_elements(By.CSS_SELECTOR, "button[aria-label='Close'], .close, [data-testid='close'], .btn-close")
                for btn in close_buttons:
                    if btn.is_displayed() and btn.is_enabled():
                        btn.click()
                        print("Đã đóng popup")
                        time.sleep(random.uniform(0.5, 1))
                        break
            except Exception:
                pass
        
        # Xử lý alert JavaScript
        try:
            alert = driver.switch_to.alert
            alert.dismiss()
            print("Đã đóng alert")
            time.sleep(random.uniform(0.5, 1))
        except Exception:
            pass
            
    except Exception as e:
        pass  # Bỏ qua lỗi khi không có popup

# Hàm click an toàn với retry
def safe_click(element, max_retries=3):
    """Click an toàn với xử lý lỗi và retry"""
    for attempt in range(max_retries):
        try:
            # Xử lý popup trước khi click
            handle_popups_and_alerts()
            
            # Scroll đến element
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.5)
            
            # Đảm bảo element có thể click được
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable(element))
            
            # Thử click bằng JavaScript nếu click thông thường không được
            try:
                element.click()
            except ElementClickInterceptedException:
                print(f"Click bị chặn, thử JavaScript click (lần {attempt + 1})")
                driver.execute_script("arguments[0].click();", element)
            
            return True
            
        except Exception as e:
            print(f"Lỗi click lần {attempt + 1}: {str(e)[:100]}")
            if attempt < max_retries - 1:
                time.sleep(random.uniform(1, 2))
                # Refresh các element nếu cần
                try:
                    refresh_elements()
                except:
                    pass
            else:
                print(f"Không thể click sau {max_retries} lần thử")
                return False
    
    return False

# Hàm refresh các element
def refresh_elements():
    """Refresh lại các element chính"""
    global buy_button, sell_button, close_all_button
    try:
        buy_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'button__label') and contains(@class, 'button__label--color_buy') and text()='Buy - Long']/ancestor::button"))
        )
        sell_button = driver.find_element(By.XPATH, "//div[contains(@class, 'button__label') and contains(@class, 'button__label--color_sell') and text()='Sell - Short']/ancestor::button")
        close_all_button = driver.find_element(By.XPATH, "//button[contains(@class, 'button_wrapper__hac7n') and contains(text(), 'Close all')]")
        return True
    except Exception as e:
        print(f"Lỗi refresh elements: {e}")
        return False

# Truy cập và đăng nhập
try:
    driver.get("https://flipster.io/en/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))
    email_input = driver.find_element(By.NAME, "email")
    password_input = driver.find_element(By.NAME, "password")
    login_button = driver.find_element(By.XPATH, "//button[@type='submit' and contains(text(), 'Log In')]")

    email_input.send_keys("tranvietthang2994@gmail.com")
    time.sleep(random.uniform(1, 2))
    password_input.send_keys("Thang2994!")
    time.sleep(random.uniform(1, 2))

    login_button.click()
    print("\033[33mNgười dùng tự giải capcha...\033[0m")
    time.sleep(random.uniform(6, 8))
    print("Đã đăng nhập thành công")

    # Chuyển đến trang giao dịch
    WebDriverWait(driver, 10).until(EC.url_contains("flipster.io"))
    driver.get("https://flipster.io/en/trade/perpetual/ETHUSDT.PERP")
    time.sleep(random.uniform(2, 3))
    print("Đã chuyển đến trang giao dịch ETHUSDT.PERP trên Flipster")

except Exception as e:
    print(f"Lỗi đăng nhập hoặc chuyển trang: {e}")
    if driver:
        driver.quit()
    exit(1)

# Tìm các nút giao dịch với retry
buy_button = sell_button = close_all_button = None
if not refresh_elements():
    print("Không thể tìm thấy các nút giao dịch")
    driver.quit()
    exit(1)

# Hàm thiết lập Leverage với xử lý lỗi
def set_leverage(leverage_value):
    try:
        leverage_input = driver.find_element(By.XPATH, "//div[contains(@class, 'selectBox_select__B6V5k')]//textarea")
        leverage_input.clear()
        leverage_input.send_keys(str(leverage_value))
        time.sleep(random.uniform(1, 2))
        leverage_input.send_keys(Keys.RETURN)
        print(f"Đã thiết lập Leverage thành {leverage_value}")
    except Exception as e:
        print(f"Lỗi khi thiết lập Leverage: {e}")
# def set_leverage(leverage_value, max_retries=3):
#     for attempt in range(max_retries):
#         try:
#             handle_popups_and_alerts()
#             leverage_input = driver.find_element(By.XPATH, "//div[contains(@class, 'selectBox_select__B6V5k')]//textarea")
#             leverage_input.clear()
#             leverage_input.send_keys(str(leverage_value))
#             time.sleep(random.uniform(1, 2))
#             leverage_input.send_keys(Keys.RETURN)
#             print(f"Đã thiết lập Leverage thành {leverage_value}")
#             return True
#         except Exception as e:
#             print(f"Lỗi thiết lập Leverage lần {attempt + 1}: {e}")
#             if attempt < max_retries - 1:
#                 time.sleep(random.uniform(1, 2))
#     return False

# Hàm thiết lập Margin với xử lý lỗi
def set_margin(margin_value, max_retries=3):
    for attempt in range(max_retries):
        try:
            handle_popups_and_alerts()
            margin_input = driver.find_element(By.NAME, "margin")
            margin_input.clear()
            margin_input.send_keys(str(margin_value))
            time.sleep(random.uniform(1, 2))
            margin_input.send_keys(Keys.RETURN)
            print(f"Đã thiết lập Margin thành {margin_value}")
            return True
        except Exception as e:
            print(f"Lỗi thiết lập Margin lần {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(random.uniform(1, 2))
    return False

# Thiết lập chạy lệnh ảo để pass alert "Close all"
try:
    set_leverage(10)
    set_margin(random.uniform(2, 10))
    time.sleep(random.uniform(5, 8))
    safe_click(buy_button)
    print(f"{datetime.datetime.now().strftime('%H:%M:%S')} Đã mở lệnh ảo ngẫu nhiên margin")
    print("\033[33mBạn hãy bấm vào 'Close all' và vượt qua thông báo alert để tiếp tục giao dịch thực tế.\033[0m")
    time.sleep(random.uniform(5, 10))
    print("Đã hoàn thành lệnh ảo, bạn có thể tiếp tục giao dịch thực tế.")
except Exception as e:
    print(f"Lỗi tạo lệnh ảo: {e}")

# Thiết lập Leverage và Margin
leverage_default = 20
margin_default = 50
set_leverage(leverage_default)
time.sleep(random.uniform(1, 2))
set_margin(margin_default)
time.sleep(random.uniform(1, 2))
print("Bắt đầu giao dịch...")

# Khởi tạo trạng thái
current_position = "none"
count_position = 0
position_data = []
last_position_time = 0
coin_used = "ETHUSDT"

# Class để quản lý thông tin vị thế
class PositionInfo:
    def __init__(self, entry_price, margin, leverage):
        self.entry_price = entry_price
        self.margin = margin
        self.leverage = leverage
        self.volume = margin * leverage
        self.timestamp = time.time()

# Hàm tính RSI 
def calculate_rsi(prices, period=14):
    if len(prices) < 2:
        return 50
    prices = np.array(prices, dtype=float)
    delta = np.diff(prices)
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = [np.mean(gain[:period])] if len(gain) >= period else [0]
    avg_loss = [np.mean(loss[:period])] if len(loss) >= period else [0]
    for i in range(period, len(gain)):
        avg_gain.append((avg_gain[-1] * (period - 1) + gain[i]) / period)
        avg_loss.append((avg_loss[-1] * (period - 1) + loss[i]) / period)
    avg_gain = np.array(avg_gain)
    avg_loss = np.array(avg_loss)
    rs = avg_gain / np.where(avg_loss == 0, np.finfo(float).eps, avg_loss)
    rsi = 100 - (100 / (1 + rs))
    return rsi[-1] if len(rsi) > 0 else 50

# Hàm tính giá trung bình có trọng số
def calculate_weighted_average_price(position_data):
    if not position_data:
        return 0
    total_volume = sum(pos.volume for pos in position_data)
    weighted_sum = sum(pos.entry_price * pos.volume for pos in position_data)
    return weighted_sum / total_volume if total_volume > 0 else 0

# Hàm tính tổng margin đã sử dụng
def calculate_total_margin(position_data):
    return sum(pos.margin for pos in position_data)

# Hàm tính tổng volume
def calculate_total_volume(position_data):
    return sum(pos.volume for pos in position_data)

# Hàm tính PnL dựa trên volume thực tế
def calculate_pnl(position_type, position_data, current_price):
    if not position_data:
        return 0, 0
    
    total_pnl = 0
    total_margin = 0
    
    for pos in position_data:
        if position_type == "long":
            pnl_points = current_price - pos.entry_price
        elif position_type == "short":
            pnl_points = pos.entry_price - current_price
        else:
            pnl_points = 0
        
        position_pnl = pnl_points * (pos.volume / pos.entry_price)
        total_pnl += position_pnl
        total_margin += pos.margin
    
    pnl_percentage = (total_pnl / total_margin * 100) if total_margin > 0 else 0
    return total_pnl, pnl_percentage

# Hàm mở lệnh với xử lý lỗi
def open_position(position_type, button, price):
    global current_position, count_position, position_data, last_position_time
    
    if not safe_click(button):
        print(f"Không thể mở lệnh {position_type}")
        return False
    
    new_position = PositionInfo(price, margin_default, leverage_default)
    position_data = [new_position]
    
    print(f"\033[32m{datetime.datetime.now().strftime('%H:%M:%S')} Đã mở {position_type} {coin_used}")
    print(f"   Giá: {price:.2f} | Margin: {margin_default} | Leverage: {leverage_default}x | Volume: {new_position.volume:.2f}\033[0m")
    
    current_position = position_type
    count_position = 1
    last_position_time = time.time()
    return True

# Hàm đóng lệnh với xử lý lỗi
def close_position(current_price):
    global current_position, count_position, position_data, last_position_time
    
    if position_data:
        final_pnl, final_pnl_pct = calculate_pnl(current_position, position_data, current_price)
        avg_price = calculate_weighted_average_price(position_data)
        total_margin = calculate_total_margin(position_data)
        
        print(f"\033[31m{datetime.datetime.now().strftime('%H:%M:%S')} Đang đóng vị thế {coin_used}")
        print(f"   Giá vào TB: {avg_price:.2f} | Giá đóng: {current_price:.2f}")
        print(f"   Tổng Margin: {total_margin} | PnL: {final_pnl:.2f} ({final_pnl_pct:.2f}%)\033[0m")
    
    # Thử thiết lập margin và đóng lệnh
    if not set_margin(margin_default):
        print("Không thể thiết lập margin để đóng lệnh")
    
    if not safe_click(close_all_button):
        print("Không thể đóng lệnh, thử lại sau")
        return False
    
    # Reset trạng thái
    current_position = "none"
    count_position = 0
    position_data = []
    last_position_time = 0
    return True

# Hàm DCA với xử lý lỗi
def dca_position(position_type, button, price):
    global count_position, position_data, last_position_time
    
    dca_margin = margin_default * (2 ** (count_position - 1))
    
    if not set_margin(dca_margin):
        print("Không thể thiết lập margin cho DCA")
        return False
    
    if not safe_click(button):
        print(f"Không thể DCA {position_type}")
        return False
    
    new_position = PositionInfo(price, dca_margin, leverage_default)
    position_data.append(new_position)
    
    avg_price = calculate_weighted_average_price(position_data)
    total_margin = calculate_total_margin(position_data)
    total_volume = calculate_total_volume(position_data)
    
    print(f"\033[32m{datetime.datetime.now().strftime('%H:%M:%S')} Đã DCA {position_type} {coin_used}")
    print(f"   Giá DCA: {price:.2f} | Margin: {dca_margin} | Volume: {new_position.volume:.2f}")
    print(f"   Giá TB mới: {avg_price:.2f} | Tổng Margin: {total_margin} | Tổng Volume: {total_volume:.2f}\033[0m")
    
    count_position += 1
    last_position_time = time.time()
    return True

# Bắt đầu vòng lặp giao dịch với xử lý lỗi toàn diện
last_update = time.time()
update_interval = 5
error_count = 0
max_errors = 10

print("🚀 Bắt đầu vòng lặp giao dịch...")

try:
    while True:
        current_time = time.time()
        if current_time - last_update >= update_interval:
            try:
                # Lấy dữ liệu từ Binance
                klines = client.get_historical_klines(coin_used, Client.KLINE_INTERVAL_1MINUTE, limit=100)
                closes = [float(k[4]) for k in klines] if klines else []
                rsi = calculate_rsi(closes)

                ticker = client.get_symbol_ticker(symbol=coin_used)
                current_price = float(ticker["price"])

                now = datetime.datetime.now().strftime("%H:%M:%S")
                
                # Hiển thị thông tin
                if current_position == "none":
                    print(f"{now} RSI: {rsi:.2f}, Giá {coin_used}: {current_price:.2f}")
                else:
                    pnl, pnl_pct = calculate_pnl(current_position, position_data, current_price)
                    avg_price = calculate_weighted_average_price(position_data)
                    total_margin = calculate_total_margin(position_data)
                    
                    print(f"{now} RSI: {rsi:.2f} | Giá: {current_price:.2f} | Vị thế: {current_position.upper()}")
                    print(f"   Giá TB: {avg_price:.2f} | Margin: {total_margin} | PnL: {pnl:.2f} ({pnl_pct:.2f}%)")

                # Logic giao dịch
                if current_position == "none":
                    if rsi <= 26:
                        if not refresh_elements():
                            print("Không thể refresh elements, bỏ qua lệnh này")
                        else:
                            time.sleep(random.uniform(2, 5))  # Thêm delay để tránh quá nhanh
                            open_position("long", buy_button, current_price)
                    elif rsi >= 74:
                        if not refresh_elements():
                            print("Không thể refresh elements, bỏ qua lệnh này")
                        else:
                            time.sleep(random.uniform(2, 5))  # Thêm delay để tránh quá nhanh
                            open_position("short", sell_button, current_price)

                elif current_position == "long":
                    pnl, pnl_pct = calculate_pnl("long", position_data, current_price)
                    time_elapsed = current_time - last_position_time
                    avg_price = calculate_weighted_average_price(position_data)
                    
                    if (rsi >= 50 and pnl > 0.8) or (time_elapsed >= 12 * 60 and pnl > 0.8):
                        if not refresh_elements():
                            print("Không thể refresh elements, bỏ qua đóng lệnh")
                        else:
                            close_position(current_price)
                    elif current_price < avg_price * 0.992 and count_position < 5:
                        if not refresh_elements():
                            print("Không thể refresh elements, bỏ qua DCA")
                        else:
                            dca_position("long", buy_button, current_price)

                elif current_position == "short":
                    pnl, pnl_pct = calculate_pnl("short", position_data, current_price)
                    time_elapsed = current_time - last_position_time
                    avg_price = calculate_weighted_average_price(position_data)
                    
                    if (rsi <= 50 and pnl > 0.8) or (time_elapsed >= 12 * 60 and pnl > 0.8):
                        if not refresh_elements():
                            print("Không thể refresh elements, bỏ qua đóng lệnh")
                        else:
                            close_position(current_price)
                    elif current_price > avg_price * 1.008 and count_position < 5:
                        if not refresh_elements():
                            print("Không thể refresh elements, bỏ qua DCA")
                        else:
                            dca_position("short", sell_button, current_price)

                last_update = current_time
                error_count = 0  # Reset error count khi thành công
                
            except Exception as e:
                error_count += 1
                print(f"Lỗi trong vòng lặp chính ({error_count}/{max_errors}): {str(e)[:200]}")
                
                if error_count >= max_errors:
                    print("Quá nhiều lỗi liên tiếp, dừng hệ thống")
                    break
                
                # Thử refresh elements khi có lỗi
                time.sleep(random.uniform(2, 5))
                try:
                    refresh_elements()
                except:
                    pass
                
        time.sleep(random.uniform(1, 2))

except KeyboardInterrupt:
    print("\n🛑 Người dùng dừng hệ thống")
except Exception as e:
    print(f"🚨 Lỗi nghiêm trọng: {e}")
# finally:
#     # Đóng WebDriver an toàn
#     if driver:
#         try:
#             print("🔄 Đang đóng WebDriver...")
#             driver.quit()
#             print("✅ Đã đóng WebDriver thành công")
#         except Exception as e:
#             print(f"⚠️ Lỗi khi đóng WebDriver: {e}")
#             try:
#                 driver.close()
#             except:
#                 pass
    
#     print("🏁 Hệ thống đã dừng hoàn toàn")