import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"])

import time

import cv2
import tempfile
import pyautogui



def find_accept_button():

    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
        screenshot_path = tmp_file.name
        pyautogui.screenshot(screenshot_path)

    image = cv2.imread(screenshot_path)
    template_accept = cv2.imread("accept_button.png")

    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    template_accept_gray = cv2.cvtColor(template_accept, cv2.COLOR_BGR2GRAY)

    result_template_accept_gray = cv2.matchTemplate(image_gray, template_accept_gray, cv2.TM_CCOEFF_NORMED)

    min_val_result_template_accept_gray, \
        max_val_result_template_accept_gray, \
        min_loc_result_template_accept_gray, \
        max_loc_result_template_accept_gray = cv2.minMaxLoc(result_template_accept_gray)

    threshold = 0.8

    if max_val_result_template_accept_gray >= threshold:
        button_width = template_accept.shape[1]
        button_height = template_accept.shape[0]
        top_left = max_loc_result_template_accept_gray

        button_center = (top_left[0] + button_width // 2, top_left[1] + button_height // 2)

        return button_center
    return None


def click_accept_button():
    button_center = find_accept_button()
    pyautogui.moveTo(button_center[0], button_center[1])
    pyautogui.click()


if __name__ == "__main__":
    print("Match Acceptor started successfully! Scanning for Button in 5 sec interval.")
    try:
        while True:
            print("Scanning for button...")
            if find_accept_button():
                click_accept_button()
            time.sleep(5)
    except KeyboardInterrupt:
        print("Match Acceptor closed.")