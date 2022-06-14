import logging

if __name__ == '__main__':
	with open("sample.txt") as f:
		firstline = f.readline().rstrip()

	logging.info("asd")
	print(firstline)
