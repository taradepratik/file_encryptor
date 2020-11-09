# This Project is created by https://github.com/taradepratik
from Crypto import Random
import os
from Crypto.Cipher import AES
import os.path
from os import listdir
from os.path import isfile, join
import time


class Encryptor:
    def __init__(self, key):
        self.key = key

    def pad(self, s):
        return s+b"\0" * (AES.block_size-len(s) % AES.block_size)

    def encrypt(self, message, key, key_size=256):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as en:
            plaintext = en.read()
        enc = self.encrypt(plaintext, self.key)
        with open(file_name + ".enc", 'wb') as en:
            en.write(enc)
        os.remove(file_name)

    def decrypt(self, cipherText, key):
        iv = cipherText[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(cipherText[AES.block_size:])
        return plaintext.rstrip(b"\0")

    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as de:
            cipherText = de.read()
        dec = self.decrypt(cipherText, self.key)
        with open(file_name[:-4], 'wb') as de:
            de.write(dec)
        os.remove(file_name)

    def getAllFiles(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dirs = []
        for dirName, subDirList, fileList in os.walk(dir_path):
            for fname in fileList:
                if(fname != 'crypto.py' and fname != 'com.additional_file.txt.enc'):
                    dirs.append(dirName+"\\"+fname)
        return dirs

    def encrypt_all_files(self):
        dirs = self.getAllFiles()
        for file_name in dirs:
            self.encrypt_file(file_name)

    def decrypt_all_files(self):
        dirs = self.getAllFiles()
        for file_name in dirs:
            self.decrypt_file(file_name)


key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
enc = Encryptor(key)
def clear(): return os.system('cls')


if os.path.isfile('com.additional_file.txt.enc'):
    while True:
        password = str(input("Enter the password: "))
        enc.decrypt_file("com.additional_file.txt.enc")
        p = ""
        with open("com.additional_file.txt") as f:
            p = f.readlines()
        if p[0] == password:
            enc.encrypt_file("com.additional_file.txt")
            break
        else:
            enc.encrypt_file("com.additional_file.txt")
            print("Wrong password!")
            continue

    while True:
        clear()
        choice = int(input(
            '''1. Press "1" to encrypt file.\n2. Press "2" to decrypt file.\n3. Press "3" to encrypt all files.\n4. Press "4" to decrypt all files.\n5. Press "5" to exit.\n''')
        )
        clear()

        if choice == 1:
            x = str(input("Enter the name of the file with extension to enrypt: "))
            if os.path.isfile(x):
                enc.encrypt_file(x)
                print("Enrypted Succesfully")
                time.sleep(2)
            else:
                print("File is not in directory!")
                time.sleep(1)

        elif choice == 2:
            y = str(input("Enter the name of the file with extension to decrypt: "))
            if os.path.isfile(y):
                enc.decrypt_file(y)
                print("Decrypted Succesfully")
                time.sleep(2)
            else:
                print("File is not in directory!")
                time.sleep(2)
        elif choice == 3:
            enc.encrypt_all_files()
            print("Enrypted Succesfully")
            time.sleep(2)
        elif choice == 4:
            enc.decrypt_all_files()
            print("Decrypted Succesfully")
            time.sleep(2)
        elif choice == 5:
            exit()
        else:
            print("please select a valid option!")
            time.sleep(2)

else:
    while True:
        clear()
        password = str(
            input("Setting up, Enter the password that will be use for decryption: "))
        repassword = str(input("confirm Password: "))
        if password == repassword:
            break
        else:
            print("Password Mismatched!")
    f = open("com.additional_file.txt", "w+")
    f.write(password)
    f.close()
    enc.encrypt_file("com.additional_file.txt")
    print("Please restart the program to complete the setup")
