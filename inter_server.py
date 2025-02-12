import requests

def test_server_connection():
    """Test the connection to the AIKI server by accessing the root endpoint."""
    try:
        response = requests.get("http://localhost:7522/")
        if response.status_code == 200:
            print("Server response:", response.json())
            return True
        else:
            print(f"Error: Server returned status code {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server")
        return False

if __name__ == "__main__":
    test_server_connection()