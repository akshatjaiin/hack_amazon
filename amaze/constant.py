prompt = """i gave u a image and some text of a online post i want you to extract some data from it and send it in a particular format.
    You have to extract 
    {
        "query":string (finds important points from the post like productName,productCatogory[like electronic etc],productColor,productSize,productVolume if presents),
        "brand":string (the brand if present),
        "price-range":string (the price-range like '1000-2000' if present)
    }
    eg.:
        {
            "query":"Apple Iphone 16 pro case, Phone Case,Transperent",
            "brand":"",
            "price-range":""
        };

    You are only allowed to response in the above formate if anyfield is found just response with {... , <field>:"", ...};
    """
