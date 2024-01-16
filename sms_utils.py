import re

#no randomness, purely based on 160 character limit split
def make_message_list(message: str):
    sentence_pattern = re.compile(r'(?<=[.!?])\s+')
    sentences = sentence_pattern.split(message)
    result = []
    current_string = ""
    for sen in sentences:
        if len(current_string) + len(sen)  <= 160:  
            current_string = current_string +" "+sen
        else:
            result.append(add_space_after_url(current_string))
            current_string = sen
    result.append(add_space_after_url(current_string))
    return result

def add_space_after_url(string: str):
    words = string.split()
    for i, word in enumerate(words):
        if word.startswith("http://") or word.startswith("https://"):
            if word[-1] in ".,!?;:":
                words[i] = word[:-1] + " " + word[-1] + " "
            else:
                words[i] = word + " "
    return " ".join(words)

class Not_US_or_Canada_number(Exception):
    """Custom exception for invalid US/Canada phone numbers."""
    pass

def format_US_number(num: str):
    num = ''.join([char for char in num if char.isdigit()])
    tup_num = tuple(num)
    
    pair = ["0", "1"]

    match tup_num:
        case ['+', '1', *rest] if len(num) == 12:
            return num
        case [first, _, _, fourth, *rest] if len(num) == 10 and first not in pair and fourth not in pair:
            return '+1' + num
        case ['1', *rest] if len(num) == 11:
            return '+' + num
        case _:
            print('not a US or Canada number')
            raise Not_US_or_Canada_number('Not a valid US or Canada number')