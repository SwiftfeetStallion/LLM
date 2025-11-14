from langchain_chroma import Chroma
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_ollama import ChatOllama
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI

import yaml

class QueryChain:
    def __init__(self, config_path, template_path):
        self.load_config(config_path)
        self.template = self.load_template(template_path)

        if self.model_type == 'ollama':
            self.llm = ChatOllama(model=self.model_name, **self.kwargs)

        elif self.model_type == 'mistral':
            self.llm = ChatMistralAI(model=self.model_name, api_key=self.api_key, **self.kwargs)

        elif self.model_type == 'huggingface':
            model = HuggingFaceEndpoint(repo_id=self.model_name, huggingfacehub_api_token=self.api_key, **self.kwargs)
            self.llm = ChatHuggingFace(llm=model)
        
        elif self.model_type == 'openai':
            self.llm = ChatOpenAI(model=self.model_name, api_key=self.api_key, **self.kwargs)

        else:
            raise Exception(f'''Unknown model type {self.model_type} is passed. 
                            The only supported are ['ollama', 'mistral', 'huggingface', 'openai']''')
        
        self.load_dataset()

    def load_config(self, config_path):
        with open(config_path, 'r') as cfg:
            conf_dict = yaml.safe_load(cfg)
            if 'dataset_path' in conf_dict:
                self.dataset_path = conf_dict['dataset_path']

            if 'llm' in conf_dict:
                llm_dict = conf_dict['llm']
                if 'model_name' in llm_dict:
                    self.model_name = llm_dict['model_name']
                if 'model_type' in llm_dict:
                    self.model_type = llm_dict['model_type']
                if 'api_key' in llm_dict:
                    self.api_key = llm_dict['api_key']
                if 'kwargs' in llm_dict:
                    self.kwargs = llm_dict['kwargs']

            if 'history_length' in conf_dict:
                self.history_length = conf_dict['history_length']
        
    def load_dataset(self) -> Chroma:
        self.db = Chroma(persist_directory=self.dataset_path)
        self.history = []

    def load_template(self, template_path) -> str:
        with open(template_path, 'r') as tmpt:
            template = tmpt.read()
            return template
        
    def format_documents(self, docs: list[Document]):
        return "\n\n".join(doc.page_content for doc in docs)

    def get_answer(self, query: str):
        prompt = PromptTemplate(
            template=self.template, input_variables=["context", "query"],
            partial_variables={"history": self.history})
        
        self.history.append(HumanMessage(content=query))

        chain = ({"context": self.db.as_retriever() | self.format_documents, "query": RunnablePassthrough()} 
                 | prompt 
                 | self.llm 
                 | StrOutputParser())
        
        answer = chain.invoke(query)
        self.history.append(AIMessage(content=answer))

        while len(self.history) > self.history_length:
            self.history.pop(0)
        
        return answer
