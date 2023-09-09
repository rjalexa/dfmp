import requests
from faker import Faker

def generate_fake_names(n=500):
    fake = Faker()
    names = []
    for _ in range(n):
        name = fake.first_name()
        surname = fake.last_name()
        names.append(f"{name}-{surname}")
    return names

def send_requests(names):
    url = "http://localhost:12345/store"
    for name in names:
        params = {'data': name}
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Failed to send request for {name}. Status code: {response.status_code}")

if __name__ == "__main__":
    names = generate_fake_names()
    send_requests(names)

