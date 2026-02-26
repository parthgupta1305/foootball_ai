"""
Gemini LLM Client - COMPLETE with ALL tools
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class GeminiClient:
    """Client for interacting with Gemini API"""
    
    def __init__(self):
        """Initialize Gemini client with API key"""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        
        # Create all tools
        tools = [genai.protos.Tool(function_declarations=self.create_all_functions())]
        
        self.model = genai.GenerativeModel('gemini-2.5-flash', tools=tools)
        self.chat_session = self.model.start_chat(history=[])
    
    def create_all_functions(self):
        """Create ALL function declarations"""
        return [
            # ===== PLAYER FUNCTIONS =====
            genai.protos.FunctionDeclaration(
                name="get_player_stats",
                description="Get detailed player statistics including goals, assists, matches, ratings for a season",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "player_id": genai.protos.Schema(type=genai.protos.Type.INTEGER, description="Player ID"),
                        "season": genai.protos.Schema(type=genai.protos.Type.INTEGER, description="Season year (default 2024)")
                    },
                    required=["player_id"]
                )
            ),
            genai.protos.FunctionDeclaration(
                name="get_player_transfers",
                description="Get complete transfer history for a player",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "player_id": genai.protos.Schema(type=genai.protos.Type.INTEGER, description="Player ID")
                    },
                    required=["player_id"]
                )
            ),
            genai.protos.FunctionDeclaration(
                name="get_player_info",
                description="Get comprehensive player info (stats + transfers combined)",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "player_id": genai.protos.Schema(type=genai.protos.Type.INTEGER, description="Player ID"),
                        "season": genai.protos.Schema(type=genai.protos.Type.INTEGER, description="Season (default 2024)")
                    },
                    required=["player_id"]
                )
            ),
            genai.protos.FunctionDeclaration(
                name="get_player_trophies",
                description="Get all trophies won by a player",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "player_id": genai.protos.Schema(type=genai.protos.Type.INTEGER, description="Player ID")
                    },
                    required=["player_id"]
                )
            ),
            # ===== TEAM FUNCTIONS =====
            genai.protos.FunctionDeclaration(
                name="get_team_squad",
                description="Get team squad/roster with all players. Use when asking 'who plays for X', 'show me X squad', 'list X players', 'main striker for X'",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "team_id": genai.protos.Schema(type=genai.protos.Type.INTEGER, description="Team ID")
                    },
                    required=["team_id"]
                )
            ),
            genai.protos.FunctionDeclaration(
                name="get_team_statistics",
                description="Get team stats for a season (goals, wins, losses)",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "team_id": genai.protos.Schema(type=genai.protos.Type.INTEGER, description="Team ID"),
                        "league_id": genai.protos.Schema(type=genai.protos.Type.INTEGER, description="League ID"),
                        "season": genai.protos.Schema(type=genai.protos.Type.INTEGER, description="Season (default 2024)")
                    },
                    required=["team_id", "league_id"]
                )
            ),
            # ===== LEAGUE FUNCTIONS =====
            genai.protos.FunctionDeclaration(
                name="get_top_scorers",
                description="Get top goal scorers in a league",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "league_id": genai.protos.Schema(type=genai.protos.Type.INTEGER, description="League ID"),
                        "season": genai.protos.Schema(type=genai.protos.Type.INTEGER, description="Season (default 2024)")
                    },
                    required=["league_id"]
                )
            ),
            genai.protos.FunctionDeclaration(
                name="get_top_assists",
                description="Get top assists providers in a league",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "league_id": genai.protos.Schema(type=genai.protos.Type.INTEGER, description="League ID"),
                        "season": genai.protos.Schema(type=genai.protos.Type.INTEGER, description="Season (default 2024)")
                    },
                    required=["league_id"]
                )
            ),
            genai.protos.FunctionDeclaration(
                name="get_standings",
                description="Get league table/standings",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "league_id": genai.protos.Schema(type=genai.protos.Type.INTEGER, description="League ID"),
                        "season": genai.protos.Schema(type=genai.protos.Type.INTEGER, description="Season (default 2024)")
                    },
                    required=["league_id"]
                )
            ),
            # ===== FIXTURES FUNCTIONS =====
            genai.protos.FunctionDeclaration(
                name="get_fixtures",
                description="Get upcoming matches/fixtures",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "team_id": genai.protos.Schema(type=genai.protos.Type.INTEGER, description="Team ID (optional)"),
                        "league_id": genai.protos.Schema(type=genai.protos.Type.INTEGER, description="League ID (optional)"),
                        "season": genai.protos.Schema(type=genai.protos.Type.INTEGER, description="Season (default 2024)")
                    }
                )
            ),
            genai.protos.FunctionDeclaration(
                name="get_head_to_head",
                description="Get head-to-head history between two teams. Use when asking 'X vs Y history', 'last time X played Y', 'who wins more X or Y'",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "team1_id": genai.protos.Schema(type=genai.protos.Type.INTEGER, description="First team ID"),
                        "team2_id": genai.protos.Schema(type=genai.protos.Type.INTEGER, description="Second team ID")
                    },
                    required=["team1_id", "team2_id"]
                )
            ),
            genai.protos.FunctionDeclaration(
                name="get_fixture_events",
                description="Get match events (goals, cards, substitutions) for a specific match",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "fixture_id": genai.protos.Schema(type=genai.protos.Type.INTEGER, description="Match/fixture ID")
                    },
                    required=["fixture_id"]
                )
            ),
            genai.protos.FunctionDeclaration(
                name="get_fixture_lineups",
                description="Get starting lineups for a match",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "fixture_id": genai.protos.Schema(type=genai.protos.Type.INTEGER, description="Match/fixture ID")
                    },
                    required=["fixture_id"]
                )
            ),
            genai.protos.FunctionDeclaration(
                name="get_predictions",
                description="Get AI predictions for a match outcome",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "fixture_id": genai.protos.Schema(type=genai.protos.Type.INTEGER, description="Match/fixture ID")
                    },
                    required=["fixture_id"]
                )
            ),
            # ===== INJURIES =====
            genai.protos.FunctionDeclaration(
                name="get_injuries",
                description="Get injury information. Use when asking 'is X injured', 'injury list', 'who is injured'",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "player_id": genai.protos.Schema(type=genai.protos.Type.INTEGER, description="Player ID (optional)"),
                        "team_id": genai.protos.Schema(type=genai.protos.Type.INTEGER, description="Team ID (optional)")
                    }
                )
            ),
            # ===== SEARCH HELPERS =====
            genai.protos.FunctionDeclaration(
                name="search_player_by_name",
                description="Search for player ID by name",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "player_name": genai.protos.Schema(type=genai.protos.Type.STRING, description="Player name")
                    },
                    required=["player_name"]
                )
            ),
            genai.protos.FunctionDeclaration(
                name="search_league_by_name",
                description="Search for league ID by name",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "league_name": genai.protos.Schema(type=genai.protos.Type.STRING, description="League name")
                    },
                    required=["league_name"]
                )
            ),
            genai.protos.FunctionDeclaration(
                name="search_team_by_name",
                description="Search for team ID by name",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "team_name": genai.protos.Schema(type=genai.protos.Type.STRING, description="Team name")
                    },
                    required=["team_name"]
                )
            )
        ]
    
    def chat(self, user_message: str, tool_executor=None) -> str:
        """Send message and handle function calls"""
        try:
            response = self.chat_session.send_message(user_message)
            
            max_iterations = 10  # Increased for complex queries
            iteration = 0
            
            while iteration < max_iterations:
                if not response.candidates:
                    break
                    
                parts = response.candidates[0].content.parts
                if not parts or not hasattr(parts[0], 'function_call'):
                    break
                
                function_call = parts[0].function_call
                if not function_call:
                    break
                    
                function_name = function_call.name
                function_args = dict(function_call.args)
                
                print(f"[FUNCTION CALL {iteration+1}] {function_name} with args: {function_args}")
                
                if tool_executor:
                    result = tool_executor(function_name, function_args)
                    
                    response = self.chat_session.send_message(
                        genai.protos.Content(
                            parts=[
                                genai.protos.Part(
                                    function_response=genai.protos.FunctionResponse(
                                        name=function_name,
                                        response={"result": result}
                                    )
                                )
                            ]
                        )
                    )
                else:
                    break
                
                iteration += 1
            
            if response.candidates and response.candidates[0].content.parts:
                return response.text
            else:
                return "I couldn't generate a response. Please try again."
                
        except Exception as e:
            return f"Error: {str(e)}"
    
    def reset_conversation(self):
        """Clear conversation history"""
        self.chat_session = self.model.start_chat(history=[])