from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Setup Chrome untuk mode headless (tanpa tampilan)
options = Options()
options.add_argument("--headless")  # Mode tanpa GUI
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")

# Setup WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# 1. Buka situs TrustPositif Komdigi
driver.get("https://trustpositif.komdigi.go.id/")
time.sleep(2)

# 2. Klik kolom pencarian untuk membuka modal input
search_trigger = driver.find_element(By.ID, "press-to-modal")
search_trigger.click()
time.sleep(2)

# 3. Masukkan domain yang ingin dicek
search_box = driver.find_element(By.ID, "input-data")
domain_to_check = "google.com"
search_box.send_keys(domain_to_check)

# 4. Klik tombol "Cari"
search_button = driver.find_element(By.ID, "text-footer1")
search_button.click()

# 5. Tunggu hasil pencarian muncul
time.sleep(5)

# 6. Ambil hasil dari tabel hasil pencarian
try:
    table = driver.find_element(By.ID, "daftar-block")
    rows = table.find_elements(By.TAG_NAME, "tr")

    for row in rows[1:]:
        columns = row.find_elements(By.TAG_NAME, "td")
        domain = columns[0].text.strip()
        status = columns[1].text.strip()
        print(f"🔹 Domain: {domain} | Status: {status}")

except Exception as e:
    print("⚠️ Gagal mengambil hasil pencarian:", e)

# 7. Tutup browser setelah selesai
driver.quit()
