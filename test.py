import requests


cookies = {
    'LEETCODE_SESSION': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiMTY0ODgzMjkiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjFiZTExNzlmOWJjNGM2OTQ3OGJmOTRlN2ZjMzIxNWMyZjdiY2NkNzRiZTBhMDAwZDU4ZGRhYWM2ZTBjNDdlNDciLCJzZXNzaW9uX3V1aWQiOiI3MWY1NDYwZCIsImlkIjoxNjQ4ODMyOSwiZW1haWwiOiJwaW1vdGFnMzI5QGd1ZnV0dS5jb20iLCJ1c2VybmFtZSI6InRlc3RpbmdwdXJwb3Nlc3Nvc28iLCJ1c2VyX3NsdWciOiJ0ZXN0aW5ncHVycG9zZXNzb3NvIiwiYXZhdGFyIjoiaHR0cHM6Ly9hc3NldHMubGVldGNvZGUuY29tL3VzZXJzL2RlZmF1bHRfYXZhdGFyLmpwZyIsInJlZnJlc2hlZF9hdCI6MTczODQwMzM4NywiaXAiOiIxMDMuNC4yMjEuMjUyIiwiaWRlbnRpdHkiOiI0MTc3MGU0MDhkNDUzZjBlMThiNmNmNTM1ZTIyMGM4NCIsImRldmljZV93aXRoX2lwIjpbIjVhZDhkN2JmMGRhMGY0NzBjMTM4MmJhZGNiMDhiOTAyIiwiMTAzLjQuMjIxLjI1MiJdLCJfc2Vzc2lvbl9leHBpcnkiOjEyMDk2MDB9.o291WC1uYbxNHfVF3AzZM1FL1T0cISuPhRjUxeXflzE',
    'csrftoken': 't2urUdUHx5cWS96ongfBnKolAVEuU5h8Bv83tC0xuY39x82Et6vaapJHLRdTfMcs',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'X-CSRFToken': 't2urUdUHx5cWS96ongfBnKolAVEuU5h8Bv83tC0xuY39x82Et6vaapJHLRdTfMcs',
    'Content-Type': 'application/json',
    'Referer': 'https://leetcode.com/problems/special-array-i/?envType=daily-question&envId=2025-02-01',
}

# The URL to submit the solution
url = "https://leetcode.com/problems/special-array-i/submit/"

data = {
    'lang': 'cpp',  # Language in which the solution is written
    'question_id': '3429',  # ID for the "Special Array I" problem
    'typed_code': """
class Solution {
public:
    static bool isArraySpecial(vector<int>& nums) {
        int n = nums.size();
        if (n == 1) return 1;
        bool prev = nums[0] & 1;
        for (int i = 1; i < n; i++) {
            bool x = nums[i] & 1;
            if (x ^ prev == 0) return 0;
            prev = x;
        }
        return 1;
    }
};
    """,  # Your C++ solution code
}

# Send the POST request to submit the solution
response = requests.post(url, cookies=cookies, headers=headers, json=data)

# Debugging information
print(f"Status Code: {response.status_code}")
print(f"Response Text: {response.text}")

# Check if submission was successful
if response.status_code == 200:
    print("Solution submitted successfully!")
else:
    print("Submission failed. Please check the response for more details.")
