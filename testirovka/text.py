# import unittest
# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager

# class YouTubeMusicTestCase(unittest.TestCase):
#     def setUp(self):
#         service = Service(ChromeDriverManager().install())
#         self.browser = webdriver.Chrome(service=service)

#     def tearDown(self):
#         self.browser.quit()

#     def test_play_multiple_songs(self):
#         # Список песен для тестирования
#         songs = [
#             "Inez - Menak Wla Meni (Hijazi Remix) | New Music 2023 🎶 | Arabic Music",
#             "Детка играй",
#             "Чем больше их, тем сильнее я!",
#             "Ты расскажи ка мне",
#         ]

#         for index, song in enumerate(songs, start=1):
#             try:
#                 print(f"Тест №{index}: Ищем песню '{song}'")
                
#                 # Открываем Google
#                 self.browser.get('http://www.google.com')
                
#                 # Ищем YouTube
#                 search_box = self.browser.find_element(By.NAME, 'q')
#                 search_box.send_keys('YouTube' + Keys.RETURN)
                
#                 # Ждём и кликаем по YouTube
#                 WebDriverWait(self.browser, 5).until(
#                     EC.presence_of_element_located((By.CSS_SELECTOR, 'h3'))
#                 )
#                 youtube_link = None
#                 results = self.browser.find_elements(By.CSS_SELECTOR, 'h3')
#                 for result in results:
#                     if 'YouTube' in result.text:
#                         youtube_link = result
#                         break
#                 if youtube_link:
#                     youtube_link.click()
#                 else:
#                     print(f"Не удалось найти ссылку на YouTube для '{song}'")
#                     continue
                
#                 # Ищем песню в YouTube
#                 WebDriverWait(self.browser, 5).until(
#                     EC.presence_of_element_located((By.NAME, 'search_query'))
#                 )
#                 youtube_search_box = self.browser.find_element(By.NAME, 'search_query')
#                 youtube_search_box.send_keys(song)
#                 youtube_search_box.send_keys(Keys.RETURN)
                
#                 # Ждём и запускаем первое видео
#                 WebDriverWait(self.browser, 5).until(
#                     EC.presence_of_element_located((By.CSS_SELECTOR, 'a#video-title'))
#                 )
#                 video_link = self.browser.find_element(By.CSS_SELECTOR, 'a#video-title')
#                 video_link.click()
                
#                 # Ждём загрузки видео
#                 WebDriverWait(self.browser, 5).until(
#                     EC.presence_of_element_located((By.CSS_SELECTOR, 'button.ytp-play-button'))
#                 )
#                 print(f"Видео для '{song}' запущено. Воспроизводим 10 секунд.")
                
#                 time.sleep(10)  # Минимальное время для воспроизведения
                
#             except Exception as e:
#                 print(f"Ошибка в тесте №{index} для песни '{song}': {e}")
#             finally:
#                 print(f"Тест №{index} завершён.")

# if __name__ == '__main__':
#     unittest.main(verbosity=2)



















import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class LocalWebAppTest(unittest.TestCase):
    def setUp(self):
        # Настраиваем браузер
        service = Service(ChromeDriverManager().install())
        self.browser = webdriver.Chrome(service=service)
        self.browser.get("http://127.0.0.1:8000/")  # Локальный сервер

    def tearDown(self):
        # Закрываем браузер
        self.browser.quit()

    def test_navigate_menu(self):
        for i in range(10):  # Повторяем 10 раз
            print(f"Итерация {i + 1}:")

            try:
                # Ждём появления кнопки "☰" и кликаем
                burger_menu = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.ID, "burgerMenu"))
                )
                burger_menu.click()
                print("Меню открыто.")

                # Нажимаем на ссылки в меню
                for link_text in ["Магазин", "Помощь", "Корзина"]:
                    link = WebDriverWait(self.browser, 5).until(
                        EC.presence_of_element_located((By.LINK_TEXT, link_text))
                    )
                    link.click()
                    print(f"Кликнуто: {link_text}.")
                    
                    # Возвращаемся обратно на главную страницу
                    self.browser.get("http://127.0.0.1:8000/")
            except Exception as e:
                print(f"Ошибка на итерации {i + 1}: {e}")
            finally:
                print(f"Итерация {i + 1} завершена.\n")

if __name__ == '__main__':
    unittest.main(verbosity=2)
