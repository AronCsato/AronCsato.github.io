from selenium import webdriver
from selenium.webdriver.common.by import By

class Web_Search:
    def __init__(self,address,price_class,product_name_class,address_class) -> None:
        self.address = address
        self.price_class = price_class
        self.product_name_class = product_name_class
        self.address_class = address_class

    def init_driver(self,driver_typ,opts)->None:
        try:
            if driver_typ=="chrome":
                self.driver = webdriver.Chrome()
            elif driver_typ=="edge":
                self.driver = webdriver.Edge()
        except Exception as error:
            print("Not correct browser type.\n",error)

    def find_product(self,product_code)->None:
        self.product_code = product_code

    def print_prices_prd_name(self,prod_names,prod_prices,address)->None:
        pass

    def find_low_price(self,prod_prices)->int:
        pass
    

class Episa(Web_Search):
    def __init__(self, address, price_class, product_name_class, address_class) -> None:
        super().__init__(address, price_class, product_name_class, address_class)

    def init_driver(self, driver_typ, opts) -> None:
        super().init_driver(driver_typ, opts)
    
    def find_product(self, product_code):
        super().find_product(product_code)
        self.driver.get(self.address+product_code)
        prices = self.driver.find_elements(By.CLASS_NAME,self.price_class)
        prod_name= self.driver.find_elements(By.CLASS_NAME,self.product_name_class)
        address = self.driver.find_elements("xpath","//div[@class='{}']/a".format(self.address_class))
        prod_name = self.filter_prod_name(prod_name)
        return prices,prod_name,address
    
    def filter_prod_name(slef,prod_names):
        for prod_name in prod_names:
            if ("Producator" not in prod_name.text):
                prod_names.remove(prod_name)
        return prod_names

    def print_prices_prd_name(self, prod_names, prod_prices, address) -> None:
        super().print_prices_prd_name(prod_names, prod_prices,address)
        for i in range(0,len(prod_prices)):
            print(prod_names[i].text)
            print(prod_prices[i].text.split("Lei",1)[1],end='\n')
            print(address[i].get_attribute('href'))

    def find_low_price(self, prod_prices) -> int:
        super().find_low_price(prod_prices)
        temp_list = []
        for j in range(0,len(prod_prices)):
            temp_list.append([int(i) for i in (prod_prices[j].text.split("Lei",1)[1]).split() if i.isdigit()])
        return temp_list.index(min(temp_list))
    
def main(part_code):
    episa = Episa("https://www.epiesa.ro/cautare-piesa/?find=","bricolaje-bottom-text","sub-product-detail","product-auto-title")
    episa.init_driver("chrome",())
    part_code = "4m0819439"
    price, product, address = episa.find_product(part_code)
    min_index = episa.find_low_price(price)
    return price,product, address, min_index
    
if __name__ == "__main__":
    part_code = "4m0819439"
    main(part_code)
#     episa = Episa("https://www.epiesa.ro/cautare-piesa/?find=","bricolaje-bottom-text","sub-product-detail","product-auto-title")
#     episa.init_driver("chrome",())
#     #Introduce the part code
#     # part_code = input("Alkatresz kod:\n")
#     part_code = "4m0819439"
#     price, product, address = episa.find_product(part_code)
#     episa.print_prices_prd_name(product,price,address)
#     # for adres in address:
    #     print(adres.)




# opts = webdriver.ChromeOptions()
# # The below line will make your browser run in background when uncommented
# # opts.add_argument('--headless')
    
# driver = webdriver.Chrome()

# driver.get("https://www.epiesa.ro/cautare-piesa/?find={}".format(part_code))

# prices = driver.find_elements(By.CLASS_NAME,"bricolaje-bottom-text")
# prod_name= driver.find_elements(By.CLASS_NAME,"sub-product-detail")



# for price in prices:
#     print(price.text)
# driver.quit()