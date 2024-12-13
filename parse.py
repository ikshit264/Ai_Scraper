from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAI
import re
import json

GEMINI_KEY = "ADD_YOUR_GEMINI_KEY"

llm = GoogleGenerativeAI(
    model="gemini-pro",  # Ensure you use the correct model identifier
    api_key=GEMINI_KEY,
    temperature=0,
    verbose=True
)

template = """
Extract product details from the given text. Follow these rules strictly:

1. **Output Format:**  
   - JSON array of objects.  
   - Each object must include only:  
     - `title`: Product title (non-empty),
     - `image_link`: Direct URL to the product's image (non-empty),
     - `price`: Product price (non-empty),
     - `prod_link`: Direct URL to the product page (non-empty),
   - Strictly give output in json format only.

2. **Conditions:**  
   - Include only products with all four fields present and non-empty.  
   - If no valid products are found, return an empty array: `[]`.  

3. **Example Output:**  
   [
     {{"title": "Product 1", "image_link": "[IMG_SRC]", "price": "$10", "prod_link": "[PROD_LINK]"}},
     {{"title": "Product 2", "image_link": "[IMG_SRC]", "price": "$20", "prod_link": "[PROD_LINK]"}}
   ]

4. **Strict JSON:**  
   - Ensure the output is valid JSON with no extra text, comments, or explanations.

5. **No Extra Content**:
    - Do not give any extra comments on anything i just want the json data.
    - **No need to add any Notes any additonal data other than json**
    
Input : {dom_content}
"""

def parse_with_Gemini(dom_chunks):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm

    parse_result = []

    for i, chunk in enumerate(dom_chunks, start=1):
        try:
            response = chain.invoke({"dom_content": chunk})
            print(f"Parsed batch {i} of {len(dom_chunks)}")
            
            # Extract the text content from the response
            if hasattr(response, "content"):
                response_text = response.content  # For AIMessage or similar objects
            else:
                response_text = response  # Fallback for unexpected formats
            
            parse_result.append(response_text)
            print(response_text)
        except Exception as e:
            print(f"Error parsing batch {i}: {e}")

    # Join all results into a single string
    result = parse_result
    return result
