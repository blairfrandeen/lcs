# Automatically format your leetcode solutions for posting to Zulip

## Install
```sh
git clone https://github.com/blairfrandeen/lcs
cd lcs
pip install .
```

## Usage
Log into leetcode.com in your browser and then go find your cookie. Run
```
lcs set-cookie
```
and paste in your leetcode.com session cookie.

Then copy the submission URL from the browser and run
```
lcs https://leetcode.com/problems/two-sum/submissions/your-brilliant-solution/
```
And paste that into Zulip like a boss.
