from sklearn.metrics import (
    classification_report,
    accuracy_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
)
import matplotlib.pyplot as plt
from collections import OrderedDict
from tabulate import tabulate

def _get_classification_report_text(y_true, y_pred, labels_names, headers):
    report = classification_report(
        y_true,
        y_pred,
        target_names=labels_names,
        output_dict=True,
        digits=4
    )

    table = []
    for label in labels_names + ["macro avg", "weighted avg"]:
        row = [label]
        for metric in ["precision", "recall", "f1-score", "support"]:
            row.append(round(report[label][metric], 4))
        table.append(row)

    accuracy = accuracy_score(y_true, y_pred)
    table.append(["accuracy", round(accuracy, 4), "", "", len(y_true)])

    return tabulate(table, headers=headers, tablefmt="github")

def get_epoch_end_loss_table(log_history, key="loss"):
    """
    Возвращает табличку с последними значениями loss на каждой эпохе.
    """
    epoch_loss_map = OrderedDict()

    for log in log_history:
        if key in log and 'epoch' in log:
            epoch = int(log['epoch'])  # округляем до целого (0, 1, 2...)
            epoch_loss_map[epoch] = log[key]  # перезаписываем, останется последнее значение

    loss_table = [(epoch, round(loss, 6)) for epoch, loss in epoch_loss_map.items()]
    return tabulate(loss_table, headers=["Epoch", key.replace('_', ' ').title()], tablefmt="github")

def _get_loss_and_accuracy_text(trainer):
    train_loss = []
    eval_loss = []
    train_acc = []
    eval_acc = []

    for log in trainer.state.log_history:
        if 'loss' in log and 'epoch' in log:
            train_loss.append((log['epoch'], log['loss']))
        if 'eval_loss' in log and 'epoch' in log:
            eval_loss.append((log['epoch'], log['eval_loss']))
        if 'accuracy' in log and 'epoch' in log:
            train_acc.append((log['epoch'], log['accuracy']))  # тренировочная
        if 'eval_accuracy' in log and 'epoch' in log:
            eval_acc.append((log['epoch'], log['eval_accuracy']))  # валидационная

    text = ""

    if train_loss:
        text += "\n📉 Train Loss per Epoch (Final Value):\n"
        text += get_epoch_end_loss_table(trainer.state.log_history, key="loss")

    if eval_loss:
        text += "\n\n🧪 Validation Loss per Epoch:\n"
        text += tabulate(eval_loss, headers=["Epoch", "Validation Loss"], tablefmt="github")

    if train_acc:
        text += "\n\n🏋️‍♂️ Train Accuracy per Epoch:\n"
        text += tabulate([(int(e), round(a, 6)) for e, a in train_acc], headers=["Epoch", "Train Accuracy"],
                         tablefmt="github")

    if eval_acc:
        text += "\n\n✅ Validation Accuracy per Epoch:\n"
        text += tabulate([(int(e), round(a, 6)) for e, a in eval_acc], headers=["Epoch", "Validation Accuracy"],
                         tablefmt="github")

    if not text:
        text = "\n⚠️ Нет данных о loss или accuracy в trainer.state.log_history"
    return text


def _get_confusion_matrix_text(y_true, y_pred, labels_names):
    cm = confusion_matrix(y_true, y_pred)
    cm_table = []

    header = [""] + labels_names
    for i, label in enumerate(labels_names):
        row = [label] + list(cm[i])
        cm_table.append(row)

    text = "\n🔢 Confusion Matrix:\n"
    text += tabulate(cm_table, headers=header, tablefmt="github")
    return text


# Визуальные графики (по желанию)
def _show_confusion_matrix(y_true, y_pred, labels_names):
    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels_names)

    plt.figure(figsize=(6, 5))
    disp.plot(cmap=plt.cm.Blues, values_format='d')
    plt.title("Confusion Matrix")
    plt.grid(False)
    plt.tight_layout()
    plt.show()


def _show_loss_graph(trainer):
    train_loss = []
    train_epochs = []
    eval_loss = []
    eval_epochs = []

    for log in trainer.state.log_history:
        if 'loss' in log and 'epoch' in log:
            train_loss.append(log['loss'])
            train_epochs.append(log['epoch'])
        if 'eval_loss' in log and 'epoch' in log:
            eval_loss.append(log['eval_loss'])
            eval_epochs.append(log['epoch'])

    if train_loss or eval_loss:
        plt.figure(figsize=(8, 5))
        if train_loss:
            plt.plot(train_epochs, train_loss, label='Train Loss', marker='o', alpha=0.7)
        if eval_loss:
            plt.plot(eval_epochs, eval_loss, label='Validation Loss', marker='o', alpha=0.7)
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.title('Training and Validation Loss')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()


def _show_accuracy_graph(trainer):
    eval_acc, eval_acc_epochs = [], []

    for log in trainer.state.log_history:
        if 'eval_accuracy' in log and 'epoch' in log:
            eval_acc.append(log['eval_accuracy'])
            eval_acc_epochs.append(log['epoch'])

    if eval_acc:
        plt.figure(figsize=(8, 5))
        plt.plot(eval_acc_epochs, eval_acc, label='Validation Accuracy', color='green', marker='o')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.title('Validation Accuracy per Epoch')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()


# Главная функция
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
    if labels_names is None:
        labels_names = list(map(str, sorted(set(y_true))))

    parts = []

    if is_classification_report:
        report_text = _get_classification_report_text(y_true, y_pred, labels_names, headers)
        print("\n📋 Classification Report:\n")
        # print(report_text)
        parts.append("📋 Classification Report:\n" + report_text)

    if is_confusion_matrix:
        confusion_text = _get_confusion_matrix_text(y_true, y_pred, labels_names)
        # print(confusion_text)
        parts.append(confusion_text)
        _show_confusion_matrix(y_true, y_pred, labels_names)

    if is_loss_graph or is_accuracy_graph:
        loss_acc_text = _get_loss_and_accuracy_text(trainer)
        # print(loss_acc_text)
        parts.append(loss_acc_text)

    if is_loss_graph:
        _show_loss_graph(trainer)
    if is_accuracy_graph:
        _show_accuracy_graph(trainer)

    if return_report_text:
        return "\n\n".join(parts)
