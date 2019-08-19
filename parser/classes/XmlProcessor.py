# from Word import Word

class PostProcessor:
	def __init__(self):
		pass

def new():
	for i in range(3):
		yield i

for count,i in enumerate(new()):
	print(count, i)
