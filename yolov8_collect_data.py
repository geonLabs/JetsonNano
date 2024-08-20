import cv2
import os
import argparse
from datetime import datetime
from ultralytics import YOLO

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=640,  # 화면에 출력할 크기
    display_height=360, # 화면에 출력할 크기
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            capture_width,
            capture_height,
        )
    )

def show_camera(output_folder="output", display=False, save=False, save_original=False):
    window_title = "CSI Camera with YOLOv8"
    
    # YOLOv8 모델 로드 (사전 학습된 COCO 모델)
    model = YOLO('yolov8n.pt')  # yolov8n.pt 대신 다른 모델을 사용할 수 있습니다.

    # GStreamer 파이프라인을 사용하여 카메라 입력 받기 (원본 해상도)
    video_capture = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)

    if (save or save_original) and not os.path.exists(output_folder):
        os.makedirs(output_folder)

    if video_capture.isOpened():
        try:
            if display:
                window_handle = cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
            frame_skip = 3  # 30fps에서 10fps로 줄이기 위해 2개의 프레임을 건너뜀
            frame_count = 0

            while True:
                ret_val, original_frame = video_capture.read()
                if not ret_val:
                    print("카메라에서 프레임을 읽을 수 없습니다.")
                    break

                # 프레임을 3개 중 1개만 처리하여 10fps로 설정
                if frame_count % frame_skip == 0:
                    # 원본 프레임을 GPU에 업로드 (CUDA 사용)
                    frame_gpu = cv2.cuda_GpuMat()
                    frame_gpu.upload(original_frame)
                    
                    # YOLOv8 모델로 객체 검출 수행
                    results = model(frame_gpu.download())  # GPU에서 CPU로 다운로드하여 YOLO 모델 적용

                    # 검출된 객체의 클래스 ID를 수집
                    class_ids = [int(detection.cls[0]) for detection in results[0].boxes]

                    if class_ids:  # 클래스 ID가 존재하면
                        class_ids_str = "_".join(map(str, class_ids))
                        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

                        if save:  # JPEG로 저장
                            filename = os.path.join(output_folder, f"{timestamp}_{class_ids_str}.jpg")
                            cv2.imwrite(filename, original_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                            print(f"Saved frame to {filename}")

                        if save_original:  # PNG로 원본 저장
                            original_filename = os.path.join(output_folder, f"{timestamp}_{class_ids_str}.png")
                            cv2.imwrite(original_filename, original_frame)
                            print(f"Saved original frame to {original_filename}")

                    if display:  # 디스플레이가 활성화된 경우
                        # 주석이 추가된 프레임을 화면에 출력할 크기로 리사이즈
                        display_frame = cv2.resize(results[0].plot(), (640, 360))

                        # 화면에 리사이즈된 프레임을 표시
                        if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
                            cv2.imshow(window_title, display_frame)
                        else:
                            break

                frame_count += 1

                if display:  # 디스플레이가 활성화된 경우
                    keyCode = cv2.waitKey(10) & 0xFF
                    if keyCode == 27 or keyCode == ord('q'):  # ESC 키 또는 'q' 키로 종료
                        break
        finally:
            video_capture.release()
            if display:
                cv2.destroyAllWindows()
    else:
        print("Error: Unable to open camera")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YOLOv8 Camera Display and Save")
    parser.add_argument("--display", action="store_true", help="Display the camera feed with detections")
    parser.add_argument("--save", action="store_true", help="Save detected frames to the output folder as JPEG")
    parser.add_argument("--save_original", action="store_true", help="Save detected frames as PNG")
    parser.add_argument("--output_folder", type=str, default="output_frames", help="Folder to save the output images")

    args = parser.parse_args()

    show_camera(output_folder=args.output_folder, display=args.display, save=args.save, save_original=args.save_original)
