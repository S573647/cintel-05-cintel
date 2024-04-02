import requests

# Define the URL of the data stream
stream_url = 'https://example.com/stream'

# Function to process data as it streams
def process_stream(response):
    for line in response.iter_lines():
        if line:
            # Process each line of streamed data
            print(line.decode('utf-8'))  # Decode bytes to string and print
            # Add your processing logic here

# Make a GET request with streaming enabled
with requests.get(stream_url, stream=True) as response:
    # Check if the request was successful
    if response.ok:
        # Process the streamed data
        process_stream(response)
    else:
        # Print error message if request fails
        print(f"Error: {response.status_code} - {response.reason}")

