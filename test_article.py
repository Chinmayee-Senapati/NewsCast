from services.article_service import extract_article_text


url = "https://apnews.com/article/pope-trump-artificial-intelligence-anthropic-0790f258461d114c920ec6158c2a1921"


text = extract_article_text(url)


print("\n")
print("=" * 60)
print("EXTRACTED ARTICLE")
print("=" * 60)
print("\n")


if text:

    print(text)

    print("\n")
    print("=" * 60)
    print(f"Characters extracted: {len(text)}")
    print("=" * 60)

else:

    print("No article text could be extracted.")