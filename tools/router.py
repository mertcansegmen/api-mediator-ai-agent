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
        "Bugün yağmur yağacak mı?",
        "Yarın İzmir'de hava nasıl olacak?",
        "Sıcaklık nedir?",
        "Hava tahmini nedir?"
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
        "Litecoin'in son 1 yıllık fiyat değişimi nasıl?"
    ]
)

routes = [weather_route, finance_route, news_route, coin_route]
route_layer = RouteLayer(encoder=encoder, routes=routes)

def route_query(user_query):
    selected_route = route_layer(user_query).name
    return selected_route