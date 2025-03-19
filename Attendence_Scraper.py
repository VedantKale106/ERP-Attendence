from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re

# Your login credentials
USERNAME = "122B1B124"
PASSWORD = "Urahara@106"

# Set up Edge WebDriver
options = webdriver.EdgeOptions()
options.add_argument("--start-maximized")  # Open browser in maximized mode
driver = webdriver.Edge(options=options)

try:
    # Open the login page
    driver.get("https://learner.pceterp.in/")

    # Wait for elements to load
    time.sleep(1)  # Adjust as needed

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
    time.sleep(2)  # Adjust as needed

    # Navigate to the attendance page
    driver.get("https://learner.pceterp.in/attendance")

    # Wait for the attendance data to load
    time.sleep(2)  # Adjust as needed

    # Collect attendance data from all subject blocks
    subject_blocks = driver.find_elements(By.XPATH, "//div[contains(@class, 'v-col-sm-4')]")

    attendance_records = []

    total_attended = 0
    total_lectures = 0

    print("Attendance Records:\n")

    for block in subject_blocks:
        try:
            # Extract subject name
            subject_name_element = block.find_element(By.XPATH, ".//div[@class='pb-5']")
            subject_name = subject_name_element.text.split("\n")[-1]  # Extracting subject name

            # Extract attendance (e.g., 28 / 30)
            attendance_element = block.find_element(By.XPATH, ".//span[contains(text(), '/')]")
            attendance_text = attendance_element.text.strip()

            # Extract attendance percentage (e.g., 93.33%)
            percentage_element = block.find_element(By.XPATH, ".//div[@class='v-progress-circular__content']")
            attendance_percentage = percentage_element.text.strip()

            # Extract type (e.g., Theory / Practical)
            try:
                type_element = block.find_element(By.XPATH, ".//div[@class='v-chip__content']")
                attendance_type = type_element.text.strip()
            except:
                attendance_type = "Unknown"

            # Parse attendance numbers
            match = re.search(r'(\d+) / (\d+)', attendance_text)
            if match:
                attended, total = map(int, match.groups())
                total_attended += attended
                total_lectures += total

            # Store data
            attendance_records.append({
                "Subject": subject_name,
                "Attendance": attendance_text,
                "Percentage": attendance_percentage,
                "Type": attendance_type
            })

            # Print the record
            print(f"{subject_name} ({attendance_type}): {attendance_text} ({attendance_percentage})")

        except Exception as e:
            print(f"Error extracting data for a subject: {e}")

    # Calculate and print current attendance percentage
    current_percentage = (total_attended / total_lectures) * 100 if total_lectures > 0 else 0
    print(f"\nCurrent Attendance Percentage: {current_percentage:.2f}%")

    # Take user input for upcoming lectures
    upcoming_lectures = int(input("\nEnter the number of upcoming lectures: "))
    attending_lectures = int(input("Enter the number of upcoming lectures you will attend: "))

    # Calculate future attendance percentage
    new_total_attended = total_attended + attending_lectures
    new_total_lectures = total_lectures + upcoming_lectures
    new_percentage = (new_total_attended / new_total_lectures) * 100 if new_total_lectures > 0 else 0

    print(f"\nProjected Attendance Percentage: {new_percentage:.2f}%")

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
