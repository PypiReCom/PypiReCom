import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
pd.set_option('display.max_columns', 4)
import time
from functools import wraps
import os

#takes a single argument for the function to be decorated
def timeit(func):
    """
    Decorator function to measure the execution time of a wrapped function.

    This decorator wraps the given function and measures the time taken by the function to execute using the
    `time.perf_counter()` function from the Python `time` module. It prints the execution time in seconds and returns
    the result of the wrapped function.

    Args:
        func (callable): The function to be wrapped and timed.

    Returns:
        callable: The wrapped function.

    Example:
        @timeit
        def my_function():
            # Code to be timed
            # ...

        my_function()  # This will print the execution time of my_function
    """
    #its used to preserve the original functions metadata
    @wraps(func)
    def wrapper(*args, **kwargs):
        #time.perf_counter() function from the Python time module to measure the time taken by the wrapped function to execute.
        start = time.perf_counter()
        result = func(*args, **kwargs)
        #end time
        end = time.perf_counter()
        #final
        print(f'{func.__name__} took {end - start:.6f} seconds to complete')
        return result
    return wrapper

@timeit
def read_data(file_path):
    """
    Read data from a CSV file and convert it into a pandas DataFrame.

    Parameters:
        file_path (str): The path of the CSV file.

    Returns:
        pd.DataFrame: A DataFrame containing the read data. 
    """
    df = pd.DataFrame()
    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            row = line.strip().split(',')
            df = df._append({'Packages': row[0], 'Date release': row[1], 'no. of packages': row[2]}, ignore_index=True)
    return df

@timeit
def encode_vectors(df):
    """
    Encode the 'CUSTOMER_ID' column text using the SentenceTransformer.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the 'CUSTOMER_ID' column.

    Returns:
        np.ndarray: Encoded vectors for the 'CUSTOMER_ID' column text.
    """
    text = df['Delivery_Desc']# Get the text from the 'Delivery_Desc' column
    encoder = SentenceTransformer("paraphrase-mpnet-base-v2")# Initialize the SentenceTransformer model
    vectors = encoder.encode(text)# Encode the text
    return vectors

@timeit
def build_index(vectors):
    """
    Build an index using Faiss for fast similarity search.

    Parameters:
        vectors (np.ndarray): The vectors to be indexed.

    Returns:
        faiss.IndexFlatL2: The built Faiss index.
    """
    vector_dimension = vectors.shape[1]
    index = faiss.IndexFlatL2(vector_dimension)

    # Ensure vectors are of type float32
    vectors = vectors.astype('float32')

    # Normalize the vectors
    faiss.normalize_L2(vectors)

    index.add(vectors)

    return index


@timeit
def perform_search(index, df, search_context):
    """
    Perform a similarity search using the given index.

    Parameters:
        index (faiss.IndexFlatL2): The Faiss index for similarity search.
        df (pd.DataFrame): The DataFrame containing the package information.
        search_context (str): The search context provided by the user.

    Returns:
        pd.DataFrame: The search results with similarity scores and package details.
    """
    search_context = '_'.join(search_context.split())
    encoder = SentenceTransformer("paraphrase-mpnet-base-v2")
    query = encoder.encode(search_context)
    search_context_vector = np.array([query])
    faiss.normalize_L2(search_context_vector)

    k = 7
    distance, index = index.search(search_context_vector, k)

    results = pd.DataFrame({'distance': distance[0], 'index': index[0]})
    results = pd.merge(results, df['Packages'], left_on='index', right_index=True)
    return results

def store_vectors(vectors, file_path):
    np.savetxt(file_path, vectors)

# Load vectors from a text file
@timeit
def load_vectors(file_path):
    return np.loadtxt(file_path)

@timeit
def encode_vectors_and_store(df, vectors_file_path):
    """
    Encode the 'Delivery_Desc' column text using the SentenceTransformer and store the vectors in a text file.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the 'CUSTOMER_ID' column.
        vectors_file_path (str): The path to the text file for storing vectors.
    """
    text = df['Packages']
    encoder = SentenceTransformer("paraphrase-mpnet-base-v2")
    vectors = encoder.encode(text)
    store_vectors(vectors, vectors_file_path)


def main():
    file_path = 'library/index.csv'
    vectors_file_path = 'encoded_vectors_file.txt'

    if not os.path.exists(vectors_file_path):
        df = read_data(file_path)
        encode_vectors_and_store(df, vectors_file_path)
    else:
        df = read_data(file_path)

    loaded_vectors = load_vectors(vectors_file_path)
    index = build_index(loaded_vectors)

    search_context = input("Enter the search context: ")
    results = perform_search(index, df, search_context)  # Pass df and search_context here
    print(results)

if __name__ == "__main__":
    main()