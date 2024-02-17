import tkinter as tk
import tkinter.scrolledtext as scrolledtext
import pyperclip
from googletrans import Translator

class TextTransformer:
    TRANSLIT_DICT = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh',
        'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
        'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts',
        'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu',
        'я': 'ya',
    }

    DIGIT_DICT = {
        'а': '4', 'б': '6', 'в': 'B', 'г': 'r', 'д': 'D', 'е': '3', 'ё': 'e', 'ж': '<<',
        'з': '3', 'и': 'u', 'й': 'n', 'к': 'k', 'л': 'JI', 'м': 'M', 'н': 'H', 'о': '0',
        'п': 'n', 'р': 'p', 'с': 'c', 'т': 'T', 'у': 'y', 'ф': 'qp', 'х': 'X', 'ц': 'u',
        'ч': '4', 'ш': 'LLI', 'щ': 'LLIb', 'ъ': '^', 'ы': 'b', 'ь': 'b', 'э': '3', 'ю': 'IO',
        'я': '9',
    }

    TRANSLIT_REVERSE_DICT = {
        'q': 'й', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е', 'y': 'н', 'u': 'г', 'i': 'ш',
        'o': 'щ', 'p': 'з', '[': 'х', ']': 'ъ', 'a': 'ф', 's': 'ы', 'd': 'в', 'f': 'а',
        'g': 'п', 'h': 'р', 'j': 'о', 'k': 'л', 'l': 'д', ';': 'ж', "'": 'э', 'z': 'я',
        'x': 'ч', 'c': 'с', 'v': 'м', 'b': 'и', 'n': 'т', 'm': 'ь', ',': 'б', '.': 'ю',
        '/': '.', 'Q': 'Й', 'W': 'Ц', 'E': 'У', 'R': 'К', 'T': 'Е', 'Y': 'Н', 'U': 'Г',
        'I': 'Ш', 'O': 'Щ', 'P': 'З', '{': 'Х', '}': 'Ъ', 'A': 'Ф', 'S': 'Ы', 'D': 'В',
        'F': 'А', 'G': 'П', 'H': 'Р', 'J': 'О', 'K': 'Л', 'L': 'Д', ':': 'Ж', '"': 'Э',
        'Z': 'Я', 'X': 'Ч', 'C': 'С', 'V': 'М', 'B': 'И', 'N': 'Т', 'M': 'Ь', '<': 'Б',
        '>': 'Ю', '?': ',',
    }

    @staticmethod
    def translit(text):
        result = []
        for char in text:
            if char.lower() in TextTransformer.TRANSLIT_DICT:
                if char.isupper():
                    result.append(TextTransformer.TRANSLIT_DICT[char.lower()].upper())
                else:
                    result.append(TextTransformer.TRANSLIT_DICT[char])
            else:
                result.append(char)
        return ''.join(result)

    @staticmethod
    def digitize(text):
        result = []
        for char in text:
            if char.lower() in TextTransformer.DIGIT_DICT:
                result.append(TextTransformer.DIGIT_DICT[char.lower()])
            else:
                result.append(char)
        return ' '.join(result)

    @staticmethod
    def translate_to_english(text):
        translator = Translator()
        translated = translator.translate(text, src='ru', dest='en')
        return translated.text

    @staticmethod
    def decode(text):
        result = []
        for char in text:
            if char in TextTransformer.TRANSLIT_REVERSE_DICT:
                result.append(TextTransformer.TRANSLIT_REVERSE_DICT[char])
            else:
                result.append(char)
        return ''.join(result)


def transform_text():
    user_input = input_text.get("1.0", tk.END).strip()
    transformation_choice = transformation_var.get()

    if transformation_choice == "Транслит":
        result = TextTransformer.translit(user_input)
    elif transformation_choice == "Цифры":
        result = TextTransformer.digitize(user_input)
    elif transformation_choice == "Перевод на английский":
        result = TextTransformer.translate_to_english(user_input)
    elif transformation_choice == "Декодировать":
        result = TextTransformer.decode(user_input)
    else:
        result = "Выберите тип трансформации!"

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)


def copy_to_clipboard():
    text_to_copy = output_text.get("1.0", tk.END).strip()
    pyperclip.copy(text_to_copy)


# Создание главного окна
root = tk.Tk()
root.title("Text Transformer")

input_text = scrolledtext.ScrolledText(root, width=40, height=5, wrap=tk.WORD)
input_text.pack(pady=5)

transformation_var = tk.StringVar()
transformation_choices = ["Транслит", "Цифры", "Перевод на английский", "Декодировать"]
for choice in transformation_choices:
    rb = tk.Radiobutton(root, text=choice, variable=transformation_var, value=choice)
    rb.pack(anchor="w")

transform_button = tk.Button(root, text="Трансформировать", command=transform_text)
transform_button.pack(pady=5)

output_text = scrolledtext.ScrolledText(root, width=40, height=5, wrap=tk.WORD)
output_text.pack(pady=5)

copy_button = tk.Button(root, text="Копировать", command=copy_to_clipboard)
copy_button.pack(pady=5)

root.mainloop()
