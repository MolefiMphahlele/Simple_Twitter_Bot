from bs4 import BeautifulSoup
import requests


def merriam_webster_query():
    url = "https://www.merriam-webster.com/word-of-the-day"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")

    page_text = doc.find(class_="word-and-pronunciation")
    webster_word= str(page_text).split("h")[1].split(">")[-1][:-2]
    word_of_day = check_word(webster_word)

    return word_of_day
    
    
def dic_query():
    url = "https://www.dictionary.com/e/word-of-the-day/"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")

    page_text = doc.find(class_="otd-item-headword__word")
    dic_word = str(page_text).split(">")[2].split("<")[0]
    word_of_day = check_word(dic_word)

    return word_of_day


def ub_query():
    url = "https://www.urbandictionary.com/random.php"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")

    page_text = doc.find(class_="mb-8 flex")
    page_text = page_text.find("a")
    urban_word= str(page_text).split(">")[-2].split("<")[0]
    word_of_day = check_word(urban_word)

    return word_of_day

def check_word(word):
    for character in word:
        if character.isdigit():
            choice = input(f"A character in {word} is invalid.")
            if choice == True:
                pass
            else:
                break

    return word
    
#word= ub_query()
#print(word)
