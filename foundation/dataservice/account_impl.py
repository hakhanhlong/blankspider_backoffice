from ..database.account import ACCOUNTS

def get_by_username(username):
    ac = ACCOUNTS.objects(username=username).first()
    return ac

def get_by_id(id):
    p = ACCOUNTS.objects(id=id).first()
    return p