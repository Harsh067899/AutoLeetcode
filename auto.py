import requests
from bs4 import BeautifulSoup
import time

# ✅ Step 1: Dynamically Fetch Session & CSRF Token (Replace manually after login)
session_id = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2NvdW50X3ZlcmlmaWVkX2VtYWlsIjpudWxsLCJhY2NvdW50X3VzZXIiOiI5dGVoNSIsIl9hdXRoX3VzZXJfaWQiOiIxNjQ4ODMyOSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjFiZTExNzlmOWJjNGM2OTQ3OGJmOTRlN2ZjMzIxNWMyZjdiY2NkNzRiZTBhMDAwZDU4ZGRhYWM2ZTBjNDdlNDciLCJzZXNzaW9uX3V1aWQiOiIyNzM5MjMwYSIsImlkIjoxNjQ4ODMyOSwiZW1haWwiOiJwaW1vdGFnMzI5QGd1ZnV0dS5jb20iLCJ1c2VybmFtZSI6InRlc3RpbmdwdXJwb3Nlc3Nvc28iLCJ1c2VyX3NsdWciOiJ0ZXN0aW5ncHVycG9zZXNzb3NvIiwiYXZhdGFyIjoiaHR0cHM6Ly9hc3NldHMubGVldGNvZGUuY29tL3VzZXJzL2RlZmF1bHRfYXZhdGFyLmpwZyIsInJlZnJlc2hlZF9hdCI6MTczODM5ODU4OCwiaXAiOiIxMDMuNC4yMjEuMjUyIiwiaWRlbnRpdHkiOiI0MTc3MGU0MDhkNDUzZjBlMThiNmNmNTM1ZTIyMGM4NCIsImRldmljZV93aXRoX2lwIjpbIjVhZDhkN2JmMGRhMGY0NzBjMTM4MmJhZGNiMDhiOTAyIiwiMTAzLjQuMjIxLjI1MiJdfQ.assjupAHFruG5olsfIJy25ni_SqoL9JjhnD0KAN2uNk"
csrf_token = "MvSxTVWGd1IoCigaKfu8LzaOEFtwJYbyiYnPRxfkTsRnJCS1Y6BdoHro8g5XKZIl"

headers = {
    "x-csrftoken": csrf_token,
    "Cookie": f"LEETCODE_SESSION={session_id}; csrftoken={csrf_token}",
    "Referer": "https://leetcode.com",
}

# ✅ Step 2: Fetch unsolved questions
def get_unsolved_questions(n, difficulty="easy"):
    url = "https://leetcode.com/api/problems/all/"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        problems = response.json()["stat_status_pairs"]
        unsolved = [
            {
                "slug": q["stat"]["question__title_slug"],
                "question_id": q["stat"]["question_id"]
            }
            for q in problems if not q.get("status") and q["difficulty"]["level"] == 
            (1 if difficulty == "easy" else 2 if difficulty == "medium" else 3)
        ]
        return unsolved[:n]
    else:
        print("❌ Failed to fetch problems.")
        return []

# ✅ Step 3: Scrape solution from Leetcode discussions
def get_best_solution(question_slug, language="python"):
    url = f"https://leetcode.com/problems/{question_slug}/solutions/?orderBy=most_votes&languageTags={language}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        code_blocks = soup.find_all("pre")
        if code_blocks:
            return code_blocks[0].text.strip()  # Get first solution
    return None

# ✅ Step 4: Test the solution before submission
def test_solution(question_slug, code, language="python"):
    url = f"https://leetcode.com/problems/{question_slug}/interpret_solution/"

    payload = {
        "lang": language,
        "question_id": question_slug,
        "typed_code": code
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        return result.get("interpret_id")
    return None

# ✅ Step 5: Check test case results
def check_test_result(interpret_id):
    url = f"https://leetcode.com/submissions/detail/{interpret_id}/check/"
    for _ in range(5):  # Retry up to 5 times
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            if result["run_success"] and result["total_correct"] == result["total_testcases"]:
                return True
        time.sleep(2)  # Wait before retrying
    return False

# ✅ Step 6: Submit the solution
def submit_solution(question_id, code, language="python"):
    url = "https://leetcode.com/problems/{}/submit/".format(question_id)

    payload = {
        "lang": language,
        "question_id": question_id,
        "typed_code": code
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.status_code == 200

# ✅ Step 7: Automate solving process
def solve_n_questions(n=5, difficulty="easy"):
    questions = get_unsolved_questions(n, difficulty)
    if not questions:
        print("❌ No questions to solve.")
        return

    for question in questions:
        question_slug = question["slug"]
        question_id = question["question_id"]
        print(f"🔍 Solving: {question_slug}")

        # Get best solution
        solution_code = get_best_solution(question_slug)
        if not solution_code:
            print(f"⚠️ Skipping {question_slug}, no solution found.")
            continue

        # Test the solution
        interpret_id = test_solution(question_slug, solution_code)
        if not interpret_id:
            print(f"❌ Failed to test {question_slug}.")
            continue

        # Check test result
        if not check_test_result(interpret_id):
            print(f"❌ Solution for {question_slug} failed test cases.")
            continue

        # Submit the solution
        if submit_solution(question_id, solution_code):
            print(f"✅ Successfully submitted {question_slug}!")
        else:
            print(f"❌ Failed to submit {question_slug}.")

# ✅ Run the bot for 5 questions
solve_n_questions(n=5, difficulty="easy")
