import from mtllm.llms {OpenAI}

glob llm = OpenAI(model_name="gpt-4o");

obj P {
    has x: int, y: int;
}

obj W {
    has s: P, e: P;
}

obj M {
    has w: list[W], b: list[P];
    has e: list[P];
    has p: P;
}

obj L {
    has n: str, d: int;
    has w: int, h: int;
    has m: M;
}

obj LevelManager {
    has current_level: int = 0, current_difficulty: int = 1,
        prev_levels: list[Level] = [];

    def foo(l: list[L]) -> L by llm();

    def gen_level -> L {
        self.current_level += 1;
        # Keeping Only the Last 3 Levels
        if len(self.prev_levels) > 3 {
            self.prev_levels.pop(0);
        }
        # Generating the New Level
        new_level = self.foo(
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
        new_level = level_manager.gen_level();
        print(new_level);
    }
}
