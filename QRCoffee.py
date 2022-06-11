from bs4 import BeautifulSoup
import requests
import qrcode
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

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
    root = Tk()
    #Define the geometry
    root.geometry("750x350")
    root.title("QRCoffee")


    def select_file():
        global path
        path = filedialog.askdirectory(title="Select a File to Store the QR Codes")
        Label(root, text=path, font=13).pack()

    #Create a label and a Button to Open the dialog
    Label(root, text= "First Select a Directory to Save the QR Codes in", font=('Aerial 14 bold')).pack(pady=20)
    button_file = ttk.Button(root, text="Open File", command = select_file)
    button_file.pack(ipadx=5, pady=15)

    Label(root, text= "Generate QR Codes", font=('Aerial 14 bold')).pack(pady=20)
    button_generate = ttk.Button(root, text="Generate", command = lambda : generateCommand(path))
    button_generate.pack(ipadx=5, pady=15)

    root.mainloop()


if __name__ == "__main__":
    main()