import time
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome()
driver.wait = WebDriverWait(driver, 5)

# def init_driver():
#     driver = webdriver.Chrome()
#     # driver = webdriver.Firefox()
#     driver.wait = WebDriverWait(driver, 5)
#     return driver


def loginCookie(driver):
    driver.get("https://web.whatsapp.com")
    driver.wait.until(EC.title_is("WhatsApp"))
    driver.wait.until(EC.presence_of_element_located((By.ID, "side")))

    driver.find_element_by_css_selector(
        "input._44uDJ.copyable-text.selectable-text")


def selectChat(person):
    driver.find_element_by_css_selector(
        "input._2zCfw.copyable-text.selectable-text").send_keys(person)
    driver.find_element_by_css_selector(
        "input._2zCfw.copyable-text.selectable-text").send_keys(Keys.ENTER)


def sendMessage(text):
    if(type(text) == list):
        for line in text:
            driver.find_element_by_css_selector(
                "div._3u328.copyable-text.selectable-text").send_keys(line)
            driver.find_element_by_css_selector(
                "div._3u328.copyable-text.selectable-text").send_keys(Keys.SHIFT, Keys.RETURN)
        driver.find_element_by_css_selector(
            "div._3u328.copyable-text.selectable-text").send_keys(Keys.RETURN)
    else:
        driver.find_element_by_css_selector(
            "div._3u328.copyable-text.selectable-text").send_keys(text)
        driver.find_element_by_css_selector(
            "div._3u328.copyable-text.selectable-text").send_keys(Keys.RETURN)


def lastMessage():
    return driver.find_elements_by_class_name(
        "message-in")[-1].find_elements_by_tag_name("span")[2].get_attribute("innerHTML")


def createGroup(group_name, tap_admin, school_admin):
    ActionChains(driver).click(
        driver.find_elements_by_css_selector("div._3j8Pd")[2]).perform()
    ActionChains(driver).click(
        driver.find_element_by_css_selector("div._3zy-4.Sl-9e")).perform()
    driver.find_element_by_css_selector(
        "input._44uDJ.copyable-text.selectable-text").send_keys(tap_admin)
    driver.find_element_by_css_selector(
        "input._44uDJ.copyable-text.selectable-text").send_keys(Keys.ENTER)
    driver.find_element_by_css_selector(
        "input._44uDJ.copyable-text.selectable-text").send_keys(school_admin)
    driver.find_element_by_css_selector(
        "input._44uDJ.copyable-text.selectable-text").send_keys(Keys.ENTER)
    ActionChains(driver).click(
        driver.find_element_by_css_selector("div._1g8sv")).perform()
    driver.find_element_by_css_selector(
        "div._3u328.copyable-text.selectable-text").send_keys(group_name)
    ActionChains(driver).click(
        driver.find_element_by_css_selector("div._1g8sv")).perform()


def sendTo(chat, message):
    selectChat(chat)
    sendMessage(message)


def addToGroup(person, group):
    selectChat(group)
    ActionChains(driver).click(
        driver.find_elements_by_css_selector("div._3j8Pd")[-1]).perform()
    ActionChains(driver).click(driver.find_element_by_css_selector(
        "li._3cfBY._2yhpw._3BqnP")).perform()
    time.sleep(0.5)
    ActionChains(driver).click(
        driver.find_element_by_css_selector("div._2WP9Q")).perform()
    driver.find_element_by_css_selector(
        "input._2zCfw.copyable-text.selectable-text").send_keys(person)
    time.sleep(0.5)
    driver.find_element_by_css_selector(
        "input._2zCfw.copyable-text.selectable-text").send_keys(Keys.ENTER)
    ActionChains(driver).click(
        driver.find_element_by_css_selector("div._1AWh3")).perform()
    ActionChains(driver).click(
        driver.find_element_by_css_selector("div._2eK7W._3PQ7V")).perform()


def scrollAll():
    SCROLL_PAUSE_TIME = 3
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


if __name__ == "__main__":
    print("yo")
    # loginCookie(driver)
