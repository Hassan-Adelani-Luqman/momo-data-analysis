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
  - Python 3.13
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

- Python 3.13 or higher
- pip (Python package manager)
- Git

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/momo-data-analysis.git
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

## Video Walkthrough

[Link to 5-minute video walkthrough will be added here]

## Contact

Your Name - your.email@example.com
Project Link: [https://github.com/yourusername/momo-data-analysis](https://github.com/yourusername/momo-data-analysis) 