import pytest
from kangaroo.cleaner.text_cleaner import clean_text

# Простейшие строки
simple_text = "Привет, мир! 123 😊 <b>Текст</b>"
list_of_texts = ["Тест №1 😁", "HTML <div>пример</div>", "СТОП слова нужно убрать!"]

list_input = ['горячие новости читать срочно', 'купи сейчас скидка только сегодня', 'это фантастика я не ожидал честно', 'апреля года — человек в космосе', 'alerthackтекст с потенциальным xss', 'год был сложным но продуктивным', 'обзор смартфона samsung galaxy s гбгб snapdragon', 'hello world python ai', 'плохой сервис ужасный магазин', 'много пробелов и табов', 'просто текст без всего', 'россия казахстан и украина — страны снг', 'html внутри html', '', '']
list_output = ['горячие новости читать срочно', 'купи скидка сегодня', 'это фантастика ожидал честно', 'апреля года — человек космосе', 'alerthackтекст потенциальным xss', 'год сложным продуктивным', 'обзор смартфона samsung galaxy s гбгб snapdragon', 'hello world python ai', 'плохой сервис ужасный магазин', 'пробелов табов', 'просто текст', 'россия казахстан украина — страны снг', 'html внутри html', '', '']
def test_clean_single_string():
    result = clean_text("Привет, мир! 123 😊", remove_digits=True, remove_emojis=True)
    assert "123" not in result
    assert "😊" not in result
    assert isinstance(result, str)

def test_remove_html():
    text = "<p>Это <b>важно</b></p>"
    cleaned = clean_text(text, remove_html=True)
    assert "<" not in cleaned and ">" not in cleaned

def test_remove_stopwords():
    text = "Это очень важное сообщение"
    result = clean_text(text, remove_stopwords=True, stopword_language="russian")
    assert "это очень важное сообщение" in result.lower()

def test_return_stopwords():
    sw = clean_text("", return_stopwords=True, stopword_language="russian")
    assert isinstance(sw, list)
    assert "и" in sw  # Слово "и" точно есть в большинстве списков стоп-слов

def test_list_of_texts_multithreaded():
    result = clean_text(
        list_of_texts,
        remove_html=True,
        remove_digits=True,
        remove_emojis=True,
        remove_stopwords=True,
        stopword_language="russian",
        batch_size=2,
        max_workers=2
    )
    assert isinstance(result, list)
    assert all(isinstance(r, str) for r in result)
    assert "😁" not in result[0]
    assert "<div>" not in result[1]
    assert "СТОП" not in result[2].lower()

def test_invalid_input_type():
    with pytest.raises(TypeError):
        clean_text(12345)

def test_large_batch():
    texts = ["Пример текста №{} 😊 <div>html</div>".format(i) for i in range(100)]
    cleaned = clean_text(texts, batch_size=10, max_workers=4)
    assert len(cleaned) == 100
    assert all("😊" not in t and "<div>" not in t for t in cleaned)

@pytest.mark.parametrize("input_text,expected_output", [
    ('горячие новости читать срочно', 'горячие новости читать срочно'),
    ('купи сейчас скидка только сегодня', 'купи скидка сегодня'),
    ('это фантастика я не ожидал честно', 'это фантастика ожидал честно'),
    ('апреля года — человек в космосе', 'апреля года — человек космосе'),
    ('alerthackтекст с потенциальным xss', 'alerthackтекст потенциальным xss'),
    ('год был сложным но продуктивным', 'год сложным продуктивным'),
    ('обзор смартфона samsung galaxy s гбгб snapdragon', 'обзор смартфона samsung galaxy s гбгб snapdragon'),
    ('hello world python ai', 'hello world python ai'),
    ('плохой сервис ужасный магазин', 'плохой сервис ужасный магазин'),
    ('много пробелов и табов', 'пробелов табов'),
    ('просто текст без всего', 'просто текст'),
    ('россия казахстан и украина — страны снг', 'россия казахстан украина — страны снг'),
    ('html внутри html', 'html внутри html'),
    ('', ''),
    ('', '')
])
def test_clean_text_expected_output(input_text, expected_output):
    cleaned = clean_text(input_text, remove_stopwords=True, stopword_language="russian")
    assert cleaned == expected_output