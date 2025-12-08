import csv

# Open the text file for reading and the CSV file for writing
with open("reviews.txt", "r") as infile, open("output.csv", "w", newline="") as outfile:
    writer = csv.writer(outfile)
    
    for line in infile:
        # Split each line into columns (here by whitespace, but you can change to ',' or '\t')
        row = line.strip().split()
        writer.writerow(row)

print("Conversion complete: output.csv created")
