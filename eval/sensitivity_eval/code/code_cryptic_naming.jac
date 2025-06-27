import from mtllm.llms {OpenAI}

glob llm = OpenAI(model_name="gpt-4o");

obj Pos {
    has lat: int, long: int;
}

obj Chasm {
    has start: Pos, end: Pos;
}

obj City {
    has chasms: list[Chasm], wells: list[Pos];
    has minion_pos: list[Pos];
    has player: Pos;
}

obj Boss {
    has name: str, diff: int;
    has wide: int, tall: int, walls: int, minions: int;
    has city: City;
}

obj LevelManager {
    has current_level: int = 0, current_difficulty: int = 1,
        prev_levels: list[Boss] = [];

    def to_next_Boss(cities: list[Boss]) -> Boss by llm();

    def gen_level -> tuple(Level, Map) {
        self.current_level += 1;
        # Keeping Only the Last 3 Levels
        if len(self.prev_levels) > 3 {
            self.prev_levels.pop(0);
        }
        # Generating the New Level
        new_level = self.to_next_Boss(
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
