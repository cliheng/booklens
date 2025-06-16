from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser  # 提取LLM返回结果中文本内容
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

def reformulate_build(question, history):

    reformulate_template = """
    你是一个具有能够理解问题并将问题改写的顶级算法。你需要根据以下对话和用户问题，将用户问题改写为新问题。注意：
    1. 请不要反问用户，改写后的问题应该是用户可以理解的。 
    2. 你的输出不应该包括聊天记录和用户的原始问题，而是只包含新问题。
    3. 请确保改写后的问题与用户问题的意思一致，如果不确定用户的意思，请尽量保留原始问题。

    ##聊天记录##
    {chat_history}
    ##用户问题##
    {question}
    """

    # 1. 创建提示词template
    template = ChatPromptTemplate.from_template(reformulate_template)

    # 2. 结果解析Parser对象
    parser = StrOutputParser()

    # 3. 创建LLM
    llm = ChatOpenAI(model=os.environ['chat_model'], #model="gpt-4o-mini", 
                    api_key=os.environ['api_key'], 
                    base_url=os.environ['base_url'],)
    # 4. 创建调用链 chain
    chain = template | llm | parser

    # 5. history转换字符串类型 : "Human:xxxxx \n AI:xxxxxx\n Human:xxxx....."
    history_str = '\n'.join([f'{talk[0]}:{talk[1].replace('\n',' ')}' for talk in history])

    response = chain.invoke({"question":question,
                             "chat_history":history_str})
    return response



def create_response(question, retrieval):
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
    llm = ChatOpenAI(os.environ['chat_model'],  #model="gpt-4o-mini",
                    api_key=os.environ['api_key'], 
                    base_url=os.environ['base_url'],)
    # 4. 创建调用链 chain
    chain = template | llm | parser

    response = chain.invoke({"question":question,
                             "retrieval":retrieval})
    return response