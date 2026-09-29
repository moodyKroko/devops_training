import requests

url = "https://api.thedogapi.com/v1/breeds/search"

# 1. Paste your actual API key here
API_KEY = "live_jY1gS7MFYAnIeVZHNM8twpjvNNkBLlg4L8QTv36NArpvPCtHn0erWwdXSx8dq2KD"

# 2. Put the key inside the headers dictionary
custom_headers = {"x-api-key": API_KEY}

# Assignment: Your code needs to do the following:

# Prompt the user for a dog breed to input
# Make an API call with the requests library to search for that dog breed
# Extract the temperament info. If the dog has the trait "protective", print out "Good boy". If it lacks that trait, print out "Bad boy." If the API call returns anything other than a 200 response, print out "Error - Invalid Entry"

user_input = input("Enter a dog breed to search for: ")
query_params = {"q": user_input}

# 3. Pass the headers into the requests.get() function
response = requests.get(url, params=query_params, headers=custom_headers)

if response.status_code == 200:
    dog_list = response.json()
    if dog_list:
        for dog in dog_list:
            temperament = dog.get("temperament", "No temperament data available")
            breed_name = dog.get("name", "Unknown Breed")

            if "protective" in temperament.lower():
                print(f"{breed_name} - Good boy")
            else:
                print(f"{breed_name} - Bad boy")

    else:
        print("Connected, but the API returned an empty list.")
else:
    print(f"Failed to connect. Status code: {response.status_code}")
    print(f"Server Response: {response.text}")
