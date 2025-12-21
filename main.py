import sys
from os import system

CLEAR_CMD: str = "cls" if sys.platform == "win32" else "clear"

wordle_size: int = 5
words: set[str] = None
BANNED_LETTERS: str = set()
CONTAINED_LETTERS: str = set()

def read_dict(filename: str) -> set[str]:
	output: set[str] = set()

	fp = open(filename, "r", encoding="utf8")
	lines = fp.readlines()
	fp.close()

	for l in lines:
		output.add(l.replace("\r", "").replace("\n", "").upper())

	return output

def filter_by_length(words: set[str], min_length: int, max_length: int) -> set[str]:
	output: set[str] = set({w for w in words if min_length <= len(w) <= max_length})

	return output

def remove_if_banned_letters(words: set[str]) -> set[str]:
	output: set[str] = set()

	if (len(BANNED_LETTERS) > 0):
		for w in words:
			valid: bool = True
			for l in w:
				if l in BANNED_LETTERS:
					valid = False

			if valid:
				output.add(w)

	return output

def keep_if_pattern(words: set[str], pattern: str="-"*5) -> set[str]:
	pairs: dict[int: set] = { i: pattern[i] for i in range(len(pattern)) if (pattern[i] != "-") }
	output: set[str] = set()

	for w in words:
		valid: bool = len(w) == len(pattern)

		if valid:
			for i, l in pairs.items():
				print(i, l)
				valid &= w[i] == l

		if valid:
			output.add(w)

	return output

def remove_if_pattern(words: set[str], pattern: str="-"*5):
	pairs: dict[int: set] = { i: pattern[i] for i in range(len(pattern)) if (pattern[i] != "-") }
	output: set[str] = set()

	for w in words:
		valid: bool = len(w) == len(pattern)

		if valid:
			for i, l in pairs.items():
				print(i, l)
				valid &= w[i] == l

		if not valid:
			output.add(w)

	return output

def remove_if_letter_not_in(words: set[str]) -> set[str]:
	output: set = set()

	if (len(CONTAINED_LETTERS) > 0):
		for w in words:
			valid: bool = True
			for l in CONTAINED_LETTERS:
				if l not in w:
					valid = False
					break

			if valid:
				output.add(w)

	else:
		output = words

	return output

class Actions:
	def reset() -> set[str]:
		system(CLEAR_CMD)
		global BANNED_LETTERS, CONTAINED_LETTERS, wordle_size, words

		BANNED_LETTERS = set()
		CONTAINED_LETTERS = set()

		wordle_size = int(input("How long is the word to guess? : "))

		words = read_dict("words_alpha.txt")
		words = filter_by_length(words, wordle_size, wordle_size)

	def keep_by_pattern() -> None:
		global words

		pattern: str = input("Enter the pattern: ").upper()

		words = keep_if_pattern(words, pattern)

	def remove_by_pattern() -> None:
		global words

		pattern: str = input("Enter the pattern: ").upper()

		words = remove_if_pattern(words, pattern)

	def add_banned_letters() -> None:
		global BANNED_LETTERS, words

		letters: str = input("Enter the banned letters you want to add: ").upper()

		for l in letters:
			BANNED_LETTERS.add(l)

		words = remove_if_banned_letters(words)

	def add_contained_letters() -> None:
		global CONTAINED_LETTERS, words

		letters: str = input("Enter the contained letters you want to add: ").upper()

		for l in letters:
			CONTAINED_LETTERS.add(l)

		words = remove_if_letter_not_in(words)

	def print_words() -> None:
		print(*sorted(words))
		input(" Press 'Enter' to go back to menu ")

	def actions_menu():
		system(CLEAR_CMD)
		lines: list[str] = [
			"[0] Reset",
			"[1] Keep by pattern",
			"[2] Remove by pattern",
			"[3] Add banned letters",
			"[4] Add contained letters",
			"[5] Print remaining words",
			"[6] Quit"
		]

		print(*lines, sep="\n")
		print(f"\n {len(words)} words remaining")
		n: int = int(input("Pick a number: "))

		match n:
			case 0:
				Actions.reset()

			case 1:
				Actions.keep_by_pattern()

			case 2:
				Actions.remove_by_pattern()

			case 3:
				Actions.add_banned_letters()

			case 4:
				Actions.add_contained_letters()

			case 5:
				Actions.print_words()

			case 6:
				sys.exit()

		Actions.actions_menu()


if __name__ == "__main__":
	words: set[str] = None

	if (words == None):
		Actions.reset()

	Actions.actions_menu()