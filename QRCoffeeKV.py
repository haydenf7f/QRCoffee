from bs4 import BeautifulSoup
import requests
import qrcode


def getProducts():

    URL = "https://politecoffee.com/collections/products"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    products = [coffee.get_text() for coffee in soup.find_all("h3", class_="card__name h4")]

    product_names = []

    # remove '|', ':', '"', and whitespace
    for coffee in products:
        if '|' in coffee:
            coffee = coffee.replace('|', '-')
        if ':' in coffee:
            coffee = coffee.replace(':', '')
        if '"' in coffee:
            coffee = coffee.replace('"', '')

        coffee = coffee.replace(' ', '')
        product_names.append(coffee)

    all_links = [link.get('href') for link in soup.find_all('a')]

    product_links = []
    for link in all_links:
        if 'collections/products' in link:
            product_links.append(f"https://politecoffee.com{link}")

    product_entries = zip(product_names, product_links)
    
    return product_entries


def generateQR(directory, saveAs, URL):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(URL)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#C92018", back_color="#FFFFFF")
    img.save(f"{directory}/{saveAs}")


def generateCommand(directory):
    products = getProducts()
    for i, (fileName, URL) in enumerate(products):
        generateQR(directory, f"{fileName}-QR.png", URL)
        # print(f"fileName = {fileName}\nURL={URL}\n")


def main():
    return


if __name__ == "__main__":
    main()