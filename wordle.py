from utils import get_user_input
from exceptions import AnswerNotFoundError

class Wordle:
	def __init__(self, first_guess, word_list_file='words_alpha.txt'):
		self.correct_chars_index = []
		self.invalid_chars= []
		self.incorrect_position_chars_index = []
		self.current_guess = first_guess
		self.guesses = []
		self.word_list_file = word_list_file
		self.remaining_words = self.get_all_words()

	def get_all_words(self):
		word_list = set()
		with open(self.word_list_file) as words:
			for word in words:
				# word has a trailing \n character, so strip it
				word = word.strip()
				if len(word) == len(self.current_guess):
					word_list.add(word)	
		return word_list

	def find_answer(self):
		while(True):
			self.guesses.append(self.current_guess)
			self.next_words = self.find_next_words()
			try:
				self.current_guess = self.find_next_word()
			except StopIteration:
				raise AnswerNotFoundError("No more words found")
			if self.is_correct():
				break
		return self.current_guess

	def find_next_words(self):
		self.valid_chars = [ch for ch in self.current_guess]
		self.correct_chars_index = list(self.find_correct_chars_index())
		self.incorrect_position_chars_index = list(self.find_incorrect_position_chars_index())
		self.invalid_chars.extend(self.find_invalid_chars())
		self.get_valid_remaining_words()
		return self.remaining_words

	def find_next_word(self):
		next_words = iter(self.next_words)
		while(True):
			next_word = next(next_words)
			user_answer = get_user_input(
       							f'Try "{next_word}". Is it acceptable by Wordle?',
                                valid_answers=['y', 'n'],
                                default_answer='y')
			if user_answer == 'y':
				return next_word
			self.remaining_words.remove(next_word)


	def find_correct_chars_index(self):
		correct_chars = get_user_input("Enter currect chars (Green chars) separated with space: ")
		for ch in correct_chars.split(" "):
			if not ch:
				continue
			if ch not in self.valid_chars:
				raise ValueError(f'{ch} is not a valid character')
			yield self.find_index(ch)

	def find_incorrect_position_chars_index(self):
		incorrect_chars = get_user_input("Enter chars which are not in correct position (Yellow chars) seperated with space: ")
		for ch in incorrect_chars.split(" "):
			if not ch:
				continue
			if ch not in self.valid_chars:
				raise ValueError(f'{ch} is not a valid character')
			yield self.find_index(ch)

	def find_invalid_chars(self):
		valid_chars = [self.current_guess[index] for index in self.correct_chars_index + self.incorrect_position_chars_index]
		return [
      		char
        	for char in self.valid_chars
          	if char not in valid_chars
        ]

	def get_valid_remaining_words(self):
		for char in self.invalid_chars:
			self.remaining_words = [word for word in self.remaining_words if char not in word]
		for index in self.correct_chars_index:
			char = self.current_guess[index]
			self.remaining_words = [word for word in self.remaining_words if word[index] == char]
		for index in self.incorrect_position_chars_index:
			char = self.current_guess[index]
			self.remaining_words = [word for word in self.remaining_words if char in word]
		for index in self.incorrect_position_chars_index:
			char = self.current_guess[index]
			self.remaining_words = [word for word in self.remaining_words if word[index] != char]
		
	def is_correct(self):
		message = f'Okay, "{self.current_guess}", Is it correct?'
		user_answer = get_user_input(message, valid_answers=['y', 'n'], default_answer='n')
		if user_answer == 'y':
			return True
		return False

	def find_index(self, ch):
		indexes = [i for i, c in enumerate(self.current_guess) if c == ch]
		if len(indexes) == 1:
			return indexes[0]
		str_indexes = [str(i + 1) for i in indexes]
		answer = get_user_input(f'{ch} is found more than once. Which one is correct?',
								valid_answers=str_indexes)
		index = int(answer) - 1
		return index
			
		
		
if __name__ == '__main__':
	guess = input("What was your first guess?: ")
	wordle = Wordle(guess)
	try:
		wordle.find_answer()
		print("Happy to help!")
	except AnswerNotFoundError:
		print("Answer not found")
	except ValueError as e:
		print(e)



				










