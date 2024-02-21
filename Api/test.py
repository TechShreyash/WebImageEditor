import requests

r =requests.post("http://127.0.0.1:8080/upload", files={"file": open("test.jpg", "rb"),'filename':'test.jpg'})
print(r.text)
print(r.status_code)
