from test_helper import TestClass
from model import QueryChain
from langsmith import Client
import time

import os

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ['LANGCHAIN_ENDPOINT'] = "https://api.smith.langchain.com"
os.environ['LANGCHAIN_PROJECT'] = 'test_langchain'
os.environ["LANGCHAIN_API_KEY"] = None # нужно добавить ключ

chain = QueryChain(os.getenv('CONFIG_PATH'), os.getenv('TEMPLATE_PATH'))
client = Client()

dataset_name = "Test Dataset"
dataset = client.create_dataset(dataset_name=dataset_name)

examples = ["Что такое variant?", "Приведите пример применения шаблонов"]
client.create_examples(inputs=[{"query": example} for example in examples], dataset_id=dataset.id)

tester = TestClass(chain, client)

tester.evaluate(tester.answer_to_query, dataset_name, tester.answer_to_query_evaluator, "answer-helpfulness")

tester.evaluate(tester.context_to_answer, dataset_name, tester.context_to_answer_evaluator, "answer_hallucination")

tester.evaluate(tester.context_to_query, dataset_name, tester.context_to_query_evaluator, "document_relevance")