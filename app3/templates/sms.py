import requests

url = "https://www.fast2sms.com/dev/bulkV2"

querystring = {
	"authorization": "nGOkyoSH7prvuf4q1ZBiFXJUl9bC2jEMhDascVwgItPe0K3T6QjEywon8OQ5xVCFpvraP4tdGciqzbh2",
	"message": "This is test Message sent from \
		Python Script using REST API.",
	"language": "english",
	"route": "q",
	"numbers": "+91-09513515270, 9513515270"}

headers = {
	'cache-control': "no-cache"
}
try:
	response = requests.request("GET", url,
								headers = headers,
								params = querystring)
	
	print("SMS Successfully Sent")
except:
	print("Oops! Something wrong")
