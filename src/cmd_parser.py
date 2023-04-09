import hints

from typing import Any, Union
from dataclasses import dataclass


@dataclass
class ParseSuccess:
	hint: str
	value: Any
	end_idx: int


@dataclass
class ParseFailure:
	msg: str


ParseResult = Union[ParseSuccess, ParseFailure]


def parse(text: str, hint: str) -> ParseResult:
	match hint:
		case "{'LIST:'}{hint}":
			pass

		case "{'UNION:'}{hints}":
			pass

		case "{'EXACT:'}{what}":
			pass

		case hints.STR:					return parse_str(text)
		case hints.STR_WORD:			return parse_str_word(text)
		case hints.STR_FORMATTED:		return parse_str_formatted(text)
		case hints.STR_UNPARSED:		return parse_str_unparsed(text)
		case hints.STR_LIST_UNARGED:	return parse_str_list_unarged(text)

		case hints.NUM:			return parse_num(text)
		case hints.NUM_INT:		return parse_num_int(text)
		case hints.NUM_FLOAT:	return parse_num_float(text)

		case hints.USER:		return parse_reference(text, hints.USER, "@")
		case hints.ROLE:		return parse_reference(text, hints.ROLE, "@&")
		case hints.SELECTOR:	pass
		case hints.USERS:		pass

		case hints.USER_ID:		return parse_id(text, hints.USER_ID)
		case hints.ROLE_ID:		return parse_id(text, hints.ROLE_ID)
		# case hints.USER_IDS:	return parse_id(text, hints.USER_IDS)

		case hints.CHANNEL_TEXT:		return parse_reference(text, hints.CHANNEL_TEXT, "#")
		case hints.CHANNEL_VOICE:		return parse_reference(text, hints.CHANNEL_VOICE, "#")
		case hints.CHANNEL_STAGE:		return parse_reference(text, hints.CHANNEL_STAGE, "#")
		case hints.CHANNEL_THREAD:		return parse_reference(text, hints.CHANNEL_THREAD, "#")
		case hints.CHANNEL_MESSAGEABLE:	return parse_reference(text, hints.CHANNEL_MESSAGEABLE, "#")
		case hints.CHANNEL_VOCAL:		return parse_reference(text, hints.CHANNEL_VOCAL, "#")

		case hints.CHANNEL_DM_ID:			return parse_id(text, hints.CHANNEL_DM_ID)
		case hints.CHANNEL_TEXT_ID:			return parse_id(text, hints.CHANNEL_TEXT_ID)
		case hints.CHANNEL_VOICE_ID:		return parse_id(text, hints.CHANNEL_VOICE_ID)
		case hints.CHANNEL_STAGE_ID:		return parse_id(text, hints.CHANNEL_STAGE_ID)
		case hints.CHANNEL_THREAD_ID:		return parse_id(text, hints.CHANNEL_STAGE_ID)
		case hints.CHANNEL_MESSAGEABLE_ID:	return parse_id(text, hints.CHANNEL_MESSAGEABLE_ID)
		case hints.CHANNEL_VOCAL_ID:		return parse_id(text, hints.CHANNEL_VOCAL_ID)


# \s
def parse_whitespace(text: str) -> ParseResult:
	it = iter(text)
	curr = next(it, "")
	idx = 0

	while curr != "" and curr.isspace():
		curr = next(it, "")
		idx += 1

	return ParseSuccess("", "", idx)


def parse_exact(text: str, what: str) -> ParseResult:
	it = iter(text)
	curr = next(it, "")
	idx = 0

	for c in what:
		if c == curr:
			curr = next(it, "")
			idx += 1
		else:
			return ParseFailure("Expected to match exactly. PLEASE UPDATE THIS VAGUE ERROR!")

	return ParseSuccess("", "", idx)


def parse_id(text: str, hint: str) -> ParseResult:
	it = iter(text)
	idx = parse_whitespace(text).end_idx
	curr = next(it, "")
	for _ in range(idx):
		curr = next(it, "")
	id = 0

	if not curr.isnumeric():
		return ParseFailure("Expected integer when parsing for id")

	res = parse_num_int(text, ">")
	if isinstance(res, ParseFailure):
		return res
	id = res.value
	for _ in range(res.end_idx):
		curr = next(it, "")
		idx += 1

	return ParseSuccess(hint, id, idx)


def parse_reference(text: str, hint: str, specifier: str) -> ParseResult:
	it = iter(text)
	idx = parse_whitespace(text).end_idx
	curr = next(it, "")
	for _ in range(idx):
		curr = next(it, "")

	if curr.isnumeric():
		return parse_id(text, hint)

	if curr != "<":
		return ParseFailure(f"Expected '<{specifier}[0-9]+>'.")
	curr = next(it, "")
	idx += 1

	for s in specifier:
		if curr != s:
			return ParseFailure(f"Expected '{s}' before id.")
		curr = next(it, "")
		idx += 1

	# print(curr)
	# print(text)
	# print(idx)

	res = parse_id(text[idx:], hint)
	if isinstance(res, ParseFailure):
		return res
	for _ in range(res.end_idx):
		curr = next(it, "")
		idx += 1

	if curr != ">":
		return ParseFailure(f"Expected '>', got '{curr}'.")
	curr = next(it, "")
	idx += 1

	res.end_idx = idx

	return res


# [0-9]+ | [0-9]*\.[0-9]*
def parse_num(text: str) -> ParseResult:
	it = iter(text)
	idx = parse_whitespace(text).end_idx
	curr = next(it, "")
	for _ in range(idx):
		curr = next(it, "")
	value = ""
	dot_count = 0

	while curr != "":
		if curr == ".":
			dot_count += 1
			if dot_count > 1:
				return ParseFailure("Unexpected decimal point when parsing integer")
		elif not curr.isnumeric():
			return ParseFailure("Unexpected non-numeric character when parsing integer")

		value += curr
		curr = next(it, "")
		idx += 1

	if dot_count == 0:
		value = int(value)
	else:
		value = float(value)

	return ParseSuccess(hints.NUM_FLOAT, value, idx)


# [0-9]+
def parse_num_int(text: str, force_end: str = "") -> ParseResult:
	it = iter(text)
	idx = parse_whitespace(text).end_idx
	curr = next(it, "")
	for _ in range(idx):
		curr = next(it, "")
	value = ""

	while curr != "" and not curr.isspace() and curr != force_end:
		if curr == ".":
			return ParseFailure("Unexpected decimal point when parsing integer.")
		elif not curr.isnumeric():
			return ParseFailure(f"Unexpected non-numeric character when parsing integer, got '{curr}'.")

		value += curr
		curr = next(it, "")
		idx += 1

	return ParseSuccess(hints.NUM_INT, int(value), idx)


# [0-9]*\.[0-9]*
def parse_num_float(text: str, force_end: str = "") -> ParseResult:
	it = iter(text)
	idx = parse_whitespace(text).end_idx
	curr = next(it, "")
	for _ in range(idx):
		curr = next(it, "")
	value = ""
	dot_count = 0

	while curr != "" and not curr.isspace() and curr != force_end:
		if curr == ".":
			dot_count += 1
			if dot_count > 1:
				return ParseFailure("Unexpected decimal point when parsing integer")
		elif not curr.isnumeric():
			return ParseFailure("Unexpected non-numeric character when parsing integer")

		value += curr
		curr = next(it, "")
		idx += 1

	return ParseSuccess(hints.NUM_FLOAT, float(value), idx)


# [^\s] | ".*"
def parse_str(text: str) -> ParseResult:
	text = text[parse_whitespace(text).end_idx:]
	res = None
	if text[0] == '"':
		res = parse_str_formatted(text)
	else:
		res = parse_str_word(text)
	res.hint = hints.STR
	return res


# [^\s]+
def parse_str_word(text: str) -> ParseResult:
	it = iter(text)
	idx = parse_whitespace(text).end_idx
	curr = next(it, "")
	for _ in range(idx):
		curr = next(it, "")
	value = ""

	while curr != "" and not curr.isspace():
		value += curr
		curr = next(it, "")
		idx += 1

	return ParseSuccess(hints.STR_WORD, value, idx)


# [^\s]+
def parse_str_unparsed(text: str) -> ParseResult:
	it = iter(text)
	idx = parse_whitespace(text).end_idx
	curr = next(it, "")
	for _ in range(idx):
		curr = next(it, "")
	value = ""

	while curr != "":
		value += curr
		curr = next(it, "")
		idx += 1

	return ParseSuccess(hints.STR_UNPARSED, value, idx)


# ".*"
def parse_str_formatted(text: str) -> ParseResult:
	it = iter(text)
	idx = parse_whitespace(text).end_idx
	curr = next(it, "")
	for _ in range(idx):
		curr = next(it, "")
	value = ""

	if curr != '"':
		return ParseFailure("Expected formatted string")
	curr = next(it, "")
	idx += 1

	while curr != "" and curr != '"':
		value += curr
		curr = next(it, "")
		idx += 1

	if curr != '"':
		return ParseFailure("Expected \" before end of statement")
	curr = next(it, "")
	idx += 1

	return ParseSuccess(hints.STR_FORMATTED, value, idx)


# ([^\s]+)+
def parse_str_list_unarged(text: str) -> ParseResult:
	res = parse_str_unparsed(text)

	return ParseSuccess(hints.STR_LIST_UNARGED, res.value.split(), res.end_idx)

