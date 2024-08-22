import pandas as pd
from llm.gemini.process import ginai_model


def read_excel_data(file_path):
    return pd.read_excal(file_path)


def main():
    data = read_excel_data("input/testing_case.xlsx")
    for index, row in data.iterrows:
        media = row['Image & Video']
        prompt = row['Prompt']
        if "image" in media:
            image_path = media
            result = ginai_model.process_image(image_path, prompt)
        elif "video" in media:
            video_path = media
            result = ginai_model.process_image(video_path, prompt)
        else:
            result = "Unknown case"


if __name__ == '__main__':
    main()
