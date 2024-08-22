import os
import google.generativeai as genai
import PIL.Image
import dotenv
import time

dotenv.load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


class GinaiModel:
    def __int__(self):
        # set up the model
        model_name = 'gemini-1.5-pro'
        generation_config = {
            "temperature": 0.2,
            "top_p": 0.8,
            "top_k": 64,
            "max_output_tokens": 8192,
        }
        self.ginai_model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config,
        )

    def process_image(self, image_path, prompt):
        prompt_parts = [
            genai.upload_file(image_path),
            prompt
        ]

        response = self.ginai_model.generate_content(prompt_parts)

        try:
            result = response.text
            print(response.text)
        except Exception as e:
            result = "Running Error"
            print("Exception: \n", e, "\n")
            print("Response: \n", response.candidates)

        return result

    def process_video(self, video_path, prompt):

        print(f"Uploading file...")
        video_file = genai.upload_file(path=video_path)
        print(f"Completed upload: {video_file.uri}")

        # Check whether the file is ready to be used.
        while video_file.state.name == "PROCESSING":
            print('.', end='')
            time.sleep(10)
            video_file = genai.get_file(video_file.name)

        if video_file.state.name == "FAILED":
            raise ValueError(video_file.state.name)

        response = self.ginai_model.generate_content([video_file, prompt],
                                                     request_options={"timeout": 600})

        try:
            result = response.text
            print(response.text)
        except Exception as e:
            result = "Running Error"
            print("Exception: \n", e, "\n")
            print("Response: \n", response.candidates)

        return result


ginai_model = GinaiModel()
