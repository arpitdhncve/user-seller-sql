from personclass import Person

class User(Person):

    def __init__(self, name, email):
        super().__init__(name, email)

    
    def add_user(self):
        return super().add_person("users")

    @staticmethod
    def login_user(email):
        return Person.login_person(email, "users")

    
    @staticmethod
    def verify_user_otp(email, otp):
        return Person.verify_otp(email, otp, "users")
