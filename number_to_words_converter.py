# Custom License - Non-Commercial Use Only  
# Copyright (c) 2025 Sam Afzali

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to use, copy, and distribute the Software for personal, educational, and non-commercial purposes, provided that the original author, Sam Afzali, is credited appropriately.

# Commercial use, modification, resale, or claiming authorship of the Software without explicit written permission from the author is strictly prohibited.

# The Software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the author be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the Software or the use or other dealings in the Software.

# Contact the author for commercial licensing or custom permissions:
# Email: samafzalicode@gmail.com


from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit,
    QPushButton, QMessageBox, QRadioButton, QButtonGroup, QSpacerItem, QSizePolicy, QHBoxLayout
)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt
import sys

# ===== تابع تبدیل عدد به حروف فارسی =====
def number_to_persian_words(number):
    ones = ["", "یک", "دو", "سه", "چهار", "پنج", "شش", "هفت", "هشت", "نه"]
    teens = ["ده", "یازده", "دوازده", "سیزده", "چهارده", "پانزده", "شانزده", "هفده", "هجده", "نوزده"]
    tens = ["", "", "بیست", "سی", "چهل", "پنجاه", "شصت", "هفتاد", "هشتاد", "نود"]
    hundreds = ["", "صد", "دویست", "سیصد", "چهارصد", "پانصد", "ششصد", "هفتصد", "هشتصد", "نهصد"]
    units = ["", "هزار", "میلیون", "میلیارد"]

    if number == 0:
        return "صفر"
    if number >= 1_000_000_000_000:
        return "عدد خیلی بزرگ است"

    def group_to_words(n):
        h = n // 100
        t = (n % 100) // 10
        o = n % 10
        parts = []
        if h:
            parts.append(hundreds[h])
        if t == 1:
            parts.append(teens[o])
        else:
            if t:
                parts.append(tens[t])
            if o:
                parts.append(ones[o])
        return " و ".join(parts)

    num_str = str(number).zfill(((len(str(number)) + 2) // 3) * 3)
    groups = [int(num_str[i:i + 3]) for i in range(0, len(num_str), 3)]
    result = []
    for i, g in enumerate(groups):
        if g == 0:
            continue
        part = group_to_words(g)
        unit = units[len(groups) - i - 1]
        result.append(f"{part} {unit}".strip())
    return " و ".join(result)

# ===== تابع تبدیل عدد به انگلیسی با inflect =====
def number_to_english_words(number):
    import inflect
    p = inflect.engine()
    return p.number_to_words(number)

# ===== تبدیل فارسی به فینگلیش =====
def number_to_finglish_words(persian_text):
    map_dict = {
        "صفر": "sefr", "و": "o",
        "یک": "yek", "دو": "do", "سه": "se", "چهار": "chahar", "پنج": "panj", "شش": "shesh",
        "هفت": "haft", "هشت": "hasht", "نه": "noh", "ده": "dah", "یازده": "yazdah",
        "دوازده": "davazdah", "سیزده": "sizdah", "چهارده": "chahardah", "پانزده": "ponzdah",
        "شانزده": "shanzdah", "هفده": "hefdah", "هجده": "hejdah", "نوزده": "noozdah",
        "بیست": "bist", "سی": "si", "چهل": "chehel", "پنجاه": "panjah", "شصت": "shast",
        "هفتاد": "haftad", "هشتاد": "hashtad", "نود": "navad",
        "صد": "sad", "دویست": "devist", "سیصد": "sisad", "چهارصد": "chaharsad",
        "پانصد": "pansad", "ششصد": "sheshsad", "هفتصد": "haftsad", "هشتصد": "hashtsad", "نهصد": "nohsad",
        "هزار": "hezar", "میلیون": "milyoon", "میلیارد": "milyard"
    }
    words = persian_text.split(" ")
    return " ".join([map_dict.get(w, w) for w in words if w.strip() != ""])


# ===== رابط گرافیکی =====
class NumberToWordsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("تبدیل عدد به حروف")
        self.setGeometry(300, 200, 520, 400)
        self.setLayoutDirection(Qt.RightToLeft)

        # رنگ پس‌زمینه
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#f1f1f1"))
        self.setPalette(palette)

        self.font_family = "IRANSans"  # یا هر فونت فارسی
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(22)

        # باکس ورودی عدد
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("عدد را وارد کنید (مثال: 123456789)")
        self.input_box.setFont(QFont(self.font_family, 11))
        self.input_box.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #ccc;
                border-radius: 10px;
                background-color: #ffffff;
            }
        """)

        # انتخاب زبان با Radio Buttons
        self.lang_group = QButtonGroup(self)
        self.radio_fa = QRadioButton("فارسی")
        self.radio_en = QRadioButton("انگلیسی")
        self.radio_faeng = QRadioButton("فینگلیش")
        self.radio_fa.setChecked(True)

        for radio in [self.radio_fa, self.radio_en, self.radio_faeng]:
            radio.setFont(QFont(self.font_family, 11))
            radio.setStyleSheet("""
                QRadioButton {
                    spacing: 10px;
                    padding: 6px;
                    border-radius: 6px;
                    background-color: #e9f9f5;
                }
                QRadioButton::indicator {
                    width: 16px;
                    height: 16px;
                }
                QRadioButton::checked {
                    background-color: #d1fff0;
                }
            """)
            self.lang_group.addButton(radio)

        # دکمه تبدیل
        self.convert_btn = QPushButton("تبدیل")
        self.convert_btn.setFont(QFont(self.font_family, 12))
        self.convert_btn.setStyleSheet("""
            QPushButton {
                background-color: #0ea480;
                color: white;
                border-radius: 12px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #0cc191;
            }
        """)
        self.convert_btn.clicked.connect(self.convert_number)

        # نمایش خروجی
        self.result_label = QLabel("")
        self.result_label.setWordWrap(True)
        self.result_label.setFont(QFont(self.font_family, 12))
        self.result_label.setStyleSheet("""
            background-color: #ffffff;
            padding: 14px;
            border-radius: 10px;
            border: 1px solid #ddd;
            min-height: 50px;
        """)

        layout.addWidget(self.input_box)
        layout.addWidget(self.radio_fa)
        layout.addWidget(self.radio_en)
        layout.addWidget(self.radio_faeng)
        layout.addWidget(self.convert_btn)
        layout.addWidget(self.result_label)
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # داخل init پنجره:
        footer_label = QLabel("برنامه نویسی شده توسط سام افضلی | Programmed by Sam Afzali")
        footer_label.setStyleSheet("""
            color: #0ea480;
            font-family: IRANSans;
            font-size: 10pt;
        """)
        footer_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)

        footer_layout = QHBoxLayout()
        footer_layout.addStretch()
        footer_layout.addWidget(footer_label)

        layout.addLayout(footer_layout)

        self.setLayout(layout)

    def convert_number(self):
        try:
            number = int(self.input_box.text().strip())
            if number >= 1_000_000_000_000:
                self.result_label.setText("عدد وارد شده بیش از حد بزرگ است.")
                return

            if self.radio_fa.isChecked():
                result = number_to_persian_words(number)
            elif self.radio_en.isChecked():
                result = number_to_english_words(number)
            elif self.radio_faeng.isChecked():
                result = number_to_finglish_words(number_to_persian_words(number))
            else:
                result = "زبان نامشخص"

            self.result_label.setText(result)

        except ValueError:
            QMessageBox.warning(self, "خطا", "لطفاً یک عدد معتبر وارد کنید.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NumberToWordsApp()
    window.show()
    sys.exit(app.exec_())