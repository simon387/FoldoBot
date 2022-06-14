# python
import json
from urllib import parse, request

url = "http://api.giphy.com/v1/gifs/"
url = "http://api.giphy.com/v1/gifs/random?api_key=0UTRbFtkMxAplrohufYco5IY74U8hOes&rating=pg-13&limit=1"

params = parse.urlencode({
	"type": "random",
	"rating": "pg-13",
	"api_key": "0UTRbFtkMxAplrohufYco5IY74U8hOes",
	"baseURL": "https://api.giphy.com/v1/gifs/",
})

with request.urlopen("".join((url, "?", params))) as response:
	data = json.loads(response.read())

print(json.dumps(data, sort_keys=True, indent=4))
