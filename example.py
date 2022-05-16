import os 

platforms = []

file = open('data.csv', 'r')
content = file.readlines()
for line in content:
    row = line.split(',')
    for tile in row:
        tile = (int)(row[0])
        if tile != -1:
            print("Yes")
        else:
            print("No")