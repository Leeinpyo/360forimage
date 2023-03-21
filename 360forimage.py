import cv2
from tkinter import Tk, filedialog, simpledialog, messagebox
import os
import sys

# Create a Tkinter root window (it won't be shown)
root = Tk()
root.withdraw()

# Ask the user to select a video file
video_path = filedialog.askopenfilename(title='변환할 비디오 파일을 선택해 주세요.')
if not video_path:
    messagebox.showwarning('경고', '비디오 파일이 선택되지 않았습니다.')
    sys.exit()

# Check if the selected file is a video file
if not os.path.splitext(video_path)[1].lower() in ('.avi', '.mp4', '.mov', '.mkv'):
    messagebox.showwarning('경고', '선택한 파일이 비디오 파일이 아닙니다.')
    sys.exit()

# Ask the user to select a save location for the extracted frames
save_path = filedialog.askdirectory(title='이미지들이 저장될 경로를 선택해 주세요.')
if not save_path:
    messagebox.showwarning('경고', '저장 경로가 선택되지 않았습니다.')
    sys.exit()

# Ask the user to enter the number of frames they want to extract
frame_count = None
while frame_count is None or not 0 <= frame_count <= 99:
    frame_count_str = simpledialog.askstring('Frame count', '몇 프레임으로 나누고 싶으신가요? 0~99정수입력')
    try:
        frame_count = int(frame_count_str)
    except ValueError:
        messagebox.showwarning('경고', '0~99 사이의 정수를 입력해주세요.')

# Load the video
cap = cv2.VideoCapture(video_path)

# Check if the video was opened successfully
if not cap.isOpened():
    messagebox.showwarning('경고', '비디오 파일을 열 수 없습니다.')
    sys.exit()

# Get the total number of frames in the video
total_frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Calculate the interval between frames to extract
interval = total_frame_count // frame_count

for i in range(frame_count):
    # Set the position of the next frame to read
    cap.set(cv2.CAP_PROP_POS_FRAMES, i * interval)
    
    # Read the frame from the video
    ret, frame = cap.read()
    
    # Save the frame as an image with zero-padded index
    file_name = f"{save_path}/img{i:02d}.jpg"
    cv2.imwrite(file_name, frame)

# Release resources
cap.release()