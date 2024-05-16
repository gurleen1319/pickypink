import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

def scrape_google_shopping(query):
    url = f"https://www.google.co.in/search?tbm=shop&q={urllib.parse.quote(query)}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        products = []
        for result in soup.find_all('div', class_='sh-dgr__grid-result'):
            product = {}
            product['name'] = result.find('h3', class_='tAxDx').text.strip()
            product['price'] = result.find('span', class_='a8Pemb').text.strip()
            product['image'] = result.find('img')['src']
            product['buy_link'] = result.find('a', class_='shntl')['href']
            product['site_name'] = result.find('div', class_='aULzUe').text.strip()
            products.append(product)
            if len(products) == 9:
                break
        return products
    else:
        return None

# Streamlit UI
st.title("Picky Advance Search")
query = st.text_input("Enter your search query:")
if st.button("Search"):
    if query:
        products = scrape_google_shopping(query)
        if products:
            num_products = len(products)
            num_rows = num_products // 3 + (1 if num_products % 3 != 0 else 0)
            for i in range(num_rows):
                col1, col2, col3 = st.columns(3)
                for j in range(3):
                    index = i * 3 + j
                    if index < num_products:
                        product = products[index]
                        with col1 if j == 0 else col2 if j == 1 else col3:
                            st.subheader(f"Product {index + 1}")
                            st.write(f"Name: {product['name']}")
                            st.write(f"Price: {product['price']}")
                            st.write(f"Image: {product['image']}")
                            st.write(f"Buy Link: {product['buy_link']}")
                            st.write(f"Site Name: {product['site_name']}")
                            st.markdown("---")
        else:
            st.write("Failed to retrieve search results. Please try again later.")
    else:
        st.write("Please enter a search query.")

# Change background color to light pink
st.markdown(
    """
    <style>
    body {
        background-color: #FFB6C1;
    }
    </style>
    """,
    unsafe_allow_html=True
)
