import qrcode
from constants import *
import shopify


def generateProductHandles(product_type="Beans"):    
    """generates a list of product handles to be used in URL generation and file naming schemes

    Args:
        product_type (str): Specifies the type of product. Defaults to "Beans".
    Returns:

    """    
    
    products = shopify.Product._find_every(fields="handle", product_type=product_type)
    handles = []
    for product in products:
        # before string manipulation: "{'handle': 'colombia-decaf'}"
        # after string manipution: "colombia-decaf"
        handles.append(str(product.attributes)[:-1].split()[1].replace("'",''))
        
    return handles


def generateAddresses(handles):
    """generates a list of addresses to products on the product page

    Args:
        handles (list): array of product handles used to generate addresses

    Returns:
        list: array of addresses to products
    """    
    
    addresses = []
    for handle in handles:
        addresses.append(f"https://politecoffee.com/products/{handle}")
    return addresses


def generateSingleQR(handle, address, saveDirectory="./QRCodes"):
    """generates a single QR code for a product

    Args:
        handle (str): Name of the file (-QR.png will be appended)
        address (str): The web address of the product
        saveDirectory (str): The directory to save the QR code to. Defaults to "./QRCodes".
    """    
    
    print(f"fileName = {handle}-QR.png\nURL={address}\n")
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )

    qr.add_data(address)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#C92018", back_color="#FFFFFF")
    img.save(f"{saveDirectory}/{handle}-QR.png")


def generateAllQR(handles, addresses, saveDirectory="./QRCodes"):
    """generates multiple QR codes using the generateSingleQR function
    
    Args:
        handle (list): Array of file names
        address (list): Array of web address for the products
        saveDirectory (str): The directory to save the QR code to. Defaults to "./QRCodes".
    """    
    
    products = zip(handles, addresses)
    for i, (handle, address) in enumerate(products):
        generateSingleQR(handle, address, saveDirectory)
          
    
def main():
    handles = generateProductHandles()
    addresses = generateAddresses(handles)
    generateAllQR(handles, addresses)
        
if __name__ == "__main__":
    session = shopify.Session(shop_url=SHOP_URL, version=VERSION, token=PASSWORD)
    shopify.ShopifyResource.activate_session(session)
    main()
    shopify.ShopifyResource.clear_session()