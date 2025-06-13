from langchain_community.document_loaders import PDFMinerLoader
from langchain.text_splitter import TokenTextSplitter
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_experimental.graph_transformers import LLMGraphTransformer

from langchain_community.graphs import Neo4jGraph  # 用来操作 Neo4j 图数据库的类
from dotenv import find_dotenv, load_dotenv  # 用来加载环境变量的库
import os
import tempfile

load_dotenv(find_dotenv())

def parse_pdf(upload_pdf):

    # 使用临时文件方式保存
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(upload_pdf.getbuffer())
        pdf_path = temp_file.name

    # 加载pdf文件
    loader = PDFMinerLoader(pdf_path)
    document = loader.load()
    return document

def document_splitter(document):
    # 文本拆分
    text_splitter = TokenTextSplitter(chunk_size=300, chunk_overlap=50)
    docs = text_splitter.split_documents(document)
    return docs

def extract_entities(docs):
        # 从文本段中抽取实体信息（LLM分析并提取）
        prompt_template = """
        你是一个从旨在从结构化格式中提取信息以构建知识图谱的顶尖算法，你的任务是的任务是识别用户提示中请求的实体和关系，并从给定文本中提取出这些信息对应的节选。。
        您需要以JSON格式生成输出，包含一个列表，列表中的每个元素都是一个JSON对象。
        每个对象应包含以下键："head", "head_type", "relation", "tail" 和 "tail_type"。


        "head" 键必须包含提取实体的文本。
        "head_type" 键必须包含提取的头部实体的类型。
        "relation" 键必须包含 "head" 和 "tail" 之间的关系的类型。
        "tail" 键应代表作为关系尾部的提取实体的文本。
        "tail_type" 键必须包含尾部实体的类型。

        尽可能多地提取实体和关系。并保持实体一致性：在提取实体时，确保一致性至关重要。
        如果文本中多次提到某个实体，例如"李华"，但使用了不同的名称或代词（例如，同事称他为"李先生"，妻子称呼他为"老李"，作者使用"他"来指代）时，请始终使用该实体的最完整标识符。
        知识图谱应当是连贯且易于理解的，因此保持实体引用的一致性非常关键。

        最后，按照文本的语言来选择输出的语言。如果文本是中文的，就使用中文来表达实体、关系等信息，不要使用不具备意义的数字或者英文单词。

        ##待提取的文本##

        {input}

        再次强调：使用中文来表达实体、关系等信息，不要使用不具备意义的数字或者英文单词。
    """
        # 初始化LLM模型 
        llm = ChatOpenAI(model="gpt-4o-mini", 
                        api_key=os.environ['api_key'], 
                        base_url=os.environ['base_url'],)
        # 初始化prompt模板
        prompt = ChatPromptTemplate.from_template(prompt_template)
        # 初始化LLMGraphTransformer
        graph_transformer = LLMGraphTransformer(llm=llm, prompt=prompt)
        # 从文本中抽取实体信息
        graph_docs = graph_transformer.convert_to_graph_documents(docs)

        return graph_docs

def store_in_neo4j(graph_docs, db_name='neo4j'):
    # 实体信息存入neo4j数据库
    neo4jGraph = Neo4jGraph(
        url="bolt://localhost:7687",  # 数据库地址
        username="neo4j",  # 数据库用户名
        password="12345678",  # 数据库密码
        database=db_name  # 数据库名称
    )
    
    neo4jGraph.add_graph_documents(
            graph_docs,
            baseEntityLabel=True,  # 是否使用实体类型作为标签
            include_source=True    # 是否将原始文本作为属性存储
    )

def search_database():
    # 从neo4j数据库中查询数据
    neo4jGraph = Neo4jGraph(
        url="bolt://localhost:7687",  # 数据库地址
        username="neo4j",  # 数据库用户名
        password="12345678",  # 数据库密码
        database="neo4j"  # 默认数据库名称
    )

    result = neo4jGraph.query("show database;")

    return [db['name'] for db in result if db['name'] != 'system']  # 返回所有数据库名称

def create_database(db_name):
    # 创建neo4j数据库
    neo4jGraph = Neo4jGraph(
        url="bolt://localhost:7687",  # 数据库地址
        username="neo4j",  # 数据库用户名
        password="12345678",  # 数据库密码
        database="neo4j"  # 默认数据库名称
    )

    # 检查数据库是否存在
    databases = search_database()
    if db_name in databases:
        raise ValueError(f"数据库 {db_name} 已存在")  # 手工抛出错误
    # 创建数据库
    neo4jGraph.query(f"create database {db_name};")

    return db_name in search_database()

def drop_database(db_name):
    # 创建neo4j数据库
    neo4jGraph = Neo4jGraph(
        url="bolt://localhost:7687",  # 数据库地址
        username="neo4j",  # 数据库用户名
        password="12345678",  # 数据库密码
        database="neo4j"  # 默认数据库名称
    )

    # 检查数据库是否存在
    if db_name not in search_database():
        raise ValueError(f"要删除数据库 {db_name} 不存在！")  # 手工抛出错误
    if db_name in ['neo4j', 'system']:  # 不能删除系统数据库
        raise ValueError(f"不能删除系统数据库 {db_name}！")
    
    # 删除数据库
    neo4jGraph.query(f"drop database {db_name};")

    return db_name not in search_database()


if __name__ == '__main__':

    # 查询所有数据库
    lst = search_database()
    print(lst)
    
    # 创建数据库
    r = create_database('newdb')
    if r:
        print('数据库创建成功')

    # 删除数据库
    r = drop_database('newdb')
    if r:
        print('数据库删除成功')