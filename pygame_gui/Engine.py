import cv2
import typing
import numpy as np
import stow 
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
import threading
import queue
mp_pose = mp.solutions.pose
##fix this later by moving to another file or etc..
'''
l_shoulder_idx = mp_pose.PoseLandmark.LEFT_SHOULDER.value
r_shoulder_idx = mp_pose.PoseLandmark.RIGHT_SHOULDER.value
l_elbow_idx = mp_pose.PoseLandmark.LEFT_ELBOW.value
r_elbow_idx = mp_pose.PoseLandmark.RIGHT_ELBOW.value
l_wrist_idx = mp_pose.PoseLandmark.LEFT_WRIST.value
r_wrist_idx = mp_pose.PoseLandmark.RIGHT_WRIST.value
'''

#dictionary to make writing to file much easier 
'''
landmark_subset_dict = {l_shoulder_idx:"left-shoulder", r_shoulder_idx: "right-shoulder",
                       l_elbow_idx: "left-elbow", r_elbow_idx:"right-elbow", 
                       l_wrist_idx: "left-wrist", r_wrist_idx: "right-wrist"}
'''
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
        self.queue = queue.Queue()
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
        print("goodbye!")
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
    def process_video(self) -> None:
        """Process video for given video_path and creates processed video in same path
        """
        mp_pose = mp.solutions.pose
        mp_drawing = mp.solutions.drawing_utils
    

     
        if not stow.exists(self.video_path):
           raise Exception(f"Given video path doesn't exists {self.video_path}")

        # Create a VideoCapture object and read from input file
        cap = cv2.VideoCapture(self.video_path)

        # Check if camera opened successfully
        if not cap.isOpened():
            raise Exception(f"Error opening video stream or file {self.video_path}")

        # Capture video details
        width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Create video writer in the same location as original video
        output_path = self.video_path.replace(f".{stow.extension(self.video_path)}", f"_{self.output_extension}.mp4")
        out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'MP4V'), fps, (width, height))
        rgb_frame = None
        # Read all frames from video
        for fnum in range(frames):
            # Capture frame-by-frame
            with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
                success, frame = cap.read()
                if not success:
                    break
                
                if self.check_video_frames_range(fnum):
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    # Process image with MediaPipe Pose model
                    results = pose.process(rgb_frame)

                    # Extract pose landmarks
                    pose_landmarks = results.pose_landmarks

                    if pose_landmarks is not None:
                        landmark_subset = landmark_pb2.NormalizedLandmarkList (
                        landmark = [results.pose_landmarks.landmark[landmark_pt] for landmark_pt in self.user_landmark_list]
                    )
                    
                        
                        mp_drawing.draw_landmarks(
                            image=frame,
                            landmark_list=landmark_subset,
                            connections=None, #custom_connections.CUSTOM_CONNECTIONS
                            landmark_drawing_spec = mp_drawing.DrawingSpec(color=(0,0,255), thickness=3, circle_radius=4)
                            )
            cv2.imshow('MediaPipe Pose', frame)
            if cv2.waitKey(5) & 0xFF == 27:
                break
                   # out.write(rgb_frame)
            if self.break_on_end and fnum >= self.end_video_frame:
                break
            continue

                #frame = self.custom_processing(self.flip(frame))

                #out.write(frame)

                #if not self.display(frame):
                    #break

        cap.release()
        out.release()
   
       
    
    def run(self):
        '''
            Main function to start processing image input
        '''
        if self.video_path:
           self.process_video_with_mediapipe()
        else:    
            self.process_webcam_new()




    def process_video_with_mediapipe(self):
        # 
        # Initialize the Mediapipe pose detection module
        mp_pose = mp.solutions.pose
        mp_drawing = mp.solutions.drawing_utils
    
        # Loop through the frames of the video
        if not stow.exists(self.video_path):
           raise Exception(f"Given video path doesn't exists {self.video_path}")
        cap = cv2.VideoCapture(self.video_path)
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
                    # Loop through all the landmarks
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
                cv2.imshow('Processed Video', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # Release the video file and close all windows
            cap.release()
            cv2.destroyAllWindows()

    '''
    def process_frame(self,frame):
        # Initialize the Mediapipe pose detection module
        mp_pose = mp.solutions.pose

        # Convert the frame to RGB format (required by Mediapipe)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect the landmarks on the person in the frame
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            results = pose.process(frame_rgb)
            landmarks = results.pose_landmarks

        # Draw the landmarks on the frame
        if landmarks is not None:
            # Loop through all the landmarks
            for landmark in landmarks.landmark:
                # Draw a small circle at each landmark point
                x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

        # Return the processed frame
        return frame

    def process_video_with_mediapipe_multithread(self):
        # Open the video file for processing
        cap = cv2.VideoCapture(self.video_path)

        # Get the frame rate of the video
        fps = cap.get(cv2.CAP_PROP_FPS)

        # Create a VideoWriter object to write the processed video to disk
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter('output.mp4', fourcc, fps, (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

        # Define a list to store the threads
        threads = []

        # Loop through the frames of the video
        while True:
            # Read a frame from the video file
            ret, frame = cap.read()

            # Check if the frame was successfully read
            if not ret:
                break

            # Create a separate thread for processing the frame
            t = threading.Thread(target=lambda frame: threads.append(self.process_frame(frame)), args=(frame,))
            t.start()

            # Wait for all threads to complete before displaying the frame
            for thread in threads:
                thread.join()

            # Display the processed frame
            cv2.imshow('Video', threads[-1])

            # Write the processed frame to disk
            #out.write(threads[-1])

            # Clear the list of threads
            threads.clear()

            # Wait for a key press to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the video file and the VideoWriter object, and close all windows
        cap.release()
        out.release()
        cv2.destroyAllWindows()'''
   
    def process_video_with_mediapipe_multithread(self):
        # Open the video file
        NUM_THREADS=4
        MAX_THREADS=4
        cap = cv2.VideoCapture(self.video_path)

        # Create a list to store the processed frames
        threads = []

        # Create a queue to hold the frames to be processed
        queue= self.queue

        # Create a lock to synchronize access to the threads list
        lock = threading.Lock()

        # Start the worker threads
        for i in range(NUM_THREADS):
            thread = threading.Thread(target=self.process_frames, args=(queue, lock, threads))
            thread.start()

        # Read the first frame from the video
        ret, frame = cap.read()

        # Loop through all the frames in the video
        while ret:
            # Add the frame to the queue
            queue.put(frame)

            # Read the next frame from the video
            ret, frame = cap.read()

            # Display the last processed frame
            if threads and len(threads) > 0:
                cv2.imshow('Video', threads[-1])
                #cv2.waitKey(1)

        # Release the video capture object
        cap.release()

        # Stop the worker threads
        for i in range(NUM_THREADS):
            queue.put(None)
        for thread in threading.enumerate():
            if thread != threading.current_thread():
                thread.join()
    def process_frames(self,queue, lock, threads):
            NUM_THREADS=4
            MAX_THREADS=20
            # Initialize the mediapipe pose detection model
            mp_pose = mp.solutions.pose
            mp_drawing = mp.solutions.drawing_utils
            # Loop until the main thread signals to stop
            while True:
                # Wait for a frame to be added to the queue
                frame = queue.get()

                # Check if this is the sentinel value indicating the end of the video
                if frame is None:
                    # Signal to stop processing
                    break

                # Convert the frame to RGB format
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Process the frame with mediapipe
                with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
                    results = pose.process(frame_rgb)
                    landmarks = results.pose_landmarks

                # Draw the landmarks on the frame
                    if landmarks is not None:
                        # Loop through all the landmarks
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

               

                # Acquire the lock to modify the threads list
                with lock:
                    # Add the processed frame to the threads list
                    threads.append(frame)

                    # Remove the oldest frames from the threads list to limit its size
                    if len(threads) > MAX_THREADS:
                        threads.pop(0)

                # Release the lock
                lock.release()

                # Signal to the queue that the frame has been processed
                queue.task_done()      
