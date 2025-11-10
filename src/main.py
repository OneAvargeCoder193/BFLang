from builder import Builder
import parser

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
output.dupe()
output.setLocal("b")
output.dumpNum()

output.push(10)
output.dump()

output.push(233)
output.logicalNotEql()
output.whileEnd()

with open("out.bf", "w") as file:
    file.write(output.getContent(compact=False))