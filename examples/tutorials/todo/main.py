import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty


class TodoItem(BoxLayout):
    text = StringProperty("")
    done = BooleanProperty(False)


class TodoList(BoxLayout):
    todo_layout = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def add_todo(self, text, done=False):
        todo = TodoItem(text=text, done=done)
        self.todo_layout.add_widget(todo)
        self.text_input.text = ''

    def __iter__(self):
        for item in self.todo_layout.children:
            item_data = {'text': item.text, 'done': item.done}
            yield item_data


class TodoApp(App):
    def build(self):
        self.todo_list = TodoList()
        self.load()
        return self.todo_list

    def save(self, fname='todos.json'):
        todos = [todo for todo in self.todo_list]
        json.dump(todos, open(fname, 'w'))

    def load(self, fname="todos.json"):
        todos = json.load(open(fname, 'r'))
        for todo in reversed(todos):
            self.todo_list.add_todo(todo['text'], todo['done'])


if __name__ in ('__main__'):
    TodoApp().run()
