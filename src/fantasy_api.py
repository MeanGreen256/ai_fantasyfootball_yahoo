import yahoo_fantasy_api as yfa
from yahoo_oauth import OAuth2
import logging
from pathlib import Path

# --- CONFIGURATION ---
# You can find your league ID in the URL of your league's homepage.
# e.g., https://football.fantasysports.yahoo.com/f1/123456 -> LEAGUE_ID = '123456'
LEAGUE_ID = "160889"
GAME_CODE = "nfl"  # 'nfl' for football


def authenticate():
    """
    Authenticates with the Yahoo Fantasy API using OAuth2.
    Looks for 'private.json' for credentials in the project root.
    """
    try:
        # Correct path from /src to the root directory
        cred_path = Path(__file__).parent.parent / 'private.json'
        if not cred_path.exists():
            logging.error(f"Credential file not found at {cred_path}. Please create 'private.json'.")
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
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred during authentication: {e}")
        return None


def get_league(sc):
    """
    Retrieves the league object using the configured GAME_CODE and LEAGUE_ID.
    """
    if not sc:
        return None
    try:
        gm = yfa.Game(sc, GAME_CODE)
        # The league ID format is {game_id}.l.{league_id}
        league = gm.to_league(f"{gm.game_id()}.l.{LEAGUE_ID}")
        logging.info(f"Successfully connected to league: {league.settings()['name']}")
        return league
    except Exception as e:
        logging.error(f"Failed to get league with ID '{LEAGUE_ID}'. Error: {e}")
        logging.error("Please ensure your LEAGUE_ID is correct in src/fantasy_api.py.")
        return None


def get_standings(league):
    """
    Fetches and returns the current league standings as a list of dicts.
    """
    try:
        logging.info("Fetching standings...")
        return league.standings()
    except Exception as e:
        logging.error(f"Could not fetch standings. Error: {e}")
        return []


def get_scoreboard_for_week(league, week):
    """
    Fetches and returns the scoreboard for a given week.
    """
    try:
        logging.info(f"Fetching scoreboard for week {week}...")
        return league.scoreboard(week=week)
    except Exception as e:
        logging.error(f"Could not fetch scoreboard for week {week}. Error: {e}")
        return None