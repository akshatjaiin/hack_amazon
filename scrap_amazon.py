import requests
from bs4  import BeautifulSoup
_HEADER:dict = {
    'User-Agent':"Mozilla/5.0 (X11; Linuin zipx x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    'Accept-Language': 'en-US, en;q=0.5',
};

def amazon_scrapper(**args)->None:
    url:str ="https://www.amazon.com/s?" ;
    if("productName" in args):url+="&k="+args["productName"];
    if("productType" in args):url+="&i="+args["productType"];
    if("brand" in args):url+="&rh=p_89:="+args["brand"];
    if("priceRange" in args):url+="&rh=p_36:="+args["priceRange"];

    data = requests.get(url,headers=_HEADER);
    soup = BeautifulSoup(data.content,"html.parser");
    titles = list(map( lambda x:x.find("h2").find("span").string , soup.find_all("div",attrs={
        "data-cy":"title-recipe",
    }) ));
    links = list(map( lambda x:"https://www.amazon.com"+x.find("a").get("href"), soup.find_all("span",attrs={
        "data-component-type":"s-product-image",
    }) ));
    reviews = list(map(lambda x:x.find("span",attrs={"class":"a-icon-alt"}).string,soup.find_all("div",attrs={
        "data-cy":"reviews-block"
    })));
    prices = list(map(lambda x:x.find("span",attrs={"class":"a-offscreen"}).string,soup.find_all("div",attrs={
        "data-cy":"price-recipe"
    })));
    images = soup.find_all("img",attrs={
        "class":"s-image"
    });
    print("URL: ",url);
    return {
        "titles":titles,
        "reviews":reviews,
        "prices":prices,
        "images":images,
        "links":links
    }


if __name__ == "__main__":
    data = amazon_scrapper(productName="iPhone16Pro");
