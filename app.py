from rembg import remove 


input_image = "input1.png"
output = "output1.png"

with open(input_image,"rb") as input_file:
    in_image = input_file.read()

with open(output_image,"wb") as output_file:
     output_file.write(out_image) 


out_image = remove(in_image)
