## Python Task:

# We’d like you to write us a program that:
# Generates 8-digit hexadecimal codes to be used for 2FA.

# The rules are as follows:
# Every time you run the program, it should emit one 8-digit hexadecimal code;
# It should emit every possible code before repeating;
# It should not print "odd-looking" codes such as 0xAAAAAAAA or 0x01234567 or any commonly used words, phrases, or hexspeak such as 0xDEADBEEF;
# Codes should be emitted in apparently random order.

# If we like what we see, we will invite you to a call to conduct a code review of your program.
import uuid
import time
import pickle
import os.path

from english_words import english_words_lower_alpha_set
from http.server import HTTPServer, BaseHTTPRequestHandler


PORT = 12345
DB_NAME = "hex_database.db"

# # Read DB or create a blank (for simplicity — dict, as it indexed)
if os.path.isfile(DB_NAME): 
    with open(DB_NAME, 'rb') as dbfile:
        USED_HEXS = pickle.load(dbfile)
else:
    USED_HEXS = set([])


def read_leet(leet_string):
    """ Replace numbers with "leet" chars """
    return leet_string.replace("0", "o")\
                      .replace("2", "z")\
                      .replace("3", "e")\
                      .replace("4", "a")\
                      .replace("5", "s")\
                      .replace("6", "g")\
                      .replace("7", "t")\
                      .replace("8", "b")\
                      .replace("9", "g")


def check_words(hex_string):
    """ Split string and check in dictionary """
    is_leet = (hex_string in english_words_lower_alpha_set)  # Check whole word
    
    for x in range(3, len(hex_string) - 2):
        if is_leet:
            break  # Stop search if already detected
        word1, word2 = hex_string[:x], hex_string[x:]
        _is_leet_1 = (word1 in english_words_lower_alpha_set)  # Part I
        _is_leet_2 = (word2 in english_words_lower_alpha_set)  # Part II
        is_leet = _is_leet_1 and _is_leet_2 or is_leet
        print(f"TR = {word1} — {_is_leet_1} . {word2} — {_is_leet_2}")  # Sanity check
    return is_leet


def check_hexspeak(hex_string):
    """ Check if hex number is a hexspeak or 1337 (leet) speak """
    hex_string = read_leet(hex_string)  # Convert numbers to symbols
    print(f"TR = {hex_string}\n")
    if "1" in hex_string:
        return check_words(hex_string.replace("1", "l")) or check_words(hex_string.replace("1", "i"))
    else:
        return check_words(hex_string)
    

def check_not_repeat(check_string):
    """ Update DB with a new hex string or return False """
    if check_string in USED_HEXS:
        return False  # Repeated!
    else:
        USED_HEXS.add(check_string)
        return True


def gen_hex():
    """ Generate hex number from UUID for diversity """
    start = time.time()
    true_flase = True  # Repeat until not leet/hex speak
    while true_flase:
        hex_string = uuid.uuid4().hex
        check_string = hex_string[:8]
        # check_string = "deadbeef"  #  <—— Override for testing purposes
        if check_not_repeat(check_string):
            # Not repeated, check hexspeak 
            true_flase = check_hexspeak(check_string)
    end = time.time()
    print(f"Request handled in: {(end - start):.5f}")
    return str.encode(f"0x{check_string.upper()}")


# —————————————————-  Handle requests
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """ Responds with proper HEX number """
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(gen_hex())


# Start a Server
try:
    httpd = HTTPServer(('127.0.0.1', PORT), SimpleHTTPRequestHandler)
    print(f"Listening to port: {PORT}")
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\nKeyboardInterrupt — Exiting...")
except Exception as e:
    print(f"Exception: {e}")
# Save DB and exit
with open(DB_NAME, 'wb') as dbfile:
    pickle.dump(USED_HEXS, dbfile)  # Save DB to disk
print("Bye!")
