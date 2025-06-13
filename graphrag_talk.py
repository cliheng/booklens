from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser  # 提取LLM返回结果中文本内容
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

def create_response(question):
    response_template = """
    你是一个具有能够理解问题并回答问题的智能机器人。你需要根据以下参考资料和用户问题，回答用户问题。注意：
    1. 如果没有参考资料或参考资料信息不足，则根据你已有的知识回答该问题。使用自然语言。
    2. 你的输出不应该包含参考资料和用户问题，而是只包含你最终的回答，不要反问用户。

    ##参考资料##
    {retrieval}
    ##用户问题##
    {question}
    """

    # 1. 创建提示词template
    template = ChatPromptTemplate.from_template(response_template)

    # 2. 结果解析Parser对象
    parser = StrOutputParser()

    # 3. 创建LLM
    llm = ChatOpenAI(model="glm-4-flash-250414", 
                    api_key=os.environ['api_key'], 
                    base_url=os.environ['base_url'],)
    # 4. 创建调用链 chain
    chain = template | llm | parser

    response = chain.invoke({"question":question,
                            "retrieval":""})
    return response