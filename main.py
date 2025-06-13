from langchain_community.vectorstores.neo4j_vector import Neo4jVector

# from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings

from dotenv import find_dotenv, load_dotenv
import os

if __name__ == '__main__':

    load_dotenv(find_dotenv())

    # 用户问题
    question ="人工智能发展"

    # neo4j环境变量
    os.environ['NEO4J_URI']="bolt://localhost:7687"
    os.environ['NEO4J_USERNAME']="neo4j"
    os.environ['NEO4J_PASSWORD']="12345678"
    os.environ['NEO4J_DATABASE']="neo4j"

    embedding = OpenAIEmbeddings(api_key=os.environ["api_key"], base_url=os.environ["base_url"])

    # 基于neo4j中文本节点词向量集合
    vector_index = Neo4jVector.from_existing_graph(
        embedding=embedding,
        search_type='hybrid',           # 检索方式：混合模式
        node_label="Document",          # 节点类型
        text_node_properties=["text"],    # 节点中构建Embedding向量的文本的属性名
        embedding_node_property="embedding",  # 节点中Embedding向量的属性名
    )

    # 检索问题获取匹配文档Docuemnt列表
    docs = vector_index.similarity_search(question)

    filted_docs = [doc.page_content.replace('\n',' ') for doc in docs]
    retrieval_docs = '\n'.join(filted_docs)
    print(retrieval_docs)







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



    

    