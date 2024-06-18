import requests

BASE_URL = 'http://127.0.0.1:5000/api'

# Log in to get the access token
login_url = f'{BASE_URL}/login'
login_data = {
    'username': 'pippo',
    'password': 'pluto'
}
login_response = requests.post(login_url, json=login_data)
print(login_response.json())

access_token = login_response.json().get('access_token')
headers = {
    'Authorization': f'Bearer {access_token}'
}

# Convert an image to black and white
convert_url = f'{BASE_URL}/convert-to-bw'
files = {'image': open('prova.jpeg', 'rb')}
convert_response = requests.post(convert_url, headers=headers, files=files)

if convert_response.status_code == 200:
    with open('bw_image.jpeg', 'wb') as f:
        f.write(convert_response.content)
    print('Image converted and saved as bw_image.jpeg')
else:
    print(convert_response.json())
