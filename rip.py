from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from faker import Faker
import time
import random

fake = Faker('da_DK')

EMAILS = [
	"1@touchgrass.store",
	"2@touchgrass.store",
	"3@touchgrass.store",
]

def setup_driver():
	chrome_options = Options()
	chrome_options.add_argument("--log-level=3")
	chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

	ua = UserAgent()
	user_agent = ua.random
	chrome_options.add_argument(f"user-agent={user_agent}")

	driver = webdriver.Chrome(service=Service(), options=chrome_options)
	driver.get("https://game.scratcher.io/guldhornene-aalborg-lykkehjul-1")
	return driver

def start_flow(driver, wait: WebDriverWait):
	time.sleep(3)
	start_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "activate-button")))
	start_button.click()

def fill_form(driver, wait: WebDriverWait, email):
	input_name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#register-form > input:nth-child(2)")))
	input_name.clear()
	
	input_name.send_keys(generate_random_name())

	input_email = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#register-form > input.form-input.js-mailcheck")))
	input_email.clear()
	input_email.send_keys(email)

	input_phone = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#register-form > div.phone-number-field > input")))
	input_phone.clear()
	input_phone.send_keys(generate_random_phone_number())

	checkbox = driver.find_element(By.ID, "cb_gdpr")
	driver.execute_script("arguments[0].checked = true;", checkbox)

def submit_form(driver, wait: WebDriverWait):
	submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#register-form > button.tickets-btn.tickets-btn-primary.register-button")))
	submit_button.click()

def check_already_submitted(driver, wait: WebDriverWait):
	try:
		WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.sweet-alert.swal-warning.showSweetAlert.visible")))
		return True
	except:
		return False

def spin(driver, wait: WebDriverWait, email):
	spin_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.run-game-button")))
	spin_button.click()

	won = False

	while not won:
		try:
			try_again_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#tickets-app > div.page-container > div > div.element-1100841 > div.game-container > div.game-wrapper > div.try-again > button")))
			try_again_button.click()

			spin_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.run-game-button")))
			spin_button.click()
		except Exception:
			won = True
			prize = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "prize-name")))
			print(f"\n🤑 You won: {prize.text}\nWith email: {email}\n")

def generate_random_name():
	return fake.first_name()

def generate_random_phone_number():
	valid_phone_number_prefixes = ['2', '30', '31', '40', '41', '42', '50', '51', '52', '53', '60', '61', '71', '81', '91', '92', '93']
	prefix = random.choice(valid_phone_number_prefixes)
	remaining_length = 8 - len(prefix)
	number = prefix + ''.join(random.choices('0123456789', k=remaining_length))
	return number

def main():
	for email in EMAILS:
		driver = setup_driver()
		wait = WebDriverWait(driver, 10)
		try:
			start_flow(driver, wait)
			fill_form(driver, wait, email)
			submit_form(driver, wait)
			if check_already_submitted(driver, wait):
				print(f"❌ Email {email} has already spinned this week!")
				continue
			spin(driver, wait, email)
		except Exception as e:
			print("Error:", e)
			continue
		finally:
			driver.quit()

	print("\n✅ Finished email list!")

if __name__ == "__main__":
	main()
