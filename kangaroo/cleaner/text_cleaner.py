import re
import string
import html
from typing import Union, Iterable, Optional
import emoji
from nltk.corpus import stopwords
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

# Ручный кэш для стоп-слов
STOPWORDS_CACHE = {}

def get_stopwords(language: str) -> set:
    if language not in STOPWORDS_CACHE:
        try:
            STOPWORDS_CACHE[language] = set(stopwords.words(language))
        except LookupError:
            raise ValueError(f"Стоп-слова для языка '{language}' не найдены. Используйте nltk.download().")
    return STOPWORDS_CACHE[language]


def clean_single_text(
    t: str,
    *,
    remove_html: bool,
    remove_digits: bool,
    to_lower: bool,
    remove_punctuation: bool,
    remove_emojis: bool,
    stop_words: Optional[set]
) -> str:
    if remove_html:
        t = html.unescape(t)
        t = re.sub(r'<.*?>', '', t)

    if remove_emojis:
        t = emoji.replace_emoji(t, replace='')

    if remove_digits:
        t = re.sub(r'\d+', '', t)

    if to_lower:
        t = t.lower()

    if remove_punctuation:
        t = t.translate(str.maketrans('', '', string.punctuation))

    t = re.sub(r'\s+', ' ', t).strip()

    if stop_words:
        tokens = t.split()
        tokens = [word for word in tokens if word not in stop_words]
        t = ' '.join(tokens)

    return t


def batched(iterable, batch_size):
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    if batch:
        yield batch


def clean_text(
    text: Union[str, Iterable[str]],
    remove_html: bool = True,
    remove_digits: bool = True,
    to_lower: bool = True,
    remove_punctuation: bool = True,
    remove_emojis: bool = True,
    remove_stopwords: bool = False,
    stopword_language: Optional[str] = "russian",
    return_stopwords: bool = False,
    batch_size: int = 10000,
    max_workers: int = 4,
    show_progress: bool = True,
) -> Union[str, list[str]]:
    """
    Универсальная функция очистки текста с многопоточностью и батчами.

    Параметры:
    - text: строка или коллекция строк
    - remove_html и другие: параметры очистки
    - batch_size: размер пакета при обработке списков
    - max_workers: число потоков
    - show_progress: отображать прогресс-бар
    """

    if return_stopwords:
        return list(get_stopwords(stopword_language or "russian"))

    stop_words = get_stopwords(stopword_language or "russian") if remove_stopwords else None

    if isinstance(text, str):
        return clean_single_text(
            text,
            remove_html=remove_html,
            remove_digits=remove_digits,
            to_lower=to_lower,
            remove_punctuation=remove_punctuation,
            remove_emojis=remove_emojis,
            stop_words=stop_words
        )

    if not isinstance(text, Iterable):
        raise TypeError("text должен быть строкой или итерируемым объектом строк")

    cleaned_all = []

    total = len(text) if hasattr(text, '__len__') else None
    batches = batched(text, batch_size)

    for batch in tqdm(batches, desc="Cleaning text", total=(total // batch_size + 1 if total else None), disable=not show_progress):
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(
                lambda t: clean_single_text(
                    t,
                    remove_html=remove_html,
                    remove_digits=remove_digits,
                    to_lower=to_lower,
                    remove_punctuation=remove_punctuation,
                    remove_emojis=remove_emojis,
                    stop_words=stop_words
                ),
                batch
            ))
        cleaned_all.extend(results)

    return cleaned_all
