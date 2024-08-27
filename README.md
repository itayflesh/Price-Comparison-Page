# Price Comparison Page

## Description

https://drive.google.com/file/d/1CGaTq_J0mQbhbe2j7ibwVrS-ijpgohhG/view?usp=share_link

This project is a web application that allows users to compare prices of products across multiple e-commerce websites. Users can enter a product name, and the application will search for the product on Walmart, Newegg, and Best Buy, displaying the results in a table format. This tool helps users find the best deals quickly and easily.

## Installation

### Prerequisites
- Python 3.7+
- Node.js 12+
- npm (usually comes with Node.js)
- Google Chrome version 114 (not later versions)

### Backend Setup
1. Clone the repository:
   ```
   git clone https://github.com/your-username/price-comparison-page.git
   cd price-comparison-page
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required Python packages:
   ```
   pip install fastapi uvicorn requests beautifulsoup4 selenium webdriver_manager
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```
   cd product-search
   ```

2. Install the required Node.js packages:
   ```
   npm install
   ```
   This will create the `node_modules` folder with all necessary dependencies.

## How to Run

1. Start the backend server:
   ```
   uvicorn main:app --reload
   ```
   The API will be available at `http://localhost:8000`.

2. In a new terminal, start the frontend development server:
   ```
   cd product-search
   npm run dev
   ```
   The web application will be available at `http://localhost:3000`.

## How It Works

1. The user enters a product name in the search box on the web page.
2. When the search button is clicked, the frontend sends requests to the backend API for each website (Walmart, Newegg, and Best Buy).
3. The backend uses web scraping techniques to search for the product on each website and extract the relevant information (product title, price, and URL).
4. The results are sent back to the frontend, which displays them in a table format.
5. Users can click on the product titles to visit the original product pages on the respective websites.

## Technologies Used

### Backend
- FastAPI: A modern, fast (high-performance) web framework for building APIs with Python.
- BeautifulSoup: A library for parsing HTML and XML documents.
- Requests: A library for making HTTP requests in Python.
- Selenium: A tool for automating web browsers, used here for dynamic content scraping.

### Frontend
- Next.js: A React framework for building server-side rendered and static web applications.
- React: A JavaScript library for building user interfaces.

### Development Tools
- uvicorn: An ASGI server for running the FastAPI application.
- npm: The package manager for JavaScript, used for managing frontend dependencies.
