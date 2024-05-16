from os import read
import re

import click
from click_default_group import DefaultGroup
import requests
import pyperclip


ENDPOINT = "https://leetcode.com/graphql"


def payload(submission_id: int) -> dict[str, str | dict[str, int]]:
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
    return payload


def read_cookie():
    try:
        with open("cookie", "r") as cf:
            cookie = cf.read()
    except FileNotFoundError:
        raise click.UsageError(
            "Could not find cookie. Run lcs set-cookie --help for instructions."
        )
    return cookie


def solution_str(submission_details: dict) -> str:
    solstr = f"```spoiler [{submission_details['question']['title']}]"
    solstr += "(https://leetcode.com/problems/{submission_details['question']['titleSlug']}) | :python:\n"
    solstr += f"```{submission_details['lang']['name']}\n"
    solstr += submission_details["code"]
    solstr += "```\n```"
    return solstr


@click.group(cls=DefaultGroup, default="solution")
def cli():
    pass


@cli.command()
def set_cookie() -> None:
    """Set your session cookie.

    1. Navitage your browser to https://leetcode.com and make sure you're logged in.
    2. Press ctrl+shift+i to open the inspector
    3. Go to the network tab
    4. Refresh the page and look at the headers in the GET requests
    5. Find the cookie, right click and copy the value, and paste it here.
    """
    cookie = input("Paste cookie: ")
    with open("cookie", "w") as cf:
        cf.write(cookie)


@cli.command()
@click.argument("solution_url")
def solution(solution_url: str) -> None:
    """Output text suitable for posting solution to Zulip"""
    submission_id = re.search(r"submissions/(\d+)", solution_url)
    if not submission_id:
        raise click.UsageError("Invalid URL Specified")
    submission_id = int(submission_id.groups()[0])
    req_payload = payload(submission_id)
    cookie = read_cookie()
    response = requests.post(ENDPOINT, json=req_payload, headers={"Cookie": cookie})

    if response.status_code == 200:
        data = response.json()
        submission_details = data["data"]["submissionDetails"]
        sol = solution_str(submission_details)
        print(sol)
        pyperclip.copy(sol)
        print("Copied to your clipboard.")
    else:
        print("Request failed with status code:", response.status_code)


if __name__ == "__main__":
    cli()
