from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import math
import numpy as np
import collections
import pyautogui
import sys


class Web_Search:
    _instance = None

    def __init__(self,address,price_class,product_name_class,address_class) -> None:
        self.address = address
        self.price_class = price_class
        self.product_name_class = product_name_class
        self.address_class = address_class

    @staticmethod
    def init_driver(driver_typ,opts):
        try:
            if Web_Search._instance is None:
                if driver_typ=="chrome":
                    opts = webdriver.ChromeOptions()
                    # opts.add_argument('--headless')
                    opts.add_experimental_option("useAutomationExtension", False)
                    opts.add_experimental_option("excludeSwitches", ['enable-automation']) 
                    opts.add_argument("--disable-extensions")
                    opts.add_argument("--disable-popup-blocking")
                    opts.add_argument("--profile-directory=Default")
                    opts.add_argument("--ignore-certificate-errors")
                    opts.add_argument("--disable-plugins-discovery")
                    # opts.add_argument("--incognito")
                    # opts.add_argument("user_agent=DN")
                    opts.add_argument("--user-data-dir=C:\\Users\\PC\\AppData\\Local\\Google\\Chrome\\User Data")
                    # driver.get('https://www.google.ro/')
                    # driver.delete_all_cookies()
                    # driver.get("chrome://settings/clearBrowserData")
                    # driver.switchTo().activeElement()
                    # driver.findElement(By.cssSelector("* /deep/ #clearBrowsingDataConfirm")).click()
                    Web_Search._instance = webdriver.Chrome(opts)
                elif driver_typ=="edge":
                    opts = webdriver.EdgeOptions()
                    opts.add_experimental_option("useAutomationExtension", False)
                    opts.add_experimental_option("excludeSwitches", ['enable-automation']) 
                    Web_Search._instance = webdriver.Edge(opts)
            return  Web_Search._instance
        except Exception as error:
            print("Not correct browser type.\n",error)
    

    def login_with_user(self,login_pg,user,password):
        self.login_pg = login_pg
        self.user = user
        self.password = password

    def close_all_open_tabs(self):
        if Web_Search._instance:
            for i in range(1,len(Web_Search._instance.window_handles)):
                Web_Search._instance.switch_to.window(Web_Search._instance.window_handles[i])
                Web_Search._instance.close()

    def input_in_search_bar(self,product_code,input_bar,input_bar_search):
        input = self.wait_for_element(input_bar_search,input_bar)
        input[0].send_keys(product_code)
        input[0].send_keys(Keys.RETURN)
        

    def new_tab(self)->None:
        if Web_Search._instance:
            # Open a new tab
            Web_Search._instance.execute_script("window.open('');")
            # Switch to the new tab
            Web_Search._instance.switch_to.window(Web_Search._instance.window_handles[len(Web_Search._instance.window_handles)-1])
        else:
            print("The browsre is not initialized")
            sys.exit()
        

    def find_product(self,product_code)->None:
        self.product_code = product_code

    def print_prices_prd_name(self,prod_names,prod_prices,address)->None:
        pass

    def find_low_price(self,prod_prices)->int:
        pass

    def create_table_elements(self,prod_names,prod_prices,address):
        pass

    def close_webdriver(self):
        Web_Search._instance.quit()

    def wait_for_element(self,search_by,elem_name):
        try:
            elem = WebDriverWait(Web_Search._instance, 30).until(EC.presence_of_all_elements_located((search_by, elem_name)))
            return elem
        except:
            print("Loading time out")
        

class Episa(Web_Search):
    def __init__(self, address, price_class, product_name_class, address_class) -> None:
        super().__init__(address, price_class, product_name_class, address_class)
        self.driver = Web_Search.init_driver("chrome",())

    def input_in_search_bar(self,product_code):
        elem = self.wait_for_element(By.XPATH,"//*[@name='find']")
        elem[1].send_keys(product_code)
        elem[1].send_keys(Keys.RETURN)

    def find_product(self, product_code):
        super().find_product(product_code)
        # driver.get(self.address+product_code)
        self.driver.get(self.address)
        self.input_in_search_bar(product_code)
        prices = self.wait_for_element(By.CLASS_NAME,self.price_class)
        prod_name= self.wait_for_element(By.CLASS_NAME,self.product_name_class)
        address = self.wait_for_element("xpath","//div[@class='{}']/a".format(self.address_class))
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
            prices.append(prod_prices[i].text.split("Lei",1)[0].split(" ",1)[0])
            prod_name.append(prod_names[i].text.split("Producator: ",1)[1].split("\n")[0])
            prod_address.append(address[i].get_attribute('href'))
        return prices,prod_name,prod_address

    def print_prices_prd_name(self, prod_names, prod_prices, address) -> None:
        super().print_prices_prd_name(prod_names, prod_prices,address)
        for i in range(0,len(prod_prices)):
            print(prod_names[i].text.split("Producator:",1)[1],end='\n')
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
        self.driver = Web_Search.init_driver("chrome",())


    def input_in_search_bar(self,product_code):
        input = self.wait_for_element(By.ID,"header-search-box")
        if len(input) ==0:
            input = self.wait_for_element(By.ID,"aside-nav-search-box")
        input[0].send_keys(product_code)
        input[0].send_keys(Keys.RETURN)
        input[0].send_keys(Keys.RETURN)


    
    def find_product(self, product_code):
        super().find_product(product_code)
        # driver.get(self.address+product_code)
        self.input_in_search_bar(product_code)
        scroll, one_page_height, nr_of_scrolls = self.get_scrollable_object()
        prices = []
        prod_name = []
        address = []
        for i in range(1,nr_of_scrolls):
            price = self.wait_for_element(By.CLASS_NAME,self.price_class)
            prod = self.wait_for_element(By.CLASS_NAME,self.product_name_class)
            addres = self.wait_for_element(By.CLASS_NAME,self.address_class)
            prices_temp,prod_name_temp,address_temp = self.create_table_elements(price,prod,addres) 
            prices.append(prices_temp)
            prod_name.append(prod_name_temp)
            address.append(address_temp)
            self.driver.execute_script("arguments[0].scrollTop = {}".format(i*one_page_height), scroll)

        prices = self.flatten_arrays(prices)
        prod_name = self.flatten_arrays(prod_name)
        address = self.flatten_arrays((address))
        prices,prod_name,address =self.delete_duplicates(prices,prod_name,address)
        return  prices,prod_name,address
        
    
    def create_table_elements(self, prod_prices,prod_names, address):
        super().create_table_elements(prod_names, prod_prices, address)
        prices = []
        prod_name = []
        prod_address = []
        address = self.create_address(address)
        
        for i in range(0,min(len(prod_prices),len(prod_names),len(address))):
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
        # scroll = driver.find_element(By.CSS_SELECTOR,'.without-focus-style:nth-child(1) .app-mixed-size-virtual-scroll-viewport') 
        scroll = self.wait_for_element(By.CLASS_NAME,'app-mixed-size-virtual-scroll-viewport')
        max_height = self.driver.execute_script("return arguments[0].scrollHeight", scroll[0])
        one_page_height = scroll[0].size['height']
        nr_of_scrolls_needed = math.ceil(max_height/one_page_height)
        return scroll[0],one_page_height,nr_of_scrolls_needed


    def login_with_user(self, login_pg, user, password):
        super().login_with_user(login_pg, user, password)
        self.driver.get(login_pg)
        # user_name = driver.find_element(By.ID,'login-username')
        # pass_word = driver.find_element(By.ID,'login-password')
        # login_btn = self.wait_for_element(By.CLASS_NAME,'button__key-command')
        # user_name.send_keys(self.user)
        # time.sleep(10)
        # pass_word.send_keys(self.password)
        # time.sleep(10)
        # login_btn = login_btn[1]

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
    
class Autokarma(Web_Search):

    def __init__(self, address, price_class, product_name_class, address_class) -> None:
        super().__init__(address, price_class, product_name_class, address_class)
        self.driver = Web_Search.init_driver("chrome",())

    def find_product(self, product_code):
        super().find_product(product_code)
        self.driver.get(self.address)
        self.input_in_search_bar(product_code,'//input[@name = "searchcode"]',By.XPATH)
        prices = self.wait_for_element(By.XPATH,self.price_class)
        prod_name = self.wait_for_element(By.XPATH,self.product_name_class)
        address = [None]*len(prod_name)
        prices_temp,prod_name_temp,address_temp = self.create_table_elements(prod_name,prices,address)
        while self.go_to_next_page():
            price = self.wait_for_element(By.XPATH,self.price_class)
            prod = self.wait_for_element(By.XPATH,self.product_name_class)
            addres = [None]*len(prod)
            prices_temp2,prod_name_temp2,address_temp2 = self.create_table_elements(prod,price,addres)
            prices_temp.extend(prices_temp2)
            prod_name_temp.extend(prod_name_temp2)
            address_temp.extend(address_temp2)

        return  prices_temp,prod_name_temp,address_temp
    
    def create_table_elements(self, prod_names, prod_prices, address):
        super().create_table_elements(prod_names, prod_prices, address)
        prices = []
        prod_name = []
        prod_address = []
        for i in range(0,len(prod_prices)):
            prices.append(prod_prices[i].text.split("Ron",1)[0].split(" ",1)[0])
            prod_name.append(prod_names[i].text)
            prod_address.append(address[i])
        return prices,prod_name,prod_address


    def go_to_next_page(self) -> bool:
        next_btn = self.driver.find_elements(By.XPATH,"//*[@id='products']/div[2]/ul/li/a")
        if next_btn:
            next_btn = next_btn[-2]
            if next_btn.text != ">":
                return False
            else:
                self.driver.execute_script("arguments[0].click();", next_btn)
                return True
        else:
            return False

    
def min_index_find(price):
    temp_list = []
    for j in range(0,len(price)):
        temp_list.append(float(price[j].split(" ", 1)[0].replace(".","").replace(",",".")))
    return temp_list,temp_list.index(min(temp_list))
    
def main(part_code):
    
    Web_Search.init_driver("chrome",())
    episa = Episa("https://www.epiesa.ro/cautare-piesa/?find=","bricolaje-bottom-text","sub-product-detail","product-auto-title")
    episa.new_tab()
    price, product, address = episa.find_product(part_code)
    unix = Unix("https://www.unixauto.ro/webshop/cikklista?cSearch=","price__amount--single","product-data--title--text","product-id")
    unix.new_tab()
    unix.login_with_user('https://www.unixauto.ro/webshop/login','','')
    price_1, product_1, address_1 = unix.find_product(part_code)
    autokarma = Autokarma("https://www.autokarma.ro","//div[3]/div/div/div[4]/div[1]/div/span","//div[1]/div/div[2]/div[1]/div[1]/div[2]/span","")
    autokarma.new_tab()
    price_3, product_3, address_3 = autokarma.find_product(part_code)

    price.extend(price_1)
    price.extend(price_3)
    product.extend(product_1)
    product.extend(product_3)
    address.extend(address_1)
    address.extend(address_3)
    price_list,min_index = min_index_find(price)
    return price_list, product, address, min_index
    # return price_1, product_1, address_1, min_index

    
    
# if __name__ == "__main__":
# #     # part_code = "1C0906517A"


#     part_code = '8E0411318'
#     main(part_code)
# #     price_list, product, address, min_index = main(part_code)
# #     print(price_list)
