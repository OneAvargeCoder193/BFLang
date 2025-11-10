import re

class Builder:
	def __init__(self):
		self.content = ""
		self.locals = {}
		self.stackPos = 0

	# BASICS:
	def push(self, val: int) -> None:
		self.content += f"push {val}: {'+' * val}>\n"
		self.stackPos += 1

	def add(self) -> None:
		self.content += f"add: <[-<+>]\n"
		self.stackPos -= 1

	def sub(self) -> None:
		self.content += f"sub: <[-<->]\n"
		self.stackPos -= 1

	def mul(self) -> None:
		self.content += f"mul: <<[>>>+<<<-]\n\t>>>[<<[<+>>+<-]>[<+>-]>-]<<[-]\n"
		self.stackPos -= 1

	def div(self) -> None:
		self.content += f"div: <<[>>+<<-]\n\t>>[\n\t\t<[>>+>+<<<-]\n\t\t>>>[<<<+>>>-]\n\t\t<[\n\t\t\t>+\n\t\t\t<<-[>>[-]>+<<<-]\n\t\t\t>>>[<<<+>>>-]\n\t\t\t<[\n\t\t\t\t<-\n\t\t\t\t[<<<->>>[-]]+\n\t\t\t>-]\n\t\t<-]\n\t\t<<<+\n\t>>]<\n"
		self.stackPos -= 1

	def whileStart(self) -> None:
		self.content += f"whileStart: <[>\n"
	
	def whileEnd(self) -> None:
		self.content += f"whileEnd: <]\n"
	
	def ifStart(self) -> None:
		self.content += f"ifStart: <[>\n"
	
	def ifEnd(self) -> None:
		self.content += f"ifEnd: <[-]]\n" # Must be in same location of stack as ifStart
		self.stackPos -= 1

	def logicalEql(self) -> None:
		self.content += f"eql: <<[->-<]+>[<->[-]]\n"
		self.stackPos -= 1

	def logicalNot(self) -> None:
		self.content += f"not: +<[>-<-]>[-<+>]\n"

	def pop(self) -> None:
		self.content += f"pop: <[-]\n"
		self.stackPos -= 1

	def dump(self) -> None:
		self.content += f"dump: <.[-]\n"
		self.stackPos -= 1
	
	def swap(self) -> None:
		self.content += f"swap: <[->+<]<[->+<]>>[-<<+>>]\n"
	
	# COMPOUNDS:
	def pushLocal(self, name: str, val: int) -> None:
		self.locals[name] = self.stackPos
		self.push(val)

	def getLocal(self, name: str) -> None:
		diff = self.stackPos - self.locals[name]
		self.content += f"get: {'<' * diff}[-{'>' * diff}+>+{'<' * diff}<]{'>' * diff}>[-{'<' * diff}<+{'>' * diff}>]\n"
		self.stackPos += 1

	def logicalNotEql(self) -> None:
		self.logicalEql()
		self.logicalNot()

	def getContent(self, compact: bool = False) -> str:
		if compact:
			pattern = f"[^{re.escape('+-<>[],.')}]"
			return re.sub(pattern, "", self.content)
		else:
			return self.content

output = Builder()

output.pushLocal("x", 32)
output.pushLocal("y", 33)
output.getLocal("x")
output.getLocal("y")
output.add()

with open("out.bf", "w") as file:
	file.write(output.getContent(compact=False))