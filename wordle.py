class Wordle:
	def __init__(self, first_guess, word_length=5, word_list_file='words_alpha.txt'):
		self.correct_chars = []
		self.invalid_chars = []
		self.incorrect_position_chars = []
		self.current_guess = first_guess
		self.guesses = []
		self.word_list_file = word_list_file
		self.remaining_words = self.get_all_words(word_length)

	def get_all_words(self, word_length):
		word_list = set()
		with open(self.word_list_file) as words:
			for word in words:
				if len(word) == word_length:
					word_list.add(word)	
		return words

	def find_answer(self):
		while(True):
			self.guesses.append(self.current_guess)
			self.next_words = self.find_next_words()
			self.current_guess = self.find_next_word()
			if self.is_correct():
				break
		return self.current_guess

	def find_next_words(self):
		self.valid_chars = [ch for ch in self.current_guess]
		self.correct_chars = self.find_correct_chars()
		self.incorrect_position_chars = self.find_incorrect_position_chars()
		self.invalid_chars.extend(self.find_invalid_chars())
		self.get_valid_remaining_words()
		return self.remaining_words

	def find_next_word(self):
		next_words = iter(self.next_words)
		while(True):
			next_word = next(next_words)
			user_answer = input(f'Try "{next_word}". Is it acceptable by Wordle? (y/n)[y]: ')
			while (user_answer.lower() not in ['y', 'ye', 'yes', '', 'n', 'no']):
				user_answer = input('incorrect answer, type "y" for yes or "n" fro no: ')
			if user_answer.startswith('y') or not user_answer:
				return next_word
			self.remaining_words.remove(next_word)


	def find_correct_chars(self):
		correct_chars = input("Enter currect chars (Green chars) separated with space: ")
		return [ch for ch in correct_chars.split(" ") if ch in self.valid_chars]

	def find_incorrect_position_chars(self):
		incorrect_chars = input("Enter chars which are not in correct position (Yellow chars) seperated with space: ")
		return [ch for ch in incorrect_chars.split(" ") if ch in self.valid_chars]

	def find_invalid_chars(self):
		return [ch for ch in self.valid_chars if ch not in self.correct_chars + self.incorrect_position_chars]

	def get_valid_remaining_words(self):
		for ch in self.invalid_chars:
			self.remaining_words = [word for word in self.remaining_words if ch not in word]
		for ch in self.correct_chars:
			index = self.current_guess.index(ch)
			self.remaining_words = [word for word in self.remaining_words if word[index] == ch]
		for ch in self.incorrect_position_chars:
			self.remaining_words = [word for word in self.remaining_words if ch in word]
		for ch in self.incorrect_position_chars:
			index = self.current_guess.index(ch)
			self.remaining_words = [word for word in self.remaining_words if word[index] != ch]
		
	def is_correct(self):
		user_answer = input(f'Okay, "{self.current_guess}", Is it correct? (y/n)[n]: ')
		while (user_answer.lower() not in ['y', 'ye', 'yes', '', 'n', 'no']):
			user_answer = input('incorrect answer, type "y" for yes or "n" fro no: ')
		if user_answer.startswith('y'):
			return True
		return False
			
		
if __name__ == '__main__':
	guess = input("What was your first guess?: ")
	wordle = Wordle(guess)
	wordle.find_answer()
	print("Happy to help!")



				










