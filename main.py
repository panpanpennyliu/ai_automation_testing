import os
import dotenv
import logging
import pandas as pd
from llm.gemini.process import GinaiModel
from llm.openai.process import OpenAIModel

dotenv.load_dotenv()

# config logging
logging.basicConfig(filename='log/log.txt', filemode='w', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# read excel
def read_excel_data(file_path):
    return pd.read_excel(file_path)


def main():
    logging.info('started...')

    # config AI_MODEL in .env file
    if os.getenv("AI_MODEL") == "OPENAI":
        ai_model = OpenAIModel()
    elif os.getenv("AI_MODEL") == "GOOGLE_API":        
        ai_model = GinaiModel()

    data = read_excel_data("input/testing_case.xlsx") # read input excel   
    data.dropna(subset=['Image & Video','Prompt'], inplace=True) # ignore the row if column  'Image & Video' or 'Prompt' is blank

    processed_data = [] # for saving output data

    logging.info('interate test cases in input excel')
    for index, row in data.iterrows():
        case_name = row['Case Name']        
        ira_module = row['IRA Module']
        case_scenario = row['Case Scenario']
        media = row['Image & Video']
        media = media.replace("\\", "/")
        prompt = row['Prompt']
        expected_result = row['Expected Result']

        logging.info('=== process %s ===', case_name)

        if "image" in media:
            image_path = media
            result = ai_model.process_image(image_path, prompt)
        elif "video" in media:
            video_path = media
            result = ai_model.process_video(video_path, prompt)
        else:
            result = 'Unknown case'

        logging.info('Response: \n %s', result)

        if pd.isna(expected_result):
            verification_result = ""
        if result.strip() == "Running Error":
            verification_result = "Running Error"
        if result.strip() == str(expected_result).strip():
            verification_result = "SUCCESS"
        elif isinstance(expected_result, str) and str(expected_result).strip() in result.strip():
            verification_result = "SUCCESS"
        else:
            verification_result = "FAIL"

        processed_data.append([case_name, ira_module, case_scenario, media, prompt, result, expected_result, verification_result])
    
    # write to output excel
    output_df = pd.DataFrame(processed_data, columns=['Case Name', 'IRA Module', 'Case Scenario', 'Image & Video', 'Prompt', 'Actual Response', 'Expected Response', 'Verification Result'])
    output_df.to_excel("output/result.xlsx", index=False) 

    logging.info('finished...')

if __name__ == '__main__':    
    main()
