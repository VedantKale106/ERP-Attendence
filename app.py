from flask import Flask, render_template, request, redirect, url_for, session
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Set a secret key for session management

def fetch_attendance(username, password):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(options=options)  # Use Chrome instead of Edge

    try:
        driver.get("https://learner.pceterp.in/")
        time.sleep(1)

        # Enter login credentials
        driver.find_element(By.XPATH, "//input[@type='text']").send_keys(username)
        driver.find_element(By.XPATH, "//input[@type='password']").send_keys(password)
        driver.find_element(By.XPATH, "//button[contains(@class, 'v-btn') and contains(., 'Sign In')]").click()
        time.sleep(2)

        # Navigate to attendance page
        driver.get("https://learner.pceterp.in/attendance")
        time.sleep(2)

        # Extract student name
        try:
            student_name_element = driver.find_element(By.XPATH, "//span[contains(@class, 'ml-3 font-weight-bold text-medium-emphasis')]")
            student_name = student_name_element.text.strip()
        except:
            student_name = "Unknown"

        subject_blocks = driver.find_elements(By.XPATH, "//div[contains(@class, 'v-col-sm-4')]")

        attendance_records = []
        total_attended = 0
        total_lectures = 0

        for block in subject_blocks:
            try:
                subject_name = block.find_element(By.XPATH, ".//div[@class='pb-5']").text.split("\n")[-1]
                attendance_text = block.find_element(By.XPATH, ".//span[contains(text(), '/')]").text.strip()
                percentage = block.find_element(By.XPATH, ".//div[@class='v-progress-circular__content']").text.strip()

                try:
                    attendance_type = block.find_element(By.XPATH, ".//div[@class='v-chip__content']").text.strip()
                    attendance_type = attendance_type.split()[0]  # Extract only the first word
                except:
                    attendance_type = "Unknown"

                match = re.search(r'(\d+) / (\d+)', attendance_text)
                if match:
                    attended, total = map(int, match.groups())
                else:
                    attended, total = 0, 0  # Default if parsing fails

                if total == 0:
                    continue  

                total_attended += attended
                total_lectures += total

                attendance_records.append({
                    "Subject": subject_name,
                    "Attendance": attendance_text,
                    "Percentage": float(percentage.replace("%", "")),
                    "Type": attendance_type
                })

            except Exception as e:
                print(f"Error extracting data for a subject: {e}")

        driver.quit()

        current_percentage = (total_attended / total_lectures) * 100 if total_lectures > 0 else 0

        attendance_records.sort(key=lambda x: x["Percentage"])

        low_attendance_subjects = attendance_records[:6]
        high_attendance_subjects = attendance_records[-6:]

        low_attendance_chart = generate_bar_chart(low_attendance_subjects, "Top 6 Subjects with Lowest Attendance", "red")
        high_attendance_chart = generate_bar_chart(high_attendance_subjects, "Top 6 Subjects with Highest Attendance", "green")

        lectures_to_bunk = 0
        if current_percentage >= 75:
            lectures_to_bunk = calculate_bunk_limit(total_attended, total_lectures)

        return {
            "student_name": student_name,  # Pass the student's name
            "current_percentage": current_percentage,
            "attendance_data": attendance_records,
            "low_attendance_subjects": low_attendance_subjects,
            "high_attendance_subjects": high_attendance_subjects,
            "lectures_to_bunk": lectures_to_bunk,
            "low_attendance_chart": low_attendance_chart,
            "high_attendance_chart": high_attendance_chart
        }

    except Exception as e:
        driver.quit()
        return {"error": str(e)}



# Function to generate bar chart and return it as a base64 string
def generate_bar_chart(subjects, title, color):
    if not subjects:
        return None

    subjects_names = [sub["Subject"] for sub in subjects]
    percentages = [sub["Percentage"] for sub in subjects]

    plt.figure(figsize=(8, 5))
    plt.bar(subjects_names, percentages, color=color)
    plt.xlabel("Subjects")
    plt.ylabel("Attendance (%)")
    plt.title(title)
    plt.ylim(0, 100)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Save plot to a BytesIO object and encode as base64
    img_io = io.BytesIO()
    plt.savefig(img_io, format='png')
    img_io.seek(0)
    encoded_img = base64.b64encode(img_io.read()).decode("utf-8")
    plt.close()

    return f"data:image/png;base64,{encoded_img}"

# Function to calculate how many lectures a student can bunk
def calculate_bunk_limit(attended, total):
    lectures_to_bunk = 0
    while ((attended / (total + lectures_to_bunk)) * 100) >= 75:
        lectures_to_bunk += 1
    return lectures_to_bunk - 1  # Subtract 1 to ensure the threshold doesn't drop below 75%

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["username"] = request.form["username"]
        session["password"] = request.form["password"]
        return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/dashboard", methods=["GET"])
def dashboard():
    username = session.get("username")
    password = session.get("password")

    if not username or not password:
        return redirect(url_for("login"))

    attendance_data = fetch_attendance(username, password)

    if "error" in attendance_data:
        return f"Error: {attendance_data['error']}"

    return render_template("dashboard.html", data=attendance_data)

if __name__ == "__main__":
    app.run(debug=True)
