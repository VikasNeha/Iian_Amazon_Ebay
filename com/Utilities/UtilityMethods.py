import config
from bs4 import BeautifulSoup
from urllib2 import urlopen
import csv


def readURLs():
    fileName = 'Resources\AmazonProductURLs.txt'
    f = open(config.get_main_dir() + "\\" + fileName)
    for line in f.readlines():
        config.amazonURLS.append(line.rstrip('\n'))
    f.close()


def make_soup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html, "html5lib")


def convert_pounds_to_kgs(weight_in_pound):
    tempWeight = weight_in_pound.strip()
    tempWeight = tempWeight[:tempWeight.index(' ')]
    tempWeight = float(tempWeight)
    tempWeight = round(tempWeight * 0.453592, 2)
    return tempWeight


def convert_ounces_to_kgs(weight_in_ounce):
    tempWeight = weight_in_ounce.strip()
    tempWeight = tempWeight[:tempWeight.index(' ')]
    tempWeight = float(tempWeight)
    tempWeight = round(tempWeight * 0.0283495, 2)
    return tempWeight


def write_csv_output():
    fileName = 'Output\Scrape_output.csv'
    ofile = open(config.get_main_dir() + "\\" + fileName, "wb")
    csv_writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

    csv_writer.writerow([
        "Action(SiteID=Australia|Country=AU|Currency=AUD|Version=585|CC=ISO-8859-1)", "*Category", "*ConditionID",
        "StoreCategory", "*Title", "picURL", "*Quantity", "*Format", "*StartPrice", "BuyItNowPrice", "*Duration",
        "ImmediatePayRequired", "BestOfferEnabled", "AutoAcceptEnabled",
        "BestOfferAutoAcceptPrice", "MinimumBestOfferPrice", "GalleryType", "BoldTitle",
        "Subtitle", "IncludeSubTitleInSearch", "Featured", "Highlight", "Region", "*Location", "PayPalAccepted",
        "PayPalEmailAddress", "PaymentInstructions", "DomesticInsuranceOption", "DomesticInsuranceFee",
        "InternationalInsuranceOption", "InternationalInsuranceFee", "ShippingService-1:Option",
        "ShippingService-1:Cost", "ShippingService-1:AdditionalCost", "ShippingService-1:Priority",
        "ShippingService-2:Option", "ShippingService-2:Cost", "ShippingService-2:AdditionalCost",
        "ShippingService-2:Priority", "ShippingService-3:Option", "ShippingService-3:Cost",
        "ShippingService-3:AdditionalCost", "ShippingService-3:Priority", "DispatchTimeMax", "GetItFast",
        "ReturnsAcceptedOption", "RefundOption", "ReturnsWithinOption", "ShippingCostPaidBy", "*ShippingType",
        "*OriginatingPostalCode", "*PackageLength", "*PackageDepth", "*PackageWidth",
        "*WeightMajor", "*WeightMinor", "*Description"])

    for prod in config.amazonProducts:
        html_desc_fileName = 'Resources\desc_html.html'
        html_ifile = open(config.get_main_dir() + "\\" + html_desc_fileName, "r")
        html_desc = html_ifile.read()
        html_ifile.close()
        html_desc = html_desc.replace("**TITLE**", prod.ItemTitle)
        html_desc = html_desc.replace("**DESCRIPTION**", prod.Description)
        html_desc = html_desc.replace("**IMAGE1**", prod.ImageURL1)
        html_desc = html_desc.replace("**IMAGE2**", prod.ImageURL2)
        html_desc = html_desc.replace("**IMAGE3**", prod.ImageURL3)
        html_desc = html_desc.replace("**IMAGE4**", prod.ImageURL4)
        csv_writer.writerow([
            "Add", "105965", "1000",
            "1", prod.ItemTitle, prod.ImageURL1, "5", "StoresFixedPrice", prod.EbaySalesPrice, "", "30",
            "0", "0", "",
            "", "", "", "0",
            "0", "0", "0", "0", "", "Sydney, NSW", "1",
            "test@gmail.com", "", "NotOffered", "",
            "NotOffered", "", "AU_Regular",
            "", "", "1",
            "AU_Express", "", "",
            "2", "", "",
            "", "", "4", "0",
            "ReturnsAccepted", "MoneyBack", "Days_7", "Buyer", "Calculated",
            "2000", prod.EbayLength, prod.EbayHeight, prod.EbayWidth,
            prod.EbayProdWtKg, prod.EbayProdWtGram, html_desc
        ])
    ofile.close()