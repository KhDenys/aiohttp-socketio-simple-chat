from .views import ChatView


routes = [
    ('*', '/', ChatView, 'index'),
]
