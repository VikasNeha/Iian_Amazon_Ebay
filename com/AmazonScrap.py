from Utilities import UtilityMethods
import config
from PageEvents import amazonProduct
from selenium import webdriver


# for prod in config.amazonProducts:
#     print "----------------------"
#     print prod.ItemTitle
#     print prod.Price
#     print prod.Description
#     print prod.BoxContains
#     print prod.Dimensions
#     print prod.ProductWeight
#     print prod.ShippingWeight
#     print prod.ImageURLs
#     print prod.ASIN
#     print prod.AmazonURL
#     print "\n"


def setup_driver():
    dcap = dict(webdriver.DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36")
    service_args = ['--load-images=false', '--proxy-type=none', '--ignore-ssl-errors=true']
    phantomBinary = config.get_main_dir() + "\\Resources\\phantomjs.exe"
    config.driver = webdriver.PhantomJS(
        executable_path=phantomBinary, service_args=service_args, desired_capabilities=dcap)


UtilityMethods.readURLs()
setup_driver()
amazonProduct.scrape_all_products()
amazonProduct.do_field_manipulations()
UtilityMethods.write_csv_output()
if config.driver:
    config.driver.quit()