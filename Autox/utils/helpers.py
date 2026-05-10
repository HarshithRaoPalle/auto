import os
from datetime import datetime


def take_screenshot(driver, name):

    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    path = f"screenshots/{name}_{timestamp}.png"

    driver.save_screenshot(path)

    return path