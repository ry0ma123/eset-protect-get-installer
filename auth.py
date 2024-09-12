import urllib, getpass, re, json, urllib.request

#Funtions
def validate_email(username):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, username))

#Access Tokenの取得
def auth(username, password):
    auth_url = "https://jpn.business-account.iam.eset.systems/oauth/token"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "password",
        "username": username,
        "password": password,
        "client_id": "",
        "client_secret": "",
        "refresh_token": "",
    }
    data = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(auth_url, data=data, headers=headers)
    with urllib.request.urlopen(req) as response:
        status_code = response.status
        if status_code == 200:
            print(status_code)
            response_data = response.read().decode("utf-8")
            response_json = json.loads(response_data)
            access_token = response_json.get("access_token")
            refresh_token = response_json.get("refresh_token")
            print("Acquired access token")
        else:
            print(f"error: status code is {status_code}")
    return access_token

def get_api_key(access_token):
    return "Bearer " + access_token

def get_eset_installers(token):
    access_token = token
    url = 'https://jpn.installer-management.eset.systems/v1/installers?usable=true&pageSize=1000'
    req = urllib.request.Request(url)
    req.add_header('accept', 'application/json')
    req.add_header('Authorization', f'{access_token}')

    try:
        with urllib.request.urlopen(req) as res:
            body = res.read()
            return json.loads(body)
    except urllib.error.HTTPError as e:
            print(f'Error:status code is {e.code}')
            return None

#グローバル変数
email_check = True
retry = 3

#Main
username = input(f"Please enter your username, the username should be an email address \n")

while email_check is True:    
    check = validate_email(username)
    if retry == 0:
        print("Too many attemps, please check your username and try again")
        raise Exception("Too many attemps! please check your username and rerun the script again.")

    elif check == True:
        password = getpass.getpass(f"Please enter your password: \n")
        break
    
    elif check == False:
        username = input(f"wrong format of the username, please try again \n")
        retry -= 1

access_token = get_api_key(auth(username, password))
print(access_token)


installers = get_eset_installers(access_token)
installers = installers.get("installers", [])
for installer in installers:
    display_name = installer.get("displayName")
    download_url = installer.get("downloadUrl")
    print(f"Display Name: {display_name}")
    print(f"Download URL: {download_url}")