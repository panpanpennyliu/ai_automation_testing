import logging
import os
from openai import OpenAI

import dotenv
import time
import base64
import cv2
from moviepy.editor import VideoFileClip
from IPython.display import Image, display, Audio, Markdown

dotenv.load_dotenv()


class OpenAIModel:
    def __init__(self):
        self.logger = logging.getLogger('process')
        # set up the model
        self.model_name = 'gpt-4o-mini' #GPT-3.5
        # self.model_name = 'gpt-4o-2024-08-06' #GPT-4o

        self.openai_model = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE")
        )
        
        self.logger.info('set up OpenAI model')

    def encode_image(self,image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
        
    # process with image input
    def process_image(self, image_path, prompt):
        self.logger.info('[process image]')

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        full_image_path = os.path.join(base_dir, image_path)

        self.logger.info('image_path: %s', full_image_path)
        self.logger.info('prompt: %s', prompt)
        
        result = ""

        try:
            base64_image = self.encode_image(image_path)

        except Exception as e:
                result = "Running Error"
                self.logger.error('Exception: \n %s \n', e) 
        
        if result != "Running Error":
            for attempt in range(5): #retry up to 5 times
                try:

                    response = self.openai_model.chat.completions.create(
                        model=self.model_name,
                        messages=[
                            {"role": "user", "content": [
                                {"type": "text", "text": prompt},
                                {"type": "image_url", "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"}
                                }
                            ]}
                        ],
                        temperature=0.0,
                    )

                    result = response.choices[0].message.content
                    print(result)

                    break

                except Exception as e:
                    result = "Running Error"
                    sleep_time = 2 ** attempt
                    self.logger.error('Exception: \n %s \n', e)
                    self.logger.error('Retrying in %s seconds', sleep_time)
                    time.sleep(sleep_time)

        return result
    
    def load_video(self, video_path, seconds_per_frame=1):
        base64Frames = []
        base_video_path, _ = os.path.splitext(video_path)

        video = cv2.VideoCapture(video_path)
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = video.get(cv2.CAP_PROP_FPS)
        print(seconds_per_frame)
        frames_to_skip = int(fps * seconds_per_frame)
        curr_frame=0

        # Loop through the video and extract frames at specified sampling rate
        while curr_frame < total_frames - 1:
            video.set(cv2.CAP_PROP_POS_FRAMES, curr_frame)
            success, frame = video.read()
            if not success:
                break
            _, buffer = cv2.imencode(".jpg", frame)
            base64Frames.append(base64.b64encode(buffer).decode("utf-8"))
            curr_frame += frames_to_skip
        video.release()

        # Extract audio from video
        audio_path = f"{base_video_path}.mp3"
        clip = VideoFileClip(video_path)
        # clip.audio.write_audiofile(audio_path, bitrate="32k")
        # clip.audio.close()
        clip.close()

        print(f"Extracted {len(base64Frames)} frames")
        print(f"Extracted audio to {audio_path}")
        return base64Frames, audio_path
        
    # process with video input
    def process_video(self, video_path, prompt):
        self.logger.info('[process video]')

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        full_video_path = os.path.join(base_dir, video_path)

        self.logger.info('video_path: %s', full_video_path)
        self.logger.info('prompt: %s', prompt)
        
        result = ""
        
    
        if result != "Running Error":
            for attempt in range(5): #retry up to 5 times
                try:

                    base64Frames, audio_path = self.load_video(video_path, 1)

                    response = self.openai_model.chat.completions.create(
                        model=self.model_name,
                        messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": [
                            "These are the frames from the video.",
                            *map(lambda x: {"type": "image_url", 
                                            "image_url": {"url": f'data:image/jpg;base64,{x}', "detail": "low"}}, base64Frames)
                            ],
                        }
                        ],
                        temperature=0,
                    )
                    result = response.choices[0].message.content
                    print(result)

                    break

                except Exception as e:
                    result = "Running Error"
                    sleep_time = 2 ** attempt
                    self.logger.error('Exception: \n %s \n', e)
                    self.logger.error('Retrying in %s seconds', sleep_time)
                    time.sleep(sleep_time)

        return result
        