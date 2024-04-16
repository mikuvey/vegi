import sys
import pytesseract
from PIL import Image, ImageGrab

def screenGrab(rect):
    """ Given a rectangle, return a PIL Image of that part of the screen.
        Uses ImageGrab on Windows. """
    x, y, width, height = rect
    image = ImageGrab.grab(bbox=(x, y, x + width, y + height))
    return image

### Do some rudimentary command line argument handling
### So the user can specify the area of the screen to watch
if __name__ == "__main__":
    EXE = sys.argv[0]
    del(sys.argv[0])

    # EDIT: catch zero-args
    if len(sys.argv) != 4 or sys.argv[0] in ('--help', '-h', '-?', '/?'):  # some minor help
        sys.stderr.write(EXE + ": monitors section of screen for text\n")
        sys.stderr.write(EXE + ": Give x, y, width, height as arguments\n")
        sys.exit(1)

    # TODO - add error checking
    x, y, width, height = map(int, sys.argv[:4])

    # Area of screen to monitor
    screen_rect = [x, y, width, height]
    print(EXE + ": watching " + str(screen_rect))

    ### Loop forever, monitoring the user-specified rectangle of the screen
    while True:
        image = screenGrab(screen_rect)  # Grab the area of the screen
        text = pytesseract.image_to_string(image)  # OCR the image

        # IF the OCR found anything, write it to stdout.
        text = text.strip()
        if len(text) > 0:
            print(text)
