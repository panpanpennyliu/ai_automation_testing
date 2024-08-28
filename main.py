import logging
import pandas as pd
from llm.gemini.process import GinaiModel

# config logging
logging.basicConfig(filename='log/log.txt', filemode='w', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# read excel
def read_excel_data(file_path):
    return pd.read_excel(file_path)


def main():
    logging.info('started...')

    ginai_model = GinaiModel()

    data = read_excel_data("input/testing_case.xlsx")    
    data.dropna(subset=['Image & Video','Prompt'], inplace=True)
    logging.info('interate excel input file')
    processed_data = []
    for index, row in data.iterrows():
        case_name = row['Case Name']        
        ira_module = row['IRA Module']
        case_scenario = row['Case Scenario']
        media = row['Image & Video']
        prompt = row['Prompt']
        expected_result = row['Expected Result']

        logging.info('===process %s ===', case_name)

        if "image" in media:
            image_path = media
            result = ginai_model.process_image(image_path, prompt)
        elif "video" in media:
            video_path = media
            result = ginai_model.process_video(video_path, prompt)
        else:
            result = 'Unknown case'

        logger.info('Response: \n %s', result)
        if pd.isna(expected_result):
            verification_result = ""
        if result.strip() == "Running Error":
            verification_result = "Running Error"
        if result.strip() == str(expected_result).strip():
            verification_result = "SUCCESS"
        else:
            verification_result = "FAIL"

        processed_data.append([case_name, ira_module, case_scenario, media, prompt, result, expected_result, verification_result])

    output_df = pd.DataFrame(processed_data, columns=['Case Name', 'IRA Module', 'Case Scenario', 'Image & Video', 'Prompt', 'Actual Result', 'Expected Result', 'Verification Result'])
    output_df.to_excel("output/result.xlsx", index=False)
    logging.info('finished...')

if __name__ == '__main__':
    main()
