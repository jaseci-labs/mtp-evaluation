import from mtllm.llms {OpenAI}

glob llm = OpenAI(model_name="gpt-4o");

obj Position {
    has x: int, y: int;
}

obj Wall {
    has start: Position, end: Position;
}

obj Map {
    has walls: list[Wall], blocks: list[Position];
    has enemies: list[Position];
    has player: Position;
}

obj Level {
    has name: str, diff: int;
    has wide: int, tall: int, walls: int, enemies: int;
    has map: Map;
}

obj LevelManager {
    has current_level: int = 0, current_difficulty: int = 1,
        prev_levels: list[Level] = [];

    def create_next_level(last_levels: list[Level]) -> Level by llm();

    def gen_level -> tuple(Level, Map) {
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
        return (new_level);
    }
}

with entry {
    level_manager = LevelManager();
    for i in range(2) {
        new_level = level_manager.gen_level();
        print(new_level);
    }
}
