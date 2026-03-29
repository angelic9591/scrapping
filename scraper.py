import requests
from bs4 import BeautifulSoup
from image_downloader import download_image
from csv_writer import save_products

BASE_URL = "https://www.casespanther.com"
COLLECTION_URL = BASE_URL + "/collections/phone-cases"

response = requests.get(COLLECTION_URL)
soup = BeautifulSoup(response.text, "lxml")

products = []

product_cards = soup.select("div.quick-add-modal__content-info")
print("Products found:", len(product_cards))

for i, product in enumerate(product_cards):

    title_tag = product.select_one("h3")
    title = title_tag.text.strip().replace("/", "_") if title_tag else f"product_{i}"
    product_name = title.replace(" ", "_")

    link_tag = product.select_one("a.full-unstyled-link")
    link = BASE_URL + link_tag["href"] if link_tag else ""

    price_tag = product.select_one("span.price-item--regular")
    price = price_tag.text.strip() if price_tag else ""

    img_tags = product.select("img")

    raw_images = []
    processed_images = []

    for index, img in enumerate(img_tags):

        img_url = img.get("src")

        if not img_url:
            continue

        if img_url.startswith("//"):
            img_url = "https:" + img_url

        raw_path, processed_path = download_image(img_url, product_name, index)

        if raw_path:
            raw_images.append(raw_path)

        if processed_path:
            processed_images.append(processed_path)

    products.append({
        "title": title,
        "price": price,
        "product_url": link,
        "raw_images": raw_images,
        "processed_images": processed_images
    })

save_products(products)