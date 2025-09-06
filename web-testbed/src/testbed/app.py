import toga
from toga.style import Pack
from toga.style.pack import COLUMN

try:
    import js
except ModuleNotFoundError:
    js = None
try:
    from pyodide.ffi import create_proxy
except ModuleNotFoundError:
    pyodide = None


class HelloWorld(toga.App):
    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN))
        self.label = toga.Label(id="myLabel", text="Test App - Toga Web Testing")
        self.button1 = toga.Button("Hello")
        self.button2 = toga.Button(icon=toga.Icon("resources/star"))

        if js is not None:
            js.window.test_cmd = create_proxy(self.cmd_test)

        main_box.add(self.label)
        main_box.add(self.button1)
        main_box.add(self.button2)
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def cmd_test(self, code):
        local_vars = {}
        try:
            exec(code, {"self": self, "toga": toga}, local_vars)
            return local_vars.get("result", "No result")
        except Exception as e:
            return f"Error: {e}"


def main():
    return HelloWorld()
