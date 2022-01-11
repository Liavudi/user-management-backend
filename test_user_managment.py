import unittest
from user_managment import UserManagment, User


class TestUser(unittest.TestCase):
    pass

# class TestUserManagment(unittest.TestCase):
#     def TestCreateUser(self):
#         self.create = "c"
#         return self.create
#     def TestUpdateName(self):
#         self.update = user_managment.UserManagment.update_user_name()


# Tests done with sahar
class TestUserManagement(unittest.TestCase):
    def setUp(self):
        self.um = UserManagment()

    def test_add_user(self):
        sahar_user = User(name='sahar', age=29)
        self.um.add_user(sahar_user)
        users = self.um.list_users()
        self.assertEquals(1, len(users))
        self.assertEquals(sahar_user, users[0])

    def test_update_user(self):
        sahar_user = User(name='sahar', age=29)
        self.um.add_user(sahar_user)
        self.um.update_user_name('sahar', 'liav')
        users = self.um.list_users()
        self.assertEquals('liav', users[0].name)

    def test_dont_update_non_existing_user(self):
        sahar_user = User(name='sahar', age=29)
        self.um.add_user(sahar_user)
        self.um.update_user_name('sahar2', 'liav')
        users = self.um.list_users()
        self.assertEquals(1, len(users))
        self.assertEquals('sahar', users[0].name)

    def test_delete_user(self):
        sahar_user = User(name='sahar', age=29)
        self.um.add_user(sahar_user)
        exist_user = "sahar"
        self.um.delete_user(exist_user)
        users = self.um.list_users()
        self.assertEquals(0, len(users))

if __name__ == '__main__':
    unittest.main()
