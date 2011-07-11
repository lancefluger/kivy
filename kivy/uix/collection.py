'''
Collection
======


The Collection is a :class:`~kivy.uix.collection.Collection` that creates a widget
which will automatically create it's child widgets from the data set in it' s
:data:`Collection.items` property.  For each dict item in the items list, a widget 
will be build using the template set with the :data:`Collection.template` property.

For example.  You can define a new template in your kv file, or register it using 
Builder ::

    [CollectionItem@Label]:
        text: ctx.name

And then in your python code, you can create a Collection, and pass it a list of
dicts to be used for each child, and teh name of your template.  this will create 
teh CollectionWidget, and ad for each item in data, a new child widget built using
teh CollectionItem template ::

    data = [
        {'name': 'item1', 'data':'1'},
        {'name': 'item2', 'data':'2'},
        {'name': 'item3', 'data':'3'},
    ]

    col = Collection(items=data, template="CollectionItem")

Since Collection is a very basic class, that just manages its items list property
to add its child widgets, you can easily use multiple inheritance to e,g. build a 
list/grid using layout classes::

#This will work just like A BoxLayout, and automatically create the child widgets 
#based on the dictionary data in it's items list
class BoxLayoutCollection(Collection, BoxLayout):
    pass

#or use grid layout instead..or use any other widget class you want to be the parent
class GridLayoutCollection(Collection, GridLayout):
    pass

'''

__all__ = ('Collection', )

from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, StringProperty


class Collection(Widget):
    items = ListProperty([])
    template = StringProperty("CollectionItem")

    def __init__(self, **kwargs):
        super(Collection, self).__init__(**kwargs)
        self._widgets_items = {}

    def on_items(self, *args):
        self.clear_widgets()
        for item in self.items:
            w = Builder.template(self.template, **item)
            self.add_widget(w)

