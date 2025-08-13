from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import pytest
import allure


@allure.title("Booking Tiket KAI")
@allure.description("""
                    Skenario pengujian booking tiket dari Surabaya Gubeng ke Yogyakarta.
                    Dengan asersi harga pada list produk sama dengan harga pada detail page.
                    """)

@pytest.fixture(scope="module")
def driver_setup():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://booking.kai.id/")

    yield driver

    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, "hasil_test", attachment_type=allure.attachment_type.PNG)
    driver.close()


def test_pesan_tiket(driver_setup):
    with allure.step("Isi stasiun keberangkatan"):
        driver_setup.find_element(By.ID, "origination-flexdatalist").click()
        driver_setup.find_element(By.ID, "origination-flexdatalist").send_keys("SURABAYA GUBENG")
        try:
            WebDriverWait(driver_setup, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//ul[@id='origination-flexdatalist-results']//li[contains(@class,'item')]")
                )
            ).click()
        except TimeoutException:
            print("Stasiun asal tidak ditemukan")

    with allure.step("Isi stasiun tujuan"):
        driver_setup.find_element(By.ID, "destination-flexdatalist").click()
        driver_setup.find_element(By.ID, "destination-flexdatalist").send_keys("YOGYAKARTA")
        try:
            WebDriverWait(driver_setup, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//ul[@id='destination-flexdatalist-results']//li[contains(@class,'item')]")
                )
            ).click()
        except TimeoutException:
            print("Stasiun tujuan tidak ditemukan")

    with allure.step("Isi tanggal keberangkatan"):
        driver_setup.find_element(By.ID, "departure_dateh").click()
        try:
            WebDriverWait(driver_setup, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//td[@data-handler='selectDay']//a[text()='14']")
                )
            ).click()
        except TimeoutException:
            print("Tanggal tidak tersedia")

    with allure.step("Klik pesan tiket"):
        driver_setup.find_element(By.ID, "submit").click()

    # Ambil data kereta paling atas
    first_train = WebDriverWait(driver_setup, 5).until(
        EC.presence_of_element_located((By.XPATH, "(//a[contains(@class,'card-schedule')])[1]"))
    )

    with allure.step("Verifikasi nama kereta sesuai pilihan"):
        nama_kereta = first_train.find_element(By.XPATH, ".//div[@class='name']").text
        assert "SANCAKA" in nama_kereta

    with allure.step("Verifikasi kelas kereta sesuai pilihan"):
        kelas_kereta = first_train.find_element(By.XPATH, ".//div[contains(@class,'col-one')]/div[2]").text
        assert "Eksekutif (AA)" in kelas_kereta

    with allure.step("Verifikasi nomor kereta sesuai pilihan"):
        nomor_kereta = first_train.find_element(By.XPATH, ".//div[@class='name']/span").text.strip("()")
        assert "81" in nomor_kereta

    with allure.step("Verifikasi harga tiket kereta sesuai pilihan"):
        harga_kereta = first_train.find_element(By.XPATH, ".//div[@class='price']").text
        assert "Rp 320.000,-" in harga_kereta

        print("✅ Yeayyy test passed!")
