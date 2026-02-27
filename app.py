"""
Football AI Assistant - COMPLETE VERSION
All 25+ endpoints integrated
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from football_api import FootballAPI, FootballAPIError, PLAYER_IDS, LEAGUE_IDS, TEAM_IDS
from llm.gemini_client import GeminiClient

app = Flask(__name__)
CORS(app)

# Initialize clients
football_api = FootballAPI()
gemini = GeminiClient()


def find_player_id(player_name: str) -> int:
    """Find player ID from name"""
    name_lower = player_name.lower().strip()
    if name_lower in PLAYER_IDS:
        return PLAYER_IDS[name_lower]
    raise ValueError(f"Player '{player_name}' not found.")


def find_league_id(league_name: str) -> int:
    """Find league ID from name"""
    name_lower = league_name.lower().strip()
    if name_lower in LEAGUE_IDS:
        return LEAGUE_IDS[name_lower]
    raise ValueError(f"League '{league_name}' not found.")


def find_team_id(team_name: str) -> int:
    """Find team ID from name"""
    name_lower = team_name.lower().strip()
    if name_lower in TEAM_IDS:
        return TEAM_IDS[name_lower]
    raise ValueError(f"Team '{team_name}' not found.")


def execute_tool(tool_name: str, tool_input: dict) -> dict:
    """Execute tools called by Gemini"""
    try:
        # ===== PLAYER ENDPOINTS =====
        if tool_name == "get_player_stats":
            player_id = int(tool_input['player_id'])
            season = int(tool_input.get('season', 2024))
            data = football_api.get_player_stats(player_id, season)
            return {'success': True, 'player_id': player_id, 'data': data}

        elif tool_name == "get_player_transfers":
            player_id = int(tool_input['player_id'])
            data = football_api.get_player_transfers(player_id)
            return {'success': True, 'player_id': player_id, 'data': data}

        elif tool_name == "get_player_info":
            player_id = int(tool_input['player_id'])
            season = int(tool_input.get('season', 2024))
            data = football_api.get_player_info(player_id, season)
            return data

        elif tool_name == "get_player_trophies":
            player_id = int(tool_input['player_id'])
            data = football_api.get_trophies(player_id=player_id)
            return {'success': True, 'player_id': player_id, 'data': data}

        # ===== TEAM ENDPOINTS =====
        elif tool_name == "get_team_squad":
            team_id = int(tool_input['team_id'])
            data = football_api.get_team_squad(team_id)
            return {'success': True, 'team_id': team_id, 'data': data}

        elif tool_name == "get_team_statistics":
            team_id = int(tool_input['team_id'])
            league_id = int(tool_input['league_id'])
            season = int(tool_input.get('season', 2024))
            data = football_api.get_team_statistics(team_id, league_id, season)
            return {'success': True, 'team_id': team_id, 'data': data}

        # ===== LEAGUE ENDPOINTS =====
        elif tool_name == "get_top_scorers":
            league_id = int(tool_input['league_id'])
            season = int(tool_input.get('season', 2024))
            data = football_api.get_top_scorers(league_id, season)
            return {'success': True, 'league_id': league_id, 'data': data}

        elif tool_name == "get_top_assists":
            league_id = int(tool_input['league_id'])
            season = int(tool_input.get('season', 2024))
            data = football_api.get_top_assists(league_id, season)
            return {'success': True, 'league_id': league_id, 'data': data}

        elif tool_name == "get_standings":
            league_id = int(tool_input['league_id'])
            season = int(tool_input.get('season', 2024))
            data = football_api.get_standings(league_id, season)
            return {'success': True, 'league_id': league_id, 'data': data}

        # ===== FIXTURES ENDPOINTS =====
        elif tool_name == "get_fixtures":
            team_id = int(tool_input['team_id']) if 'team_id' in tool_input else None
            league_id = int(tool_input['league_id']) if 'league_id' in tool_input else None
            season = int(tool_input.get('season', 2024))
            data = football_api.get_fixtures(team_id, league_id, season)
            return {'success': True, 'data': data}

        elif tool_name == "get_head_to_head":
            team1_id = int(tool_input['team1_id'])
            team2_id = int(tool_input['team2_id'])
            data = football_api.get_head_to_head(team1_id, team2_id)
            return {'success': True, 'data': data}

        elif tool_name == "get_fixture_events":
            fixture_id = int(tool_input['fixture_id'])
            data = football_api.get_fixture_events(fixture_id)
            return {'success': True, 'fixture_id': fixture_id, 'data': data}

        elif tool_name == "get_fixture_lineups":
            fixture_id = int(tool_input['fixture_id'])
            data = football_api.get_fixture_lineups(fixture_id)
            return {'success': True, 'fixture_id': fixture_id, 'data': data}

        elif tool_name == "get_predictions":
            fixture_id = int(tool_input['fixture_id'])
            data = football_api.get_predictions(fixture_id)
            return {'success': True, 'fixture_id': fixture_id, 'data': data}

        # ===== INJURIES =====
        elif tool_name == "get_injuries":
            player_id = int(tool_input['player_id']) if 'player_id' in tool_input else None
            team_id = int(tool_input['team_id']) if 'team_id' in tool_input else None
            data = football_api.get_injuries(team_id, player_id)
            return {'success': True, 'data': data}

        # ===== SEARCH HELPERS =====
        elif tool_name == "search_player_by_name":
            player_name = tool_input['player_name']
            player_id = find_player_id(player_name)
            return {'success': True, 'player_name': player_name, 'player_id': player_id}

        elif tool_name == "search_league_by_name":
            league_name = tool_input['league_name']
            league_id = find_league_id(league_name)
            return {'success': True, 'league_name': league_name, 'league_id': league_id}

        elif tool_name == "search_team_by_name":
            team_name = tool_input['team_name']
            team_id = find_team_id(team_name)
            return {'success': True, 'team_name': team_name, 'team_id': team_id}

        else:
            return {'success': False, 'error': f"Unknown tool: {tool_name}"}

    except FootballAPIError as e:
        return {'success': False, 'error': f"API Error: {str(e)}"}
    except Exception as e:
        return {'success': False, 'error': f"Error: {str(e)}"}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({'error': 'Empty message'}), 400

        response = gemini.chat(user_message, tool_executor=execute_tool)
        return jsonify({'response': response})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/reset', methods=['POST'])
def reset():
    gemini.reset_conversation()
    return jsonify({'status': 'Conversation reset'})


if __name__ == '__main__':
    print("=" * 60)
    print("🚀 FOOTBALL AI ASSISTANT")
    print("=" * 60)
    print()
    
    # Use environment variable for port (Render requirement)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)