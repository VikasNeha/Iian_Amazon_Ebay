from Utilities import UtilityMethods
from PageEvents.amazonProduct import AmazonProduct


def scrape_US_URL(ProductURL):
    soup = UtilityMethods.make_soup(ProductURL)
    # print soup
    currProduct = AmazonProduct()
    currProduct.ItemTitle = get_item_title(soup)
    currProduct.Description = get_item_description(soup)
    currProduct.BoxContains = get_box_contains(soup)
    currProduct.Price = get_price(soup)
    currProduct.Dimensions = get_dimensions(soup)
    currProduct.ProductWeight = get_item_weight(soup)
    currProduct.ShippingWeight = get_shipping_weight(soup)
    imgURLS = get_image_urls(soup)
    try:
        currProduct.ImageURL1 = imgURLS[0]
        currProduct.ImageURL2 = imgURLS[1]
        currProduct.ImageURL3 = imgURLS[2]
        currProduct.ImageURL4 = imgURLS[3]
    except IndexError:
        pass
    currProduct.ASIN = get_ASIN(soup)
    currProduct.AmazonURL = ProductURL
    return currProduct


def get_item_title(soup):
    itemTitle = soup.find("h1", id="title")
    if itemTitle:
        return itemTitle.text.strip()
    itemTitle = soup.find("span", id="btAsinTitle")
    return itemTitle.text.strip()


def get_item_description(soup):
    itemDescription = soup.find("div", id="productDescription")
    seeAll = itemDescription.find("div", class_="seeAll")
    if seeAll:
        soupDesc = UtilityMethods.make_soup(seeAll.a["href"])
        return get_exact_item_description(soupDesc)
    else:
        return get_exact_item_description(soup)


def get_exact_item_description(soup):
    itemDescription = soup.find("div", id="productDescription")
    itemDescription = itemDescription.find("div", class_="content")
    tags = itemDescription.descendants

    containsImage = False
    for tag in tags:
        if tag.name is not None:
            if 'aplus' in str(tag.get("class")):
                containsImage = True
                break

    if containsImage:
        description = ''
        itemDescription = itemDescription.find("div", class_="aplus")
        tags = itemDescription.contents
        multipleCols = False
        for tag in tags:
            if tag.name:
                if 'col' in str(tag.get("class")):
                    multipleCols = True
                    break
        if multipleCols:
            tags = []
            cols = itemDescription.descendants
            for col in cols:
                if col.name:
                    # colTags = col.contents
                    # for colTag in colTags:
                    tags.append(col)
        for tag in tags:
            if tag.name:
                if tag.name in ['p', 'ul', 'strong'] or 'h' in tag.name:
                    tagString = tag.text.encode('ascii', 'ignore')
                    description += tagString.strip() + "<br><br>"
        return description.strip()
    else:
        tags = itemDescription.contents
        description = ''
        skipNext = False
        for tag in tags:
            if tag.name is not None:
                tagString = tag.text.encode('ascii', 'ignore')
                if 'Box Contains' in tagString:
                    skipNext = True
                    continue
                if skipNext:
                    skipNext = False
                    continue
                description += tagString.strip() + "<br><br>"
        return description.strip()


def get_box_contains(soup):
    itemDescription = soup.find("div", id="productDescription")
    seeAll = itemDescription.find("div", class_="seeAll")
    if seeAll:
        soup = UtilityMethods.make_soup(seeAll.a["href"])
    itemDescription = soup.find("div", id="productDescription")
    itemDescription = itemDescription.find("div", class_="content")

    tags = itemDescription.contents
    found = False
    boxContains = ''
    for tag in tags:
        if tag.name is not None:
            tagString = tag.text.encode('ascii', 'ignore')
            if found:
                subTags = tag.contents
                for subTag in subTags:
                    if subTag.name is None:
                        boxContains += str(subTag.string).strip() + "<br><br>"
                return boxContains.strip()
            if 'Box Contains' in tagString:
                found = True
    return ''


def get_price(soup):
    price = soup.find("span", id="priceblock_ourprice")
    price = price.text.strip()
    price = price[1:]
    price = round(float(price), 2)
    return price


def get_dimensions(soup):
    div_details = soup.find("div", id="detail-bullets")
    if div_details:
        lis = div_details.find_all("li")
        for li in lis:
            if 'Product Dimensions' in li.text:
                tags = li.contents
                for tag in tags:
                    if tag.name is None:
                        tagString = tag.string.strip()
                        if ';' in tagString:
                            tagString = tagString[:tagString.index(';')]
                        return tagString.strip()
    else:
        td = soup.find("td", text="Product Dimensions")
        try:
            return td.next_sibling.text
        except:
            return ''
    return ''


def get_item_weight(soup):
    div_details = soup.find("div", id="detail-bullets")
    if div_details:
        lis = div_details.find_all("li")
        for li in lis:
            if 'Product Dimensions' in li.text:
                tags = li.contents
                for tag in tags:
                    if tag.name is None:
                        tagString = tag.string.strip()
                        if ';' in tagString:
                            tagString = tagString[tagString.index(';') + 1:]
                        return tagString.strip()
    else:
        td = soup.find("td", text="Item Weight")
        try:
            return td.next_sibling.text
        except:
            return ''
    return ''


def get_shipping_weight(soup):
    div_details = soup.find("div", id="detail-bullets")
    if div_details:
        lis = div_details.find_all("li")
        for li in lis:
            if 'Shipping Weight' in li.text:
                tags = li.contents
                for tag in tags:
                    if tag.name is None:
                        tagString = tag.string.strip()
                        return tagString.rstrip('(')
    else:
        td = soup.find("td", text="Shipping Weight")
        try:
            return td.next_sibling.text
        except:
            return ''
    return ''


def get_image_urls(soup):
    thumbs_images = soup.find("div", id="thumbs-image")
    imgs = thumbs_images.find_all("img")
    if len(imgs) > 4:
        imgs = imgs[:4]
    imgURLs = []
    for img in imgs:
        imgURL = img.get("src")
        while True:
            if imgURL.rindex("/") > imgURL.rindex("."):
                break
            imgURL = imgURL[:imgURL.rindex(".")]
        imgURL += ".SS400.jpg"
        imgURLs.append(imgURL)
    return imgURLs


def get_ASIN(soup):
    div_details = soup.find("div", id="detail-bullets")
    if div_details:
        lis = div_details.find_all("li")
        for li in lis:
            if 'ASIN' in li.text:
                tags = li.contents
                for tag in tags:
                    if tag.name is None:
                        tagString = tag.string.strip()
                        return tagString.strip()
    else:
        td = soup.find("td", text="ASIN")
        try:
            return td.next_sibling.text
        except:
            return ''
    return ''