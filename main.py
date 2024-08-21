import google.generativeai as genai
import os
import dotenv
import time

if __name__ == '__main__':
    dotenv.load_dotenv()

    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    video_file_name = "GreatRedSpot.mp4"

    print(f"Uploading file...")
    video_file = genai.upload_file(path=video_file_name)
    print(f"Completed upload: {video_file.uri}")

    # Check whether the file is ready to be used.
    while video_file.state.name == "PROCESSING":
        print('.', end='')
        time.sleep(10)
        video_file = genai.get_file(video_file.name)

    if video_file.state.name == "FAILED":
        raise ValueError(video_file.state.name)

    model = genai.GenerativeModel(model_name="gemini-1.5-pro")

    prompt = "Summarize this video. Then create a quiz with answer key based on the information in the video."

    response = model.generate_content([video_file, prompt],
                                      request_options={"timeout": 600})

    try:
        print(response.text)
    except Exception as e:
        print("Exception: \n", e, "\n")
        print("Response: \n", response.candidates)
