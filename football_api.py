"""
API-Football Wrapper (Direct API) - COMPLETE VERSION
Official football data API from api-football.com
"""

import requests
import time
import os
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()


class FootballAPIError(Exception):
    """Custom exception for API errors"""
    pass


class FootballAPI:
    """
    Wrapper for API-Football Direct API
    Free tier: 100 requests/day
    """
    
    BASE_URL = "https://v3.football.api-sports.io"
    
    def __init__(self):
        """Initialize API client"""
        self.api_key = os.getenv('API_FOOTBALL_KEY')
        if not self.api_key:
            raise ValueError("API_FOOTBALL_KEY not found in .env file")
        
        self.headers = {
            "x-apisports-key": self.api_key
        }
        
        # Simple in-memory cache
        self.cache = {}
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 1  # 1 second between requests
    
    def _rate_limit(self):
        """Enforce rate limiting"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()
    
    def _get_from_cache(self, cache_key: str) -> Optional[Dict]:
        """Check cache"""
        if cache_key in self.cache:
            cached_data, cached_time = self.cache[cache_key]
            # Cache for 24 hours
            if time.time() - cached_time < 86400:
                print(f"[CACHE HIT] {cache_key}")
                return cached_data
        return None
    
    def _save_to_cache(self, cache_key: str, data: Dict):
        """Save to cache"""
        self.cache[cache_key] = (data, time.time())
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make API request with caching"""
        cache_key = f"{endpoint}_{str(params)}"
        
        # Check cache
        cached = self._get_from_cache(cache_key)
        if cached:
            return cached
        
        # Rate limit
        self._rate_limit()
        
        # Make request
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            print(f"[API REQUEST] {endpoint} with params: {params}")
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Check for API errors
            if data.get('errors') and len(data.get('errors', {})) > 0:
                raise FootballAPIError(f"API Error: {data['errors']}")
            
            # Save to cache
            self._save_to_cache(cache_key, data)
            
            return data
            
        except requests.exceptions.RequestException as e:
            raise FootballAPIError(f"Request failed: {e}")
    
    # ========== Player Endpoints ==========
    
    def get_player_stats(self, player_id: int, season: int = 2024) -> Dict:
        """Get player statistics for a season"""
        params = {"id": player_id, "season": season}
        return self._make_request("players", params)
    
    def get_player_transfers(self, player_id: int) -> Dict:
        """Get player transfer history"""
        params = {"player": player_id}
        return self._make_request("transfers", params)
    
    def search_player(self, name: str, season: int = 2024) -> Dict:
        """Search for a player by name"""
        params = {"search": name, "season": season}
        return self._make_request("players", params)
    
    def get_player_info(self, player_id: int, season: int = 2024) -> Dict:
        """Get comprehensive player information"""
        try:
            stats = self.get_player_stats(player_id, season)
            transfers = self.get_player_transfers(player_id)
            
            player_data = {}
            if stats.get('response') and len(stats['response']) > 0:
                player_info = stats['response'][0]['player']
                player_stats = stats['response'][0]['statistics']
                
                player_data = {
                    'name': player_info.get('name'),
                    'age': player_info.get('age'),
                    'nationality': player_info.get('nationality'),
                    'photo': player_info.get('photo'),
                    'stats': player_stats
                }
            
            return {
                'success': True,
                'player_id': player_id,
                'season': season,
                'data': player_data,
                'transfers': transfers.get('response', [])
            }
        except Exception as e:
            return {
                'success': False,
                'player_id': player_id,
                'error': str(e)
            }
    
    def get_team_squad(self, team_id: int) -> Dict:
        """Get team squad/roster with all players"""
        params = {"team": team_id}
        return self._make_request("players/squads", params)
    
    # ========== League & Competition Endpoints ==========
    
    def get_top_scorers(self, league_id: int, season: int = 2024) -> Dict:
        """Get top scorers in a league"""
        params = {"league": league_id, "season": season}
        return self._make_request("players/topscorers", params)
    
    def get_top_assists(self, league_id: int, season: int = 2024) -> Dict:
        """Get top assists in a league"""
        params = {"league": league_id, "season": season}
        return self._make_request("players/topassists", params)
    
    def get_top_yellow_cards(self, league_id: int, season: int = 2024) -> Dict:
        """Get players with most yellow cards"""
        params = {"league": league_id, "season": season}
        return self._make_request("players/topyellowcards", params)
    
    def get_top_red_cards(self, league_id: int, season: int = 2024) -> Dict:
        """Get players with most red cards"""
        params = {"league": league_id, "season": season}
        return self._make_request("players/topredcards", params)
    
    def get_standings(self, league_id: int, season: int = 2024) -> Dict:
        """Get league standings/table"""
        params = {"league": league_id, "season": season}
        return self._make_request("standings", params)
    
    # ========== Fixtures & Matches Endpoints ==========
    
    def get_fixtures(self, team_id: int = None, league_id: int = None, season: int = 2024, 
                     date: str = None, next_matches: int = 5) -> Dict:
        """Get fixtures/matches"""
        params = {}
        if date:
            params["date"] = date
        else:
            params["season"] = season
        
        if team_id:
            params["team"] = team_id
            params["next"] = next_matches
        elif league_id:
            params["league"] = league_id
        
        return self._make_request("fixtures", params)
    
    def get_head_to_head(self, team1_id: int, team2_id: int) -> Dict:
        """Get head-to-head records between two teams"""
        params = {"h2h": f"{team1_id}-{team2_id}"}
        return self._make_request("fixtures/headtohead", params)
    
    def get_fixture_events(self, fixture_id: int) -> Dict:
        """Get match events (goals, cards, substitutions)"""
        params = {"fixture": fixture_id}
        return self._make_request("fixtures/events", params)
    
    def get_fixture_lineups(self, fixture_id: int) -> Dict:
        """Get starting lineups for a match"""
        params = {"fixture": fixture_id}
        return self._make_request("fixtures/lineups", params)
    
    def get_fixture_statistics(self, fixture_id: int) -> Dict:
        """Get detailed match statistics"""
        params = {"fixture": fixture_id}
        return self._make_request("fixtures/statistics", params)
    
    def get_fixture_players(self, fixture_id: int) -> Dict:
        """Get player statistics for a specific match"""
        params = {"fixture": fixture_id}
        return self._make_request("fixtures/players", params)
    
    # ========== Team Endpoints ==========
    
    def get_team_statistics(self, team_id: int, league_id: int, season: int = 2024) -> Dict:
        """Get team statistics for a season"""
        params = {"team": team_id, "league": league_id, "season": season}
        return self._make_request("teams/statistics", params)
    
    def get_team_info(self, team_id: int) -> Dict:
        """Get team information"""
        params = {"id": team_id}
        return self._make_request("teams", params)
    
    # ========== Predictions ==========
    
    def get_predictions(self, fixture_id: int) -> Dict:
        """Get AI predictions for a match"""
        params = {"fixture": fixture_id}
        return self._make_request("predictions", params)
    
    # ========== Injuries & Sidelined ==========
    
    def get_injuries(self, team_id: int = None, player_id: int = None, 
                     league_id: int = None, season: int = None) -> Dict:
        """Get injury information"""
        params = {}
        if player_id:
            params["player"] = player_id
        elif team_id:
            params["team"] = team_id
        if league_id:
            params["league"] = league_id
        if season:
            params["season"] = season
        return self._make_request("injuries", params)
    
    # ========== Coaches & Venues ==========
    
    def get_coach_info(self, coach_id: int) -> Dict:
        """Get coach information"""
        params = {"id": coach_id}
        return self._make_request("coachs", params)
    
    def get_venue_info(self, venue_id: int) -> Dict:
        """Get stadium/venue information"""
        params = {"id": venue_id}
        return self._make_request("venues", params)
    
    # ========== Trophies ==========
    
    def get_trophies(self, player_id: int = None, coach_id: int = None) -> Dict:
        """Get trophies won by player or coach"""
        params = {}
        if player_id:
            params["player"] = player_id
        elif coach_id:
            params["coach"] = coach_id
        return self._make_request("trophies", params)
    
    def clear_cache(self):
        """Clear all cached data"""
        self.cache.clear()
        print("Cache cleared")


# Player ID mappings for API-Football
PLAYER_IDS = {
    'messi': 154,
    'lionel messi': 154,
    'cristiano ronaldo': 874,
    'ronaldo': 874,
    'neymar': 276,
    'mbappe': 1486,
    'kylian mbappe': 1486,
    'haaland': 1100,
    'erling haaland': 1100,
    'salah': 306,
    'mohamed salah': 306,
    'kane': 184,
    'harry kane': 184,
    'de bruyne': 629,
    'kevin de bruyne': 629,
    'vinicius': 532,
    'vinicius jr': 532,
    'vinicius junior': 532,
    'benzema': 726,
    'lewandowski': 9,
    'robert lewandowski': 9,
    'son': 832,
    'son heung-min': 832,
    'bellingham': 1100,
    'jude bellingham': 1100,
    'pedri': 882,
    'gavi': 906,
    'rodri': 640,
}

# League IDs for API-Football
LEAGUE_IDS = {
    'premier league': 39,
    'epl': 39,
    'english premier league': 39,
    'la liga': 140,
    'spanish league': 140,
    'serie a': 135,
    'italian league': 135,
    'bundesliga': 78,
    'german league': 78,
    'ligue 1': 61,
    'french league': 61,
    'champions league': 2,
    'ucl': 2,
    'europa league': 3,
    'world cup': 1,
}

# Team IDs for API-Football
TEAM_IDS = {
    'real madrid': 541,
    'barcelona': 529,
    'atletico madrid': 530,
    'manchester united': 33,
    'man united': 33,
    'manchester city': 50,
    'man city': 50,
    'liverpool': 40,
    'chelsea': 49,
    'arsenal': 42,
    'tottenham': 47,
    'spurs': 47,
    'bayern munich': 157,
    'bayern': 157,
    'psg': 85,
    'paris saint germain': 85,
    'juventus': 496,
    'milan': 489,
    'ac milan': 489,
    'inter': 505,
    'inter milan': 505,
}


if __name__ == "__main__":
    # Test the API
    api = FootballAPI()
    
    print("\n=== Testing Endpoints ===")
    
    # Test squad
    print("\n1. Manchester United Squad:")
    squad = api.get_team_squad(33)
    print(f"Players: {len(squad.get('response', [{}])[0].get('players', []))}")
    
    # Test H2H
    print("\n2. Real Madrid vs Barcelona H2H:")
    h2h = api.get_head_to_head(541, 529)
    print(f"Total matches: {len(h2h.get('response', []))}")