<p align="center">
  <img src="https://github.com/user-attachments/assets/effe85fb-52ec-48ab-83a3-f4d35c8dd9f4" width="400"/>
</p>

# 🧹 textcleaner

**textcleaner** — это простая и удобная Python-библиотека для очистки текстов от мусора: HTML-тегов, эмодзи, лишних пробелов, стоп-слов, спецсимволов и прочего.

---

## 🚀 Возможности

- Удаление HTML и JavaScript/XSS кода
- Удаление эмодзи и спецсимволов
- Очистка лишних пробелов, табов, переносов строк
- Удаление или замена стоп-слов
- Поддержка кириллицы и латиницы
- Готово для использования в NLP-задачах

---

## 📚 Доступные функции

### 🔹 `clean_text(...)`

Функция для глубокой очистки текста. Поддерживает как одиночную строку, так и списки строк.
```python
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
```
```python
from kangaroo_tools.textcleaner import clean_text

text = "💥 Срочно! Купи сейчас! <b>Скидка 50%</b> только сегодня 😱"
cleaned = clean_text(text, remove_stopwords=True)
print(cleaned)
# Вывод: "срочно купи сейчас скидка только сегодня"
```
---
🔹 print_metrics(...)
Функция для визуализации и анализа метрик модели. Позволяет отобразить:

classification report

confusion matrix

графики потерь и точности

```python
def print_metrics(
    trainer,
    y_true,
    y_pred,
    labels_names=None,
    headers=["label", "precision", "recall", "f1-score", "support"],
    is_classification_report=True,
    is_confusion_matrix=True,
    is_loss_graph=True,
    is_accuracy_graph=True,
    return_report_text=False
):
```
```python
from kangaroo_tools.metrics import print_metrics

report_text = print_metrics(
    trainer=trainer,
    y_true=y_true,
    y_pred=y_pred,
    labels_names=["negative", "neutral", "positive"],
    return_report_text=True
)
print(report_text)
```
---