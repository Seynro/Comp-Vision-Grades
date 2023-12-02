# Comp-Vision-Grades

### Programm starts with main_aplication.exe

## How to use:
1) Create 2 dictionares:
    1) Students dictionary ```{type: {'Name Surname': Student ID}}```
    ```py
    {24: {'Alexey Voronov': 62517},
    5: {'Marina Ivanova': 77634},
    26: {'Sergey Petrov': 52557},
    18: {'Ekaterina Smirnova': 71863},
    1: {'Nikita Kuznetsov': 10113},
    3: {'Anna Popova': 63950},
    17: {'Ivan Vasilyev': 41908},
    22: {'Olga Sokolova': 28919}}
    ```
    2) Questions dictionary ```{type(starting from 1): {question(starting from 0): answer(starting from 0)}} ```
    ```py
    {1:{0: 0,  1: 1,  2: 1,  3: 1,  4: 2,
    5: 2,  6: 3,  7: 3,  8: 1,  9: 1},

    29:{0: 1,  1: 1,  2: 1,  3: 1,  4: 2,
    5: 2,  6: 3,  7: 3,  8: 1,  9: 1},

    7:{0: 2,  1: 1,  2: 1,  3: 1,  4: 2,
    5: 2,  6: 3,  7: 3,  8: 1,  9: 1},

    40:{0: 3,  1: 1,  2: 1,  3: 1,  4: 2,
    5: 2,  6: 3,  7: 3,  8: 1,  9: 1}}
    ```
2) Create blanks folder
3) Input Students dictionary path in "Student's Dictionary Name", click Generate tests button
4) Make exam/quiz
5) Scan all tests
6) Put in one folder (as jpgs)
7) Type folder path in image_path and save_path (without 01.jpg) (If full path is like this C:\Users\user\Desktop\Stat\quiz_01_12_2023\business_stat_scans\file_01.jpg than path in programm should be C:\Users\user\Desktop\Stat\quiz_01_12_2023\business_stat_scans\file_)
8) Input path to Questions dictionary
9) Input name for the feature end Excel sheet (quiz_01_01_2023.xlsx) 
10) Input number of students (minimum 11)
11) Input number of questions (maximum 40)
12) Click Submit