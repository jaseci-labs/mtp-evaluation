import from mtllm.llms {OpenAI}

glob llm = OpenAI(model_name="gpt-4o", verbose=False);

obj P {
    has x: int, y: int;
}

obj W {
    has s: P, e: P;
}

obj M {
    has w: list[W], o: list[P];
    has en: list[P];
    has pl: P;
}

obj Level {
    has name: str, difficulty: int;
    has w: int, h: int, wls: int, ens: int;
    has map: M;
}

obj LevelManager {
    has current_level: int = 0, current_difficulty: int = 1,
        prev_levels: list[Level] = [];

    def create_next_level(last_levels: list[Level]) -> Level by llm();

    def get_next_level -> Level {
        self.current_level += 1;
        # Keeping Only the Last 3 Levels
        if len(self.prev_levels) > 3 {
            self.prev_levels.pop(0);
        }
        # Generating the New Level
        new_level = self.create_next_level(
            self.prev_levels,
        );
        self.prev_levels.append(new_level);
        # Increasing the Difficulty for end of every 2 Levels
        if self.current_level % 2 == 0 {
            self.current_difficulty += 1;
        }
        return new_level;
    }
}

# '''Get the map of the level'''
# can get_map(level: Level) -> str {
#     map_tiles = [['.' for _ in range(level.width)] for _ in range(level.height)];
    
#     for wall in level.map.walls {
#         for x in range(wall.start_pos.x, wall.end_pos.x + 1) {
#             for y in range(wall.start_pos.y, wall.end_pos.y + 1) {
#                 map_tiles[y-1][x-1] = 'B';
#             }
#         }
#     }
    
#     for obs in level.map.small_obstacles {
#         map_tiles[obs.y-1][obs.x-1] = 'B';
#     }
    
#     for enemy in level.map.enemies {
#         map_tiles[enemy.y-1][enemy.x-1] = 'E';
#     }
#     map_tiles[level.map.player_pos.y-1][level.map.player_pos.x-1] = 'P';
#     map_tiles = [['B'] + row + ['B'] for row in map_tiles];
#     map_tiles = [['B' for _ in range(level.width + 2)]] + map_tiles + [['B' for _ in range(level.width + 2)]];
#     return [''.join(row) for row in map_tiles];
# }

with entry {
    level_manager = LevelManager();
    for i in range(2) {
        new_level = level_manager.get_next_level();
        print(new_level);
        # print('\n'.join(get_map(new_level)));
    }
}
