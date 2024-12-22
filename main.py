# ActiPulse Motion Dectector by Samik Sarkar
# 21st December 2024
# Samie_408

import tkinter as tk
from tkinter import filedialog
import cv2
import imutils

# Function to handle webcam feed
def start_webcam():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    process_video(cap)

# Function to handle recorded video
def play_recorded_video():
    file_path = filedialog.askopenfilename(title="Select Video File",
                                           filetypes=[("Video Files", "*.mp4;*.avi;*.mkv")])
    if file_path:
        cap = cv2.VideoCapture(file_path)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        process_video(cap)

# Common video processing function
def process_video(cap):
    _, start_frame = cap.read()
    if start_frame is None:
        print("Error: Unable to read video source.")
        cap.release()
        return

    start_frame = imutils.resize(start_frame, width=500)
    start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
    start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

    alarm_mode = True
    alarm_mode2 = True
    x = 0

    # Make the windows resizable
    cv2.namedWindow("Cam", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Cam2", cv2.WINDOW_NORMAL)

    try:
        while True:

            _, frame = cap.read()
            if not _:
                print("Failed to read frame. Exiting...")
                break  # Exit the loop if the frame cannot be read.
            frame = imutils.resize(frame, width=500)

            frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)

            difference = cv2.absdiff(frame_bw, start_frame)
            threshold = cv2.threshold(difference, 20
                                      , 255, cv2.THRESH_BINARY)[1]
            start_frame = frame_bw

            if alarm_mode2:
                cv2.namedWindow("Cam", cv2.WINDOW_NORMAL)
                cv2.imshow("Cam", frame)

            if alarm_mode:
                if threshold.sum() > 1800000:
                    print("Detected")
                    x += 1
                    print(x)
                cv2.namedWindow("Cam2", cv2.WINDOW_NORMAL)
                cv2.imshow("Cam2", threshold)

            key_pressed = cv2.waitKey(30)
            if key_pressed == ord("t"):
                alarm_mode = not alarm_mode
            if key_pressed == ord("p"):
                if alarm_mode2:
                    alarm_mode2 = False
                    alarm_mode = False
                else:
                    alarm_mode2 = True
                    alarm_mode = True
            if key_pressed == ord("r"):
                x = 0
                print("Reset")
                print(x)
            if key_pressed == ord("d"):
                if x > 10:
                    x -= 10
                print("Reduced")
                print(x)
            if key_pressed == ord("q"):
                alarm_mode = False
                print("Quitting")
                break
    except KeyboardInterrupt:
        print("\nProgram interrupted manually. Exiting...")

    finally:
        cap.release()
        cv2.destroyAllWindows()
        show_final_x_value(x)

# Function to show the final value of x in a new window
def show_final_x_value(final_x):
    final_window = tk.Toplevel(root)
    final_window.title("Result")
    final_window.geometry("600x300")

    final_window.resizable(True, True)  # Allow resizing in both directions

    final_label = tk.Label(final_window, text=f"Final value of x: {final_x}", font=("Arial", 16))
    final_label.pack(pady=40)

    if final_x > 600:
        final_label = tk.Label(final_window, text="ADHD detected", font=("Arial", 16, "bold"), fg="blue")
        final_label.pack(pady=10)
    else:
        final_label = tk.Label(final_window, text="No ADHD detected", font=("Arial", 16, "bold"), fg="blue")
        final_label.pack(pady=10)

    btn_ok = tk.Button(final_window, text="OK", command=final_window.destroy)
    btn_ok.pack(pady=10)


# Creating the GUI
root = tk.Tk()
root.title("ActiPulse by Samik Sarkar")

root.resizable(True, True)  # Allow resizing in both directions

header_label = tk.Label(root, text="ActiPulse", font=("Times New Roman", 24, "bold"), fg="blue")
header_label.pack(pady=20)


label = tk.Label(root, text="Choose Video Source", font=("Arial", 16))
label.pack(pady=10)

btn_webcam = tk.Button(root, text="Use Webcam", command=start_webcam, width=80)
btn_webcam.pack(pady=5)

btn_recorded = tk.Button(root, text="Play Recorded Video", command=play_recorded_video, width=80)
btn_recorded.pack(pady=5)

btn_exit = tk.Button(root, text="Exit", command=root.quit, width=80)
btn_exit.pack(pady=20)

root.mainloop()
