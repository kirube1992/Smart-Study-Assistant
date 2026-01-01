def extract_difficulty_features(self):
        if not self.tokens:
            self.preprocess_text()
        word_count = len(self.tokens)
        if word_count == 0:
            return[0,0,0,0]
        avg_word_length = sum(len(w) for w in self.tokens)/word_count
        unique_ratio = len(set(self.tokens)) / word_count
        long_word_ratio = len([w for w in self.tokens if len(w) >6]) /word_count

        return [
            word_count,
            avg_word_length,
            unique_ratio,
            long_word_ratio
        ]