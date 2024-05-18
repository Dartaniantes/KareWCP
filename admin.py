from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pyperclip as clip
import translator as tr
import os

login = os.environ['ADM_LOGIN']
pw = os.environ['ADM_PW']

active = False
driver = None


def init():
    global driver
    global active
    active = True
    options = Options()
    options.add_experimental_option('detach', True)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get('https://www.kare-design.in.ua/minimus/')

    login_field = driver.find_element('xpath', "//input[contains(@name, 'login')]")
    pw_field = driver.find_element('xpath', "//input[contains(@name, 'passwd')]")

    login_field.send_keys(login)
    pw_field.send_keys(pw)
    driver.find_element('xpath', "//a[contains(@class,'txt0')]").click()  # authorize button


def open_product(articul):
    if driver.current_url != 'https://www.kare-design.in.ua/minimus/tovars/':
        driver.get('https://www.kare-design.in.ua/minimus/tovars/')
    driver.find_elements('xpath', "//input[@name='articul']")[0].send_keys(articul) #articul field
    driver.find_element('xpath', "//a[contains(@href, \"javascript:TODO('search')\")]").click()
    driver.find_elements('xpath', "//a[contains(@href,'edit.php?cat_id=')]")[1].click()


def init_and_get_product(articul):
    init()
    open_product(articul)


def is_parsed():
    return fully_parsed() or partially_parsed()


def fully_parsed():
    desc = extract_text('description', 'ru')
    tech = extract_text('tech', 'ru')
    if desc is None:
        return False
    if desc.strip() == '':
        return False
    if tech is None:
        return False
    if tech.strip() == '':
        return False
    return True


def partially_parsed():
    text = extract_text('description', 'ru')
    if text is None: return False
    detection = tr.detect(text)
    return detection.confidence > 80 and detection.language == 'ru' and text.__contains__('Информация о товаре')


def extract_text(text_type, lang):
    open_editor(text_type, lang)
    switch_to_editor(define_editor_name(text_type))
    component = driver.find_element("xpath", '//a[@id="cke_15"]')
    if component.get_attribute('class').__contains__('disabled'):
        print("empty")
        return None
    component.click()  # copy if contains text
    switch_to_product()
    return clip.paste()


def commit_product(urk_text, rus_text):
    save_urk_text(urk_text)
    save_rus_text(rus_text)
    driver.find_element('xpath', "//a[@title='Сохранить и вернуться к списку товаров']").click()


def save_rus_text(rus_text):
    rus_text.strip()
    save_text(rus_text[:rus_text.index("\n")], 'description', "ru")
    save_text(rus_text[rus_text.index("\n")+1:], 'tech', "ru")


def save_urk_text(urk_text):
    urk_text.strip()
    save_text(urk_text[:urk_text.index("\n")], 'description', "uk")
    save_text(urk_text[urk_text.index("\n")+1:], 'tech', "uk")


def switch_to_editor(name):
    handles = driver.window_handles
    while driver.title != name:
        for handle in handles:
            driver.switch_to.window(handle)
            if driver.title == name:
                break
    driver.find_element("xpath", '//a[@id="cke_22"]').click()


def save_text(text, text_type, lang):
    open_editor(text_type, lang)
    commit_text(text)


def open_editor(text_type, lang):
    lang = 1 if lang == "ru" else 2 if lang == "uk" else None
    editor = define_editor_name(text_type)
    if lang is None:
        raise Exception("Invalid data language entered. Should be 'ru' or 'ua' only")
    if editor is None:
        raise Exception("Invalid data type entered. Should be 'description' or 'tech' only")


    xpath = "//a[contains(@href,' {lang},')]//img[contains(@src,'{type}')]".format(lang=lang, type=text_type)

    driver.find_element('xpath', xpath).click()
    switch_to_editor(editor)


def define_editor_name(text_type):
    return 'Full content' if text_type == 'description' else 'Tech properties' if text_type == 'tech' else None

def commit_text(text):
    clip.copy(text)
    driver.find_element("xpath", '//iframe[@aria-describedby=\'cke_65\']').send_keys(Keys.CONTROL + "v")
    driver.find_element("xpath", '//a[@id="cke_11"]').click()  # save
    driver.close()
    switch_to_product()


def switch_to_product():
    handles = driver.window_handles
    for handle in handles:
        driver.switch_to.window(handle)
        if driver.title.__contains__("Товары"):
            break



