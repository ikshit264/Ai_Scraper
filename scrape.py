import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

def extract_body_content(html_content):
    """Extracts the body content from the HTML source."""
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body(body_content, base_url):
    """Cleans the body content by extracting and preserving image links and product links."""
    soup = BeautifulSoup(body_content, "html.parser")

    # Remove script and style elements only
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Handle <img> tags by inserting placeholders for their src attributes
    for img_tag in soup.find_all("img"):
        img_placeholder = f"[IMG_SRC={img_tag.get('src', '')}]"
        img_tag.insert_before(soup.new_string(img_placeholder))
        # Keep the img tag as it is without removing it

    # Handle <a> tags by inserting placeholders for their href attributes
    for a_tag in soup.find_all("a"):
        href = a_tag.get('href', '')
        # Check if the href does not start with a '/'
        if not href.startswith('/'):
            href = '/' + href
        href_placeholder = f"[PROD_LINK={base_url + href}]"
        a_tag.insert_before(soup.new_string(href_placeholder))
        a_tag.unwrap()  # Remove the <a> tag but keep its inner content


    # Extract visible text content along with preserved placeholders
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())

    return cleaned_content



def web_scraping(website):
    """Performs web scraping using Selenium with scrolling and returns the HTML source."""
    print("Launching Chrome browser in headless mode...")

    chrome_driver_path = "./chromedriver.exe"
    options = webdriver.ChromeOptions()

    # Enable headless mode
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")  # Recommended for headless mode
    options.add_argument("--no-sandbox")  # Helps on Linux systems
    options.add_argument("--disable-dev-shm-usage")  # Helps with memory issues

    # Add user-agent to mimic real browser usage
    user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    )
    options.add_argument(f"user-agent={user_agent}")

    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        # Visit the website
        driver.get(website)
        print("Page Loaded...")

        time.sleep(2)  # Initial delay for the page to load

        # Find the body element to send scrolling commands
        body = driver.find_element("tag name", "body")
        
        for _ in range(7):  # Scroll down 5 times
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)  # Pause between scrolls to allow content to load

        # Extract the HTML source
        html = driver.page_source

        return html

    finally:
        # Close the browser
        driver.quit()

def split_dom_content(dom_content, max_length=5000):
    """Splits the DOM content into chunks of a specified maximum length."""
    return [dom_content[i:i+max_length] for i in range(0, len(dom_content), max_length)]