import hashlib
import json
from tqdm import tqdm

def decrypt(pass_md5, pass_salt):
    with open("./words_dictionary.json") as f:
        english_vocabulary = json.load(f)

    for word in tqdm(english_vocabulary.keys()):
        possible_psw = word+pass_salt
        result = hashlib.md5(possible_psw.encode())
        if result.hexdigest() == pass_md5:
            print("Password found: ", word)
            break


if __name__ == "__main__":
    decrypt("f2b31b3a7a7c41093321d0c98c37f5ad", "yhbG")