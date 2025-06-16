import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.neo4j_vector import Neo4jVector

def search_retrieval(question, limit=5):
    """
    基于neo4j中文本节点词向量集合进行检索
    question: 用户问题
    limit: 检索结果数量 
    """
    embedding = OpenAIEmbeddings(
        model=os.environ['embedding_model'],
        api_key=os.environ["api_key"], 
        base_url=os.environ["base_url"])

    # 基于neo4j中文本节点词向量集合
    vector_index = Neo4jVector.from_existing_graph(
        embedding=embedding,
        search_type='hybrid',           # 检索方式：混合模式
        node_label="Document",          # 节点类型
        text_node_properties=["text"],    # 节点中构建Embedding向量的文本的属性名
        embedding_node_property="embedding",  # 节点中Embedding向量的属性名
    )

    # 检索问题获取匹配文档Docuemnt列表
    docs = vector_index.similarity_search(question, k=limit)

    filted_docs = [doc.page_content.replace('\n',' ') for doc in docs]
    retrieval_docs = '\n'.join(filted_docs)
    return retrieval_docs