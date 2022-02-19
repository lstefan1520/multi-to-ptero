import requests
import json
import random

def con_create_allocation(ptero_api_host, apikey, nodeid, ip, port):
    url = '{0}/api/application/nodes/{1}/allocations'.format(ptero_api_host, nodeid)
    headers = {
        "Authorization": "Bearer {0}".format(apikey),
        "Accept": "application/json",
        "Content-Type": "application/json",
        "cookie": "pterodactyl_session=eyJpdiI6InhIVXp5ZE43WlMxUU1NQ1pyNWRFa1E9PSIsInZhbHVlIjoiQTNpcE9JV3FlcmZ6Ym9vS0dBTmxXMGtST2xyTFJvVEM5NWVWbVFJSnV6S1dwcTVGWHBhZzdjMHpkN0RNdDVkQiIsIm1hYyI6IjAxYTI5NDY1OWMzNDJlZWU2OTc3ZDYxYzIyMzlhZTFiYWY1ZjgwMjAwZjY3MDU4ZDYwMzhjOTRmYjMzNDliN2YifQ%253D%253D"
    }
    payload = {'ip': '{0}'.format(ip), 'ports': ['{0}'.format(port)]}
    response = requests.request('POST', url, json=payload, headers=headers)
    if response.status_code != 204:
        exit("Error while creating allocation")
    else:
        print("[INFO] Pterodactyl allocation created")

def con_get_allocation_id(ptero_api_host, apikey, nodeid, ip, port):
    url = '{0}/api/application/nodes/{0}/allocations'.format(ptero_api_host, nodeid)
    headers = {
        "Authorization": "Bearer {0}".format(apikey),
        "Accept": "application/json",
        "Content-Type": "application/json",
        "cookie": "pterodactyl_session=eyJpdiI6InhIVXp5ZE43WlMxUU1NQ1pyNWRFa1E9PSIsInZhbHVlIjoiQTNpcE9JV3FlcmZ6Ym9vS0dBTmxXMGtST2xyTFJvVEM5NWVWbVFJSnV6S1dwcTVGWHBhZzdjMHpkN0RNdDVkQiIsIm1hYyI6IjAxYTI5NDY1OWMzNDJlZWU2OTc3ZDYxYzIyMzlhZTFiYWY1ZjgwMjAwZjY3MDU4ZDYwMzhjOTRmYjMzNDliN2YifQ%253D%253D"
    }
    response = requests.request('GET', url, headers=headers)
    data = json.loads(response.text)
    data = data['data']

    for i in data:
        if i['attributes']['ip'] == ip and i['attributes']['port'] == int(port):
            return (i['attributes']['id'])

def con_user_create(ptero_api_host, apikey, email, first_name, last_name):
    url = '{0}/api/application/users'.format(ptero_api_host)
    headers = {
        "Authorization": "Bearer {0}".format(apikey),
        "Accept": "application/json",
        "Content-Type": "application/json",
        "cookie": "pterodactyl_session=eyJpdiI6InhIVXp5ZE43WlMxUU1NQ1pyNWRFa1E9PSIsInZhbHVlIjoiQTNpcE9JV3FlcmZ6Ym9vS0dBTmxXMGtST2xyTFJvVEM5NWVWbVFJSnV6S1dwcTVGWHBhZzdjMHpkN0RNdDVkQiIsIm1hYyI6IjAxYTI5NDY1OWMzNDJlZWU2OTc3ZDYxYzIyMzlhZTFiYWY1ZjgwMjAwZjY3MDU4ZDYwMzhjOTRmYjMzNDliN2YifQ%253D%253D"
    }
    # generate random username
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5']
    num = int(8)
    username = random.sample(letters, num)
    username = ''.join([str(elem) for elem in username])

    payload = {'email': '{0}'.format(email), 'username': '{0}'.format(username), 'first_name': '{0}'.format(first_name), 'last_name': '{0}'.format(last_name)}
    response = requests.request('POST', url, json=payload, headers=headers)
    if response.status_code != 201 and response.status_code != 422:
        exit("Error while creating user")
    else:
        print("[INFO] Pterodactyl user account created")

def con_get_user_id(ptero_api_host, apikey, email):
    url = '{0}/api/application/users'.format(ptero_api_host)
    headers = {
        "Authorization": "Bearer {0}".format(apikey),
        "Accept": "application/json",
        "Content-Type": "application/json",
        "cookie": "pterodactyl_session=eyJpdiI6InhIVXp5ZE43WlMxUU1NQ1pyNWRFa1E9PSIsInZhbHVlIjoiQTNpcE9JV3FlcmZ6Ym9vS0dBTmxXMGtST2xyTFJvVEM5NWVWbVFJSnV6S1dwcTVGWHBhZzdjMHpkN0RNdDVkQiIsIm1hYyI6IjAxYTI5NDY1OWMzNDJlZWU2OTc3ZDYxYzIyMzlhZTFiYWY1ZjgwMjAwZjY3MDU4ZDYwMzhjOTRmYjMzNDliN2YifQ%253D%253D"
    }

    response = requests.request('GET', url, headers=headers)
    data = json.loads(response.text)

    for i in data['data']:
        if i['attributes']['email'] == email:
            return (i['attributes']['id'])

def con_create_server(ptero_api_host, apikey, name, user, nestid, egg, memory, swap, disk, io, cpu, databases, backups, allocations, allocation_id):
    # Retrieve egg information
    url = '{0}/api/application/nests/{1}/eggs/{2}?include=variables'.format(ptero_api_host, nestid, egg)
    headers = {
        "Authorization": "Bearer {0}".format(apikey),
        "Accept": "application/json",
        "Content-Type": "application/json",
        "cookie": "pterodactyl_session=eyJpdiI6InhIVXp5ZE43WlMxUU1NQ1pyNWRFa1E9PSIsInZhbHVlIjoiQTNpcE9JV3FlcmZ6Ym9vS0dBTmxXMGtST2xyTFJvVEM5NWVWbVFJSnV6S1dwcTVGWHBhZzdjMHpkN0RNdDVkQiIsIm1hYyI6IjAxYTI5NDY1OWMzNDJlZWU2OTc3ZDYxYzIyMzlhZTFiYWY1ZjgwMjAwZjY3MDU4ZDYwMzhjOTRmYjMzNDliN2YifQ%253D%253D"
    }
    response = requests.request('GET', url, headers=headers)
    data = json.loads(response.text)
    docker_image = data['attributes']['docker_image']
    startup_cmd = data['attributes']['startup']

    # Get startup variables
    # TODO: Change this to ask user to supply the startup parmas instead of using the default values
    envdata = {}
    for i in data['attributes']['relationships']['variables']['data']:
        env = i['attributes']['env_variable']
        default = i['attributes']['default_value']
        envdata[env] = default

    url = '{0}/api/application/servers'.format(ptero_api_host)
    headers = {
        "Authorization": "Bearer {0}".format(apikey),
        "Accept": "application/json",
        "Content-Type": "application/json",
        "cookie": "pterodactyl_session=eyJpdiI6InhIVXp5ZE43WlMxUU1NQ1pyNWRFa1E9PSIsInZhbHVlIjoiQTNpcE9JV3FlcmZ6Ym9vS0dBTmxXMGtST2xyTFJvVEM5NWVWbVFJSnV6S1dwcTVGWHBhZzdjMHpkN0RNdDVkQiIsIm1hYyI6IjAxYTI5NDY1OWMzNDJlZWU2OTc3ZDYxYzIyMzlhZTFiYWY1ZjgwMjAwZjY3MDU4ZDYwMzhjOTRmYjMzNDliN2YifQ%253D%253D"
    }
    payload = {'name': '{0}'.format(name), 'user': '{0}'.format(user), 'egg': '{0}'.format(egg), 'docker_image': '{0}'.format(docker_image), 'startup': '{0}'.format(startup_cmd), 'environment': envdata, 'limits': {'memory': '{0}'.format(memory), 'swap': '{0}'.format(swap), 'disk': '{0}'.format(disk), 'io': '{0}'.format(io), 'cpu': '{0}'.format(cpu)}, 'feature_limits': {'databases': '{0}'.format(databases), 'backups': '{0}'.format(backups), 'allocations': '{0}'.format(allocations)}, 'allocation': {'default': '{0}'.format(allocation_id)} }
    response = requests.request('POST', url, json=payload, headers=headers)
    data = json.loads(response.text)

    if response.status_code != 201:
        print(response.text)
        exit("Error while creating server")
    else:
        print("[INFO] Pterodactyl server created")
        return data['attributes']['uuid'], data['attributes']['external_id'], data['attributes']['id'], data['attributes']['identifier']

def create_ptero_db(ptero_api_host, apikey, db_name, serverid, databaseid):
    url = '{0}/api/application/servers/{1}/databases?include=password'.format(ptero_api_host, serverid)
    headers = {
        "Authorization": "Bearer {0}".format(apikey),
        "Accept": "application/json",
        "Content-Type": "application/json",
        "cookie": "pterodactyl_session=eyJpdiI6InhIVXp5ZE43WlMxUU1NQ1pyNWRFa1E9PSIsInZhbHVlIjoiQTNpcE9JV3FlcmZ6Ym9vS0dBTmxXMGtST2xyTFJvVEM5NWVWbVFJSnV6S1dwcTVGWHBhZzdjMHpkN0RNdDVkQiIsIm1hYyI6IjAxYTI5NDY1OWMzNDJlZWU2OTc3ZDYxYzIyMzlhZTFiYWY1ZjgwMjAwZjY3MDU4ZDYwMzhjOTRmYjMzNDliN2YifQ%253D%253D"
    }
    payload = {'database': '{0}'.format(db_name), 'remote': '%', 'host': '{0}'.format(databaseid)}
    response = requests.request('POST', url, json=payload, headers=headers)
    data = json.loads(response.text)
    if response.status_code != 201:
        exit("Error while creating database")
    else:
        print("[INFO] Pterodactyl database created")
        return data['attributes']['database'], data['attributes']['username'], data['attributes']['relationships']['password']['attributes']['password']
