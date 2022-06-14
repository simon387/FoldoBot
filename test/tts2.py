import requests

url = "https://rev-ai.p.rapidapi.com/jobs/%7Bid%7D/transcript"

headers = {
	"Accept": "application/vnd.rev.transcript.v1.0+json",
	"X-RapidAPI-Host": "rev-ai.p.rapidapi.com",
	"X-RapidAPI-Key": "1ef6ab7592msh06489edeee5e68cp11a588jsneaebcfe72d2f"
}

response = requests.request("GET", url, headers=headers)

print(response.text)
