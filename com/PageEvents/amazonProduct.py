import config
from Utilities.myLogger import logger
import sys


class AmazonProduct():
    ItemTitle = None
    Price = None
    Description = None
    BoxContains = None
    Dimensions = None
    ProductWeight = None
    ShippingWeight = None
    ImageURL1 = ''
    ImageURL2 = ''
    ImageURL3 = ''
    ImageURL4 = ''
    ASIN = None
    AmazonURL = None

    EbayProdWtKg = None
    EbayProdWtGram = None
    EbayShipWtKg = None
    EbayShipWtGram = None
    EbaySalesPrice = None
    EbayHeight = None
    EbayLength = None
    EbayWidth = None

    def do_price_manipulations(self):
        AmazonPriceModified = float(self.Price) / 1.2
        ShippingCostCalculated = (self.EbayShipWtKg + float(self.EbayShipWtGram)/1000) * 4
        self.EbaySalesPrice = AmazonPriceModified + ShippingCostCalculated
        if 'amazon.co.uk' in self.AmazonURL:
            self.EbaySalesPrice *= 2.5
        elif 'amazon.com' in self.AmazonURL:
            self.EbaySalesPrice *= 1.5
        self.EbaySalesPrice = round(self.EbaySalesPrice, 2)

    def do_weight_manipulations(self):
        from Utilities import UtilityMethods
        if 'amazon.com' in self.AmazonURL:
            if 'pound' in self.ProductWeight:
                tempWeightInKg = UtilityMethods.convert_pounds_to_kgs(self.ProductWeight)
                self.EbayProdWtKg = int(tempWeightInKg)
                self.EbayProdWtGram = int((tempWeightInKg * 1000) % 1000)
            elif 'ounce' in self.ProductWeight:
                tempWeightInKg = UtilityMethods.convert_ounces_to_kgs(self.ProductWeight)
                self.EbayProdWtKg = int(tempWeightInKg)
                self.EbayProdWtGram = int((tempWeightInKg * 1000) % 1000)
            if 'pound' in self.ShippingWeight:
                tempWeightInKg = UtilityMethods.convert_pounds_to_kgs(self.ShippingWeight)
                self.EbayShipWtKg = int(tempWeightInKg)
                self.EbayShipWtGram = int((tempWeightInKg * 1000) % 1000)
            elif 'ounce' in self.ShippingWeight:
                tempWeightInKg = UtilityMethods.convert_ounces_to_kgs(self.ShippingWeight)
                self.EbayShipWtKg = int(tempWeightInKg)
                self.EbayShipWtGram = int((tempWeightInKg * 1000) % 1000)
        elif 'amazon.co.uk' in self.AmazonURL:
            if 'Kg' in self.ProductWeight:
                tempWeightInKg = self.ProductWeight.strip()
                tempWeightInKg = tempWeightInKg[:tempWeightInKg.index(' ')]
                tempWeightInKg = float(tempWeightInKg)
                self.EbayProdWtKg = int(tempWeightInKg)
                self.EbayProdWtGram = int((tempWeightInKg * 1000) % 1000)
            elif 'g' in self.ProductWeight:
                tempWeightInKg = self.ProductWeight.strip()
                tempWeightInKg = tempWeightInKg[:tempWeightInKg.index(' ')]
                tempWeightInKg = int(tempWeightInKg)
                self.EbayProdWtKg = 0
                self.EbayProdWtGram = tempWeightInKg
            if 'Kg' in self.ShippingWeight:
                tempWeightInKg = self.ShippingWeight.strip()
                tempWeightInKg = tempWeightInKg[:tempWeightInKg.index(' ')]
                tempWeightInKg = float(tempWeightInKg)
                self.EbayShipWtKg = int(tempWeightInKg)
                self.EbayShipWtGram = int((tempWeightInKg * 1000) % 1000)
            elif 'g' in self.ShippingWeight:
                tempWeightInKg = self.ShippingWeight.strip()
                tempWeightInKg = tempWeightInKg[:tempWeightInKg.index(' ')]
                tempWeightInKg = int(tempWeightInKg)
                self.EbayShipWtKg = 0
                self.EbayShipWtGram = tempWeightInKg

    def do_dimensions_manipulations(self):
        if 'amazon.com' in self.AmazonURL:
            try:
                Dimensions = self.Dimensions
                temp = Dimensions[:Dimensions.index('x')]
                temp = float(temp.strip())
                temp *= 2.54
                self.EbayHeight = round(temp, 2)

                Dimensions = Dimensions[Dimensions.index('x')+1:]
                temp = Dimensions[:Dimensions.index('x')]
                temp = float(temp.strip())
                temp *= 2.54
                self.EbayLength = round(temp, 2)

                Dimensions = Dimensions[Dimensions.index('x')+1:]
                temp = Dimensions[:Dimensions.rindex(' ')]
                temp = float(temp.strip())
                temp *= 2.54
                self.EbayWidth = round(temp, 2)
            except:
                pass
        elif 'amazon.co.uk' in self.AmazonURL:
            try:
                Dimensions = self.Dimensions
                temp = Dimensions[:Dimensions.index('x')]
                temp = float(temp.strip())
                self.EbayHeight = round(temp, 2)

                Dimensions = Dimensions[Dimensions.index('x')+1:]
                temp = Dimensions[:Dimensions.index('x')]
                temp = float(temp.strip())
                self.EbayLength = round(temp, 2)

                Dimensions = Dimensions[Dimensions.index('x')+1:]
                temp = Dimensions[:Dimensions.rindex(' ')]
                temp = float(temp.strip())
                self.EbayWidth = round(temp, 2)
            except:
                pass


def scrape_all_products():
    import AmazonUKScrape
    import AmazonUSScrape
    for URL in config.amazonURLS:
        print URL
        try:
            if 'amazon.co.uk' in URL:
                currProduct = AmazonUKScrape.scrape_UK_URL(URL)
                config.amazonProducts.append(currProduct)
            elif 'amazon.com' in URL:
                currProduct = AmazonUSScrape.scrape_US_URL(URL)
                config.amazonProducts.append(currProduct)
        except:
            logger.exception(sys.exc_info())


def do_field_manipulations():
    for prod in config.amazonProducts:
        prod.do_weight_manipulations()
        prod.do_price_manipulations()
        prod.do_dimensions_manipulations()
