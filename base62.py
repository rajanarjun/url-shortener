
BASE62_DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def encode(number):
  base62_string = ""
  while number > 0:
    remainder = int(number % 62)
    base62_string = BASE62_DIGITS[remainder] + base62_string
    number = int(number / 62)

  return base62_string


def decode(base62_string):
  number = 0
  for i, letter in enumerate(base62_string):
    power = len(base62_string) - i - 1
    index = BASE62_DIGITS.index(letter)
    value = index * (62 ** power)
    number += value

  return number


#
# For Testing
#
if __name__ == "__main__":
  encoded_string = encode(123)
  print(encoded_string)
  decoded_number = decode("1z")
  print(decoded_number)

