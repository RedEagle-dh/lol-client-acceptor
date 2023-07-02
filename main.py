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

    # Bilderkennung durchführen
    result_template_accept_gray = cv2.matchTemplate(image_gray, template_accept_gray, cv2.TM_CCOEFF_NORMED)

    min_val_result_template_accept_gray, \
        max_val_result_template_accept_gray, \
        min_loc_result_template_accept_gray, \
        max_loc_result_template_accept_gray = cv2.minMaxLoc(result_template_accept_gray)

    # Schwellenwert für die Übereinstimmung festlegen
    threshold = 0.8

    if max_val_result_template_accept_gray >= threshold:
        # Koordinaten des "Accept"-Buttons ermitteln
        button_width = template_accept.shape[1]
        button_height = template_accept.shape[0]
        top_left = max_loc_result_template_accept_gray
        # bottom_right = (top_left[0] + button_width, top_left[1] + button_height)

        # Mittelpunkt des "Accept"-Buttons berechnen
        button_center = (top_left[0] + button_width // 2, top_left[1] + button_height // 2)

        return button_center
    return None


def click_accept_button():
    button_center = find_accept_button()

    if button_center:
        pyautogui.moveTo(button_center[0], button_center[1])
        pyautogui.click()


print("Match Acceptor started successfully! Scanning for Button in 5 sec interval.")
try:
    while True:
        if find_accept_button():
            click_accept_button()
        print("Scanning for button...")
        time.sleep(5)
except KeyboardInterrupt:
    print("Match Acceptor closed.")
