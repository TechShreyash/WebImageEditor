import requests


def resizeImage(fileUrl, height, width, hash):
    fileUrl= fileUrl.split('//')[1]
    url = f"https://wsrv.nl/?url={fileUrl}&w={width}&h={height}&fit=inside"
    response = requests.get(url)
    file = response.content

    with open(f"/tmp/resized{hash}", "wb") as f:
        f.write(file)

    return f"resized{hash}" + url

def test():
    a = requests.get('https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Cat_August_2010-4.jpg/1200px-Cat_August_2010-4.jpg')
    with open('/tmp/test.jpg', 'wb') as f:
        f.write(a.content)

