from neo4j import GraphDatabase  # pip install neo4j

# Execute the query and retrieve results
def cypher_query(query):
    with driver.session() as session:  # 每个连接都是一个会话 session
        result = session.run(query)
        return [record for record in result]  # 返回所有记录
    
def modify_data(query):
    with driver.session() as session:  # 每个连接都是一个会话 session
        session.run(query)

if __name__ == '__main__':

    # Connect to the Neo4j database
    driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', '12345678'))

    ######################## Cypher query ########################
    # query = '''
    # MATCH (p:Person)-[:ACTED_IN]-(m:Movie)
    # where p.name = 'Keanu Reeves'
    # RETURN p.name, m.title
    # '''

    # results = cypher_query()
    # for record in results:
    #     print(record['p.name'], record['m.title'])

    ######################## Cypher update #######################

    # update_query = '''
    # MATCH (p:Person {name: 'mr withe'}) set p.name = '白先生'
    # '''
    # search_query = '''
    # MATCH (p:Person {name:'白先生'}) RETURN p.name
    # '''
    
    # modify_data(update_query)  # Uncomment to execute the modify_data function
    # result = cypher_query(search_query)  # Uncomment to execute the cypher_query function
    
    # print(result)  # Print the result of the query

    delete_query = '''
    MATCH (p:Person {name: '白先生'}) DETACH DELETE p
    '''

    modify_data(delete_query)  # Uncomment to execute the modify_data function

    driver.close()  # Close the driver connection when done
