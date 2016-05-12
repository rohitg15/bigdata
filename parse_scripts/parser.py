import sys



def parse(ipfile, opfile):
	with open(ipfile, "r") as file:
		lines = file.readlines()

	op = []
	for line in lines:
		line = line.strip("\n")
		if line.find("SCHOOL") == -1:
			op.append(line)

	with open(opfile, "w") as file:
		file.write("\n".join(op))



if __name__ == "__main__":
	parse(sys.argv[1], sys.argv[2])