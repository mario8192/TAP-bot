import time
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import atom.data
import gdata.data
import gdata.contacts.client
import gdata.contacts.data

from flask import Flask
from flask import request

driver = webdriver.Chrome()
driver.wait = WebDriverWait(driver, 5)

driver.get("https://web.whatsapp.com")
driver.wait.until(EC.title_is("WhatsApp"))


app = Flask(__name__)

# contact_driver = webdriver.Chrome()
# contact_driver.wait = WebDriverWait(driver, 5)
# contact_driver.get("https://contacts.google.com")
# driver.wait.until(EC.title_contains("Sign in"))
# contact_driver.find_element_by_css_selector("input.whsOnd.zHQkBf").send_keys("jimthariyal")
# contact_driver.find_element_by_css_selector("input.whsOnd.zHQkBf").send_keys(Keys.ENTER)
# contact_driver.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"span.RveJvd.snByac")))
# contact_driver.find_element_by_css_selector("input.whsOnd.zHQkBf").send_keys("jimmyjimmyjimmy")
# contact_driver.find_element_by_css_selector("input.whsOnd.zHQkBf").send_keys(Keys.ENTER)


# def init_driver():
#     driver = webdriver.Chrome()
#     # driver = webdriver.Firefox()
#     driver.wait = WebDriverWait(driver, 5)
#     return driver


# def loginCookie():
#     driver.get("https://web.whatsapp.com")
#     driver.wait.until(EC.title_is("WhatsApp"))
#     driver.wait.until(EC.presence_of_element_located((By.ID, "side")))

# driver.find_element_by_css_selector(
#     "input._44uDJ.copyable-text.selectable-text")

# def loginContact():
#     contact_driver.find_element_by_css_selector(
#         "input.whsOnd.zHQkBf").send_keys("jimthariyal")
#     contact_driver.find_element_by_css_selector(
#         "input.whsOnd.zHQkBf").send_keys(Keys.ENTER)


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


@app.route('/sendTo', methods=['POST'])
def sendTo():
    content = request.get_json()
    print(content)
    chat = content['chat']
    message = content['message']
    selectChat(chat)
    sendMessage(message)
    return "done"


def lastMessage():
    return driver.find_elements_by_class_name(
        "message-in")[-1].find_elements_by_tag_name("span")[2].get_attribute("innerHTML")


@app.route('/createGroup', methods=['POST'])
def createGroup():
    content = request.get_json()
    group_name = content['group_name']
    tap_admin = content['tap_admin']
    school_admin = content['school_admin']

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


@app.route('/addToGroup')
def addToGroup():

    person = request.form['person']
    group = request.form['group']

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


@app.route('/create_contact')
def create_contact(gd_client, phone_vol):
    new_contact = gdata.contacts.data.ContactEntry()
    # Set the contact's name.
    new_contact.name = gdata.data.Name(
        given_name=gdata.data.GivenName(text=phone_vol),
        family_name=gdata.data.FamilyName(text=''),
        full_name=gdata.data.FullName(text=''))
    new_contact.content = atom.data.Content(text='Notes')
    # Set the contact's phone numbers.
    new_contact.phone_number.append(gdata.data.PhoneNumber(
        text=phone_vol, rel=gdata.data.HOME_REL, primary='true'))
    # Send the contact data to the server.
    contact_entry = gd_client.CreateContact(new_contact)
    print("Contact's ID: %s", contact_entry.id.text)
    return contact_entry


if __name__ == "__main__":
    print("yo")
    app.run(debug=True)
    # loginCookie()
