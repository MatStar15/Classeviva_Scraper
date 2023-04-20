from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


def login():
    driver.find_element(By.ID, "login").send_keys(user)  # input user
    webElement = driver.find_element(By.ID, "password")  # input pswrd and submit the credentials
    webElement.send_keys(pswrd)
    webElement.submit()
    # time.sleep(0.2)
    print("logged in as user")


def get_marks():
    mark_containers = driver.find_elements(By.CLASS_NAME, "f_reg_voto_positivo")
    marks = []
    # print(type(marks))
    for container in mark_containers:
        mark = container.find_element(By.CLASS_NAME, "cella_trattino").text
        marks.append(mark)
    return marks


def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()


def convert_marks():
    suffix_dict = {
        "-": -0.25,
        "+": 0.25,
        "½": 0.5
    }

    for i in range(len(marks)):
        mark = marks[i]
        if is_integer(mark):
            continue
        else:
            mark = int(mark[0]) + suffix_dict.get(mark[1])
            marks[i] = mark


def get_elements():
    print("fetching data ...")
    table = driver.find_elements(By.TAG_NAME, "tr")
    elements = []
    for entry in table:
        # print(entry)
        td = entry.find_elements(By.TAG_NAME, "td")
        for element in td:
            elements.append(element)
    # print(elements)
    elements_text = []
    for element in elements:
        # print(type(td))
        elements_text.append(element.text)

    # print(elements_text)
    elements = elements[72:]
    elements_text = elements_text[72:]
    print("Done \n")
    return elements_text


if __name__ == '__main__':
    credentials = open('credentials/credentials.txt', 'r').read()
    user, pswrd = credentials.split("\n")
    print("user: " + user)  # + "\npwsrd = " + pswrd

    url = "https://web.spaggiari.eu/home/app/default/login.php"
    marks_url = "https://web.spaggiari.eu/cvv/app/default/genitori_note.php?ordine=materia&filtro=tutto"
    options = Options()
    options.add_argument('--headless=new')

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    # time.sleep(0.3)
    login()
    driver.save_screenshot('screenshots/headless.png')

    driver.get(marks_url)
    # time.sleep(0.3)
    # marks = get_marks()
    # convert_marks()

    # TODO: get marks per subject
    # TODO: do average, if possible create plots

    elements_text = get_elements()
    print(elements_text)

    # TODO: does not work yet
    print("Organizing data...\n")

    database = []
    count = 0
    subject = -1
    mark_n = 0
    for entry in elements_text:
        if entry.isupper():
            count = 0
            mark_n = 0
            database.append([entry, ])
            subject += 1

        if count in [2, 3, 4, 6]:
            if count == 2:
                database[subject].append([entry, ])
                mark_n += 1
            elif count in [3, 4, 6]:
                database[subject][mark_n].append(entry)
                # print(database[subject][mark_n])

            # print(subject)
            # print("adding " + entry + " to " + str(database[subject][0]))

        count += 1
    print(database[0])
    print(database)
