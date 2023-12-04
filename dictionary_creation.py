import numpy as np 
import pandas as pd
import random
import pickle
import re


def parse_questions(input_text):
    # Разбиваем текст на отдельные вопросы
    questions_split = input_text.strip().split('\n\n')
    questions_list = []

    for question in questions_split:
        # Извлекаем текст вопроса
        question_text = re.search(r'\d+\)(.*?)\n[A-D]', question).group(1).strip()

        # Извлекаем варианты ответов
        options = re.findall(r'[A-D]\)(.*?)\n', question)

        # Извлекаем номер правильного ответа
        correct_answer = int(re.search(r'Answer:(\d+)', question).group(1))

        # Добавляем вопрос и ответы в список
        questions_list.append({
            "MC question": question_text,
            "options": options,
            "correct answer": correct_answer
        })

    return questions_list


def dict_creation(unwrapped_questions):
    questions = parse_questions(unwrapped_questions)
    number_of_students = 3
    diction = {}
    for k in range(number_of_students):
        random.seed(k)
        np.random.seed(k)
        print(f"Type:{k+1}")
    # Randomly select 3 questions
        selected_questions = random.sample(questions, len(questions))
        # Dictionary to store the correct answers
        correct_answers = {}
        correct_nums = {}
        # Shuffle the options for each question and enumerate the questions
        for i, question in enumerate(selected_questions, start=1):
            correct_answer = question['options'][question['correct answer']]
            # print(correct_answer)
            # random.shuffle(question['options'])
            truth = [i == correct_answer for i in question["options"] ]
            print(f"Question {i}: {question['MC question']}")
            correct_nums[i-1] = np.where(truth)[0][0]
            for j, option in enumerate(question['options'], start=1):
                print(f"{chr(64+j)}: {option}")
            print("\n")
            correct_answers[f"Question {i}"] = correct_answer
        # print("Correct Answers:", correct_answers)
        diction[k+1] = correct_nums
        # print(correct_nums)
        with open("questions_dictionary", "wb") as file:
            pickle.dump(diction, file)

        return diction


