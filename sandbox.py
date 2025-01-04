from tools.router import route_query
from api_request_builders.coincap import generate_human_readable_response

user_query = "What was the Bitcoin price on April 20, 2024?"
user_query = "Fetch the historical data for Cardano."
user_query = "Get the price of Dogecoin."
user_query = "What was the price of Bitcoin at 12:00 PM UTC on April 20, 2024?" # TODO: does not work for some reason.
user_query = "What was the Bitcoin price on April 20, 2024?"
user_query = "Market payına göre en büyük 10 coin'i getir."
user_query = "Get the top 10 cryptocurrencies by market cap."
user_query = "Show me the hourly price data for Bitcoin for the last 24 hours."
user_query = "Fetch the historical data for Bitcoin and Ethereum for the last month."
user_query = "Get the prices of Bitcoin, Ethereum, and Litecoin."
user_query = "Fetch the latest data for Ethereum."
user_query = "Show me the historical data for Ethereum for the last 7 days."
user_query = "Get the current price of Bitcoin."
user_query = "10 ocak 2023'te solana fiyatı neydi"
user_query = "bitcoinin fiyatı ne"
user_query = "bitcoinin fiyatı haftaya ne olur"
user_query = "What was the Bitcoin price on April 20, 2024?"
user_query = "Fetch the price of Ethereum at midnight on January 2, 2023." # TODO: January 1, 2023 çalışmıyor, ama sorun API'de.
user_query = "What was the price of Bitcoin at 12:00 PM UTC on April 20, 2024?" 
user_query = "20 Nisan 2024 gece yarısında Bitcoin fiyatı neydi?"
user_query = "Naber?"
user_query = "Tell me a joke about Bitcoin."

print("User query: ", user_query)
print()

selected_route = route_query(user_query)
print("Selected route: ", selected_route)
print()

if selected_route == "weather":
    print("Routing to the weather API.")
elif selected_route == "finance":
    print("Routing to the finance API.")
elif selected_route == "news":
    print("Routing to the news API.")
elif selected_route == "coin":
    print("Routing to the coin API.")

    response = generate_human_readable_response(user_query)
    print("API Mediator response: ", response)
    print()

else:
    print("I can only answer questions about the weather, finance, news, and cryptocurrencies.")