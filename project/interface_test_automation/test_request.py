import requests
import json
from http.client import HTTPException
from idlelib.iomenu import encoding

url = 'http://api.yundingshui.cn/v1/tokens'
data = {
    "phone": "18977982261",
    "passwd": "1111111"
}
headers = {
  'Content-Type': 'application/json'
}
try:
    response = requests.post(url=url,headers=headers,data=json.dumps(data))
    response.encoding="urf-8"
    print(response.json())
    print(response.url)
    print(response.text)
    print(response.status_code)
except HTTPException as e:
  print(e)