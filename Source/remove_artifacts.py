import cv2

def remove_artifacts(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(output_path, fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_denoised = cv2.fastNlMeansDenoisingColored(frame, None, 10, 10, 7, 21)
        out.write(frame_denoised)

    cap.release()
    out.release()
