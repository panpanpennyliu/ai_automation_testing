import logging
import os
import google.generativeai as genai
import PIL.Image
import dotenv
import time

dotenv.load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


class GinaiModel:
    def __init__(self):
        self.logger = logging.getLogger('process')
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
        
        self.logger.info('set up ginai model')
        
    # process with image input
    def process_image(self, image_path, prompt):
        self.logger.info('[process image]')

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        full_image_path = os.path.join(base_dir, image_path)

        self.logger.info('image_path: %s', full_image_path)
        self.logger.info('prompt: %s', prompt)
        
        result = ""

        try:
            prompt_parts = [
                genai.upload_file(full_image_path),
                prompt
            ]
        except Exception as e:
                result = "Running Error"
                self.logger.error('Exception: \n %s \n', e) 
        
        if result != "Running Error":
            for attempt in range(5): #retry up to 5 times
                try:
                    response = self.ginai_model.generate_content(prompt_parts)            
                    result = response.text

                    break

                except Exception as e:
                    result = "Running Error"
                    sleep_time = 2 ** attempt
                    self.logger.error('Exception: \n %s \n', e)
                    self.logger.error('Retrying in %s seconds', sleep_time)
                    time.sleep(sleep_time)

        return result
        
    # process with video input
    def process_video(self, video_path, prompt):
        self.logger.info('[process video]')

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        full_video_path = os.path.join(base_dir, video_path)

        self.logger.info('video_path: %s', full_video_path)
        self.logger.info('prompt: %s', prompt)
        
        result = ""
        
        try:
            self.logger.info('Uploading file...')
            video_file = genai.upload_file(path=full_video_path)
            self.logger.info('Completed upload: %s', video_file.uri)

            # Check whether the file is ready to be used.
            while video_file.state.name == "PROCESSING":
                time.sleep(10)
                video_file = genai.get_file(video_file.name)        

            if video_file.state.name == "FAILED":
                self.logger.info('video cannot be used')
                raise ValueError(video_file.state.name)
            else:
                self.logger.info('video is ready to be used')
        except Exception as e:
                result = "Running Error"
                self.logger.error('Exception: \n %s \n', e)
    
        if result != "Running Error":
            for attempt in range(5): #retry up to 5 times
                try:
                    response = self.ginai_model.generate_content([video_file, prompt],
                                                        request_options={"timeout": 600})            
                    result = response.text

                    break

                except Exception as e:
                    result = "Running Error"
                    sleep_time = 2 ** attempt
                    self.logger.error('Exception: \n %s \n', e)
                    self.logger.error('Retrying in %s seconds', sleep_time)
                    time.sleep(sleep_time)

        return result
        