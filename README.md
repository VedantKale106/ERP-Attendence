# AttendenceMitra - PCCOE Attendance Dashboard

AttendenceMitra is a web application designed to help PCCOE students track, analyze, and manage their attendance records. The application scrapes attendance data from the official PCCOE ERP system and provides a user-friendly dashboard with insightful analytics.

## Features

- **Real-time Attendance Tracking**: Fetches your up-to-date attendance data from the PCCOE ERP system
- **Comprehensive Analytics**: Visualizes attendance percentages across all subjects
- **Smart Attendance Management**: Calculates how many lectures you can safely skip while maintaining the required 75% attendance
- **Low Attendance Alerts**: Identifies subjects requiring immediate attention
- **Data Visualization**: Presents attendance statistics with intuitive charts and graphs
- **Responsive Design**: Works seamlessly on both desktop and mobile devices



## Technology Stack

- **Backend**: Python with Flask
- **Frontend**: HTML, CSS (Tailwind CSS), JavaScript
- **Web Scraping**: Selenium WebDriver
- **Data Visualization**: Matplotlib
- **Deployment**: Vercel

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/erp-attendence.git
   cd erp-attendence
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install additional requirements:
   ```bash
   apt-get install build-essential  # For Linux
   ```

4. Set up environment variables:
   - Create a `.env` file in the root directory
   - Add your secret key: `SECRET_KEY=your_secret_key_here`

5. Run the application:
   ```bash
   python app.py
   ```

6. Access the application at `http://localhost:5000`

## Deployment

This application is configured for deployment on Vercel:

1. Make sure you have the Vercel CLI installed:
   ```bash
   npm install -g vercel
   ```

2. Deploy the application:
   ```bash
   vercel
   ```

## Usage

1. Log in using your PCCOE ERP credentials
2. View your overall attendance percentage
3. Analyze subject-wise attendance statistics
4. Check how many lectures you can afford to miss
5. Identify subjects requiring attendance improvement

## Security

- User credentials are not stored permanently
- Sessions are secured with secret keys
- Authentication is handled through the official PCCOE ERP system

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Known Issues

- The application requires Chrome WebDriver to be installed for the Selenium scraper
- Occasional timeouts may occur during peak server loads
- UI may need adjustments on very small screens

## Future Enhancements

- [ ] Add notification system for attendance alerts
- [ ] Implement attendance prediction based on historical data
- [ ] Create personalized attendance improvement plans
- [ ] Add export functionality for attendance reports
- [ ] Develop a mobile application


## Acknowledgments

- PCCOE for providing the ERP system
- The Flask and Selenium communities for their excellent documentation

## Disclaimer

This application is not officially affiliated with PCCOE. It's a student project created to help fellow students manage their attendance.

---

⭐ Star this repository if you find it useful! ⭐
