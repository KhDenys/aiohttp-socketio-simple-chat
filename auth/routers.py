from .views import SignIn, SignUp, SignOut


routes = [
    ('*', '/signin', SignIn, 'signin'),
    ('*', '/signup', SignUp, 'signup'),
    ('*', '/signout', SignOut, 'signout')
]
