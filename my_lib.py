# wrap_texting it well
def wrap_text(text,numchars=100):
    lines = text.split('\n')
    for line in lines:
        while len(line) > numchars:
            space_index = line[:numchars].rfind(' ')
            if space_index == -1:  # no space found
                print(line[:numchars])
                line = line[numchars:]
            else:
                print(line[:space_index])
                line = line[space_index+1:]
        print(line)
    return line

