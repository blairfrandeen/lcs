from os import read
import re

import click
from click_default_group import DefaultGroup
import requests


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
        raise click.UsageError("Could not find cookie")
    return cookie


@click.group(cls=DefaultGroup, default="solution")
def cli():
    pass


@cli.command()
def set_cookie() -> None:
    cookie = input("Paste cookie: ")
    with open("cookie", "w") as cf:
        cf.write(cookie)


@cli.command()
@click.argument("solution_url")
def solution(solution_url: str) -> None:
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


if __name__ == "__main__":
    cli()
