from mcp.server import MCPServer

# create mcp server instance
mcp = MCPServer("product-catalog")

products = [
    {
        "id": 1,
        "title": "Apple Watch Series 7",
        "price": 399.00,
        "description": "A stylish and feature-packed smartwatch from Apple",
        "tags": ["smartwatch", "apple", "fitness", "tech"],
    },
    {
        "id": 2,
        "title": "Samsung TV 4K",
        "price": 1299.00,
        "description": "A high-definition 4K smart TV from Samsung with excellent picture quality",
        "tags": ["tv", "samsung", "4k", "electronics"],
    },
    {
        "id": 3,
        "title": "Dell XPS Laptop",
        "price": 1499.00,
        "description": "A powerful and lightweight laptop from Dell with excellent performance",
        "tags": ["laptop", "dell", "xps", "gaming"],
    },
    {
        "id": 4,
        "title": "Nike Air Max 270",
        "price": 150.00,
        "description": "A stylish and comfortable sneaker from Nike",
        "tags": ["shoes", "nike", "airmax", "sneakers"],
    },
    {
        "id": 5,
        "title": "Sony Headphones WH-1000XM",
        "price": 349.00,
        "description": "A high-end wireless headphone from Sony with excellent noise-cancellation",
        "tags": ["headphones", "sony", "wh1000xm", "wireless"],
    },
    {
        "id": 6,
        "title": "Amazon Echo Dot (4th Gen)",
        "price": 49.99,
        "description": "A compact and affordable smart speaker from Amazon",
        "tags": ["smart speaker", "amazon", "echo dot", "voice assistant"],
    },
    {
        "id": 7,
        "title": "HP Pavilion Gaming Desktop",
        "price": 999.00,
        "description": "A powerful gaming desktop from HP with excellent performance",
        "tags": ["gaming desktop", "hp", "pavilion", "pc"],
    },
    {
        "id": 8,
        "title": "Microsoft Surface Laptop 3",
        "price": 1599.00,
        "description": "A premium and portable laptop from Microsoft with excellent performance",
        "tags": ["laptop", "microsoft", "surface", "tablet"],
    },
    {
        "id": 9,
        "title": "ASUS ROG Gaming Monitor",
        "price": 599.00,
        "description": "A high-end gaming monitor from ASUS with excellent performance",
        "tags": ["gaming monitor", "asus", "rog", "monitor"],
    },
    {
        "id": 10,
        "title": "Fitbit Charge 4",
        "price": 69.99,
        "description": "A stylish and feature-packed fitness tracker from Fitbit",
        "tags": ["fitness tracker", "fitbit", "charge 4", "smartwatch"],
    },
]


@mcp.tool(title="product listing")
def get_product_listings():
    """get list of all products"""
    return products


@mcp.tool(title="get product details")
def get_product_details(id: int):
    """get details of the product by its id"""
    for product in products:
        if product["id"] == id:
            return {"status": "success", "product": product}

    return {"status": "error", "message": f"product with {id} does not exist"}


@mcp.tool(title="add a new product")
def add_new_product(id: int, title: str, price: float, tags: list, description: str):
    """add a new product getting the product details"""

    products.append({"id": id, "title": title, "price": price, "tags": tags, "description": description})
    return {"status": "success", "message": f"added a new product"}


if __name__ == "__main__":
    # mcp.run(transport="streamable-http", host="0.0.0.0", port=8600)
    mcp.run(transport="stdio")
