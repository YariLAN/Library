class ReaderMapper(object):
    @staticmethod
    def toMap(name, category_id, address, phone, email):
        names = name.split(" ")
        category_id = int(category_id)
        return Reader(names[0], names[1], names[2], category_id, address, phone, email)


class Reader:
    __tableName__ = "reader"

    def __init__(self, lastName, firstName, patronymic, category_id, address, phone, email):
        self.lastName = lastName
        self.firstName = firstName
        self.patronymic = patronymic
        self.category_id = category_id
        self.address = address
        self.phone = phone
        self.email = email
