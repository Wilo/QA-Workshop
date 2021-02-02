import psycopg2
import re
from requests import session
from bs4 import BeautifulSoup as bs

hostname = "localhost"
username = "catalog"
password = "my_strong_and_secret_password"
dbname = "catalog"


def dbconnection():
    connection = psycopg2.connect(
        host=hostname,
        user=username,
        password=password,
        dbname=dbname,
    )
    return connection, connection.cursor()


def make_request(link):
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    headers = {
        "User-Agent": USER_AGENT,
    }
    request = session()
    response = request.get(link, headers=headers)
    return response.text


def parse_vendor(data):
    parsed_data = bs(data, "html.parser")
    # vendor_name = parsed_data.find("h3", "store-info__name")
    vendor_name = parsed_data.find("h3", re.compile("header__title"))
    if not vendor_name:
        vendor_name = parsed_data.find("h3", "brand")
        if not vendor_name:
            return "Perfil inaccesible"
    return str(vendor_name.text).strip("\t\n")


def parse_vendor_sales(data):
    parsed_data = bs(data, "html.parser")
    vendor_sales = parsed_data.find("p", "seller-info__subtitle-sales")
    if not vendor_sales:
        return (
            "Este vendedor aún no tiene suficientes ventas para calcular su reputación"
        )
    return str(vendor_sales.text).strip("\t\n")


def parse_vendor_location(data):
    parsed_data = bs(data, "html.parser")
    vendor_location = parsed_data.find("p", "location-subtitle")
    if not vendor_location:
        return "Sin ubicación en la página de perfil"
    return str(vendor_location.text).strip("\t\n")


if __name__ == "__main__":
    connection, cursor = dbconnection()
    cursor.execute("select id, link from product_catalog")
    data = cursor.fetchall()
    for item in data:
        response = make_request(item[1])
        vendor_name = parse_vendor(response)
        vendor_sales = parse_vendor_sales(response)
        vendor_location = parse_vendor_location(response)

        if vendor_name and vendor_sales and vendor_location:
            queryset = """UPDATE public.product_catalog
                       SET vendor_name=%s, vendor_sales=%s, vendor_location=%s
                       WHERE id=%s;"""
            items = [vendor_name] + [vendor_sales] + [vendor_location] + [item[0]]
            cursor.execute(queryset, items)
            connection.commit()

    cursor.close()
    connection.close()