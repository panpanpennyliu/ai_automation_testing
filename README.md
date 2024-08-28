# ai_automation_testing

This Python project is dedicated to testing the capabilities of multimodal models in processing images and videos. The project utilizes the powerful gemini-1.5-pro model to conduct comprehensive evaluations and experiments.

# Project Structure

- **input**: Stores the images and videos for testing, as well as an excel file named testing_case.xlsx lists all the test cases.
- **output**: Contains the test result file result.xlsx, which saves the processing results of the model on the input data.
  Column "Verification Result" in result.xlsx:
  - SUCCESS: The result get from AI is as expected.
  - FAIL: The result get from AI is not as expected.
  - (empty): No varification defined for the test case.
  - Running Error: AI runs error.
- **llm/**: Contails seperate folders of diffrent ai models like openai/ or gemini/, with API calling methods in process.py file.
- **log/**: Stores log information during the project operation.
- **main.py**: The main program file of the project, responsible for calling the model for testing and outputting the results to the specified file.
- **.env**: The config file to save API Key.
- **requirements.txt**: Lists all the necessary Python libraries and their versions required for this project. This file ensures that when you set up the project on a new environment, you can easily install all the dependencies by running a single command like pip install -r requirements.txt.

  
# Usage

1. Clone this project to local.
2. pip install -r requirements.txt
3. Update your API key in .env file.
4. Run the main.py file. The program will call the Gemini 1.5 model to process the input files and save the results to the output/results.xlsx file.

# Notes

1. Ensure that the required Python environment and related dependency libraries are correctly installed.
2. When updating the API key, please ensure its validity and correctness to ensure the normal operation of the project.
Hope this project can be useful for you in multimodal model testing.
