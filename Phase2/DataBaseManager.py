import sqlite3
from hashlib import blake2b
from hmac import compare_digest
import os
from dotenv import load_dotenv
load_dotenv()


class DataBaseManager:
    def __init__(self, databasename):
        con = sqlite3.connect(f"{databasename}.db")
        self.cur = con.cursor()

        # a = self.cur.execute("SELECT id, name FROM users").fetchone()
        #
        # print(type(a))
        # print(a)
        # print(f"{a[0]}{a[1]}")

        self.__superSecretHashKey = os.getenv('HASH_KEY')

    # Creds is tuple of the user ID, and the secret hash
    # The secret hash is the users first name hashed in sha256 using his last name
    def __sign(self, cookie):
        a = f"asdasd{self.__superSecretHashKey}"
        h = blake2b(digest_size=16, key=bytearray(a.encode()))
        h.update(bytearray(cookie.encode()))
        return h.hexdigest().encode('utf-8')

    def verify(self, cookie, sig):
        good_sig = self.__sign(cookie)
        return compare_digest(good_sig, sig)

    def sign_user(self, userId):
        data = self.cur.execute(f"SELECT id, name FROM users WHERE id = {userId}").fetchone()
        cookie = f"id:{data[0]}-user:{data[1]}"

        return self.__sign(cookie)




dbm = DataBaseManager("users")

print(dbm.sign_user(2))

