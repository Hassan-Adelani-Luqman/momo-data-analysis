## Video Walkthrough

[https://vimeo.com/1093488911/b69bede3ab?share=copy]

## The link to the report

[https://drive.google.com/file/d/1qSgP04De5DOm_9Si2tsVZpGb9-hmOIux/view?usp=drive_link]

# MoMo SMS Data Analysis Dashboard

A full-stack application for processing, analyzing, and visualizing MTN Mobile Money (MoMo) SMS transaction data. This dashboard provides insights into various types of mobile money transactions, helping users understand their financial patterns and behaviors.

## Features

- **Data Processing**: Parses and categorizes SMS messages from MTN MoMo
- **Interactive Dashboard**: Visual representation of transaction data
- **Search & Filter**: Advanced filtering capabilities by date, amount, and transaction type
- **Data Visualization**: Multiple chart types for different insights
- **Real-time Updates**: Dynamic data refresh and updates

## Transaction Categories

- Incoming Money
- Payments to Code Holders
- Transfers to Mobile Numbers
- Bank Deposits
- Airtime Bill Payments
- Cash Power Bill Payments
- Transactions Initiated by Third Parties
- Withdrawals from Agents
- Bank Transfers
- Internet and Voice Bundle Purchases

## Technology Stack

- **Backend**:
  - Python 3.8 or higher (3.11 recommended)
  - Flask (Web Framework)
  - SQLAlchemy (ORM)
  - SQLite (Database)

- **Frontend**:
  - HTML5
  - CSS3
  - JavaScript
  - Chart.js (Data Visualization)
  - Bootstrap (UI Framework)

## Prerequisites

- Python 3.8 or higher (3.11 recommended)
- pip (Python package manager)
- Git
- An XML file containing your MTN MoMo SMS data (named `modified_sms_v2.xml`)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Hassan-Adelani-Luqman/momo-data-analysis.git
   cd momo-data-analysis
   ```

2. Create and activate a virtual environment:
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   cd src
   pip install -r requirements.txt
   ```

4. Place your SMS data file:
   - Copy your `modified_sms_v2.xml` file to the root directory of the project
   - The file should be named exactly `modified_sms_v2.xml`
   - The file should contain valid MTN MoMo SMS data in XML format

## Running the Application

1. Start the Flask server:
   ```bash
   cd src
   python main.py
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## Database Setup

The application uses SQLite as its database. The database file (`app.db`) will be automatically created in the `src/database` directory when you first run the application. The database will be populated with data from your XML file.

## Troubleshooting

### Common Issues and Solutions

1. **ModuleNotFoundError: No module named 'X'**
   - Solution: Make sure you're in the virtual environment and run:
     ```bash
     pip install -r requirements.txt
     ```

2. **Database not found or empty**
   - Solution: Ensure your XML file is in the correct location and named correctly
   - The file should be named `modified_sms_v2.xml` and placed in the project root

3. **Port 5000 already in use**
   - Solution: Either:
     - Close the application using port 5000
     - Or change the port in `main.py` by setting the PORT environment variable

4. **XML parsing errors**
   - Solution: Ensure your XML file is properly formatted and contains valid MTN MoMo SMS data

5. **Permission errors on Windows**
   - Solution: Run your terminal/command prompt as administrator

### Getting Help

If you encounter any issues not covered here:
1. Check the error message carefully
2. Ensure all prerequisites are met
3. Verify your XML file format
4. Create an issue on the GitHub repository

## Project Structure

```
momo-data-analysis/
├── src/
│   ├── main.py              # Main application entry point
│   ├── models/              # Database models
│   ├── static/              # Static files (CSS, JS, images)
│   ├── templates/           # HTML templates
│   └── requirements.txt     # Python dependencies
├── data/                    # Data files
├── tests/                   # Test files
├── docs/                    # Documentation
├── README.md               # Project documentation
└── AUTHORS                 # List of contributors
```

## API Endpoints

- `GET /api/v1/messages` - Get all messages
- `GET /api/v1/categories` - Get transaction categories
- `GET /api/v1/statistics` - Get transaction statistics
- `GET /api/v1/messages/<id>` - Get specific message details

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- MTN Mobile Money for the SMS data format
- All contributors who have helped shape this project


## Contact

Project Link: [https://github.com/Hassan-Adelani-Luqman/momo-data-analysis](https://github.com/Hassan-Adelani-Luqman/momo-data-analysis) 