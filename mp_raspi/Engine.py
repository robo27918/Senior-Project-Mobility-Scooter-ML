import cv2
import typing
import numpy as np

class Engine :
    """
    Object to process webcam stream or video source
    All the processing can be customized and enhanced
    with custom objects
    """
    def __init__ (
            self,
            video_path: str = "",
            webcam_id: int = 0,
            show: bool = False,
            flip_view: bool = False,
            custom_objects: typing.Iterable = [],
            output_extension: str = 'out',
            start_video_frame: int = 0,
            end_video_frame: int = 0,
            break_on_end: bool = False,
    ) -> None:
        self.video_path = video_path
        self.webcam_id = webcam_id
        self.show = show
        self.flip_view = flip_view
        self.custom_objects = custom_objects
        self.output_extension = output_extension 
        self.start_video_frame = start_video_frame
        self.end_video_frame = end_video_frame
        self.break_on_end = break_on_end
    
    def flip (self, frame: np.ndarrray) -> np.ndarray:
         
         """Flip given frame horizontally
            Args:
                frame: (np.ndarray) - frame to be fliped horizontally

            Returns:
            frame: (np.ndarray) - fliped frame if self.flip_view = True
            """
         if self.flip_view:
             return cv2.flip(frame,1)
    def custom_processing(self, frame: np.ndarray) -> np.ndarray:
         """Process frame with custom objects (custom object must have call function for each iteration)
        Args:
            frame: (np.ndarray) - frame to apply custom processing to

        Returns:
            frame: (np.ndarray) - custom processed frame
        """
         if self.custom_objects:
             for custom_object in self.custom_objects:
                 frame = custom_object(frame)
    def process_webcam(self) -> None:
        '''
        Process webcam stream for given webcam_id
        '''
        #create a VideoCapture object for a given webcam_id
        cap = cv2.VideoCapture(self.webcam_id)
        while cap.isOpened():
            success,frame = cap.read()
            if not success:
                print("Ignoring empty camera frame")
                continue
            frame = self.custom_processing(self.flip(frame))
        else:
            raise Exception(f"Webcam with ID ({self.webcam_id}) cannot be opened")
        
        cap.release()
    def make_csv(self.):
          with open('myFile.txt','a') as f:
            for idx,landmark_name in landmark_subset_dict.items():
               
                   
                    x = pose_landmarks.landmark[idx].x
                    y = pose_landmarks.landmark[idx].y
                    z = pose_landmarks.landmark[idx].z
                    
                    str_to_file = f"time stamp: {time.time()- start_time} sec,landmark-name:{landmark_name}, x: {x}, y: {y}, z: {z}"
                    f.write(str_to_file + "\n")
                    print(f"")
    def run(self):
        '''
            Main function to start processing image input
        '''
        self.process_webcam()


