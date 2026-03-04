import urllib.request, json
url = "https://www.metacareers.com/graphql"
req = urllib.request.Request(url, method="POST", headers={"Content-Type": "application/x-www-form-urlencoded"})
data = "lsd=dummy&fb_api_caller_class=RelayModern&variables={\"search_snippet\":\"product manager\",\"offices\":[\"India\"]}..."
# Meta uses GraphQL, might be complex. Let's try RSS or generic job aggregator API
