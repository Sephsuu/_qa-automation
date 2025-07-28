from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def test_verify_last_3_months_orders(self, driver):
    # Click the "Last 3 months" dropdown button
    last_3_months_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.flex.w-\\[160px\\].cursor-pointer.items-center.border.bg-white.px-5.py-4'))
    )
    print("Clicking 'Last 3 months' button...")
    last_3_months_button.click()
    
    # Wait for orders to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'li.flex.flex-col.flex-wrap.items-start.justify-between.gap-y-3.border'))
    )
    
    # Find all order items
    order_items = driver.find_elements(By.CSS_SELECTOR, 'li.flex.flex-col.flex-wrap.items-start.justify-between.gap-y-3.border.border-\\[\\#C7BFB9\\].bg-white.p-6')
    
    print(f"Found {len(order_items)} orders in the last 3 months:")
    print("=" * 80)
    
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
    
    print("\n" + "=" * 80)
    print("Order verification completed.")

# Alternative method with more specific selectors
def test_verify_orders_detailed(self, driver):
    # Click the "Last 3 months" button
    last_3_months_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'flex w-[160px]') and .//span[text()='Last 3 months']]"))
    )
    print("Clicking 'Last 3 months' dropdown...")
    last_3_months_button.click()
    
    # Wait for orders container to load
    orders_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'ul, div[class*="orders"], div[class*="order-list"]'))
    )
    
    # Find all order list items
    order_items = driver.find_elements(By.CSS_SELECTOR, 'li.flex.flex-col.flex-wrap')
    
    print(f"\nFound {len(order_items)} orders for the last 3 months")
    print("=" * 100)
    
    for idx, order in enumerate(order_items, 1):
        print(f"\n📦 ORDER {idx}")
        print("-" * 50)
        
        # Extract Order Number
        order_number_section = order.find_element(By.CSS_SELECTOR, 'div.order-1.flex')
        order_num_label = order_number_section.find_element(By.CSS_SELECTOR, 'p.mb-1.text-sm.font-medium')
        order_num_value = order_number_section.find_element(By.CSS_SELECTOR, 'p.pl-1.text-sm.font-medium.text-\\[\\#1d1d1b\\]')
        
        print(f"🏷️  {order_num_label.text.strip()} {order_num_value.text.strip()}")
        
        # Extract View Order Link
        view_order_section = order.find_element(By.CSS_SELECTOR, 'div.order-2.w-20')
        view_order_link = view_order_section.find_element(By.CSS_SELECTOR, 'a.text-sm.underline')
        
        print(f"🔗 View Order: {view_order_link.text.strip()}")
        print(f"🌐 Link URL: {view_order_link.get_attribute('href')}")
        
        # Extract Status
        status_section = order.find_element(By.CSS_SELECTOR, 'div.order-3.flex.w-20')
        status_elements = status_section.find_elements(By.CSS_SELECTOR, 'p')
        if len(status_elements) >= 2:
            print(f"📊 {status_elements[0].text.strip()} {status_elements[1].text.strip()}")
        
        # Extract Date
        date_element = order.find_element(By.CSS_SELECTOR, 'p.leading.text-sm.leading-normal.text-\\[\\#1d1d1b\\]')
        print(f"📅 Order Date: {date_element.text.strip()}")
        
        # Extract Total
        total_sections = order.find_elements(By.CSS_SELECTOR, 'div.order-3.flex')
        for section in total_sections:
            paragraphs = section.find_elements(By.CSS_SELECTOR, 'p')
            for i in range(0, len(paragraphs), 2):
                if i + 1 < len(paragraphs) and "Total:" in paragraphs[i].text:
                    print(f"💰 {paragraphs[i].text.strip()} {paragraphs[i + 1].text.strip()}")
                    break
    
    print("\n" + "=" * 100)
    print("✅ All orders processed successfully!")

# Simplified version focusing on key data extraction
def test_extract_order_data(self, driver):
    # Click Last 3 months filter
    filter_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Last 3 months']/parent::button"))
    )
    filter_button.click()
    
    # Wait and get all orders
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li[class*="flex flex-col"]'))
    )
    
    orders = driver.find_elements(By.CSS_SELECTOR, 'li.flex.flex-col.flex-wrap.items-start.justify-between')
    
    print(f"ORDERS FOUND: {len(orders)}")
    print("*" * 60)
    
    for i, order in enumerate(orders, 1):
        print(f"\nORDER #{i}")
        
        # Order Number
        order_num = order.find_element(By.XPATH, ".//p[contains(text(), 'Order number:')]/following-sibling::p").text
        print(f"Order Number: {order_num}")
        
        # Status  
        status = order.find_element(By.XPATH, ".//p[contains(text(), 'Status:')]/following-sibling::p").text
        print(f"Status: {status}")
        
        # Date
        date = order.find_element(By.CSS_SELECTOR, "p.leading.text-sm.leading-normal.text-\\[\\#1d1d1b\\]").text
        print(f"Date: {date}")
        
        # Total
        total = order.find_element(By.XPATH, ".//p[contains(text(), 'Total:')]/following-sibling::p").text
        print(f"Total: {total}")
        
        # View Order Link
        view_link = order.find_element(By.CSS_SELECTOR, "a[data-discover='true']")
        print(f"View Order URL: {view_link.get_attribute('href')}")
        
        print("-" * 40)