from rembg import remove 


input_image = "input1.png"
output = "output1.png"

with open(input_image,"rb") as input_file:
    in_image = input_file.read()


out_image = remove(in_image)
