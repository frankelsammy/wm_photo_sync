import json
def make_map():
    customer_id_to_name = {}
    with open("accounts.json", "r") as f:
        data = json.load(f)['data']['linkedAccounts']
        for account in data:
            customer_id = format_id(account['custAccountId'])
            customer_name = account['nickName']
            customer_id_to_name[customer_id] = customer_name
    return customer_id_to_name

def format_id(customer_id):
    formatted = customer_id[3:]
    formatted = formatted[0:2] + '-' + formatted[2:7] + '-' + formatted[7:]
    return formatted
print(make_map())
