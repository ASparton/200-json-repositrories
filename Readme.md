## How to run the app

1. Clone repository
2. Have Python3, pip and pipenv installed on your system
3. Open a shell inside the root directory of the repository
4. Run "pipenv shell" 
5. Run "pipenv install"
6. Run "pyhon src/app.py"
7. Open the html file inside the build directory to see the result

## Warning

If a large number of call to the API is made without any key, the application can crash.
If it happens, just comment out the following lines in "src/app.py" and it should work:
- 82 -> 85
- 93 -> 95

## Bonus

The app can take two parameters:
1. The word to search for inside the name or description of the repositories (by default it's "json")
2. The number of repositories wanted (by default it's "200")

Example: "python src/app.py python 30" will return 30 repositories with the word python in the name or description.