import requests
from bs4 import BeautifulSoup
from random import choice
from csv import writer
from time import sleep

BASE_URL = "http://quotes.toscrape.com"

def scrape_quotes():
    all_quotes = []
    url = "/page/1/"

    while url:
        res = requests.get(f"{BASE_URL}{url}")
        print(f"Scraping {BASE_URL}{url}...")
        soup = BeautifulSoup(res.text, "html.parser")
        quotes = soup.find_all(class_="quote")

        for quote in quotes:
            text = quote.find(class_="text").get_text()
            author = quote.find(class_="author").get_text()
            bio_link = quote.find("a")["href"]
            all_quotes.append({
                "text": text,
                "author": author,
                "bio_link": bio_link
            })

        next_btn = soup.find(class_="next")
        url = next_btn.find("a")["href"] if next_btn else None
        sleep(2)

    return all_quotes

def get_author_info(bio_link):
    res = requests.get(f"{BASE_URL}{bio_link}")
    soup = BeautifulSoup(res.text, "html.parser")
    birth_date = soup.find(class_="author-born-date").get_text()
    birth_place = soup.find(class_="author-born-location").get_text()

    return birth_date, birth_place

def start_game(quotes):
    quote = choice(quotes)
    remaining_guesses = 4
    print("Here's a quote:")
    print(quote["text"])

    guess = ''
    while guess.lower() != quote["author"].lower() and remaining_guesses > 0:
        guess = input(f"Who said this quote? Guesses remaining: {remaining_guesses}\n")
        if guess.lower() == quote["author"].lower():
            print("You got it right!")
            break
        remaining_guesses -= 1
        if remaining_guesses == 3:
            print(f"Hint: The author was born on {get_author_info(quote['bio_link'])[0]}.")
        elif remaining_guesses == 2:
            print(f"Hint: The author was born in {get_author_info(quote['bio_link'])[1]}.")
        elif remaining_guesses == 1:
            first_initial = quote["author"][0]
            last_initial = quote["author"].split(" ")[-1][0]
            print(f"Hint: The author's initials are {first_initial}.{last_initial}.")
        else:
            print(f"Sorry, you're out of guesses. The answer was {quote['author']}.")

    again = ''
    while again.lower() not in ('y', 'n'):
        again = input("Would you like to play again (y/n)? ")
    if again.lower() == 'y':
        start_game(quotes)
    else:
        print("Thanks for playing!")

def write_quotes(quotes):
    with open("quotes.csv", "w", newline="", encoding="utf-8") as file:
        csv_writer = writer(file)
        csv_writer.writerow(["Text", "Author", "Bio-Link"])
        for quote in quotes:
            csv_writer.writerow([quote["text"], quote["author"], quote["bio_link"]])


if __name__ == "__main__":
    quotes = scrape_quotes()
    write_quotes(quotes)
    start_game(quotes)

