import cv2
import typing
import numpy as np
import stow 
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
import mp_landmark
import time
mp_pose = mp.solutions.pose

class MediaPipeEngine :
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
            user_landmark_list: list = []
           
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
        self.user_landmark_list = user_landmark_list
        #self.queue = queue.Queue()
        ##mediapipe initialization
       
    
    def flip (self, frame: np.ndarray) -> np.ndarray:
         
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
    def display(self, frame: np.ndarray, webcam: bool = False) -> bool:
        """Display current frame if self.show = True
        When displaying webcam you can control the background images

        Args:
            frame: (np.ndarray) - frame to be displayed
            webcam: (bool) - Add aditional function for webcam. Keyboard 'a' for next or 'd' for previous

        Returns:
            (bool) - Teturn True if no keyboard "Quit" interruption
        """
        if self.show:
            cv2.imshow('No name 1', frame)
            k = cv2.waitKey(1)
            if k & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                return False
            '''
            if webcam:
                if k & 0xFF == ord('a'):
                    for custom_object in self.custom_objects:
                        # change background to next with keyboar 'a' button
                        if isinstance(custom_object, MPSegmentation):
                            custom_object.change_image(True)
                elif k & 0xFF == ord('d'):
                    for custom_object in self.custom_objects:
                        # change background to previous with keyboar 'd' button
                        if isinstance(custom_object, MPSegmentation):
                            custom_object.change_image(False)
            '''
        return True
    
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

            if not self.display(frame,webcam=True):
                break
        else:
            raise Exception(f"Webcam with ID ({self.webcam_id}) cannot be opened")
        
        cap.release()
    def process_webcam_new(self)-> None:
            # Setup MediaPipe Pose model
        mp_pose = mp.solutions.pose
        mp_drawing = mp.solutions.drawing_utils
        cap = cv2.VideoCapture(0)

        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:

            while True:
                ret, image = cap.read()
                if not ret:
                    break
                #resize the frame:
                image = cv2.resize(image ,(1000,600))

                # Convert BGR image to RGB for processing with MediaPipe
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                # Process image with MediaPipe Pose model
                results = pose.process(rgb_image)

                # Extract pose landmarks
                pose_landmarks = results.pose_landmarks

                if pose_landmarks is not None:
                    landmark_subset = landmark_pb2.NormalizedLandmarkList (
                    landmark = [results.pose_landmarks.landmark[landmark_pt] for landmark_pt in self.user_landmark_list]
                )
                    
                    
                    mp_drawing.draw_landmarks(
                        image=image,
                        landmark_list=landmark_subset,
                        connections=None, #custom_connections.CUSTOM_CONNECTIONS
                        landmark_drawing_spec = mp_drawing.DrawingSpec(color=(0,0,255), thickness=3, circle_radius=4)
                        )
                    
                cv2.imshow('MediaPipe Pose', image)
                if cv2.waitKey(5) & 0xFF == 27:
                    break
        self.user_landmark_list = []
        cap.release()
        cv2.destroyAllWindows()
        #print("goodbye!")
    def check_video_frames_range(self, fnum):
        """Not to waste resources this function processes only specified range of video frames
        Args:
            fnum: (int) - current video frame number
        Returns:
            status: (bool) - Return True if skip processing otherwise False
        """
        if self.start_video_frame and fnum < self.start_video_frame:
            return True

        if self.end_video_frame and fnum > self.end_video_frame:
            return True
        
        return False
   
   
       
    
    def run(self):
        '''
            Main function to start processing image input
        '''
        if self.video_path:
           self.process_video_with_mediapipe()
        else:    
            self.process_webcam_new()


    #TODO: implement me please!
    def make_csv (self,landmarks, start_time):
        output_csv_path = self.video_path.replace(f".{stow.extension(self.video_path)}", f"_{self.output_extension}.csv")
        mp
        with open(output_csv_path,'a') as f:
            for idx in self.user_landmark_list:
                
                    
                        x = landmarks.landmark[idx].x
                        y = landmarks.landmark[idx].y
                        z = landmarks.landmark[idx].z
                        
                        str_to_file = f"time stamp: {time.time()- start_time} sec,landmark-name:{mp_landmark.landmark_dict[idx]}, x: {x}, y: {y}, z: {z}"
                        f.write(str_to_file + "\n")
                       
                

    def process_video_with_mediapipe(self) -> None:
        # 
        # Initialize the Mediapipe pose detection module
        mp_pose = mp.solutions.pose
        mp_drawing = mp.solutions.drawing_utils
        start_time = time.time()
        # Loop through the frames of the video
        if not stow.exists(self.video_path):
           raise Exception(f"Given video path doesn't exists {self.video_path}")
        cap = cv2.VideoCapture(self.video_path)
        # Capture video details
        width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Create video writer in the same location as original video
        output_path = self.video_path.replace(f".{stow.extension(self.video_path)}", f"_{self.output_extension}.mp4")
        out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'MP4V'), fps, (width, height))
        rgb_frame = None
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            
            while True:
                # Read a frame from the video file
                ret, frame = cap.read()

                # Check if the frame was successfully read
                if not ret:
                    break

                # Convert the frame to RGB format (required by Mediapipe)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Detect the landmarks on the person in the frame
            
                results = pose.process(frame_rgb)
                landmarks = results.pose_landmarks

                # Draw the landmarks on the frame
             
                if landmarks is not None:
                        landmark_subset = landmark_pb2.NormalizedLandmarkList (
                        landmark = [results.pose_landmarks.landmark[landmark_pt] for landmark_pt in self.user_landmark_list]
                    )
                        
                            
                        mp_drawing.draw_landmarks(
                            image=frame,
                            landmark_list=landmark_subset,
                            connections=None, #custom_connections.CUSTOM_CONNECTIONS
                            landmark_drawing_spec = mp_drawing.DrawingSpec(color=(0,0,255), thickness=3, circle_radius=4)
                            )
                # Display the processed frame
                self.make_csv(landmarks,start_time)
                cv2.imshow('Processed Video', frame)
                out.write(frame)
                if cv2.waitKey(5) & 0xFF == 27:
                    break

            # Release the video file and close all windows
            cap.release()
            out.release
            print("Printing from process_video_with_mediapipe: ", self.user_landmark_list)
            self.user_landmark_list = []
            cv2.destroyAllWindows()

   
    
