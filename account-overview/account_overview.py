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
        time.sleep(5)
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
        password_input.send_keys("P@ssword1234")

        sign_in_button = driver.find_element(By.CSS_SELECTOR, 'form[action="/account/login"] button[type="submit"]')
        print("Clicking the Sign in immediately..") 
        sign_in_button.click()
        time.sleep(10)
        
        if driver.current_url == "https://www.varley.com/account":
            print("Login successful. URL is correct.")
            print("Customer is in the account page")
        else:
            print(f"Login failed or wrong redirect. Current URL: {driver.current_url}")
            

    def test_verify_account_content(self, driver):
        # Wait for the main container to be present
        container = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.mb-15.flex.flex-col.gap-6.border'))
        )

        # Name
        name_label = container.find_element(By.CSS_SELECTOR, 'div:nth-child(1) > p.font-medium')
        name_value = container.find_element(By.CSS_SELECTOR, 'div:nth-child(1) > p:not(.font-medium)')
        print(f"Checking Name label: {name_label.text.strip()}")
        assert name_label.text.strip() == "Name", f"Expected label 'Name', got '{name_label.text.strip()}'"
        print(f"Checking Name value: {name_value.text.strip()}")
        assert name_value.text.strip() == "Des Test", f"Expected Name to be 'Des Test', got '{name_value.text.strip()}'"

        # Email
        email_label = container.find_element(By.CSS_SELECTOR, 'div:nth-child(2) > p.font-medium')
        email_value = container.find_element(By.CSS_SELECTOR, 'div:nth-child(2) > p:not(.font-medium)')
        print(f"Checking Email label: {email_label.text.strip()}")
        assert email_label.text.strip() == "Email", f"Expected label 'Email', got '{email_label.text.strip()}'"
        print(f"Checking Email value: {email_value.text.strip()}")
        assert email_value.text.strip() == "lourdes@ecrubox.com", f"Expected Email to be 'lourdes@ecrubox.com', got '{email_value.text.strip()}'"

        # Phone
        phone_label = container.find_element(By.CSS_SELECTOR, 'div:nth-child(3) > p.font-medium')
        phone_value = container.find_element(By.CSS_SELECTOR, 'div:nth-child(3) > p:not(.font-medium)')
        print(f"Checking Phone label: {phone_label.text.strip()}")
        assert phone_label.text.strip() == "Phone", f"Expected label 'Phone', got '{phone_label.text.strip()}'"
        print(f"Checking Phone value: {phone_value.text.strip()}")
        assert phone_value.text.strip() == "+447777777769", f"Expected Phone to be '+447777777769', got '{phone_value.text.strip()}'"

        # Password
        password_label = container.find_element(By.CSS_SELECTOR, 'div:nth-child(4) > p.font-medium')
        password_value = container.find_element(By.CSS_SELECTOR, 'div:nth-child(4) > p:not(.font-medium)')
        print(f"Checking Password label: {password_label.text.strip()}")
        assert password_label.text.strip() == "Password", f"Expected label 'Password', got '{password_label.text.strip()}'"
        print(f"Checking Password value: {password_value.text.strip()}")
        assert password_value.text.strip() == "**************", f"Expected Password to be '**************', got '{password_value.text.strip()}'"

        # Edit profile link
        edit_profile_link = container.find_element(By.CSS_SELECTOR, 'a.flex.w-fit.items-center.gap-1.border-b[data-discover="true"]')
        print(f"Checking Edit profile link text: {edit_profile_link.text.strip()}")
        assert "Edit profile" in edit_profile_link.text.strip(), "Edit profile link text is incorrect"
        print(f"Checking Edit profile link href: {edit_profile_link.get_attribute('href')}")
        assert edit_profile_link.get_attribute('href').endswith('/account/edit'), "Edit profile link does not end with /account/edit"

    def test_verify_last_3_months_orders(self, driver):
        # Click the "Order history" link
        print('AAAAA')
        order_history_link = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-discover="true"][href="/account/orders"]'))
        )
        print("Clicking 'Order history' link...")
        order_history_link.click()
    
        # Findding the 6 months button
        last_6_months_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, r'button.flex.w-\[160px\].cursor-pointer.items-center.border.bg-white.px-5.py-4'))
        )

        # Verify the button label matches "Last 6 months" to be sure it's the right one
        label_span = last_6_months_button.find_element(By.CSS_SELECTOR, 'span.mr-auto.text-sm')
        if label_span.text.strip() == "Last 6 months":
            print("Clicking 'Last 6 months' button...")
            last_6_months_button.click()
        else:
            print(f"Found button but label is '{label_span.text.strip()}', not 'Last 6 months'.")
        
        # Click the "Last 3 months" button
        last_3_months_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH, 
                "//button[contains(@class, 'flex') and contains(@class, 'items-center') and contains(text(), 'Last 3 months')]"
            ))
        )
        print("Clicking 'Last 3 months' button...")
        last_3_months_button.click()

        time.sleep(5)  

        self.populate_order(driver, section='last_3_months')

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

        self.populate_order(driver)

        # Locator for the button containing the span with text 'Last 6 months'
        button_locator = (
            By.XPATH,
            "//button[contains(@class, 'flex') and contains(@class, 'cursor-pointer') and .//span[text()='Last 6 months']]"
        )

        # Wait until the button is clickable, then click
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(button_locator)
        )

        button.click()
        print("Clicked the 'Last 6 months' button.")

        # XPath locator matching the button by class and exact text "2025"
        button_locator = (
            By.XPATH,
            "//button[contains(@class, 'flex') and contains(@class, 'items-center') and contains(@class, 'overflow-hidden') and contains(@class, 'py-1') and contains(@class, 'text-sm') and contains(@class, 'hover:opacity-80') and normalize-space(text())='2025']"
        )

        # Wait until the button is clickable, then click it
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(button_locator)
        )

        button.click()
        print("Clicked the '2025' button.")
        time.sleep(5)


        self.populate_order(driver, section='2025')

        print("\n" + "=" * 80)
        print("Order verification completed.")

    def populate_order(self, driver, section=''):
        print(section)
        while True:
            # Locator for the container div
            container_locator = (By.CSS_SELECTOR, "div.flex.items-center.justify-center.gap-6")

            # Wait until container is present
            container = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(container_locator)
            )

            # Find all buttons inside the container div
            buttons = container.find_elements(By.TAG_NAME, "button")

            # Confirm there are at least 2 buttons
            if len(buttons) >= 2:
                second_button = buttons[1]  # zero-indexed: 0 is first button, 1 is second button

                # Check if second button is displayed and enabled (clickable)
                is_visible = second_button.is_displayed()
                is_enabled = second_button.is_enabled()

                print(f"Second button visible: {is_visible}")
                print(f"Second button enabled (clickable): {is_enabled}")

                if is_visible and is_enabled:
                    print("Second button is clickable!")
                    # Optionally click it:
                    # second_button.click()
                else:
                    print("Second button is NOT clickable.")
            else:
                print(f"Only found {len(buttons)} button(s) inside the container. No second button available.")

        
            # Find all order items
            order_items = driver.find_elements(By.CSS_SELECTOR, 'li.flex.flex-col.flex-wrap.items-start.justify-between.gap-y-3.border.border-\\[\\#C7BFB9\\].bg-white.p-6')
            
            # Loop through each order and extract values
            for index, order_item in enumerate(order_items, 1):
                print(f"\nOrder {index}:")
                print("-" * 40)
                
                # Order Number
                order_number_label = order_item.find_element(By.CSS_SELECTOR, 'p.mb-1.text-sm.font-medium.leading-normal')
                order_number_value = order_item.find_element(By.CSS_SELECTOR, 'p.pl-1.text-sm.font-medium.leading-normal.text-\\[\\#1d1d1b\\]')
                print(f"Order Number Label: {order_number_label.text.strip()}")
                print(f"Order Number Value: {order_number_value.text.strip()}")
                
                # View Order Link
                view_order_link = order_item.find_element(By.CSS_SELECTOR, 'a.text-sm.underline[data-discover="true"]')
                print(f"View Order Link Text: {view_order_link.text.strip()}")
                print(f"View Order Link Href: {view_order_link.get_attribute('href')}")
                
                # Status
                status_elements = order_item.find_elements(By.CSS_SELECTOR, 'div.order-3.flex.w-20 p')
                if len(status_elements) >= 2:
                    status_label = status_elements[0]
                    status_value = status_elements[1]
                    print(f"Status Label: {status_label.text.strip()}")
                    print(f"Status Value: {status_value.text.strip()}")
                
                # Date
                date_element = order_item.find_element(By.CSS_SELECTOR, 'p.leading.text-sm.leading-normal.text-\\[\\#1d1d1b\\]')
                print(f"Order Date: {date_element.text.strip()}")
                
                # Total
                total_elements = order_item.find_elements(By.CSS_SELECTOR, 'div.order-3.flex.w-1\\/2.lg\\:w-auto p')
                for i in range(0, len(total_elements), 2):
                    if i + 1 < len(total_elements):
                        total_label = total_elements[i]
                        total_value = total_elements[i + 1]
                        if "Total:" in total_label.text:
                            print(f"Total Label: {total_label.text.strip()}")
                            print(f"Total Value: {total_value.text.strip()}")
                            break

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
    account_overview.test_verify_account_content(driver)
    print('ORDER HISTORY ORDER HISTORY ORDER HISTORY ORDER HISTORY ORDER HISTORY ORDER HISTORY')
    account_overview.test_verify_last_3_months_orders(driver)
    driver.quit()

