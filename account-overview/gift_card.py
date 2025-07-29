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
            
    def navigate_gift_card_balance(self, driver) -> None:
        # Locator for the 'Gift card balance' link
        gift_card_locator = (
            By.CSS_SELECTOR,
            'a[data-discover="true"][href="/account/gift-card"]'
        )
        gift_card_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(gift_card_locator)
        )
        gift_card_link.click()
        print("Clicked the 'Gift card balance' link.")
        time.sleep(10)

    def fill_embedded_contact_form(self, driver, full_name, email, subject_text, message):
        wait = WebDriverWait(driver, 15)

        # 1. Wait for the iframe container with id "contact_us_form"
        iframe_container = wait.until(
            EC.presence_of_element_located((By.ID, "contact_us_form"))
        )

        # 2. Find the iframe inside the container
        iframe = iframe_container.find_element(By.TAG_NAME, "iframe")

        # 3. Switch to the iframe context
        driver.switch_to.frame(iframe)

        # Now inside iframe, fill the form fields

        # Fill Full name
        full_name_input = wait.until(EC.visibility_of_element_located((By.ID, "fullName")))
        full_name_input.clear()
        full_name_input.send_keys(full_name)

        # Fill Email
        email_input = driver.find_element(By.ID, "email")
        email_input.clear()
        email_input.send_keys(email)

        # Select Subject from dropdown

        dropdown_toggle = driver.find_element(
            By.CSS_SELECTOR, "div.ghc-form-dropdown button[data-testid='dropdown-toggle']"
        )
        dropdown_toggle.click()
        button_locator = (
            By.XPATH,
            "//button[contains(@class, 'css-9zm586') and contains(@class, 'ey637kz2') and normalize-space(text())='Gift Card Number']"
        )

        # Wait until the button is clickable then click it
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(button_locator)
        )

        button.click()
        print("Clicked the 'Gift Card Number' button.")

        # Fill Message textarea
        message_textarea = driver.find_element(By.ID, "message")
        message_textarea.clear()
        message_textarea.send_keys(message)

        # Submit form by clicking "Send" button
        send_button = driver.find_element(
            By.CSS_SELECTOR, "button[type='submit'].btn.btn-secondary"
        )
        send_button.click()

        driver.switch_to.default_content()

        div_locator = (By.CSS_SELECTOR, "div.mb-10")

        div_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(div_locator))

        # Print the textual content inside the div (with spacing conserved)
        print(f"\n{div_element.text}\n")
        
        main_content_div = driver.find_element(By.ID, "mainContent")

        # Scroll the container to top using JavaScript
        driver.execute_script("arguments[0].scrollTop = 0;", main_content_div)

        print("Contact form submitted.")
        time.sleep(3)

        self.populate_gift_cards(driver)

    def populate_gift_cards(self, driver):
        gift_card_count = 0
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
         
            parent_container = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, 
                    "div.flex-grow.p-5.pb-15.pt-10"
                ))
            )

            # Gift card blocks inside the parent container (each <div class="pb-6">)
            gift_card_blocks = parent_container.find_elements(By.CSS_SELECTOR, "div.pb-6")

            print(f"Found {len(gift_card_blocks)} gift card(s).")

            for index, gift_card in enumerate(gift_card_blocks, 1):
                # Gift card title (e.g., "Gift card 1")
                title_elem = gift_card.find_element(By.CSS_SELECTOR, "h2.pb-4.text-lg.font-medium")
                gift_card_title = title_elem.text.strip()

                # Serial number paragraph
                serial_elem = gift_card.find_element(By.CSS_SELECTOR, "p.pb-3.text-sm")
                serial_text = serial_elem.text.strip()

                # Gift card balance div
                balance_container = gift_card.find_element(By.CSS_SELECTOR, "div.flex.pb-3.text-sm")
                # It contains text and a <b> element with a <div> holding the amount
                balance_amount_elem = balance_container.find_element(By.CSS_SELECTOR, "b.pl-\\[6px\\].font-bold > div")
                balance_amount = balance_amount_elem.text.strip()

                print(f"\nGift Card {index}:")
                print(f"  Title: {gift_card_title}")
                print(f"  Serial Number: {serial_text}")
                print(f"  Balance: {balance_amount}")
                gift_card_count += 1

            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", second_button)

            if not is_enabled:
                break

                
            second_button.click()
            time.sleep(2)

        print(f"Total gift card count: {gift_card_count}")

if __name__ == "__main__":
    account_overview = Test_Account_Overview()
    driver = account_overview.setup_driver()
    url = "https://www.varley.com/account/login"
    driver.get(url)
    time.sleep(2)
    account_overview.verify_location_modal(driver)
    account_overview.test_verify_log_in(driver)
    account_overview.navigate_gift_card_balance(driver)
    account_overview.fill_embedded_contact_form(driver, "Okotok", "okotok@gmail.com", "Gift Card Number", "Message")
    driver.quit()

