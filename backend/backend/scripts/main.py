from model import QueryChain
import sys
import os

def load_dataset():
    global chain
    chain = QueryChain(os.getenv("CONFIG_PATH"), os.getenv('TEMPLATE_PATH'))

def get_answer(query: str) -> str:
    res = chain.get_answer(query)
    return res
    

try:
    load_dataset()
except Exception as ex:
    print("Не получилось загрузить данные\n", ex)
    print("end")
    sys.exit(1)


query = []

while True:
    line = input()
    if line == "end":
        try:
            print(get_answer('\n'.join(query)))
        except Exception as ex:
            print('Ошибка. Попробуйте ещё раз\n', ex)
        print(line)
        query = []
        sys.stdout.flush()


    else:
        query.append(line)
