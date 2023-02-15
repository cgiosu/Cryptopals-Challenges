import os , sys

### Read the file line by line
with open(os.path.join(sys.path[0], "8.txt"), "r") as f:
    lines = f.readlines()

### Function counting the number of "different" blocks of 16 bytes
def repetition_score(text):
    n, blocks = len(text)//32, set()
    for i in range(n):
        blocks.add(text[32 * i : 32 * (i+1)])
    return len(blocks)

### Prints the line with at least one repetition
for text in lines:
    if repetition_score(text) < len(text)//32:
        print(text)