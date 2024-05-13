import os

path_images = os.environ.get('PATH_IMAGES', 'app/Resources/images/')

users = {
    'Библиотекарь': {'name': 'librarian', 'password': 'lib123'},
    'Администратор БД': {'name': 'root', 'password': 'SuaiYarik281_'},
    'Директор Библиотеки': {'name': 'director', 'password': 'director'},
    'Библиограф': {'name': 'bibliographer', 'password': 'bibli123'}
}
