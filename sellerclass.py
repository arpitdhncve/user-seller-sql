from personclass import Person

class Seller(Person):

    def __init__(self, name, email):
        super().__init__(name, email)

    def add_seller(self):
        return super().add_person("sellers")

    def login_seller(email):
        return Person.login_person(email, "sellers")

    def verify_otp_seller(email, otp):
        return Person.verify_otp(email, otp, "sellers")