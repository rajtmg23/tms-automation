import os
import time
import smtplib
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

baseURL = "https://tms58.nepsetms.com.np/login"
driver = webdriver.Chrome(
  service=ChromeService(ChromeDriverManager().install()))
driver.get(baseURL)
driver.maximize_window()
wait = WebDriverWait(driver, -1)

USER_NAME_FIELD = "//input[@placeholder='Client Code/ User Name']"
PASSWORD_FIELD = "//input[@id='password-field']"
SCRIPT_NAME = "NLICL"
MARKET_WATCH_URL = "https://tms58.nepsetms.com.np/tms/me/member-market-watch"
MARKET_DEPTH_URL = "https://tms58.nepsetms.com.np/tms/me/stockQuoteScreenComponent"
BUY_SELL_URL = "https://tms58.nepsetms.com.np/tms/me/memberclientorderentry"

MY_EMAIL = os.environ['EMAIL']
MY_PASSWORD = os.environ['EMAIL_PASSWORD']
USER_NAME = os.environ['USERNAME_58']
PASSWORD = os.environ['PASSWORD_58']


# ----------LOGIN------------
def login():
  wait.until(EC.presence_of_element_located((By.XPATH, USER_NAME_FIELD)))
  driver.find_element(By.XPATH, USER_NAME_FIELD).send_keys(USER_NAME)
  driver.find_element(By.XPATH, PASSWORD_FIELD).clear()
  driver.find_element(By.XPATH, PASSWORD_FIELD).send_keys(PASSWORD)


# ----------CHECK MARKET DEPTH------------
def market_depth(script=SCRIPT_NAME):
  if driver.current_url == MARKET_DEPTH_URL:
    script_input_box = driver.find_element(By.XPATH,
                                           "//input[@role='combobox']")
    script_input_box.send_keys(script)
    time.sleep(0.5)
    script_input_box.send_keys(Keys.ENTER)
  else:
    driver.get(MARKET_DEPTH_URL)
    wait.until(
      EC.presence_of_element_located((By.XPATH, "//input[@role='combobox']")))
    time.sleep(0.5)
    market_depth(script=SCRIPT_NAME)


def market_watch():
  if driver.current_url != MARKET_WATCH_URL:
    driver.get(MARKET_WATCH_URL)


def click_buy_button():
  if driver.current_url == BUY_SELL_URL:
    buy_button = "//div[@class='order__options--buysell']//label[3]"
    driver.find_element(By.XPATH, buy_button).click()
  else:
    driver.get(BUY_SELL_URL)
    click_buy_button()


def click_sell_button():
  if driver.current_url == BUY_SELL_URL:
    sell_button = "//body//app-root//app-three-state-toggle//label[1]"
    driver.find_element(By.XPATH, sell_button).click()
  else:
    driver.get(BUY_SELL_URL)
    click_sell_button()


def send_email(msg):
  with smtplib.SMTP("smtp.gmail.com", 587) as connection:
    connection.starttls()
    connection.login(user=MY_EMAIL, password=MY_PASSWORD)
    connection.sendmail(from_addr=MY_EMAIL,
                        to_addrs="jhapaliraju@gmail.com",
                        msg=f"Subject: ORDER STATUS\n\n{msg}")


# SELL UNTESTED
def sell_on_high_price(script, quantity):
  click_sell_button()
  count = 1
  script_input_box = driver.find_element(By.XPATH,
                                         "//input[@formcontrolname='symbol']")
  script_input_box.clear()
  script_input_box.send_keys(script)
  time.sleep(0.5)
  script_input_box.send_keys(Keys.ENTER)

  quantity_input_box = driver.find_element(
    By.XPATH, "//input[@formcontrolname='quantity']")
  quantity_input_box.clear()
  quantity_input_box.send_keys(quantity)

  wait.until(
    EC.presence_of_element_located((By.XPATH, "//form/div[3]/div/div[3]/b")))
  high_price_field = driver.find_element(By.XPATH,
                                         "//form/div[3]/div/div[3]/b")
  high_price_value = high_price_field.text

  price_input_box = driver.find_element(By.XPATH,
                                        "//input[@formcontrolname='price']")
  price_input_box.send_keys(high_price_value)

  select = Select(
    driver.find_element(By.XPATH,
                        "//div[@class='order__form--valid']//select"))
  select.select_by_visible_text('GTC')
  order_button = driver.find_element(By.XPATH,
                                     "//button[contains(text(),'SELL')]")
  order_button.click()

  send_email(f"{count}. Order placed successfully")
  # print(f"{count}. Order placed successfully")
  time.sleep(3)
  click_sell_button()
  time.sleep(1)

  while count < 20:
    price = high_price_field.text
    wait.until_not(
      EC.text_to_be_present_in_element(
        (By.XPATH, "//form/div[3]/div/div[3]/b"), price))
    high_price = high_price_field.text
    price_input_box.clear()
    price_input_box.send_keys(high_price)
    select.select_by_visible_text('GTC')
    order_button.click()
    count += 1
    send_email(f"{count}. Order placed successfully")
    # print(f"{count}. Order placed successfully")
    time.sleep(3)
    click_sell_button()
    time.sleep(1)


# BUY UNTESTED
def buy_on_high_price(script, quantity):
  click_buy_button()
  count = 1
  script_input_box = driver.find_element(By.XPATH,
                                         "//input[@formcontrolname='symbol']")
  script_input_box.clear()
  script_input_box.send_keys(script)
  time.sleep(0.5)
  script_input_box.send_keys(Keys.ENTER)

  quantity_input_box = driver.find_element(
    By.XPATH, "//input[@formcontrolname='quantity']")
  quantity_input_box.clear()
  quantity_input_box.send_keys(quantity)

  wait.until(
    EC.presence_of_element_located((By.XPATH, "//form/div[3]/div/div[3]/b")))
  high_price_field = driver.find_element(By.XPATH,
                                         "//form/div[3]/div/div[3]/b")
  high_price_value = high_price_field.text

  price_input_box = driver.find_element(By.XPATH,
                                        "//input[@formcontrolname='price']")
  price_input_box.send_keys(high_price_value)

  select = Select(
    driver.find_element(By.XPATH,
                        "//div[@class='order__form--valid']//select"))
  select.select_by_visible_text('GTC')
  order_button = driver.find_element(By.XPATH,
                                     "//button[contains(text(),'BUY')]")
  order_button.click()

  send_email(f"{count}. Order placed successfully")
  # print(f"{count}. Order placed successfully")
  time.sleep(3)
  click_buy_button()
  time.sleep(1)

  while count < 20:
    price = high_price_field.text
    wait.until_not(
      EC.text_to_be_present_in_element(
        (By.XPATH, "//form/div[3]/div/div[3]/b"), price))
    high_price = high_price_field.text
    price_input_box.clear()
    price_input_box.send_keys(high_price)
    select.select_by_visible_text('GTC')
    order_button.click()
    count += 1
    send_email(f"{count}. Order placed successfully")
    # print(f"{count}. Order placed successfully")
    time.sleep(3)
    click_buy_button()
    time.sleep(1)


def log_out():
  driver.find_element(
    By.XPATH, "//a[@class='ubadge__item']//i[@class='nf-user']").click()
  driver.find_element(By.XPATH, "//span[normalize-space()='Log Out']").click()
  time.sleep(2)
  driver.quit()
