import os
import requests
from dotenv import load_dotenv
from langchain.tools import Tool

load_dotenv()

API_URL = f"http://localhost:{int(os.getenv("PORT", 3000))}/api"


def fetch_all_product_data():
    try:
        response = requests.get(f"{API_URL}products/") 
        if response.status_code == 200:
            products = response.json()
            return products  
        else:
            return {"error": "Failed to fetch product data", "status_code": response.status_code}
    except Exception as e:
        return {"error": str(e)}


def fetch_product_from_id(product_id: int):
    try:
        response = requests.get(f"{API_URL}products/{product_id}") 
        if response.status_code == 200:
            products = response.json()
            return products  
        else:
            return {"error": "Failed to fetch reviews data", "status_code": response.status_code}
    except Exception as e:
        return {"error": str(e)}


def fetch_review_from_id(review_id: int):
    try:
        response = requests.get(f"{API_URL}/reviews/{review_id}") 
        if response.status_code == 200:
            products = response.json()
            return products  
        else:
            return {"error": "Failed to fetch review data", "status_code": response.status_code}
    except Exception as e:
        return {"error": str(e)}


def fetch_reviews_from_product_id(product_id: int):
    try:
        response = requests.get(f"{API_URL}/reviews/product/{product_id}") 
        if response.status_code == 200:
            products = response.json()
            return products  
        else:
            return {"error": "Failed to fetch review data", "status_code": response.status_code}
    except Exception as e:
        return {"error": str(e)}


products_tool = Tool(
    name="fetch_all_products",
    func=fetch_all_product_data,
    description=
    """
    This tool fetches all available product data from the backend API.
    It returns a list of products with their details such as:
        - id: Unique identifier of the product
        - name: Name of the product
        - description: A brief description of the product
        - price: Price of the product
        - stock: Quantity of the product available
        - category: The category of the product
        - seller: The seller who is offering the product
        - created_at: When the product was created in the system
        - updated_at: When the product information was last updated

    This tool helps retrieve the product catalog in its entirety, making it useful for displaying products in an 
    inventory system, e-commerce platform, or for analyzing the available products.
    """
)


product_by_id_tool = Tool(
    name="fetch_product_by_productId",
    func=fetch_product_from_id,
    description="""
    Use this tool to retrieve detailed information about a specific product from the backend API, given its product ID.

    Input:
        - product_id (int): The unique identifier of the product.

    Output:
        A dictionary containing detailed information about the product, including:
        - id: Product ID
        - name: Name of the product
        - description: Product description
        - price: Price of the product
        - stock: Current available stock
        - category: Name of the product category
        - seller: Username of the seller
        - created_at: Timestamp when the product was created
        - updated_at: Timestamp when the product was last updated

    This tool is useful when you need information about a specific product, such as for customer inquiries, product pages, or chat-based recommendations.
    """
)


review_by_id_tool = Tool(
    name="fetch_review_by_reviewId",
    func=fetch_review_from_id,
    description="""
    Use this tool to fetch a specific product review using its unique review ID.

    Input:
        - review_id (int): The unique identifier of the review.

    Output:
        A dictionary containing detailed information about the review, including:
        - id: Review ID
        - product_id: ID of the reviewed product
        - user: Username of the reviewer
        - rating: Numerical rating given (e.g., 1 to 5)
        - comment: Text content of the review
        - created_at: Timestamp when the review was submitted

    This tool is useful when you want to retrieve or display a specific review, such as for moderation, response, or detailed analysis.
    """
)


reviews_by_product_tool = Tool(
    name="fetch_reviews_by_productId",
    func=fetch_reviews_from_product_id,
    description="""
    Use this tool to retrieve all customer reviews associated with a specific product, identified by its product ID.

    Input:
        - product_id (int): The unique identifier of the product.

    Output:
        A list of reviews, where each review includes:
        - id: Review ID
        - user: Username of the reviewer
        - rating: Numerical score (e.g., from 1 to 5)
        - comment: Text of the customer’s review
        - created_at: When the review was submitted

    This tool is helpful when users request to see feedback or opinions about a particular product, 
    or when the system needs to evaluate a product’s reputation based on customer experiences.
    """
)

tools = [products_tool, product_by_id_tool, review_by_id_tool, reviews_by_product_tool]

