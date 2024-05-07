import sys
from PIL import Image, ImageGrab
import easyocr

def screenGrab(rect):
    """ Given a rectangle, return a PIL Image of that part of the screen.
        Uses ImageGrab on Windows. """
    x, y, width, height = rect
    image = ImageGrab.grab(bbox=(x, y, x + width, y + height))
    return image

if __name__ == "__main__":
    EXE = sys.argv[0]
    del(sys.argv[0])

    if len(sys.argv) != 4 or sys.argv[0] in ('--help', '-h', '-?', '/?'):  
        sys.stderr.write(EXE + ": monitors section of screen for text\n")
        sys.stderr.write(EXE + ": Give x, y, width, height as arguments\n")
        sys.exit(1)

    x, y, width, height = map(int, sys.argv[:4])
    screen_rect = [x, y, width, height]
    print(EXE + ": watching " + str(screen_rect))

    reader = easyocr.Reader(['en'])  # Initialize EasyOCR with English language

    while True:
        image = screenGrab(screen_rect)  
        text = reader.readtext(image)  # Use EasyOCR to read text from the image

        # Process the EasyOCR results
        for result in text:
            detected_text = result[1]  # Extract the detected text
            detected_text = detected_text.strip()
            if len(detected_text) > 0:
                print(detected_text)

