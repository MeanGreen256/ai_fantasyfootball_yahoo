import yahoo_fantasy_api as yfa
from yahoo_oauth import OAuth2
import logging
from pathlib import Path
import pandas as pd

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- CONFIGURATION ---
# TODO: Replace with your actual League ID
# You can find your league ID in the URL of your league's homepage.
# e.g., https://football.fantasysports.yahoo.com/f1/123456 -> LEAGUE_ID = '123456'
# key 7pgr68k
LEAGUE_ID = "160889"
GAME_CODE = "nfl"  # 'nfl' for football


def authenticate():
    """
    Authenticates with the Yahoo Fantasy API using OAuth2.
    Looks for 'private.json' for credentials in the parent directory.
    """
    try:
        # The credential file is in the parent directory of /src
        cred_path = Path(__file__).parent.parent / 'ai_fantasyfootball_yahoo' / 'private.json'
        if not cred_path.exists():
            print (f"Credential file not found at {cred_path}. Please create 'private.json' with your Yahoo App's consumer_key and consumer_secret.")
            raise FileNotFoundError(f"Credential file not found at {cred_path}")
        sc = OAuth2(None, None, from_file=cred_path)
        if not sc.token_is_valid():
            logging.info("Authentication token is not valid or expired. Re-authenticating...")
            sc.login()
            
        logging.info("Authentication successful.")
        return sc
    except FileNotFoundError:
        logging.error("Error: 'private.json' not found in the root project directory.")
        logging.error("Please create 'private.json' with your Yahoo App's consumer_key and consumer_secret.")
        logging.error("See README.md for more details.")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred during authentication: {e}")
        return None


def get_league(sc, game_code, league_id):
    """
    Retrieves the league object.
    """
    if not sc:
        return None
    try:
        gm = yfa.Game(sc, game_code)
        # The league ID format is {game_id}.l.{league_id}
        league = gm.to_league(f"{gm.game_id()}.l.{league_id}")
        logging.info(f"Successfully connected to league: {league.settings()['name']}")
        return league
    except Exception as e:
        logging.error(f"Failed to get league with ID '{league_id}'. Error: {e}")
        logging.error("Please ensure your LEAGUE_ID is correct in src/main.py.")
        return None


def display_standings(league):
    """
    Fetches and displays the current league standings.
    """
    try:
        print("\n--- Current League Standings ---")
        standings = league.standings()
        for team in standings:
            print(
                f"{team['rank']}. {team['name']} "
                f"({team['wins']}-{team['losses']}-{team['ties']}) - "
                f"Points For: {team['points_for']:.2f}"
            )
    except Exception as e:
        logging.error(f"Could not fetch or display standings. Error: {e}")


def display_scoreboard_for_week(league, week):
    """
    Fetches and displays the scoreboard for a given week.
    """
    try:
        print(f"\n--- Scoreboard for Week {week} ---")
        sb = league.scoreboard(week=week)
        for match in sb['matchups']:
            team1 = match['teams'][0]
            team2 = match['teams'][1]
            print(
                f"{team1['name']} ({team1['points']:.2f}) vs. "
                f"{team2['name']} ({team2['points']:.2f})"
            )
    except Exception as e:
        logging.error(f"Could not fetch or display scoreboard for week {week}. Error: {e}")

def save_report_to_html(league, filename="fantasy_report.html"):
    """Saves standings and scoreboard to a single HTML file."""
    try:
        output_path = Path(__file__).parent.parent / filename
        logging.info(f"Generating HTML report at {output_path}...")

        # Get standings and convert to HTML table
        standings_df = pd.DataFrame(league.standings())
        standings_html = standings_df.to_html(index=False, border=0, classes="table table-striped")

        # Get scoreboard and format as HTML
        week = league.current_week()
        sb = league.scoreboard(week=week)
        scoreboard_html = f"<h2>Scoreboard for Week {week}</h2><ul>"
        for match in sb['matchups']:
            team1 = match['teams'][0]
            team2 = match['teams'][1]
            scoreboard_html += f"<li>{team1['name']} ({team1['points']:.2f}) vs. {team2['name']} ({team2['points']:.2f})</li>"
        scoreboard_html += "</ul>"

        # Basic HTML structure with some style
        html_template = f"""
        <html>
        <head>
            <title>{league.settings()['name']} Report</title>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
            <style> body {{ padding: 2em; }} </style>
        </head>
        <body>
            <h1>{league.settings()['name']}</h1>
            <h2>Current Standings</h2>
            {standings_html}
            <hr>
            {scoreboard_html}
        </body>
        </html>
        """

        with open(output_path, "w") as f:
            f.write(html_template)
        logging.info(f"Successfully saved HTML report to {output_path}")

    except Exception as e:
        logging.error(f"Could not generate HTML report. Error: {e}")


def main():
    """
    Main function to run the fantasy football stats application.
    """
    logging.info("Starting Yahoo Fantasy Football Stats Application...")

    if LEAGUE_ID == "YOUR_LEAGUE_ID":
        logging.error("Please update the LEAGUE_ID in src/main.py before running.")
        return

    session_context = authenticate()
    if not session_context:
        return

    league = get_league(session_context, GAME_CODE, LEAGUE_ID)
    if not league:
        return

    display_standings(league)
    display_scoreboard_for_week(league, league.current_week())
    ##TODO: testing html file generation
    save_report_to_html(league)


if __name__ == "__main__":
    main()