from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window

# ──── لون الخلفية ────
Window.clearcolor = (0.12, 0.12, 0.15, 1)


class CalculatorApp(App):
    def build(self):
        # ──── المتغيرات ────
        self.expression = ""
        self.current = ""

        # ──── الحاوية الرئيسية ────
        root = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # ──── عنوان التطبيق ────
        title = Label(
            text="Calculator",
            font_size=22,
            size_hint_y=0.08,
            color=(0.7, 1, 0.7, 1),
            bold=True,
        )
        root.add_widget(title)

        # ──── شاشة العرض ────
        display_box = BoxLayout(
            orientation="vertical",
            size_hint_y=0.15,
            padding=5,
        )

        self.lbl_expression = Label(
            text="",
            font_size=20,
            halign="left",
            valign="middle",
            color=(0.6, 0.6, 0.6, 1),
            size_hint_y=0.4,
        )

        self.lbl_result = Label(
            text="0",
            font_size=36,
            halign="right",
            valign="middle",
            color=(1, 1, 1, 1),
            bold=True,
            size_hint_y=0.6,
        )

        display_box.add_widget(self.lbl_expression)
        display_box.add_widget(self.lbl_result)
        root.add_widget(display_box)

        # ──── أزرار الحاسبة ────
        btn_grid = GridLayout(cols=4, spacing=8, size_hint_y=0.72)

        buttons = [
            ("C",  (0.9, 0.3, 0.3, 1),  "action"),
            ("+/-", (0.6, 0.6, 0.6, 1), "action"),
            ("%",   (0.6, 0.6, 0.6, 1), "action"),
            ("/",  (1.0, 0.6, 0.0, 1),  "operator"),

            ("7",  (0.25, 0.25, 0.3, 1), "number"),
            ("8",  (0.25, 0.25, 0.3, 1), "number"),
            ("9",  (0.25, 0.25, 0.3, 1), "number"),
            ("*",  (1.0, 0.6, 0.0, 1),  "operator"),

            ("4",  (0.25, 0.25, 0.3, 1), "number"),
            ("5",  (0.25, 0.25, 0.3, 1), "number"),
            ("6",  (0.25, 0.25, 0.3, 1), "number"),
            ("-",  (1.0, 0.6, 0.0, 1),  "operator"),

            ("1",  (0.25, 0.25, 0.3, 1), "number"),
            ("2",  (0.25, 0.25, 0.3, 1), "number"),
            ("3",  (0.25, 0.25, 0.3, 1), "number"),
            ("+",  (1.0, 0.6, 0.0, 1),  "operator"),

            ("0",  (0.25, 0.25, 0.3, 1), "number"),
            (".",  (0.25, 0.25, 0.3, 1), "number"),
            ("DEL", (0.4, 0.4, 0.45, 1), "action"),
            ("=",  (0.2, 0.8, 0.3, 1),  "equals"),
        ]

        for text, color, category in buttons:
            btn = Button(
                text=text,
                font_size=28,
                background_color=color,
                background_normal="",
                color=(1, 1, 1, 1),
            )
            if category == "number":
                btn.bind(on_press=self.on_number)
            elif category == "operator":
                btn.bind(on_press=self.on_operator)
            elif category == "action":
                btn.bind(on_press=self.on_action)
            elif category == "equals":
                btn.bind(on_press=self.on_equals)
            btn_grid.add_widget(btn)

        root.add_widget(btn_grid)
        return root

    # ──── وظائف الأزرار ────

    def on_number(self, instance):
        """عند الضغط على رقم أو نقطة"""
        if self.current == "0" and instance.text != ".":
            self.current = instance.text
        else:
            self.current += instance.text
        self.lbl_result.text = self.current

    def on_operator(self, instance):
        """عند الضغط على عامل (+ - * /)"""
        if self.current:
            self.expression += self.current + " " + instance.text + " "
            self.lbl_expression.text = self.expression
            self.current = ""

    def on_action(self, instance):
        """عند الضغط على C أو +/- أو % أو DEL"""
        text = instance.text

        if text == "C":
            self.expression = ""
            self.current = ""
            self.lbl_expression.text = ""
            self.lbl_result.text = "0"

        elif text == "DEL":
            if self.current:
                self.current = self.current[:-1]
                if not self.current:
                    self.current = ""
                    self.lbl_result.text = "0"
                else:
                    self.lbl_result.text = self.current

        elif text == "+/-":
            if self.current:
                if self.current.startswith("-"):
                    self.current = self.current[1:]
                else:
                    self.current = "-" + self.current
                self.lbl_result.text = self.current

        elif text == "%":
            if self.current:
                try:
                    value = float(self.current) / 100
                    self.current = str(value)
                    self.lbl_result.text = self.current
                except ValueError:
                    pass

    def on_equals(self, instance):
        """عند الضغط على = لحساب النتيجة"""
        if not self.current and not self.expression:
            return

        full_expr = self.expression + self.current

        try:
            result = eval(full_expr)
            if isinstance(result, float) and result == int(result):
                result = int(result)
            self.lbl_expression.text = full_expr + " ="
            self.lbl_result.text = str(result)
            self.current = str(result)
            self.expression = ""
        except ZeroDivisionError:
            self.lbl_result.text = "Error: div by 0"
            self.current = ""
            self.expression = ""
        except Exception:
            self.lbl_result.text = "Error"
            self.current = ""
            self.expression = ""


if __name__ == "__main__":
    CalculatorApp().run()
