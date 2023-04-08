import openai
import pandas as pd
import itertools
import datetime
import os

# Load the API key from the file (change this to reflect where you've put 
#your API key)
with open("../key/key.txt", "r") as key_file:
    api_key = key_file.read().strip()
    openai.api_key = api_key

# Function to process a single prompt
def process_prompt(prompt, engine, temperature):
    """
    Processes a given prompt using the specified engine and temperature.

    Args:
        prompt (str): The input prompt to be processed by the model.
        engine (str): The OpenAI engine to be used for processing.
        temperature (float): The temperature parameter for controlling randomness in the output.

    Returns:
        str: The generated response from the model.
    """
    messages = [
        {"role": "user", "content": prompt}
    ]
    try:
        response = openai.ChatCompletion.create(model=engine, messages=messages, max_tokens=1024, n=1, temperature=temperature)
        return response.choices[0]['message']['content']
    except Exception as e:
        print(f"Error processing prompt. Engine: {engine}, Prompt: {prompt}, Error: {str(e)[:100]}")
        return ''

# Function to process a list of prompts for one iteration
def one_iteration(prompts, engine, temperature):
    """
    Processes a list of prompts using the specified engine and temperature for one iteration.

    Args:
        prompts (list): A list of input prompts to be processed.
        engine (str): The OpenAI engine to be used for processing.
        temperature (float): The temperature parameter for controlling randomness in the output.

    Returns:
        tuple: A tuple containing the list of processed prompts and their corresponding responses.
    """
    responses = []
    for prompt in prompts:
        response = process_prompt(prompt, engine, temperature)
        responses.append(response)

    return prompts, responses

# Main function to run the script

def main():
    """
    Runs the main script for processing prompts, iterating over different engines and temperatures.

    Args:
        iterations (int, optional): The number of iterations to run. Default is 1.

    Returns:
        pd.DataFrame: A DataFrame containing the datetime, prompts, responses, engines, iterations, and temperatures.
    """

    # Define the combinations of engines, iterations, and temperatures to use
    dictMeta = {
        "engines": ["gpt-3.5-turbo"],
        "iterations": [i for i in range(2)],
        "temperatures": [.1, .9]
    }
    combinations = [i for i in itertools.product(*dictMeta.values())]

    # Define the prompts to use
    prompts = ["Write me a poem about Chicago",
               "Explain prime factorization to me like I'm six",
               "What's the song that never ends?",
               "Can you tell me what a data scientist does?"]

    # Create an empty list to store the results for each combination of inputs
    df_list = []

    # Iterate over each combination of inputs and process the prompts
    for combination in combinations:
        engine, iteration, temperature = combination
        try:
            processed_prompts, responses = one_iteration(prompts, engine, temperature)
            dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            df = pd.DataFrame({"datetime": dt, "prompt": processed_prompts, "response": responses, "engine": engine, "iteration": iteration, "temperature": temperature})
            df_list.append(df)
        except Exception as e:
            error_message = f"Error in combination: {combination}. Error message: {e}"
            print(error_message)

    # Concatenate the dataframes for each combination of inputs into a single dataframe
    df = pd.concat(df_list)

    # Return the final dataframe
    return df

if __name__ == "__main__":
    fileName="output.xlsx"  # change this if you want the file called something else
    # this runs your code, using n iterations of each parameter (so, n=2 means it runs everything twice)
    df = main()
    # looks for the filename, if it finds it reads the file in and appends to
    if fileName in os.listdir(os.getcwd()):
        old_df=pd.read_excel(fileName)
        df=pd.concat([old_df, df])
    # writes out to the filename
    df.to_excel(fileName, index=False)
