import re

class Context:
	def __init__(self, startPos, parent=None):
		self.startPos = startPos
		self.parent = parent
		self.locals = {}
	
	def get(self, name: str):
		if name not in self.locals:
			return self.parent.get(name)
		return self.locals[name]

	def put(self, name: str, value: int):
		self.locals[name] = value

class Builder:
	def __init__(self):
		self.content = ""
		self.stackPos = 0
		self.context = Context(self.stackPos)

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
		self.context = Context(self.stackPos, parent=self.context)
	
	def whileEnd(self) -> None:
		self.content += f"whileEnd:"
		if self.stackPos != self.context.startPos:
			self.content += f"\n\t{'<[-]' * (self.stackPos - self.context.startPos)}\n"
			self.stackPos = self.context.startPos
		self.content += "<]\n"
		self.context = self.context.parent

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
	
	def dumpNum(self) -> None:
		self.content += f"dump num: >++++++++++<<[->+>-[>+>>]>[+[-<+>]>+>>]<<<<<<]>>[-]>>>++++++++++<[->-[>+>>]>[+[-\n\t<+>]>+>>]<<<<<]>[-]>>[>++++++[-<++++++++>]<.<<+>+>[-]]<[<[->-<]++++++[->++++++++\n\t<]>.[-]]<<++++++[-<++++++++>]<.[-]<<[-<+>]\n\t<[-]\n"
		self.stackPos -= 1
	
	def swap(self) -> None:
		self.content += f"swap: <[->+<]<[->+<]>>[-<<+>>]\n"
	
	def dupe(self) -> None:
		self.content += f"dupe: <[->+>+<<]>>[-<<+>>]\n"
		self.stackPos += 1
	
	# COMPOUNDS:
	def pushLocal(self, name: str, val: int) -> None:
		self.context.put(name, self.stackPos)
		self.push(val)

	def getLocal(self, name: str) -> None:
		diff = self.stackPos - self.context.get(name)
		self.content += f"get: {'<' * diff}[-{'>' * diff}+>+{'<' * diff}<]{'>' * diff}>[-{'<' * diff}<+{'>' * diff}>]\n"
		self.stackPos += 1

	def setLocal(self, name: str) -> None:
		diff = self.stackPos - self.context.get(name)
		self.content += f"set: <[-{'<' * diff}+{'>' * diff}]"
		self.stackPos -= 1

	def logicalNotEql(self) -> None:
		self.logicalEql()
		self.logicalNot()

	def getContent(self, compact: bool = False) -> str:
		if self.stackPos != self.context.startPos:
			self.content += f"{'<[-]' * (self.stackPos - self.context.startPos)}\n"
			self.stackPos = self.context.startPos
		if compact:
			pattern = f"[^{re.escape('+-<>[],.')}]"
			return re.sub(pattern, "", self.content)
		else:
			return self.content

output = Builder()

output.pushLocal("a", 0)
output.pushLocal("b", 1)
output.push(1)

output.whileStart()
output.pop()

output.getLocal("a")
output.getLocal("b")
output.add()

output.getLocal("b")
output.setLocal("a")

output.dupe()
output.setLocal("b")
output.dumpNum()

output.push(10)
output.dump()

output.push(1)
output.whileEnd()

with open("out.bf", "w") as file:
	file.write(output.getContent(compact=False))