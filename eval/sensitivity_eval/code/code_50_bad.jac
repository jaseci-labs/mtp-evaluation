import from mtllm.llms {OpenAI}

glob llm = OpenAI(model_name="gpt-4o");

obj P {
    has x: int, y: int;
}

obj W {
    has s: P, e: P;
}

obj Map {
    has w: list[W], o: list[P];
    has en: list[P];
    has pl: P;
}

obj Level {
    has name: str, difficulty: int;
    has width: int, height: int, num_wall: int, num_enemies: int;
    has time_countdown: int, n_retries_allowed: int;
    has map: Map;
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

with entry {
    level_manager = LevelManager();
    for i in range(2) {
        new_level = level_manager.get_next_level();
        print(new_level);
    }
}
