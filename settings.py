import os

path_images = os.environ.get('PATH_IMAGES', 'app/Resources/images/')

users = {
    'Библиотекарь': {'name': 'librarian', 'password': 'lib123'},
    'Администратор БД': {'name': 'root', 'password': 'SuaiYarik281_'},
    'Директор Библиотеки': {'name': 'director', 'password': 'director'},
    'Библиограф': {'name': 'bibliographer', 'password': 'bibli123'}
}

rights_role = {
    'Библиотекарь': ["reader", "issued", "returning_books", "fines"],
    'Директор Библиотеки': ["books", "ibrarians", "discount_type", "fine_type", "category_type"],
    'Библиограф': ["books", "genre", "literature_type"]
}
