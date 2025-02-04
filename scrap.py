import requests
from bs4 import BeautifulSoup

# Function to get the problem ID dynamically
def get_problem_id():
    # URL for the problem page
    problem_url = 'https://leetcode.com/problems/two-sum/'
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(problem_url, headers=headers)
    
    if response.status_code == 200:
        # Parse the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Search for the problem ID in the page's data
        # This part can vary, you'll need to inspect the page for the exact element containing the ID
        problem_data = soup.find('script', {'type': 'application/json'})
        
        if problem_data:
            # Extract the problem ID from the JSON data (or any required field)
            return problem_data.text.strip()  # Modify based on actual structure
    return None

# Call the function to get the problem ID
problem_id = get_problem_id()
if problem_id:
    print(f"Found problem ID: {problem_id}")
else:
    print("Failed to find problem ID.")
