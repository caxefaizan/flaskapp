# StealthMatch
Portfolio website developed using flask.

## Demo

- Clone the project
    ```shell
    git clone https://github.com/caxefaizan/stealthmatch.git
    cd stealthmatch
    ```
- Create a virtual environment
    ```shell
    python3 -m venv .venv
    source .venv/bin/activate
    ```
- Install the dependencies
    ```shell
    python3 -m pip install -r server/requirements.txt
    ```
- Initialize the DB
    ```shell
    sqlite3 server/instance/flaskr.sqlite < server/flaskr/schema.sql
    ```
- Start the server
    ```shell
    flask --app server/flaskr run --debug
    ```

## Contributing Guidelines
- Create an Issue in the Repo 
- Add the feature or bug as title name
- Add description as how it can improve the portal
- Fork the project
- Create a Branch eg. feature/enable-saml or bugfix/incorrect-form-fields
- Improvise the code
- Create Merge request