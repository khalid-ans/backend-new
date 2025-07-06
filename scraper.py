import requests
from bs4 import BeautifulSoup
import logging
import time

logger = logging.getLogger(__name__)

def get_price(medicine):
    try:
        query = medicine.replace(" ", "+")
        url = f"https://www.1mg.com/search/all?name={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        # Add timeout to prevent hanging
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try multiple possible price selectors
        price_selectors = [
            "div[class*='price-tag']",
            "span[class*='price']",
            ".price",
            "[class*='price']"
        ]
        
        price_tag = None
        for selector in price_selectors:
            price_tag = soup.select_one(selector)
            if price_tag:
                break
        
        if price_tag:
            price_text = price_tag.text.strip()
            logger.info(f"Found price for {medicine}: {price_text}")
            return price_text
        else:
            logger.warning(f"No price found for {medicine}")
            return "₹0"
            
    except requests.exceptions.Timeout:
        logger.error(f"Timeout while fetching price for {medicine}")
        return "₹0"
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error for {medicine}: {str(e)}")
        return "₹0"
    except Exception as e:
        logger.error(f"Unexpected error while fetching price for {medicine}: {str(e)}")
        return "₹0" 