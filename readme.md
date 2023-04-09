# GPT Prompt Processing Via the API

This script allows you, if you have a GPT API key, to process a list of prompts, systematically varying the prompt, model, and temperature settings, as well as how many iterations you want to run for each combination of these. 

The output is saved in an Excel file with separate columns for datetime, engine, iteration numbers, temperature, prompt, and model response.

## Key Features

- Process prompts by varying engine, prompt, and temperature via a series of conversations with GPT
- Does error handling/prints out error messages
- Save the results in an Excel file. (If the file already exists because you've run this before, this will read in the existing file and append to it.)

## Usage

1. [Register for an API key.](https://platform.openai.com/account/api-keys)
2. Install the required dependencies, including the `openai` package, via the requirements.txt file.
3. Update the `api_key` variable in the script to reflect to the name/location of your API key.
4. Modify the `prompts` list with the list of prompts you want to process.
5. Modify the `engines` list with the list of engines you want to use.
6. Modify the `temperatures` list with the list of temperatures you want to use.
7. Modify the number in the range() for the "iterations" with the number of times you want to run each of these combinations.
8. Run the script and get the output saved in an Excel file named "output.xlsx". Each time you run this, it will read in and append to that file.

## Model and Temperature Parameters

- Model: This script uses the GPT-3.5-turbo model from OpenAI. You can read more about other available models in the [OpenAI API documentation](https://platform.openai.com/docs/models/overview), and if you want to work with them, you can add them to the`engines` list.

- Temperature: The temperature parameter controls the randomness of the model's output. Lower values like 0.1 or 0.2 make the output more focused and deterministic, while higher values like 0.8 or 1.0 make the output more random and creative.

## Additional Notes

- You can read more about other possible parameters to pass to GPT in the [OpenAI API documentation](https://platform.openai.com/docs/api-reference/chat/create)

- If you want to get more information on the parameters you sent (and other response information) directly from the API, you can look at the object being returned by `response = openai.ChatCompletion.create()`. It has a lot of other fields in it; you just have to unpack it from the JSON object that's returned.

- Remember that the number of API calls you're making grows quickly with the number of inputs. For instance, if you go from 1 engine to 2 (or one temperature to 2), you're doubling the number of API calls. You can track your usage/spending [here](https://platform.openai.com/account/usage), and also [see the rate limits](https://platform.openai.com/docs/guides/rate-limits).
