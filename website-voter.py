from tkinter import *
import requests
import json

s = requests.session()


# ~~~ GUI Functions ~~~ #

def updateacclist():
    accarr = []
    acclist = ""

    for a in accounts:
        accarr.append([a, "*" * len(accounts[a])])
    for e in accarr:
        acclist = acclist + "\n" + str(accarr.index(e) + 1) + ": " + e[0] + "         " + e[1]
    accs.configure(text=acclist)


def add():
    accname = newacc.get()
    passwd = newpw.get()
    accounts[accname] = passwd
    with open("accounts.json", "w") as outfile:
        json.dump(accounts, outfile)
    updateacclist()


def delete():
    accname = deleteacc.get()
    accounts.pop(accname)
    with open("accounts.json", "w") as outfile:
        json.dump(accounts, outfile)
    updateacclist()


def executevote():
    for a in accounts:
        csrf = get_csrf()
        payload = set_payload(a, accounts[a], csrf)
        login(payload)
        vote(csrf)
        logout()



# ----- ~~~System Functions~~~ ----- #

def get_csrf():
    csrf = s.get("https://examplewebsite.com").cookies["csrf_cookie_name"]
    return csrf


def set_payload(username, password, csrf):
    payload_login = {
        "csrf_token_name": csrf,
        "login_username": username,
        "login_password": password,
        "login_submit": "Log in!"
    }
    return payload_login


def login(payload):
    print("--------" + payload["login_username"])
    response = s.post("https://examplewebsite.com/login", data=payload)
    print("Login:" + str(response.status_code))


def vote(csrf):
    s.get("https://examplewebsite.com/vote")
    payload_vote = {
        "csrf_token_name": csrf,
        "id": "13"
    }
    response = s.post("https://examplewebsite.com/site", data=payload_vote)
    print("Vote:" + str(response.status_code))


def logout():
    response = s.get("https://examplewebsite.com/logout")
    print("Logout:" + str(response.status_code))




# ~~~~ Widget Calls ~~~~ #

# ----- Main Window ----- #
root = Tk()
root.title("Example Website Voter v1.0")
root.geometry("800x600")
root.resizable(width=False, height=False)

# ----- Add ----- #
newacc = Entry(root, width=50, bg="darkblue", fg="white", borderwidth=6)
newacc.pack()
newacc.insert(0, "Enter Account Name")

newpw = Entry(root, width=50, bg="darkred", fg="white", borderwidth=6)
newpw.pack()
newpw.insert(0, "Enter Password")

Button(root, text="Add Account", padx=50, pady=2, command=add, bg="#F8F8F8", fg="black").pack()

# ----- Delete ----- #
deleteacc = Entry(root, text="Choose Account to delete", width=50, bg="darkblue", fg="white", borderwidth=6)
deleteacc.pack()
Button(root, text="Delete Account", padx=50, pady=10, command=delete, bg="#F8F8F8", fg="black").pack()

# ----- Vote ----- #
Button(root, text="Vote!", padx=50, pady=10, command=executevote, bg="#F8F8F8", fg="black").pack()

# ----- Account List ----- #
Label(root, text="Account         Password", width=200).pack()

# ~~~ Access Database ~~~ #
file = open("accounts.json", "r")
accounts = json.load(file)
file.close()
accs = Label(root, text="", pady=10)
accs.pack()
updateacclist()

root.mainloop()
