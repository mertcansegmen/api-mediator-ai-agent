from tools.router import route_query
from tools.humanized_api import make_humanized_api_request

print("How can I help you today? You can ask me questions related to the weather, finance, news, and cryptocurrencies.")
user_query = input("> ")

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
    print("Routing to the coin API(CoinCap).")

    response = make_humanized_api_request(user_query, "coincap")
    print("API Mediator response: ", response)
    print()
elif selected_route == "public_holidays":
    print("Routing to the public holidays API(Nager.Date).")

    response = make_humanized_api_request(user_query, "nager")
    print("API Mediator response: ", response)
    print()
else:
    print("I can only answer questions about the weather, finance, news, and cryptocurrencies.")