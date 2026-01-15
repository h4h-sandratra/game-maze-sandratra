import requests
# api class
class GameMazeAPI:
    base_url = "https://hire-game-maze.pertimm.dev/"
    def __init__(self, player = "readyPlayer1"):
        self.player = player
        # start a new game
        r = requests.post(self.base_url + "start-game/", data = { 'player': self.player } )
        data = r.json()
        print ( data )
        #get move url
        self.url_move = data['url_move']
        #get discover url
        self.url_discover = data['url_discover']
        #get initial position
        self.position_x = data['position_x']
        self.position_y = data['position_y']

    def move(self, new_x, new_y):
        r = requests.post(self.url_move, data = { 'position_x': new_x, 'position_y' : new_y } )
        data = r.json()
        print ( data )
        return data
    
    def discover(self):
        r = requests.post(self.url_discover)
        data = r.json()
        print ( data )
        return data
    
class GameMaze:
    def __init__(self, api: GameMazeAPI):
        self.api = api


if __name__ == "__main__":
    api = GameMazeAPI()