from random import randint
from database import create_connection
import sqlite3
from sqlite3 import Error
from abc import ABC








class Person(ABC):

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.verifyOtp = False



    def add_person(self, table_name):
          with create_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM {table_name} WHERE email = ?", (self.email,))
                user = cursor.fetchone()
                print(user)
                if user:
                    if user["verifyOtp"] == 1:
                        return "Email already registered", False
                    else:

                        new_otp = Person.generate_otp()
                        cursor.execute(f"UPDATE {table_name} SET otp = ? WHERE email = ?", (new_otp, self.email))
                        return "User already there but not verified", True
                
                cursor.execute(f"INSERT INTO {table_name} (name, email, verifyOtp, otp) VALUES (?,?,?, ?)", (self.name, self.email, self.verifyOtp, Person.generate_otp()))
                conn.commit()
                return "User created Successfully", True
            except Error as e:
                conn.rollback()
                return str(e), False

    

    @staticmethod
    def login_person(email, table_name):
       with create_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM {table_name} WHERE email = ? AND verifyOtp = 1", (email,))
                user = cursor.fetchone()
                if user:
                   new_otp = Person.generate_otp()
                   cursor.execute(f"UPDATE {table_name} SET otp = ? WHERE  email = ?", (new_otp, email))
                   conn.commit()
                   return "OTP Send", True
                else:
                    return "User don't exist, please register", False
            
            except Error as e:
                conn.rollback()
                return str(e), False



    @staticmethod
    def generate_otp():
        return randint(1001, 9999)



    @staticmethod
    def verify_otp(email, otp, table_name):
        with create_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM {table_name} WHERE email = ?", (email,))
                user = cursor.fetchone()
                print(user)
                if user:
                    if user["otp"] == otp:
                        cursor.execute(f"UPDATE {table_name} SET verifyOtp = ? , otp = ? WHERE email = ?", (True, None, email))
                        conn.commit()
                        return "OTP Verfied", True
                    else:
                        return "Wrong OTP", False
                else:
                    return "User Does Not Exist", False
            except Error as e:
                conn.rollback()
                return str(e), False

    
    












  



    
    
        