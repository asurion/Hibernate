from random import SystemRandom


def generateRandomString(size):
  chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

  cryptogen = SystemRandom()
  randomNumbers = [cryptogen.randrange(len(chars)) for i in range(size)]

  randomChars = [chars[i] for i in randomNumbers]
  randomStr = ''.join(randomChars)

  return randomStr