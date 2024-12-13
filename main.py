import streamlit as st
from scrape import web_scraping, clean_body, extract_body_content, split_dom_content
from parse import parse_with_llama

# Streamlit Application
st.title("AI Web Scraper")

# Initialize session state variables
if "dom_content" not in st.session_state:
    st.session_state.dom_content = ""
if "dom_content_split" not in st.session_state:
    st.session_state.dom_content_split = []
if "total_chunks" not in st.session_state:
    st.session_state.total_chunks = 0

# Input query
query = st.text_input("Enter your search query:")

# Predefined URLs for the e-commerce sites
base_urls = {
    "flipkart": "https://www.flipkart.com/search?q={query}",
    "myntra": "https://www.myntra.com/rawquery={query}",
    "amazon": "https://www.amazon.com/s?k={query}",
    "ajio": "https://www.ajio.com/search/?text={query}",
}

# Buttons for the e-commerce sites
col1, col2, col3, col4 = st.columns(4)
selected_site = None

with col1:
    if st.button("Flipkart"):
        selected_site = "flipkart"
with col2:
    if st.button("Myntra"):
        selected_site = "myntra"
with col3:
    if st.button("Amazon"):
        selected_site = "amazon"
with col4:
    if st.button("Ajio"):
        selected_site = "ajio"

# Process URL based on selected site
if selected_site:
    if query:
        # Format the query appropriately
        formatted_query = query.replace(" ", "+")  # Replace spaces with '+' for search engines
        url = base_urls[selected_site].format(query=formatted_query)
        st.write(f"Scraping the {selected_site} URL: {url}")

        # Extract base URL dynamically
        base_url = f"https://{selected_site}.com"

        try:
            # Perform web scraping
            result = web_scraping(url)
            body_content = extract_body_content(result)
            clean_content = clean_body(body_content, base_url)

            # Store cleaned content in session state
            st.session_state.dom_content = clean_content
            st.session_state.dom_content_split = split_dom_content(clean_content)
            st.session_state.total_chunks = len(st.session_state.dom_content_split)
            st.success("Scraping successful!")
        except Exception as e:
            st.error(f"An error occurred during scraping: {e}")
    else:
        st.warning("Please enter a search query.")

# View DOM content
if st.session_state.dom_content:
    with st.expander("View DOM Content"):
        st.text_area("DOM Content", st.session_state.dom_content, height=400)
    st.write(f"Total chunks: {st.session_state.total_chunks}")

    # Parse content based on user description
    if st.button("Parse Content"):
        try:
            # Parse DOM content in chunks of 10
            st.write("Parsing the content based on the description...")
            half_length = int(st.session_state.total_chunks / 2)
            parse_result = parse_with_llama(st.session_state.dom_content_split[half_length:half_length+10])  # Adjust chunking logic as needed

            st.success("Parsing successful!")
            st.write(parse_result)  # Display parsed content
        except Exception as e:
            st.error(f"An error occurred during parsing: {e}")
