import requests
users = ['bulbulali22-cell', 'ParthSachdeva26', 'ShivangiGautam08', 'teeya831-cmd']
for u in users:
    r = requests.get(f'https://api.github.com/users/{u}')
    data = r.json()
    if 'id' in data:
        name = data.get('name') or u
        email = f"{data['id']}+{u}@users.noreply.github.com"
        print(f"{name} <{email}>")
    else:
        print(f"Could not find {u}")
