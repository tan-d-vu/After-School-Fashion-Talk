import os
filename = os.path.dirname(os.path.realpath(__file__)) + "\\brand_list.txt"
import sys
sys.stdout = open('brand_set.txt', 'w', encoding="utf-8")

with open(filename, encoding="utf-8") as my_brand_list:
    my_brand_set = set(line.strip() for line in my_brand_list)
    choice_list = []
    choice_cell = ()
    i = 0
    for des in my_brand_set:
        choice_cell = (str(i), str(des))
        choice_list.append(choice_cell)
        i+=1
    print(choice_list)
