from graphrag_data_builder import parse_pdf, document_splitter, extract_entities, store_in_neo4j

if __name__ == '__main__':

    pdf_path = 'example.pdf'
    document = parse_pdf(pdf_path)
    docs = document_splitter(document)
    graph_docs = extract_entities(docs)
    store_in_neo4j(graph_docs)

    print()