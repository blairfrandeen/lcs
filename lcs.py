import re
import sys

import requests

submission = sys.argv[1]
submission_id = int(re.search(r"submissions/(\d+)", submission).groups()[0])

ENDPOINT = "https://leetcode.com/graphql"

query = """
query submissionDetails($submissionId: Int!) {
  submissionDetails(submissionId: $submissionId) {
    runtimeDisplay
    runtimePercentile
    memoryDisplay
    memoryPercentile
    code
    lang {
      name
      verboseName
    }
    question {
      title
      titleSlug
    }
  }
}
"""
payload = {
    "query": query,
    "variables": {"submissionId": submission_id},
    "operationName": "submissionDetails",
}
headers = {
    "authority": "leetcode.com",
    "referer": "https://leetdoce.com/problemset/",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Cookie": "csrftoken=aTrplFoawEgwX3kal1khlnRQ5j4lwzClY1d3tDZXeR4qz5g3rWMTPizJXM1Eoj0E; messages=.eJyLjlaKj88qzs-Lz00tLk5MT1XSMdAxMtVRCi5NTgaKpJXm5FQqFGem56WmKGTmKSQWKyTlJGYWpRUl5qWkpubpKcXqDG4jIvNLFTISy1Jh2vNLS6hjYywAFaxtsQ:1s7Z2h:Hi8p8r7Q3ULPYlzO3wI66Imdqyj3WL7hw3WSnACZn5A; INGRESSCOOKIE=f8c83c96446c6f5217982d1cfc824cd6|8e0876c7c1464cc0ac96bc2edceabd27; __cf_bm=eMB8_gOKtlD_BSQ8nm8He2Mccre_LcgV383qFTaCkpw-1715857896-1.0.1.1-4OUtl6a.g13gRXRboXTIvUVOjYS650TcI5xoOIvnnTixVKD.yoVXR66hQT5p26qoanKq0PVArQZYDIwQrku2qQ; _dd_s=rum=0&expire=1715858878450; LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiODc3MDk0NSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjRmNmMxY2U1YjBlM2Y1NDNkNzk0MzE5N2Q4ODRjZjkwZGY0MzNlZDBjM2ViOGI3YWE0ZWU2MTFiYmQ0ZmY3N2EiLCJpZCI6ODc3MDk0NSwiZW1haWwiOiJibGFpcmZyYW5kZWVuQGdtYWlsLmNvbSIsInVzZXJuYW1lIjoiYmxhaXJmcmFuZGVlbiIsInVzZXJfc2x1ZyI6ImJsYWlyZnJhbmRlZW4iLCJhdmF0YXIiOiJodHRwczovL2Fzc2V0cy5sZWV0Y29kZS5jb20vdXNlcnMvYXZhdGFycy9hdmF0YXJfMTY3NjMxMDkwOS5wbmciLCJyZWZyZXNoZWRfYXQiOjE3MTU4NTc5NzksImlwIjoiNDcuMjI5LjE2OC4zIiwiaWRlbnRpdHkiOiIyNTAxOGIxNzVmODEyNjE3NzQ1OTBlMzdiZGIwNDliYyIsInNlc3Npb25faWQiOjYxNjIzMjkwfQ.7PsEIXixJbEHvJp-62IL3a26wF4WCo8aW-jWG_zSpEkcsrftoken=aTrplFoawEgwX3kal1khlnRQ5j4lwzClY1d3tDZXeR4qz5g3rWMTPizJXM1Eoj0E; messages=.eJyLjlaKj88qzs-Lz00tLk5MT1XSMdAxMtVRCi5NTgaKpJXm5FQqFGem56WmKGTmKSQWKyTlJGYWpRUl5qWkpubpKcXqDG4jIvNLFTISy1Jh2vNLS6hjYywAFaxtsQ:1s7Z2h:Hi8p8r7Q3ULPYlzO3wI66Imdqyj3WL7hw3WSnACZn5A; INGRESSCOOKIE=f8c83c96446c6f5217982d1cfc824cd6|8e0876c7c1464cc0ac96bc2edceabd27; __cf_bm=eMB8_gOKtlD_BSQ8nm8He2Mccre_LcgV383qFTaCkpw-1715857896-1.0.1.1-4OUtl6a.g13gRXRboXTIvUVOjYS650TcI5xoOIvnnTixVKD.yoVXR66hQT5p26qoanKq0PVArQZYDIwQrku2qQ; _dd_s=rum=0&expire=1715858878450; LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiODc3MDk0NSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjRmNmMxY2U1YjBlM2Y1NDNkNzk0MzE5N2Q4ODRjZjkwZGY0MzNlZDBjM2ViOGI3YWE0ZWU2MTFiYmQ0ZmY3N2EiLCJpZCI6ODc3MDk0NSwiZW1haWwiOiJibGFpcmZyYW5kZWVuQGdtYWlsLmNvbSIsInVzZXJuYW1lIjoiYmxhaXJmcmFuZGVlbiIsInVzZXJfc2x1ZyI6ImJsYWlyZnJhbmRlZW4iLCJhdmF0YXIiOiJodHRwczovL2Fzc2V0cy5sZWV0Y29kZS5jb20vdXNlcnMvYXZhdGFycy9hdmF0YXJfMTY3NjMxMDkwOS5wbmciLCJyZWZyZXNoZWRfYXQiOjE3MTU4NTc5NzksImlwIjoiNDcuMjI5LjE2OC4zIiwiaWRlbnRpdHkiOiIyNTAxOGIxNzVmODEyNjE3NzQ1OTBlMzdiZGIwNDliYyIsInNlc3Npb25faWQiOjYxNjIzMjkwfQ.7PsEIXixJbEHvJp-62IL3a26wF4WCo8aW-jWG_zSpEk",
}
response = requests.post(ENDPOINT, json=payload, headers=headers)

if response.status_code == 200:
    data = response.json()
    submission_details = data["data"]["submissionDetails"]
    print(f"```spoiler [{submission_details['question']['title']}]", end="")
    print(
        f"(https://leetcode.com/problems/{submission_details['question']['titleSlug']})",
        end="",
    )
    print(" | :python:")
    print(f"```{submission_details['lang']['name']}")
    print(submission_details["code"])
    print(f"```\n```")
else:
    print("Request failed with status code:", response.status_code)
