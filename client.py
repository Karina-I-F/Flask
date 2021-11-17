import requests

HOST = 'http://127.0.0.1:5000'

resp = requests.get(f'{HOST}/health').json()
print(resp)


# create user1
# resp = requests.post(f'{HOST}/api/v1.0/register',
#                     json={
#                         "username": "test1",
#                         "email": "test@test.test",
#                         "password": "sgdsppo34FET32325"}).json()
# print(resp)


# create user2
# resp = requests.post(f'{HOST}/api/v1.0/register',
#                     json={
#                         "username": "test2",
#                         "email": "test2@test.test",
#                         "password": "sgwefpo34FET32325"}).json()
# print(resp)


# get user by id
resp = requests.get(f'{HOST}/api/v1.0/users/1')
print(resp.json())
print(resp.status_code)


# login 1
# resp = requests.post(f'{HOST}/api/v1.0/login',
#                     json={
#                         "email": "test@test.test",
#                         "password": "sgdsppo34FET32325"})
# print(resp.json())
# print(resp.status_code)


# login 2
# resp = requests.post(f'{HOST}/api/v1.0/login',
#                     json={
#                         "email": "test2@test.test",
#                         "password": "sgwefpo34FET32325"})
# print(resp.json())
# print(resp.status_code)


# create ad 1
resp = requests.post(f'{HOST}/api/v1.0/ads/',
                     json={
                         "title": "test",
                         "description": "test"
                     },
                     headers={
                         'Authorization': 'Bearer put_your_token_here'
                     })
print(resp.json())
print(resp.status_code)


# create ad 2
# resp = requests.post(f'{HOST}/api/v1.0/ads/',
#                     json={
#                         "title": "test4",
#                         "description": "test 4 test"
#                     },
#                     headers={
#                         'Authorization': 'Bearer put_your_token_here'
#                     })
# print(resp.json())
# print(resp.status_code)


# patch ad
# resp = requests.put(f'{HOST}/api/v1.0/ads/6',
#                     json={
#                         "title": "test 5",
#                         "description": "test 5 test"
#                     },
#                     headers={
#                         'Authorization': 'Bearer put_your_token_here'
#                     })
# print(resp.json())
# print(resp.status_code)


# delete ad
# resp = requests.delete(f'{HOST}/api/v1.0/ads/5',
#                     headers={
#                         'Authorization': 'Bearer put_your_token_here'
#                     })
# print(resp.json())
# print(resp.status_code)


# get ads
resp = requests.get(f'{HOST}/api/v1.0/ads')
print(resp.json())
print(resp.status_code)
