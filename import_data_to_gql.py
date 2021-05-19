from saleor_gql_loader import ETLDataLoader

# I generated a token for my app as explained in the README.md
# https://github.com/grll/saleor-gql-loader/blob/master/README.md
etl_data_loader = ETLDataLoader("LcLNVgUt8mu8yKJ0Wrh3nADnTT21uv")


def create_default_warehouse():
    # create a default warehouse
    warehouse_id = etl_data_loader.create_warehouse()


def create_default_shipping_zone():
    # create a default shipping zone associated
    shipping_zone_id = etl_data_loader.create_shipping_zone(addWarehouses=[warehouse_id])


# define my products usually extracted from csv or scraped...
products = [
    {
        "name": "tea a",
        "description": "description for tea a",
        "category": "green tea",
        "price": 5.5,
        "strength": "medium"
    },
    {
        "name": "tea b",
        "description": "description for tea b",
        "category": "black tea",
        "price": 10.5,
        "strength": "strong"
    },
    {
        "name": "tea c",
        "description": "description for tea c",
        "category": "green tea",
        "price": 9.5,
        "strength": "light"
    }
]


def add_sku(product_list):
    # adds basic sku to products, will have to return it
    for index, prod in enumerate(product_list):
        prod["sku"] = "{:05}-00".format(index)


def create_attribute(product_list, new_attribute):
    # create a new attribute
    new_attribute_id = etl_data_loader.create_attribute(name=new_attribute)
    unique_attribute = set([prod['strength'] for prod in product_list])
    for new_attribute in unique_attribute:
        etl_data_loader.create_attribute_value(new_attribute_id, name=new_attribute)


"""# create another quantity attribute used as variant:
qty_attribute_id =  etl_data_loader.create_attribute(name="qty")
unique_qty = {"100g", "200g", "300g"}
for qty in unique_qty:
    etl_data_loader.create_attribute_value(qty_attribute_id, name=qty)"""


def create_product_type():
    # create a product type: tea
    product_type_id = etl_data_loader.create_product_type(name="tea",
                                                          hasVariants=True,
                                                          productAttributes=[strength_attribute_id],
                                                          variantAttributes=[qty_attribute_id])


def create_product_category():
    # create categories
    unique_categories = set([product['category'] for product in products])


cat_to_id = {}
for category in unique_categories:
    cat_to_id[category] = etl_data_loader.create_category(name=category)

for i, product in enumerate(products):
    product_id = etl_data_loader.create_product(product_type_id,
                                                name=product["name"],
                                                description=product["description"],
                                                basePrice=product["price"],
                                                sku=product["sku"],
                                                category=cat_to_id[product["category"]],
                                                attributes=[
                                                    {"id": strength_attribute_id, "values": [product["strength"]]}],
                                                isPublished=True)
    products[i]["id"] = product_id

"""# create some variant for each product:
for product in products:
    for i, qty in enumerate(unique_qty):
        variant_id = etl_data_loader.create_product_variant(product_id,
                                                            sku=product["sku"].replace("-00", "-1{}".format(i + 1)),
                                                            attributes=[{"id": qty_attribute_id, "values": [qty]}],
                                                            costPrice=product["price"],
                                                            weight=0.75,
                                                            stocks=[{"warehouse": warehouse_id, "quantity": 15}])"""
