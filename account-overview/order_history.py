import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions


class Test_Account_Overview:   
    def test_nav_to_page(self, env) -> None:
        driver = self.setup_driver()
        url = "https://www.varley.com/account/login"
        driver.get(url)
        time.sleep(2)
        
        self.verify_location_modal(driver)
        self.test_verify_log_in(driver)
        # self.text_validate_elements(driver)
        # self.test_validate_email(driver)
        driver.quit()
    
    def setup_driver(self):
        driver_path = r"C:\Users\Joseph\Downloads\edgedriver_win64\msedgedriver.exe"  # Your downloaded driver path
        service = EdgeService(executable_path=driver_path)
        options = EdgeOptions()
        driver = webdriver.Edge(service=service, options=options)
        return driver
    
    def verify_location_modal(self, driver) -> None:
        print("Location Modal Test")
        time.sleep(2)
        geoip_modal = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[id^="headlessui-dialog-panel"]'))
        )
        if geoip_modal.is_displayed():
            print("GeoIP modal is visible")
            close_button = geoip_modal.find_element(By.CSS_SELECTOR, 'svg.cursor-pointer')
            close_button.click()
            time.sleep(2)
            print("GeoIP modal is now closed. Continuing with the test\n")
        else:
            print("GeoIP modal is closed. Continuing with test.\n")
            
    def test_verify_log_in(self, driver) -> None:
    
        # Input valid email
        print("Entering valid email")
        email_input = driver.find_element(By.CSS_SELECTOR, 'input[name="email"]')
        email_input.send_keys("lourdes@ecrubox.com")

        # Input valid password
        print("Entering valid password")
        password_input = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
        password_input.send_keys("P@ssword123")

        sign_in_button = driver.find_element(By.CSS_SELECTOR, 'form[action="/account/login"] button[type="submit"]')
        print("Clicking the Sign in immediately..") 
        sign_in_button.click()
        time.sleep(5)
        
        if driver.current_url == "https://www.varley.com/account":
            print("Login successful. URL is correct.")
            print("Customer is in the account page")
        else:
            print(f"Login failed or wrong redirect. Current URL: {driver.current_url}")
            
    def navigate_order_history(self, driver) -> None:
        # Locator for the 'Order history' link using the data attribute and href and click the button
        order_history_locator = (
            By.CSS_SELECTOR, 
            'a[data-discover="true"][href="/account/orders"]'
        )
        order_history_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(order_history_locator)
        )
        order_history_link.click()
        print("Clicked the 'Order history' link.")

    def nagivate_to_last_3_months_orders(self, driver) -> None:
        # Findding the 6 months button and clicks it
        last_6_months_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, r'button.flex.w-\[160px\].cursor-pointer.items-center.border.bg-white.px-5.py-4'))
        )
        label_span = last_6_months_button.find_element(By.CSS_SELECTOR, 'span.mr-auto.text-sm')
        if label_span.text.strip() == "Last 6 months":
            print("Clicking 'Last 6 months' button...")
            last_6_months_button.click()
        else:
            print(f"Found button but label is '{label_span.text.strip()}', not 'Last 6 months'.")

        # Find last 3 month button and clicks it
        last_3_months_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH, 
                "//button[contains(@class, 'flex') and contains(@class, 'items-center') and contains(text(), 'Last 3 months')]"
            ))
        )
        print("Clicking 'Last 3 months' button...")
        last_3_months_button.click()
        time.sleep(2)

        self.populate_order(driver, section='last 3 months')

        # Navigate to 6 months
        last_3_months_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH, 
                "//button[contains(@class, 'flex') and contains(@class, 'cursor-pointer') and contains(@class, 'items-center') and ./span[text()='Last 3 months']]"
            ))
        )
        print("Clicking 'Last 3 months' button...")
        last_3_months_button.click()
        last_6_months_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[contains(@class, 'flex') and contains(@class, 'items-center') and contains(., 'Last 6 months')]"
            ))
        )
        print("Clicking 'Last 6 months' button...")
        last_6_months_button.click()
        time.sleep(3)

        self.populate_order(driver, section='last 6 months')

    def populate_order(self, driver, section=''):
        while True:
            # Locator for the container div
            container_locator = (By.CSS_SELECTOR, "div.flex.items-center.justify-center.gap-6")
            container = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(container_locator)
            )
            buttons = container.find_elements(By.TAG_NAME, "button")
            if len(buttons) >= 2:
                second_button = buttons[1] 
                is_visible = second_button.is_displayed()
                is_enabled = second_button.is_enabled()
                print(f"Second button visible: {is_visible}")
                print(f"Second button enabled (clickable): {is_enabled}")
                if is_visible and is_enabled:
                    print("Second button is clickable!")
                else:
                    print("Second button is NOT clickable.")
            else:
                print(f"Only found {len(buttons)} button(s) inside the container. No second button available.")

        
            # Find all order items
            order_items = driver.find_elements(By.CSS_SELECTOR, 'li.flex.flex-col.flex-wrap.items-start.justify-between.gap-y-3.border.border-\\[\\#C7BFB9\\].bg-white.p-6')
            
            # Loop through each order and extract values
            for index, order_item in enumerate(order_items, 1):
                # Locate the "View order" link inside this order item
                view_order_link = order_item.find_element(By.CSS_SELECTOR, 'a.text-sm.underline[data-discover="true"]')
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(view_order_link))
                view_order_link.click()
                print(f"Clicked 'View order' for order {index}")
                time.sleep(5)

                # Locator for the parent container div
                parent_container_locator = (By.CSS_SELECTOR, "div.flex-grow.p-5.pb-15.pt-10.md\\:p-10.lg\\:p-20.lg\\:pb-20.lg\\:pt-20")
                parent_container = driver.find_element(*parent_container_locator)
                child_product_locator = "div.flex.gap-4.pb-6.md\\:gap-16.md\\:border-b.md\\:border-\\[\\#C7BFB9\\].md\\:pt-6.xl\\:gap-x-32"
                product_children = parent_container.find_elements(By.CSS_SELECTOR, child_product_locator)
                print(f"Found {len(product_children)} product item(s).")

                for index, product in enumerate(product_children, 1):
                    # Extract product name inside <dt>
                    dt_elements = product.find_elements(By.TAG_NAME, "dt")
                    if dt_elements:
                        item_name = dt_elements[0].text.strip()
                    else:
                        item_name = "<No item name found>"

                    # Check for image presence inside <a> tag with data-discover='true'
                    a_tags = product.find_elements(By.CSS_SELECTOR, "a[data-discover='true']")
                    if a_tags:
                        images = a_tags[0].find_elements(By.TAG_NAME, "img")
                        has_image = len(images) > 0
                    else:
                        has_image = False

                    print(f"Product {index}: Name = '{item_name}', Has image = {has_image}")



                driver.back()
                time.sleep(2)
                if section == 'last 3 months':
                    # Findding the 6 months button and clicks it
                    last_6_months_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, r'button.flex.w-\[160px\].cursor-pointer.items-center.border.bg-white.px-5.py-4'))
                    )
                    label_span = last_6_months_button.find_element(By.CSS_SELECTOR, 'span.mr-auto.text-sm')
                    if label_span.text.strip() == "Last 6 months":
                        print("Clicking 'Last 6 months' button...")
                        last_6_months_button.click()
                    else:
                        print(f"Found button but label is '{label_span.text.strip()}', not 'Last 6 months'.")

                    # Find last 3 month button and clicks it
                    last_3_months_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((
                            By.XPATH, 
                            "//button[contains(@class, 'flex') and contains(@class, 'items-center') and contains(text(), 'Last 3 months')]"
                        ))
                    )
                    print("Clicking 'Last 3 months' button...")
                    last_3_months_button.click()
                    time.sleep(2)


            print(is_enabled)

            if not is_enabled:
                break

                
            second_button.click()
            time.sleep(2)
        
          
    def is_element_present(self, driver, locator):
        return len(driver.find_elements(*locator)) > 0
 
    
if __name__ == "__main__":
    account_overview = Test_Account_Overview()
    driver = account_overview.setup_driver()
    url = "https://www.varley.com/account/login"
    driver.get(url)
    time.sleep(2)
    account_overview.verify_location_modal(driver)
    account_overview.test_verify_log_in(driver)
    account_overview.navigate_order_history(driver)
    account_overview.nagivate_to_last_3_months_orders(driver)
    driver.quit()

