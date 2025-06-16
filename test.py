from kangaroo.cleaner.text_cleaner import clean_text

text = "Это очень важное сообщение"
result = clean_text(text, remove_stopwords=True, stopword_language="russian")

print(result)
