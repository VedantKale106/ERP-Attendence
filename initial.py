from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re

# Your login credentials
USERNAME = "user"
PASSWORD = "pass"

# Set up Edge WebDriver
options = webdriver.EdgeOptions()
options.add_argument("--start-maximized")  # Open browser in maximized mode
driver = webdriver.Edge(options=options)

try:
    # Open the login page
    driver.get("https://learner.pceterp.in/")

    # Wait for elements to load
    time.sleep(3)  # Adjust as needed

    # Locate and enter username
    username_input = driver.find_element(By.XPATH, "//input[@type='text']")
    username_input.send_keys(USERNAME)

    # Locate and enter password
    password_input = driver.find_element(By.XPATH, "//input[@type='password']")
    password_input.send_keys(PASSWORD)

    # Locate and click the Sign In button
    sign_in_button = driver.find_element(By.XPATH, "//button[contains(@class, 'v-btn') and contains(., 'Sign In')]")
    sign_in_button.click()

    # Wait for login process to complete
    time.sleep(5)  # Adjust as needed

    # Navigate to the attendance page
    driver.get("https://learner.pceterp.in/attendance")

    # Wait for the attendance data to load
    time.sleep(5)  # Adjust as needed

    # Collect attendance data
    attendance_elements = driver.find_elements(By.XPATH, "//span[contains(@data-v-a826b744, '')]")
    attendance_data = set()  # Using a set to store unique attendance values
    total_attended = 0
    total_lectures = 0

    for element in attendance_elements:
        match = re.search(r'(\d+) / (\d+)', element.text)
        if match:
            attended, total = map(int, match.groups())
            total_attended += attended
            total_lectures += total
            attendance_data.add(match.group())

    # Calculate and print current attendance percentage
    current_percentage = (total_attended / total_lectures) * 100 if total_lectures > 0 else 0
    print("Attendance Records:")
    for record in sorted(attendance_data):
        print(record)
    print(f"Current Attendance Percentage: {current_percentage:.2f}%")

    # Take user input for upcoming lectures
    upcoming_lectures = int(input("Enter the number of upcoming lectures: "))
    attending_lectures = int(input("Enter the number of upcoming lectures you will attend: "))

    # Calculate future attendance percentage
    new_total_attended = total_attended + attending_lectures
    new_total_lectures = total_lectures + upcoming_lectures
    new_percentage = (new_total_attended / new_total_lectures) * 100 if new_total_lectures > 0 else 0

    print(f"Projected Attendance Percentage: {new_percentage:.2f}%")

    # Calculate max lectures you can skip to stay above 80%
    max_possible_skips = (total_attended - (0.8 * total_lectures)) / 0.2
    max_possible_skips = max(0, int(max_possible_skips))
    print(f"You can afford to skip up to {max_possible_skips} out of {total_lectures} lectures while staying above 80%.")


    # Wait to observe result
    time.sleep(500)  # Adjust as needed

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the browser
    driver.quit()
