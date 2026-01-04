from __future__ import annotations

import sys

from os import system
from time import time

CLEAR_CMD: str = "cls" if sys.platform == "win32" else "clear"

wordle_size: int = 5
words: set[str] = None
logger: Logger = None
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
				valid &= w[i] == l

		if valid:
			output.add(w)

	return output

def remove_if_pattern(words: set[str], pattern: str="-"*5):
	pairs: dict[int: set] = { i: pattern[i] for i in range(len(pattern)) if (pattern[i] != "-") }
	output: set[str] = set()

	for w in words:
		valid: bool = len(w) == len(pattern)

		writeWord: bool = True

		if valid:
			for i, l in pairs.items():
				if w[i] == l:
					writeWord = False
					break

		if writeWord:
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

class Logger:
	def __init__(self):
		self.fp = open(f"logs_wordle_{int(time())}.log", "w")

	def close(self) -> None:
		self.fp.close()
		self.fp = None

	def logAction(self, actionCode: int, arg: str, remainingWords: int) -> None:
		if actionCode in Actions.ACTIONS:
			self.fp.write(f"{actionCode}\t{arg}\t{remainingWords}\n")
			self.fp.flush()

class Actions:
	RESET: int = 0
	KEEP_PATTERN: int = 1
	REMOVE_PATTERN: int = 2
	BAN_LETTERS: int = 3
	INCLUDE_LETTERS: int = 4
	LIST_WORDS: int = 5
	EXIT: int = 6

	ACTIONS: list[int] = [RESET, KEEP_PATTERN, REMOVE_PATTERN, BAN_LETTERS, INCLUDE_LETTERS, LIST_WORDS, EXIT]

	def reset() -> set[str]:
		system(CLEAR_CMD)
		global BANNED_LETTERS, CONTAINED_LETTERS, wordle_size, words, logger

		if logger == None:
			logger = Logger()
		else:
			logger.close()
			logger = Logger()

		BANNED_LETTERS = set()
		CONTAINED_LETTERS = set()

		wordle_size = int(input("How long is the word to guess? : "))

		words = read_dict("words_alpha.txt")
		words = filter_by_length(words, wordle_size, wordle_size)
		logger.logAction(Actions.RESET, "RESET", len(words))

	def keep_by_pattern() -> None:
		global words

		pattern: str = input("Enter the pattern: ").upper()

		words = keep_if_pattern(words, pattern)
		logger.logAction(Actions.KEEP_PATTERN, pattern, len(words))

	def remove_by_pattern() -> None:
		global words

		pattern: str = input("Enter the pattern: ").upper()

		words = remove_if_pattern(words, pattern)
		logger.logAction(Actions.REMOVE_PATTERN, pattern, len(words))

	def add_banned_letters() -> None:
		global BANNED_LETTERS, words

		letters: str = input("Enter the banned letters you want to add: ").upper()

		for l in letters:
			BANNED_LETTERS.add(l)

		words = remove_if_banned_letters(words)
		logger.logAction(Actions.BAN_LETTERS, letters, len(words))

	def add_contained_letters() -> None:
		global CONTAINED_LETTERS, words

		letters: str = input("Enter the contained letters you want to add: ").upper()

		for l in letters:
			CONTAINED_LETTERS.add(l)

		words = remove_if_letter_not_in(words)
		logger.logAction(Actions.INCLUDE_LETTERS, letters, len(words))

	def print_words() -> None:
		print(*sorted(words))
		logger.logAction(Actions.LIST_WORDS, "LIST WORDS", len(words))
		input(" Press 'Enter' to go back to menu ")

	def exit_program() -> None:
		global logger

		logger.logAction(Actions.EXIT, "END OF PROGRAM", len(words))
		logger.close()
		logger = None
		sys.exit()

	def actions_menu():
		system(CLEAR_CMD)
		global logger

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
		actionCode: int = int(input("Pick a number: "))

		if actionCode in Actions.ACTIONS:
			match actionCode:
				case Actions.RESET:
					Actions.reset()

				case Actions.KEEP_PATTERN:
					Actions.keep_by_pattern()

				case Actions.REMOVE_PATTERN:
					Actions.remove_by_pattern()

				case Actions.BAN_LETTERS:
					Actions.add_banned_letters()

				case Actions.INCLUDE_LETTERS:
					Actions.add_contained_letters()

				case Actions.LIST_WORDS:
					Actions.print_words()

				case Actions.EXIT:
					Actions.exit_program()

		Actions.actions_menu()

if __name__ == "__main__":
	words: set[str] = None

	if (words == None):
		Actions.reset()

	Actions.actions_menu()