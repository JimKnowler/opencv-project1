import cv2

from app import App


def main():
    app = App()

    while True:
        video_feeds = app.process_frame()

        cv2.imshow('opencv-project1', video_feeds)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            # user has pressed 'q' to exit
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
