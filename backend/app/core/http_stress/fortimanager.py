import requests

def create_object():
    url = "https://10.28.84.10/jsonrpc"
    headers = {"Content-Type": "application/json"}
    payload = {
        "method": "add",
        "params": [{
            "url": "/pm/config/adom/root/obj/firewall/address",
            "data": [{
                "name": "H_1.2.3.4",
                "subnet": "1.2.3.4/32",
                "type": "ipmask"
            }]
        }],
        "id": 1,
        "session": "fxxx voir fonction gitlab bnp"
    }

    response = requests.post(url, json=payload, headers=headers, verify=False)
    print("create host:", response.json())

def create_rule():
    
    url = "https://10.28.84.10/jsonrpc"
    headers = {"Content-Type": "application/json"}
    payload = {
        "method": "add",
        "params": [{
            "url": "/pm/config/adom/root/pkg/your-policy-package/firewall/policy",
            "data": [{
                "name": "loadtest-rule",
                "srcaddr": ["H_1.2.3.4"],
                "dstaddr": ["H_1.2.3.4"],
                "service": ["ALL"],
                "action": "accept",
                "srcintf": ["any"],
                "dstintf": ["any"],
                "schedule": "always",
                "nat": "enable"
            }]
        }],
        "id": 2,
        "session": "fxxx voir fonction gitlab bnp"
    }

    response = requests.post(url, json=payload, headers=headers, verify=False)
    # todo: parsing en fonction de response si connection ou pas + returned code et update le test dans la bdd
    print("create rule:", response.json())