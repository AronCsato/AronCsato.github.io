from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import math
import numpy as np
import collections


class Web_Search:
    def __init__(self,address,price_class,product_name_class,address_class) -> None:
        self.address = address
        self.price_class = price_class
        self.product_name_class = product_name_class
        self.address_class = address_class

    def init_driver(self,driver_typ,opts)->None:
        try:
            if driver_typ=="chrome":
                opts = webdriver.ChromeOptions()
                # opts.add_argument('--headless')
                opts.add_experimental_option("useAutomationExtension", False)
                opts.add_experimental_option("excludeSwitches", ['enable-automation']) 
                # opts.add_argument("--disable-extensions")
                # opts.add_argument("--disable-popup-blocking")
                # opts.add_argument("--profile-directory=Default")
                # opts.add_argument("--ignore-certificate-errors")
                # opts.add_argument("--disable-plugins-discovery")
                # opts.add_argument("--incognito")
                # opts.add_argument("user_agent=DN")
                opts.add_argument("--user-data-dir=C:\\Users\\PC\\AppData\\Local\\Google\\Chrome\\User Data")
                self.driver = webdriver.Chrome(opts)
                # self.driver.delete_all_cookies()
            elif driver_typ=="edge":
                opts = webdriver.EdgeOptions()
                opts.add_experimental_option("useAutomationExtension", False)
                opts.add_experimental_option("excludeSwitches", ['enable-automation']) 
                self.driver = webdriver.Edge(opts)
        except Exception as error:
            print("Not correct browser type.\n",error)

    def login_with_user(self,login_pg,user,password):
        self.login_pg = login_pg
        self.user = user
        self.password = password

    def find_product(self,product_code)->None:
        self.product_code = product_code

    def print_prices_prd_name(self,prod_names,prod_prices,address)->None:
        pass

    def find_low_price(self,prod_prices)->int:
        pass

    def create_table_elements(self,prod_names,prod_prices,address):
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
        prices_temp,prod_name_temp,address_temp = self.create_table_elements(prices,prod_name,address)

        return prices_temp,prod_name_temp,address_temp
    
    def filter_prod_name(self,prod_names):
        for prod_name in prod_names:
            if ("Producator" not in prod_name.text):
                prod_names.remove(prod_name)
        return prod_names
    
    def create_table_elements(self,prod_prices,prod_names, address):
        super().create_table_elements(prod_names, prod_prices, address)
        prices = []
        prod_name = []
        prod_address = []
        for i in range(0,len(prod_prices)):
            prices.append(prod_prices[i].text.split("Lei",1)[1].lstrip("\n"))
            prod_name.append(prod_names[i].text)
            prod_address.append(address[i].get_attribute('href'))
        return prices,prod_name,prod_address

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
            temp_list.append([int(i) for i in (prod_prices[j]).split() if i.isdigit()])
        return temp_list.index(min(temp_list))
    

class Unix(Web_Search):
    def __init__(self, address, price_class, product_name_class, address_class) -> None:
        super().__init__(address, price_class, product_name_class, address_class)

    def init_driver(self, driver_typ, opts) -> None:
        super().init_driver(driver_typ, opts)
    
    def find_product(self, product_code):
        super().find_product(product_code)
        self.driver.get(self.address+product_code)
        time.sleep(10)
        scroll, one_page_height, nr_of_scrolls = self.get_scrollable_object()
        prices = []
        prod_name = []
        address = []
        for i in range(1,nr_of_scrolls):
            prices_temp,prod_name_temp,address_temp = self.create_table_elements(self.driver.find_elements(By.CLASS_NAME,self.price_class),self.driver.find_elements(By.CLASS_NAME,self.product_name_class),self.driver.find_elements(By.CLASS_NAME,self.address_class)) 
            prices.append(prices_temp)
            prod_name.append(prod_name_temp)
            address.append(address_temp)
            self.driver.execute_script("arguments[0].scrollTop = {}".format(i*one_page_height), scroll)

        prices = self.flatten_arrays(np.asarray(prices))
        prod_name = self.flatten_arrays(np.asarray(prod_name))
        address = self.flatten_arrays(np.asarray(address))
        prices,prod_name,address =self.delete_duplicates(prices,prod_name,address)
        return  prices,prod_name,address
        
    
    def create_table_elements(self, prod_prices,prod_names, address):
        super().create_table_elements(prod_names, prod_prices, address)
        prices = []
        prod_name = []
        prod_address = []
        address = self.create_address(address)
        for i in range(0,len(prod_prices)):
            prices.append(prod_prices[i].text.split(" ", 1)[0])
            prod_name.append(prod_names[i].text)
            prod_address.append(address[i])
        return prices,prod_name,prod_address

    def delete_duplicates(self,prod_prices,prod_names, address):
        unique_elements, indices = np.unique(address, return_index=True)
        prod_price_temp = [prod_prices[i] for i in indices]
        prod_names_temp = [prod_names[i] for i in indices]
        address_temp = [address[i] for i in indices]
        return prod_price_temp,prod_names_temp,address_temp


    def flatten_arrays(self,array):
        temp_array =  [item for sublist in array for item in sublist]
        return temp_array


    def get_scrollable_object(self):
        scroll = self.driver.find_element(By.CSS_SELECTOR,'.without-focus-style:nth-child(1) .app-mixed-size-virtual-scroll-viewport') 
        max_height = self.driver.execute_script("return arguments[0].scrollHeight", scroll)
        one_page_height = scroll.size['height']
        nr_of_scrolls_needed = math.ceil(max_height/one_page_height)
        return scroll,one_page_height,nr_of_scrolls_needed

    def login_with_user(self, login_pg, user, password):
        super().login_with_user(login_pg, user, password)
        self.driver.get(login_pg)
        user_name = self.driver.find_element(By.ID,'login-username')
        pass_word = self.driver.find_element(By.ID,'login-password')
        login_btn = self.driver.find_elements(By.CLASS_NAME,'col-12.pb-2.col-md-6')
        user_name.send_keys(self.user)
        time.sleep(10)
        pass_word.send_keys(self.password)
        time.sleep(10)
        login_btn = login_btn[1]
        time.sleep(3)
        login_btn.click()

    def filter_prod_name(self,prod_names):
        for prod_name in prod_names:
            if ("Producator" not in prod_name.text):
                prod_names.remove(prod_name)
        return prod_names
    
    def create_address(self,address):
        addres=[]
        link_for_part = "https://www.unixauto.ro/webshop/termek-adatlap/"
        for i in range(0,len(address)):
            addres.append(link_for_part + address[i].text.split(" ", 2)[2].split("\n", 1)[0])
        return addres

    def print_prices_prd_name(self, prod_names, prod_prices, address) -> None:
        super().print_prices_prd_name(prod_names, prod_prices,address)
        for i in range(0,len(prod_prices)):
            print(prod_names[i].text)
            print(prod_prices[i].text.split(" ", 1)[0])
            print(address[i])

    def find_low_price(self, prod_prices) -> int:
        super().find_low_price(prod_prices)
        temp_list = []
        for j in range(0,len(prod_prices)):
            temp_list.append(float(prod_prices[j].text.split(" ", 1)[0].replace(",",".")))
        return temp_list.index(min(temp_list))
    
def main(part_code):
    episa = Episa("https://www.epiesa.ro/cautare-piesa/?find=","bricolaje-bottom-text","sub-product-detail","product-auto-title")
    episa.init_driver("chrome",())
    price, product, address = episa.find_product(part_code)
    min_index = episa.find_low_price(price)
    # unix = Unix("https://www.unixauto.ro/webshop/cikklista?cSearch=","price__amount--single","product-data--title--text","product-id")
    # unix.init_driver("chrome",())
    return price,product, address, min_index
    # part_code = "4m0819439"
    # price, product, address = unix.find_product(part_code)
    
    
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

# table = self.driver.find_element(By.CSS_SELECTOR,'.table-columns-and-body.d-flex.flex-column.flex-grow-1.position-relative.min-height-0')
# scroll = self.driver.find_element(By.CSS_SELECTOR,'.without-focus-style:nth-child(1) .app-mixed-size-virtual-scroll-viewport')
# self.driver.execute_script("aruments[0].scrollintoView();",scroll)
# self.driver.execute_script("arguments[0].scroll(0, arguments[0].scrollHeight);",scroll) ### ez mukodik
# last_height = self.driver.execute_script("return arguments[0].scrollHeight", scroll)
# self.driver.execute_script("arguments[0].scrollTop = {}".format(Y), scroll) # ez is mukodik