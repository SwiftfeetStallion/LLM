from model import QueryChain
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langsmith import Client
from langsmith.evaluation import evaluate

class TestClass:
    def __init__(self, chain: QueryChain, client: Client):
        self.chain = chain
        self.client = client

    def context_to_query(self, example: dict) -> dict:
        query = example['query']
        doc_chain = self.chain.db.as_retriever() | self.chain.format_documents
        context = doc_chain.invoke(query)
        return {"query": query, "context": context}

    def context_to_answer(self, example: dict) -> dict:
        query = example['query']
        doc_chain = self.chain.db.as_retriever() | self.chain.format_documents
        context = doc_chain.invoke(query)
        answer = self.chain.get_answer(query)
        return {"answer": answer, "context": context}

    def answer_to_query(self, example: dict) -> dict:
        query = example['query']
        answer = self.chain.get_answer(query)
        return {"answer": answer, "query": query}
    
    def get_llm_grader(self):
        model_type = self.chain.model_type

        if model_type == 'ollama':
            return ChatOllama(model=self.chain.model_name, temperature=0)

        if model_type == 'mistral':
            return ChatMistralAI(model=self.chain.model_name, api_key=self.chain.api_key, temperature=0)

        if model_type == 'huggingface':
            model = HuggingFaceEndpoint(repo_id=self.chain.model_name, huggingfacehub_api_token=self.chain.api_key, temperature=0)
            return ChatHuggingFace(llm=model)
        
        if model_type == 'openai':
            base_url = self.chain.kwargs.get("base_url")
            return ChatOpenAI(model=self.chain.model_name, api_key=self.chain.api_key, base_url=base_url, temperature=0)

        raise Exception(f'''Unknown model type {model_type} is passed. 
                            The only supported are ['ollama', 'mistral', 'huggingface', 'openai']''')
    
    def context_to_answer_evaluator(self, run: dict, example: dict) -> dict:

        prompt = self.client.pull_prompt("langchain-ai/rag-answer-hallucination")

        answer = run.outputs["answer"]
        context = run.outputs['context'] 

        llm_grader = self.get_llm_grader()

        grader = prompt | llm_grader

        score = grader.invoke({"documents": context, "student_answer": answer})
        score = score["Score"]

        return {"key": "answer_hallucination", "score": score}
    
    def context_to_query_evaluator(self, run: dict, example: dict) -> dict:
        prompt = self.client.pull_prompt("langchain-ai/rag-document-relevance")

        query = example.inputs["query"]
        context = run.outputs['context'] 

        llm_grader = self.get_llm_grader()

        grader = prompt | llm_grader

        score = grader.invoke({"documents": context, "question": query})
        score = score["Score"]

        return {"key": "document_relevance", "score": score}
    
    def answer_to_query_evaluator(self, run: dict, example: dict) -> dict:
        prompt = self.client.pull_prompt("langchain-ai/rag-answer-helpfulness")

        query = example.inputs["query"]
        answer = run.outputs['answer'] 

        llm_grader = self.get_llm_grader()

        grader = prompt | llm_grader

        score = grader.invoke({"student_answer": answer, "question": query})
        score = score["Score"]

        return {"key": "answer-helpfulness", "score": score}
    
    def evaluate(self, function, dataset_name: str, evaluator, prefix: str):
        evaluate(function, data=dataset_name, evaluators=[evaluator], experiment_prefix=prefix)