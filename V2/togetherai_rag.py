from langchain.chains import GraphQAChain
from langchain_community.graphs.networkx_graph import NetworkxEntityGraph
from langchain_together import ChatTogether
from langchain.prompts import PromptTemplate

# Initialize your LLM model
chat_model = ChatTogether(
    together_api_key="019d5b390bf9b379deefbc22ed4cb09750a79f34f667e5b491828bd12959db2e",
    model="meta-llama/Llama-3-70b-chat-hf",
    temperature=0.2,
)

def load_gml_and_query_graph(question, gml_file_path):
    # Define the GML file path and load the graph
    # gml_file_path = "./graph.gml"
    graph = NetworkxEntityGraph.from_gml(gml_file_path)
    context= triples = graph.get_triples()
    # print(context)
    # print(graph.get_number_of_nodes())

    # Define the prompt template for QA generation
    qa_generation_template = """You are an assistant that analyzes graph data stored in a NetworkX graph.
    The graph context section contains results derived from a NetworkX graph, including nodes and edges
    represented as triples seperated by commas (,) So whereever you find comma seperated values it is a triple 

    The user asked the following question:
    {question}

    Here are the extracted triples from the graph:
    {context}

    Please provide an answer based on these triples.

    Helpful Answer:
    """

    # Create the prompt template instance
    qa_generation_prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=qa_generation_template
    )

    # Define the entity prompt template (if needed for extracting graph entities)
    entity_prompt_template = """You are extracting entities from the following graph data:
    {context}

    Please list the key entities (nodes) and their relationships (edges)  from the graph.
    Extracted Entities:
    """
    entity_prompt = PromptTemplate(input_variables=["context"], template=entity_prompt_template)

    # Initialize the GraphQAChain with LLM, graph, and prompt templates
    chain = GraphQAChain.from_llm(
        llm=chat_model,
        graph=graph,
        qa_prompt=qa_generation_prompt,
        entity_prompt= entity_prompt,
        verbose=True
    )

    # Convert graph triples to string format for context
    triples = graph.get_triples()
    context = ", ".join([f"({t[0]}, {t[1]}, {t[2]})" for t in triples])

    # Define your question
    # question = "find all the dependencies of backend-base"

    # Invoke the chain with both query and context
    response = chain.invoke({
        "query": question,
        "context": triples
    })

    # Print the response
    print("Response:", response)

    return response