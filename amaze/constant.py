
prompt = """i gave u a image and some text of a online post i want you to extract some data from it and send it in a particular format.
    You have to extract 
   {
    "companyName": "string",  // Name of the company
    "productCategory": "string",  // E.g., "tech", "food"
    "productType": "string",  // E.g., "keyboard", "watch"
    "listingDetails": {
        "productTitle": "string",  // The main product title, e.g., "Wireless Bluetooth Keyboard"
        "productDescription": "string",  // A detailed description
        "price": {
        "currency": "string",  // E.g., "USD", "INR"
        "amount": "number"  // E.g., 49.99
        },
        "productImages": [
        {
            "imageURL": "string",  // URL of the product image
            "altText": "string"  // Short description of the image
        }
        ],
        "productAttributes": {
        "color": "string",  // E.g., "black", "red"
        "size": "string",  // E.g., "Medium", "15-inch"
        "weight": "string",  // E.g., "500g"
        "dimensions": {
            "length": "number",  // Length in cm
            "width": "number",  // Width in cm
            "height": "number"  // Height in cm
        },
        "material": "string",  // E.g., "plastic", "metal"
        "warranty": "string",  // E.g., "1 year"
        "ageRecommendation": "string",  // E.g., "12+", "Adult"
        "version": "string",  // E.g., "2023 Model"
        "otherAttributes": "JSON"  // Custom additional attributes as a nested JSON object
        },
        "availability": {
        "inStock": "boolean",  // Whether the item is in stock
        "quantity": "number"  // Available quantity
        },
        "shippingDetails": {
        "weight": "number",  // Shipping weight in kg
        "dimensions": {
            "length": "number",
            "width": "number",
            "height": "number"
        }
        },
        "categoryHierarchy": [
        "string"  // E.g., ["Electronics", "Computers", "Keyboards"]
        ]
    },
    "sellerInfo": {
        "sellerName": "string",  // Name of the seller or store
        "contactEmail": "string",  // Contact email for support
        "sellerRating": "number"  // E.g., 4.5 (rating out of 5)
    }
    };

        You are only allowed to response in the above formate if anyfield is found just response with {... , <field>:"", ...};
    """
