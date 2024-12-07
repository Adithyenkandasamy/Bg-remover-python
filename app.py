from rembg import remove 


input_image = "input1.png"
output_image = "output1.png"

try:

    with open(input_image,"rb") as input_file:
      in_image = input_file.read()
    
    out_image = remove(in_image)

    with open(output_image,"wb") as output_file:
      output_file.write(out_image) 

    print("background from the input image is reoved sucessfully!")  

except Exception as e:
    print("Error:"e)

out_image = remove(in_image)
