from semantic_router import Route
from semantic_router.encoders import HuggingFaceEncoder
from semantic_router.layer import RouteLayer

encoder = HuggingFaceEncoder(name="sentence-transformers/all-MiniLM-L6-v2")
# encoder = HuggingFaceEncoder(name="BAAI/bge-m3")
# encoder = HuggingFaceEncoder(name="sentence-transformers/all-mpnet-base-v2")
# encoder = HuggingFaceEncoder(name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
# encoder = HuggingFaceEncoder(name="nomic-ai/nomic-embed-text-v1.5")

weather_route = Route(
    name="weather",
    utterances=[
        "Hava durumu nasıl?",
        "Bugün hava nasıl olacak?",
        "Yarın yağmur yağacak mı?",
        "Kar ne zaman yağacak?",
        "İstanbul'da hava durumu nedir?",
        "Hava tahmini nedir?",
        "Bu hafta hava durumu nasıl?",
        "Bugün sıcaklık kaç derece?",
        "Hava açık mı yoksa bulutlu mu?",
        "Yağmur yağacak mı?",
        "Hava rüzgarlı mı olacak?",
        "Sıcaklık tahmini nedir?",
        "Akşam hava soğuyacak mı?",
        "Saatlik hava durumu raporunu ver.",
        "Haftalık hava tahminini paylaş.",
        "Hava durumu güncellemeleri neler?",
        "Nem oranı nedir?",
        "Rüzgar hızı kaç km/saat?",
        "Bölgedeki hava kirliliği nasıl?",
        "Hava durumu raporlarını nasıl alabilirim?",
        "Bugün dışarıda yürüyüş yapmak için uygun mu?",
        "Şehirde buzlanma bekleniyor mu?",
        "Fırtına uyarısı var mı?",
        "Hava durumuyla ilgili özel bir uyarı var mı?",
        "Deniz kenarında hava nasıl olacak?",
        "Saat kaçta güneş doğacak?",
        "Bugün güneş batışı saat kaçta?",
        "Meteoroloji hava raporuna göre durum nedir?",
        "Hava sıcaklığı rekor seviyede mi?",
        "What is the weather like?",
        "How's the weather today?",
        "Will it rain tomorrow?",
        "When will it snow?",
        "What’s the weather forecast for New York?",
        "What’s the temperature right now?",
        "Is it sunny or cloudy?",
        "Will it rain later today?",
        "Is it going to be windy today?",
        "What’s the temperature forecast for tomorrow?",
        "Will it get colder tonight?",
        "Can I get an hourly weather report?",
        "What’s the weekly weather forecast?",
        "Are there any weather updates?",
        "What’s the humidity level?",
        "How strong is the wind?",
        "What’s the air quality like in this area?",
        "Is it a good day for a walk outside?",
        "Is there any risk of ice on the roads?",
        "Are there any storm warnings?",
        "Are there any special weather alerts?",
        "What’s the weather by the sea?",
        "What time is sunrise today?",
        "What time does the sun set today?",
        "What does the meteorological report say?",
        "Is the temperature hitting record levels?",
        "Can I expect snow this week?",
        "What’s the weather going to be like this weekend?",
        "Is it safe to drive with the current weather conditions?",
        "Will there be thunderstorms this evening?",
        "What’s the real feel temperature outside?"
    ]
)

finance_route = Route(
    name="finance",
    utterances=[
        "Dolar kuru nedir?",
        "Borsa bugün nasıl?",
        "Altın fiyatları ne durumda?",
        "Bitcoin fiyatı nedir?",
        "Ekonomi haberleri nelerdir?",
        "Nvidia hisse fiyatı neydi?"
    ]
)

news_route = Route(
    name="news",
    utterances=[
        "Son haberler neler?",
        "Dünya haberleri nedir?",
        "Spor haberleri var mı?",
        "Teknoloji dünyasında neler oluyor?",
        "Politika haberleri nelerdir?"
    ]
)

coin_route = Route(
    name="coin",
    utterances=[
        "Bitcoin fiyatı nedir?",
        "Ethereum'un güncel fiyatı ne kadar?",
        "Son 24 saatte en çok artan kripto para hangisi?",
        "Cardano'nun piyasa değeri ne kadar?",
        "Bitcoin'in son 7 günlük fiyat grafiğini göster.",
        "En büyük 10 kripto para hangileri?",
        "Dogecoin'in tarihsel verilerini getir.",
        "Solana'nın son 1 aylık fiyat değişimi nasıl?",
        "Kripto piyasasının toplam değeri ne kadar?",
        "Binance Coin'in güncel fiyatı nedir?",
        "Polkadot'un son 24 saatteki işlem hacmi ne kadar?",
        "Ripple'ın son 1 yıllık fiyat grafiğini göster.",
        "En popüler 5 kripto para hangileri?",
        "Bitcoin'in son 1 saatteki fiyat değişimi nasıl?",
        "Avalanche'ın piyasa değeri ne kadar?",
        "Kripto para birimlerinin güncel fiyatlarını listele.",
        "Chainlink'in son 30 günlük performansı nasıl?",
        "Uniswap'ın güncel fiyatı nedir?",
        "Kripto piyasasında en çok işlem gören coin hangisi?",
        "Litecoin'in son 1 yıllık fiyat değişimi nasıl?",
        "What is the price of Bitcoin?",
        "What is the current price of Ethereum?",
        "Which cryptocurrency has increased the most in the last 24 hours?",
        "What is the market cap of Cardano?",
        "Show the 7-day price chart of Bitcoin.",
        "What are the top 10 cryptocurrencies?",
        "Get the historical data of Dogecoin.",
        "What is the 1-month price change of Solana?",
        "What is the total market value of the crypto market?",
        "What is the current price of Binance Coin?",
        "What is the 24-hour trading volume of Polkadot?",
        "Show the 1-year price chart of Ripple.",
        "What are the top 5 most popular cryptocurrencies?",
        "What is the 1-hour price change of Bitcoin?",
        "What is the market cap of Avalanche?",
        "List the current prices of cryptocurrencies.",
        "What is the 30-day performance of Chainlink?",
        "What is the current price of Uniswap?",
        "Which cryptocurrency is the most traded in the market?",
        "What is the 1-year price change of Litecoin?"
    ]
)

public_holidays_route = Route(
    name="public_holidays",
    utterances=[
        "What are the next public holidays in the United States?",
        "List all public holidays in Germany for 2024.",
        "Are there any public holidays in Canada in January 2025?",
        "What countries have public holidays on January 1, 2025?",
        "What are the next public holidays worldwide?",
        "What are the public holidays in January 2025 globally?",
        "When is the next public holiday in France?",
        "Is January 1, 2025, a public holiday in Brazil?",
        "Does the United States observe Christmas as a public holiday?",
        "Türkiye'deki resmi tatiller nelerdir?",
        "Almanya'daki 2024 yılı resmi tatil günlerini listele.",
        "Ocak 2025'te Kanada'da resmi tatil var mı?",
        "1 Ocak 2025 tarihinde hangi ülkelerde resmi tatil var?",
        "Dünyadaki bir sonraki resmi tatiller nelerdir?",
        "Ocak 2025'teki küresel resmi tatiller nelerdir?",
        "Fransa'daki bir sonraki resmi tatil ne zaman?",
        "1 Ocak 2025, Brezilya'da resmi tatil mi?",
        "ABD'de Noel resmi tatil olarak kutlanıyor mu?"
    ]
)

routes = [weather_route, finance_route, news_route, coin_route, public_holidays_route]
route_layer = RouteLayer(encoder=encoder, routes=routes)

def route_query(user_query):
    selected_route = route_layer(user_query).name
    return selected_route