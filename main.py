from dotenv import find_dotenv, load_dotenv
import os

from graphrag_retrieval import search_retrieval


if __name__ == '__main__':

    load_dotenv(find_dotenv())

    # neo4j环境变量
    os.environ['NEO4J_URI']="bolt://localhost:7687"
    os.environ['NEO4J_USERNAME']="neo4j"
    os.environ['NEO4J_PASSWORD']="12345678"
    os.environ['NEO4J_DATABASE']="neo4j"

    # 用户问题
    question ="人工智能发展"

    result = search_retrieval(question)
    print(result)
   

    







    # 
    # reformulate_template = """
    # 你是一个具有能够理解问题并将问题改写的顶级算法。你需要根据以下对话和用户问题，将用户问题改写为新问题。注意：
    # 1. 请不要反问用户，改写后的问题应该是用户可以理解的。 
    # 2. 你的输出不应该包括聊天记录和用户的原始问题，而是只包含新问题。
    # 3. 请确保改写后的问题与用户问题的意思一致，如果不确定用户的意思，请尽量保留原始问题。

    # ##聊天记录##
    # {chat_history}
    # ##用户问题##
    # {question}
    # """



    

    