import http
import json
import time

import requests


def main():
    url = 'http://localhost:8080'
    with open('test.json', 'r') as f:
        test = json.loads(f.read())
    r = requests.post(f'{url}/test', json=test)
    assert r.status_code == http.HTTPStatus.OK
    time.sleep(1)
    r = requests.get(f'{url}/result?packageId=11')
    assert r.status_code == http.HTTPStatus.OK
    print(r.content)


if __name__ == '__main__':
    main()