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
        self.status = data
        
    def move(self, new_x, new_y):
        r = requests.post(self.url_move, data = { 'position_x': new_x, 'position_y' : new_y } )
        data = r.json()
        self.status = data
    
    def discover(self):
        r = requests.get(self.url_discover)
        data = r.json()
        # print ( data )
        return data
    
class MouseMazeSolver:
    
    unresolved = True
    def __init__(self, maze: GameMazeAPI):
        self.maze = maze
        # init maze size with starting position
        self.maze_map = [[0]* (maze.status['position_x'] + 1) for _ in range(maze.status['position_y'] + 1)]
        # mark starting position
        self.maze_map[maze.status['position_y']][maze.status['position_x']] = '1'
        self.print_maze ()
        # evaluate environment
        # self.evaluate_environment()

    def print_maze(self):
        for row in self.maze_map:
            print(" ".join(map(str, row)))

    def update_maze_map(self, position):
        if(self.maze_map[position['y']][position['x']] == 'X') : 
            pass
        elif (
            position['move'] 
            & (position['value'] in (["path", "home", "stop"])) 
            & (self.maze_map[position['y']][position['x']] == 0 ) # pas touche au marqué
            ):
            self.maze_map[position['y']][position['x']] = '1' # if can move 1 
        else :
            self.maze_map[position['y']][position['x']] = '0' 

    def evaluate_environment(self):
        data = self.maze.discover()
        # print (data)
        # update map
        for position in data: 
            #check if position.x in maze map
            if position['y'] >= len(self.maze_map):
                self.extend_maze( 1, 0) # add one row
            if position['x'] >= len(self.maze_map[0]):
                self.extend_maze(0, 1) # add one column
            # update maze map
            self.update_maze_map(position)
        self.print_maze()
        # # Check if we need to extend the maze map
        # if current_y >= len(self.maze_map):
        #     self.extend_maze(current_y - len(self.maze_map) + 1, 0)
        # if current_x >= len(self.maze_map[0]):
        #     self.extend_maze(0, current_x - len(self.maze_map[0]) + 1)
    
    def extend_maze(self, new_rows, new_cols):
        # Extend the number of rows
        for _ in range(new_rows):
            self.maze_map.append([0] * len(self.maze_map[0]))
        
        # Extend the number of columns in existing rows
        for row in self.maze_map:
            row.extend([0] * new_cols)

    def resolve_maze(self):
        current_x = self.maze.status['position_x']
        current_y = self.maze.status['position_y']
        # mark current position as visited
        self.maze_map[current_y][current_x] = 'X'
        self.evaluate_environment()
        # move if maze map is possible 1
        if (self.maze_map[current_y][current_x + 1] == '1' and self.unresolved ) :
            print ("move right")
            self.maze.move(current_x + 1, current_y)
            if ( self.maze.status['dead']  | self.maze.status['win'] ):
                self.print_maze()
                print (f"game over dead { self.maze.status['dead'] } win {self.maze.status['win']}")
                self.unresolved = False
                return
            self.resolve_maze()
            self.maze.move(current_x, current_y)

        if (self.maze_map[current_y + 1][current_x ] == '1'  and self.unresolved ) :
            print ("move down")
            self.maze.move(current_x , current_y + 1)
            if ( self.maze.status['dead']  | self.maze.status['win'] ):
                self.print_maze()
                print (f"game over dead { self.maze.status['dead'] } win {self.maze.status['win']}")
                self.unresolved = False
                return
            self.resolve_maze()
            self.maze.move(current_x, current_y)

        if (self.maze_map[current_y -1 ][current_x ] == '1'  and self.unresolved ) :
            print ("move up")
            self.maze.move(current_x , current_y - 1)
            if ( self.maze.status['dead']  | self.maze.status['win'] ):
                self.print_maze()
                print (f"game over dead { self.maze.status['dead'] } win {self.maze.status['win']}")
                self.unresolved = False
                return
            self.resolve_maze()
            self.maze.move(current_x, current_y)

        if (self.maze_map[current_y  ][current_x -1 ] == '1'  and self.unresolved ) :
            print ("move left")
            self.maze.move(current_x  -1 , current_y)
            if ( self.maze.status['dead']  | self.maze.status['win'] ):
                self.print_maze()
                print (f"game over dead { self.maze.status['dead'] } win {self.maze.status['win']}")
                self.unresolved = False
                return
            self.resolve_maze()
            self.maze.move(current_x, current_y)
            
        # revert and uncheck position
        if( self.unresolved ):
            self.maze_map[current_y][current_x] = '1'
        

if __name__ == "__main__":
    server = GameMazeAPI()
    solver = MouseMazeSolver(server)
    solver.resolve_maze()
    solver.print_maze()