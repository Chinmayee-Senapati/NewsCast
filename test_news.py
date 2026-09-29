from services.news_service import search_news


articles = search_news("Artificial Intelligence", "en")


for article in articles[:5]:

    print("\nTITLE:", article["title"])
    print("SOURCE:", article["source"])
    print("DATE:", article["date"])
    print("LINK:", article["link"])