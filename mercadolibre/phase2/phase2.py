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
    request = session()
    response = request.get(link)
    return response.text


def parse_categories(data):
    parsed_data = bs(data, "html.parser")
    items = parsed_data.find_all("a", re.compile("breadcrumb"))
    collect = []
    for item in items:
        collect.append(str(item.text).strip("\t\n"))
    return collect


def parse_vendor_link(data):
    parsed_data = bs(data, "html.parser")
    items = parsed_data.find_all("a", re.compile("ui-box-component__action"))
    vendor = []
    for item in items:
        vendor.append(str(item["href"]))
    return vendor


if __name__ == "__main__":
    connection, cursor = dbconnection()
    cursor.execute("select id, link from product_catalog")
    data = cursor.fetchall()
    for item in data:
        response = make_request(item[1])
        categories = parse_categories(response)
        vendor_link = parse_vendor_link(response)

        categories = categories[1:]

        if len(categories) < 3:
            categories.append("")
        elif len(categories) > 3:
            categories.pop()

        # ipdb.set_trace()

        if not vendor_link:
            vendor_link.append("")

        print(f"categories: {categories}, vendor_link: {vendor_link}")

        if categories and vendor_link:
            queryset = """UPDATE public.product_catalog 
                   SET classification=%s, product_type=%s, brand=%s, vendor_link=%s
                   WHERE id=%s;"""

            items = categories + vendor_link + [item[0]]
            print(items)
            cursor.execute(queryset, items)
            connection.commit()

    cursor.close()
    connection.close()