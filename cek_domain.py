from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from webdriver_manager.chrome import ChromeDriverManager

# Setup Chrome untuk mode headless di VPS
options = Options()
options.add_argument("--headless")  # Mode tanpa GUI
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")

# Setup WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    # 1. Buka situs TrustPositif Komdigi
    driver.get("https://trustpositif.komdigi.go.id/")
    wait = WebDriverWait(driver, 10)

    # 2. Klik kolom pencarian untuk membuka modal input
    search_trigger = wait.until(EC.element_to_be_clickable((By.ID, "press-to-modal")))
    search_trigger.click()
    time.sleep(2)  # Tunggu modal muncul

    # 3. Masukkan domain yang ingin dicek
    search_box = wait.until(EC.presence_of_element_located((By.ID, "input-data")))
    domain_to_check = "google.com"
    search_box.send_keys(domain_to_check)

    # 4. Klik tombol "Cari"
    search_button = wait.until(EC.element_to_be_clickable((By.ID, "text-footer1")))

    # Scroll ke tombol sebelum mengklik untuk menghindari error
    driver.execute_script("arguments[0].scrollIntoView();", search_button)
    search_button.click()

    # 5. Tunggu hasil pencarian muncul
    time.sleep(5)
    result_table = wait.until(EC.presence_of_element_located((By.ID, "daftar-block")))

    # 6. Ambil hasil dari tabel hasil pencarian
    try:
        rows = result_table.find_elements(By.TAG_NAME, "tr")
        for row in rows[1:]:  # Skip header
            columns = row.find_elements(By.TAG_NAME, "td")
            domain = columns[0].text.strip()
            status = columns[1].text.strip()
            print(f"🔹 Domain: {domain} | Status: {status}")

    except Exception as e:
        print("⚠️ Gagal mengambil hasil pencarian:", e)

finally:
    # 7. Tutup browser setelah selesai
    driver.quit()
