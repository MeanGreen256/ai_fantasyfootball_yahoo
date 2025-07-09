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
    The main dashboard route. Fetches data and renders the homepage.
    """
    logging.info("Dashboard route accessed. Fetching data...")

    # 1. Authenticate and get the league object
    session_context = fantasy_api.authenticate()
    if not session_context:
        flash("Authentication failed. Check logs for details.", "danger")
        return render_template('index.html')

    league = fantasy_api.get_league(session_context)
    if not league:
        flash("Could not connect to the league. Check your LEAGUE_ID.", "danger")
        return render_template('index.html')

    # 2. Fetch the data for the template
    current_week = league.current_week()
    standings = fantasy_api.get_standings(league)
    scoreboard = fantasy_api.get_scoreboard_for_week(league, current_week)
    league_settings = league.settings()

    # 3. Render the page with the data
    return render_template('index.html',
                           standings=standings,
                           scoreboard=scoreboard,
                           week=current_week,
                           league_name=league_settings['name'])