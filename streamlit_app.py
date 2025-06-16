import streamlit as st
import graphrag_data_builder as gdb
import graphrag_talk as gt
import graphrag_retrieval as gr
from dotenv import find_dotenv, load_dotenv
import os

def main():
    # 标题
    st.title("GraphRAG 智能助手")

    # 放置侧边栏
    with st.sidebar:
        st.header("Graph 管理")

        # 上传文件
        uploaded_file = st.file_uploader("上传文件", type="pdf", help='请上传 PDF 文件')
        # 指定数据库
        db_name = st.selectbox(
            "选择或输入数据库名",
            st.session_state.databases,  # 数据库列表
            accept_new_options=True
        )
        # 创建两栏布局
        col1, col2 = st.columns(2)

        with col1:
            response = st.button("导入 Graph")  # 创建一个按钮，返回一个布尔值，表示用户是否点击了按钮
            if response: 
                if not db_name:  # 如果用户没有输入数据库名
                    st.warning("请输入数据库名！")
                else:
                    if uploaded_file is not None:  # 如果用户点击了按钮并且上传了文件
                        # 验证数据库是否存在
                        if db_name in gdb.search_database():
                            result = True
                        else:
                            result = gdb.create_database(db_name)  # 创建数据库
                            st.success(f"数据库 {db_name} 创建成功！")

                        if result:  # 如果数据库验证成功
                            pdf_path = gdb.parse_pdf(uploaded_file)
                            docs = gdb.document_splitter(pdf_path)
                            graph_docs = gdb.extract_entities(docs)
                            gdb.store_in_neo4j(graph_docs, db_name)
                            st.success("文档导入成功！")
                            st.session_state.databases = gdb.search_database()  # 更新数据库列表
                        else:  # 如果数据库创建失败
                            st.error(f"数据库 {db_name} 创建失败！")
                    else:  # 如果用户没有上传文件
                        st.warning("请上传pdf文件！")
        with col2:
            response = st.button("重置 Graph")


        if response and db_name:
            # 查询数据库存在决定是否重置
            if db_name in gdb.search_database():
                gdb.reset_database(db_name)
                st.info(f'数据库{db_name}重置成功！')
            else:
                st.warning(f'数据库{db_name}不存在，重置失败！')

    # 实现聊天功能
    question = st.chat_input("输入问题提问....")  # 创建一个聊天输入框，返回用户输入的问题

    if question is not None and question != "":
        
        chat_history = st.session_state.chat_history
        # 指定查询neo4j数据库
        os.environ['NEO4J_DATABASE']=db_name

        # 利用聊天历史信息重构问题
        new_question = gt.reformulate_build(question, chat_history)
        # 检索问题相关文档
        retrieval = gr.search_retrieval(new_question)

        # 使用检索知识解答问题
        resp = gt.create_response(new_question, retrieval)
        st.session_state.chat_history.append(('Human', question))
        st.session_state.chat_history.append(('AI', resp))

        for chat in chat_history:
            role, content = chat
            with st.chat_message(role):
                st.write(content)

if __name__ == '__main__':

    load_dotenv(find_dotenv())

    # neo4j环境变量
    os.environ['NEO4J_URI']="bolt://localhost:7687"
    os.environ['NEO4J_USERNAME']="neo4j"
    os.environ['NEO4J_PASSWORD']="12345678"
    os.environ['NEO4J_DATABASE']="neo4j"

    # 查询所有数据库
    if 'databases' not in st.session_state:  # 如果会话状态中没有数据库列表
        st.session_state.databases = gdb.search_database()  # 查询数据库列表并存储在会话状态中

    # 聊天历史信息
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [] # 初始化聊天历史

    main()