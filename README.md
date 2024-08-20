# ai_automation_testing

This Python project is dedicated to testing the capabilities of multimodal models in processing images and videos. The project utilizes the powerful gemini-1.5-pro model to conduct comprehensive evaluations and experiments.

# Project Structure

- **input/**: Stores the images and videos for testing.
- **output/**: Contains the test result file results.xlsx, which saves the processing results of the model on the input data.
- **log/**: Stores log information during the project operation.
- **main.py**: The main program file of the project, responsible for calling the model for testing and outputting the results to the specified file.
- **.env**: The config file to save API Key.
  
# Usage

1. Clone this project to local.
2. Update your API key in .env file.
3. Run the main.py file. The program will automatically call the Gemini 1.5 model to process the input files and save the results to the output/results.xlsx file.

# Notes

1. Ensure that the required Python environment and related dependency libraries are correctly installed.
2. When updating the API key, please ensure its validity and correctness to ensure the normal operation of the project.
Hope this project can be useful for you in multimodal model testing.
