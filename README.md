# AI Fantasy Football - Yahoo

A Python application to pull and analyze fantasy football stats from your Yahoo Fantasy Sports league.

## Setup

1.  **Install Dependencies:**
    Open a terminal in this project folder and run:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Create a Yahoo App:**
    *   Go to the [Yahoo Developer Network](https://developer.yahoo.com/apps/create/).
    *   Click "Create an App".
    *   Fill in the application name (e.g., "My Fantasy Stats").
    *   Select "Installed App" as the Application Type.
    *   Under "API Permissions", check "Fantasy Sports".
    *   After creation, you will receive a **Client ID** (Consumer Key) and **Client Secret** (Consumer Secret).

3.  **Configure Credentials:**
    *   In the root directory of the project (`ai_fantasyfootball_yahoo/`), create a file named `private.json`.
    *   Copy the contents of `private.json.example` into it.
    *   Replace the placeholder values with your actual Client ID and Client Secret.
      ```json
      {
          "consumer_key": "YOUR_CLIENT_ID",
          "consumer_secret": "YOUR_CLIENT_SECRET"
      }
      ```
    *   **Important:** This file contains sensitive information and is included in `.gitignore` to prevent it from being committed to version control.

## Usage

1.  **Find your League ID:**
    *   Navigate to your league's homepage on Yahoo Fantasy.
    *   The URL will look something like `https://football.fantasysports.yahoo.com/f1/123456`.
    *   Your league ID is the number at the end, e.g., `123456`.

2.  **Update the main script:**
    *   Open `src/main.py`.
    *   Change the `LEAGUE_ID` variable on line 12 to your league ID.

3.  **Run the application:**
    ```bash
    python src/main.py
    ```
    *   The first time you run the script, a browser window will open asking you to log in to Yahoo and authorize the application.
    *   After authorization, a `yahoo_token.json` file will be created in the root directory to store your session token for future runs.

## Usage for new flask implementation
1. **Open your terminal and navigate to the src directory:**
    * cd /Users/chasestuart/Documents/code_projects/ai_fantasyfootball_yahoo/src

2. **Tell flask where to run your app**
    * # For macOS/Linux
    export FLASK_APP=app.py
    flask run
    # For Windows (Command Prompt)
    # set FLASK_APP=app.py
    # flask run

3. **Open Browser**
    * and go to the URL shown in the terminal, which is usually http://127.0.0.1:5000.

You should now see a webpage displaying your league's standings and the current week's scoreboard! Any user on your local network can also access this page by navigating to your computer's local IP address followed by :5000.