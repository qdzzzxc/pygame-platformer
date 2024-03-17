import requests

# Replace with your server IP and desired quote ID
server_ip = "127.0.0.1"
quote_id = 1

# # GET a random quote
# response = requests.get(f"http://{server_ip}:5000/ai-quotes/10")
# print(response.json())

# # Example data for creating a new quote
# new_quote_data = {
#     "author": "Your Name",
#     "quote": "This is my new AI quote."
# }

# POST a new quote (replace with your desired ID or leave blank)
# response = requests.post(f"http://{server_ip}:5000/ai-quotes/10", json=new_quote_data)
# print(response.json())

# # GET a specific quote by ID
# response = requests.get(f"http://{server_ip}:5000/ai-quotes/10")
# print(response.json())

# new_quote_data = {
#     "query": "как дела",
# }
# response = requests.get(f"http://{server_ip}:5000", json=new_quote_data)
# print(response.json())




# put_data = {
#     "old_document_id": -1,
#     "chunks": [['doc23', 'with length 3']],
#     "sources": [[34, '434']],
#     "document_type": 'pdf',
#     "pages": [[1, 2]],
# }
# response = requests.put(f"http://{server_ip}:5000", json=put_data)
# print(response.json())

# post_data = {
#     "chunks": [['i love cooking', 'hello my best friend', 'how are you bro', 'lol too chunks here']],
#     "sources": [[34, '434', '234234', 'googler.com']],
#     "document_type": 'pdf',
#     "pages": [[1, 2,5, 6]],
# }
# response = requests.post(f"http://127.0.0.1:5000", json=post_data)
# print(response.json())

# delete_data = {
#     "ids": [[-1, 0]],
# }

# response = requests.delete(f"http://{server_ip}:5000", json=delete_data)
# print(response.json())

get_data = {
#     "query": 'friends forever',
        "return_all": True
}

response = requests.get(f"http://127.0.0.1:5000", json=get_data)
print(response.json())

