import requests
from bs4 import BeautifulSoup

URL = "https://www.newegg.com/d/Best-Sellers/All-Laptop/s/ID-32"

HEADERS = { #headers form chrome dev tools
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "", #make sure NOT to accept any encoding 
}


def get_page(url):
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200: #make sure request is good
            print(f"Debug code: {response.status_code}")
            print(f"{response.text}")
        return response.text
    except:
        print("Error: Could not send request")
    return None


def save_page(html, filename="page.html"): #debug func
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
    except:
        print("Error: Could not save page")


def find_laptops(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select(".goods-container")

    if not items:
        print("Error: No products found")
        return []

    laptops = []
    for item in items:
        name_el = item.select_one(".goods-title")
        dollars_el = item.select_one(".goods-price-value strong")
        cents_el = item.select_one(".goods-price-value sup")
        rating_el = item.select_one(".goods-rating i[aria-label]")

        name = "N/A" #set all vars to N/A incase they don't exist
        price = "OUT OF STOCK" #when we can't find price it usually means it out of stock on the page
        rating = "N/A"

        if name_el:                        #if each one exists format and set
            name = name_el.text.strip() 
        if dollars_el and cents_el:
            price = f"${dollars_el.text.strip()}{cents_el.text.strip()}" 
        if rating_el:
            rating = rating_el["aria-label"] 

        laptops.append({"name": name, "price": price, "rating": rating})

    return laptops


def display_laptops(laptops): 
    if not laptops:
        print("No laptops to display.")
        return

    i = 1
    for laptop in laptops:
        print(f"[{i}]")
        print(f"Laptop: {laptop['name']}")
        print(f"Price:  {laptop['price']}")
        print(f"Rating: {laptop['rating']}")
        print()
        i += 1


def main():
    print("\"Best sellers\" in laptops on Newegg: \n")

    data = get_page(URL)
    if not data:
        print("Error: No data received")
        return

    #save_page(data) #for debugging
    laptops = find_laptops(data)
    display_laptops(laptops)


if __name__ == "__main__":
    main()
