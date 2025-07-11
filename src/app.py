from flask import Flask, render_template, flash
import logging
import fantasy_api

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the Flask application
app = Flask(__name__)
# A secret key is needed for flashing messages
app.secret_key = 'super_secret_key_change_me'


@app.route('/')
def dashboard():
    """
    The main dashboard route. Authenticates, connects to the league,
    and then fetches data to display. Renders a base page even if
    secondary data fetches fail.
    """
    logging.info("Dashboard route accessed. Starting authentication...")

    # 1. CRITICAL PATH: Authenticate and get the league object.
    # The app cannot function without these.
    session_context = fantasy_api.authenticate()
    if not session_context:
        flash("Authentication with Yahoo failed. Please ensure your credentials are set up correctly and try again.", "danger")
        return render_template('index.html', league_name="Fantasy Football Dashboard")

    league = fantasy_api.get_league(session_context)
    if not league:
        flash("Successfully authenticated, but could not connect to the league. Please verify your LEAGUE_ID.", "warning")
        return render_template('index.html', league_name="Fantasy Football Dashboard")

    # 2. DEFAULT VIEW: At this point, we have a connection.
    # We can render a useful page with basic league info.
    league_settings = league.settings()
    league_name = league_settings.get('name', 'Fantasy League')
    current_week = league.current_week()
    logging.info(f"Successfully connected to {league_name}. Now fetching data for week {current_week}.")
    

    # 3. NON-CRITICAL DATA: Fetch standings and scoreboard.
    # The page will still render if these return no data.
    standings = fantasy_api.get_standings(league)
    scoreboard = fantasy_api.get_scoreboard_for_week(league, current_week)
    if not scoreboard:
        flash("Successfully authenticated, pull scoreboard data failed. Please try again later.", "warning")
        return render_template('index.html', league_name=league_name)
    # 4. Render the page with all available data.
    else:
        logging.info(f"Standings and scoreboard fetched successfully for week {current_week}.")
        return render_template('index.html',
                           league_name=league_name,
                           standings=standings,
                           scoreboard=scoreboard,
                           week=current_week)