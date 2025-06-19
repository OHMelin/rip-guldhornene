from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import time

NAME = "Oliver Melin"
PHONE = "51782325"
EMAILS = [
	"example1@gmail.com",
	"ohmelin23@gmail.com",
	"example23@gmail.com",
	"example3@gmail.com",
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
	input_name.send_keys(NAME)

	input_email = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#register-form > input.form-input.js-mailcheck")))
	input_email.clear()
	input_email.send_keys(email)

	input_phone = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#register-form > div.phone-number-field > input")))
	input_phone.clear()
	input_phone.send_keys(PHONE)

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
			else:
				spin(driver, wait, email)
		except Exception as e:
			print("Error:", e)
			continue
		finally:
			driver.quit()

	print("\n✅ Finished email list!")

if __name__ == "__main__":
	main()
