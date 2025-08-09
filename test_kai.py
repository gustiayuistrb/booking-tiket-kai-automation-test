from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

driver = webdriver.Chrome()

driver.get("https://booking.kai.id/")

# Pilih stasiun asal
driver.find_element(By.ID, "origination-flexdatalist").click()
driver.find_element(By.ID, "origination-flexdatalist").send_keys("SURABAYA GUBENG")
try:
    WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, "//ul[@id='origination-flexdatalist-results']//li[contains(@class,'item')]"))).click()
except TimeoutException:
    print('Stasiun asal tidak ditemukan')

# Pilih stasiun tujuan
driver.find_element(By.ID, "destination-flexdatalist").click()
driver.find_element(By.ID, "destination-flexdatalist").send_keys("YOGYAKARTA")
try:
    WebDriverWait(driver,5).until(EC.element_to_be_clickable(
        (By.XPATH, "//ul[@id='destination-flexdatalist-results']//li[contains(@class,'item')]"))).click()
except TimeoutException:
    print('Stasiun tujuan tidak ditemukan')

# Pilih tanggal
driver.find_element(By.ID, "departure_dateh").click()
try:
    WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, "//td[@data-handler='selectDay']//a[text()='10']"))).click()
except TimeoutException:
    print("Tanggal tidak tersedia")

# Klik cari tiket
driver.find_element(By.ID, "submit").click()

# Test ambil data kereta paling atas
first_train = WebDriverWait(driver,5).until(EC.presence_of_element_located(
    (By.XPATH, "(//a[contains(@class,'card-schedule')])[1]"))
)

nama_kereta = first_train.find_element(By.XPATH, ".//div[@class='name']").text
assert "SANCAKA" in nama_kereta

kelas_kereta = first_train.find_element(By.XPATH, ".//div[contains(@class,'col-one')]/div[2]").text
assert "Eksekutif (AC)" in kelas_kereta

nomor_kereta = first_train.find_element(By.XPATH, ".//div[@class='name']/span").text.strip("()")
assert "81" in nomor_kereta

harga_kereta = first_train.find_element(By.XPATH, ".//div[@class='price']").text
assert "Rp 340.000,-" in harga_kereta


print("✅ Yeayyy test passed!")
driver.quit()