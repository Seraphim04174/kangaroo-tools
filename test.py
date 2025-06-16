from kangaroo.cleaner.text_cleaner import clean_text

print(clean_text("Привет, мир! 😊 <b>HTML</b>", remove_emojis=True, remove_html=True))
