import requests
from .models import Product  # Import your Product model
from django.utils.text import slugify
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.management import call_command
from django.db import transaction
from django.utils import timezone

# Define the API URL
api_url = "https://fakestoreapi.com/products"


def fetch_data_from_api():
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(
                f"Failed to fetch data from the API. Status Code: {response.status_code}"
            )
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
        return None


@transaction.atomic
def populate_product_model(data):
    for product_data in data:
        category_name = product_data["category"]

        category, _ = Category.objects.get_or_create(name=category_name)
        slug = slugify(product_data["title"])
        image_url = product_data["image"]
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(requests.get(image_url).content)
        img_temp.flush()
        product = Product.objects.create(
            name=product_data["title"],
            img=File(img_temp),
            price=product_data["price"],
            stock=0,
            description=product_data["description"],
            slug=slug,
            manufactured_on=timezone.now(),
            category=category,
            features="",
        )


if __name__ == "__main__":
    from .models import Category

    data = fetch_data_from_api()
    if data:
        populate_product_model(data)
        print("Data successfully populated in the Product model.")
