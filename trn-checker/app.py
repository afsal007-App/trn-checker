import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

# Set up Selenium
def get_page_content_selenium():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://tax.gov.ae/en/statuscheck.aspx")
        time.sleep(3)  # Wait for page to load
        page_source = driver.page_source
        return driver, page_source
    except Exception as e:
        st.error(f"Failed to load the page: {e}")
        return None, None

# Submit TRN and CAPTCHA
def check_trn_selenium(driver, trn, captcha):
    try:
        driver.find_element(By.ID, "ContentPlaceHolder1_txtTRN").send_keys(trn)
        driver.find_element(By.ID, "ContentPlaceHolder1_txtCaptcha").send_keys(captcha)
        driver.find_element(By.ID, "ContentPlaceHolder1_btnSearch").click()
        time.sleep(3)  # Wait for result
        return driver.page_source
    except Exception as e:
        st.error(f"Failed to submit the form: {e}")
        return None

# Parse the result
def parse_result(html):
    try:
        soup = BeautifulSoup(html, "html.parser")
        result_div = soup.find("div", {"id": "ContentPlaceHolder1_pnlResult"})
        if result_div:
            legal_name = result_div.find("span", {"id": "ContentPlaceHolder1_lblLegalName"})
            return legal_name.text.strip() if legal_name else "No result found."
        return "Invalid TRN or CAPTCHA. Please try again."
    except Exception as e:
        st.error(f"Failed to parse the result: {e}")
        return "Error parsing the result."

# Streamlit app
def main():
    st.title("UAE TRN Checker")
    st.write("Enter a 15-digit Tax Registration Number (TRN) to verify it.")

    trn = st.text_input("Enter TRN (15 digits)", max_chars=15)
    st.write("Please visit https://tax.gov.ae/en/statuscheck.aspx to view the CAPTCHA, then enter it below.")
    captcha = st.text_input("Enter CAPTCHA code")

    if st.button("Check TRN"):
        if len(trn) != 15 or not trn.isdigit():
            st.error("Please enter a valid 15-digit TRN.")
        elif not captcha:
            st.error("Please enter the CAPTCHA code.")
        else:
            with st.spinner("Verifying TRN..."):
                driver, page_content = get_page_content_selenium()
                if driver and page_content:
                    result_html = check_trn_selenium(driver, trn, captcha)
                    if result_html:
                        result = parse_result(result_html)
                        st.success(f"Result: {result}")
                    driver.quit()
                else:
                    st.error("Unable to proceed due to page load failure.")

if __name__ == "__main__":
    main()
