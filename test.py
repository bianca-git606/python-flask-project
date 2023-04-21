import requests

blog_data = requests.get(url="https://api.npoint.io/c790b4d5cab58020d391").json()

all_blogs = [blog for blog in blog_data]

for blog in all_blogs:
    print(blog)