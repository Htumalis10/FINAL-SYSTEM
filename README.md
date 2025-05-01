# HanyThrift - Secondhand Shopping Platform

HanyThrift is a modern web application for buying and selling secondhand items, built with Next.js for the frontend and Python FastAPI for the backend. The platform features secure authentication, real-time cart management, and a responsive user interface.

## 🌟 Features

- **User Authentication**
  - Secure JWT-based authentication
  - Token refresh mechanism
  - User registration and login
  - Protected routes and API endpoints

- **Product Management**
  - Browse products by category
  - Featured products section
  - Detailed product views
  - Image caching for offline viewing
  - Product search functionality

- **Shopping Experience**
  - Real-time cart management
  - "Buy Now" option for direct checkout
  - Secure payment integration
  - Order history tracking

- **UI/UX Features**
  - Responsive design
  - Category-based navigation
  - Loading states and error handling
  - Toast notifications
  - Offline support for images

## 💻 Technologies and System Architecture

### Languages and Frameworks
- **Frontend**:
  - TypeScript: Primary language for type-safe frontend development
  - React: Component-based UI library
  - Next.js 14: React framework for production
  - Tailwind CSS: Utility-first CSS framework for styling
  
- **Backend**:
  - Python 3.8+: Primary language for backend development
  - FastAPI: Modern, high-performance web framework
  - SQLAlchemy: SQL toolkit and ORM
  - Pydantic: Data validation and settings management

### System Architecture
- **Client-Server Model**: The application follows a client-server architecture where the Next.js frontend communicates with the FastAPI backend via RESTful API calls.

- **Data Flow**:
  1. User interacts with the Next.js frontend
  2. Frontend makes API requests to the backend using the API client (`/lib/api.ts`)
  3. Backend processes requests, interacts with the SQLite database, and returns responses
  4. Frontend updates the UI based on responses

- **Authentication Flow**:
  1. User credentials are sent to the backend
  2. Backend validates credentials and issues JWT tokens
  3. Frontend stores tokens (access token in memory, refresh token in localStorage)
  4. Tokens are automatically refreshed before expiration
  5. Protected routes check for valid tokens before allowing access

- **State Management**:
  - React Context API used for global state (auth, cart)
  - Component-level state for UI interactions
  - Backend maintains session information via JWT tokens

- **Database Design**:
  - SQLite database with SQLAlchemy ORM
  - Core models: User, Product, Order, OrderItem, CartItem
  - Relationships maintained through foreign keys

## 🚀 Quick Start Guide

### Prerequisites

- Node.js (v18 or higher)
- Python (v3.8 or higher)
- Git

### Option 1: One-Click Start (Windows)

For Windows users, you can use the provided PowerShell script to start both frontend and backend services with a single command:

```powershell
./run-dev.ps1
```

This will:
1. Start the FastAPI backend server in a new PowerShell window
2. Start the Next.js frontend development server in the current window

### Option 2: Manual Setup

#### Step 1: Frontend Setup

1. Install Node.js dependencies:
   ```bash
   npm install
   ```

2. Start the frontend development server:
   ```bash
   npm run dev
   # Or use the batch file
   ./run_frontend.bat
   ```

   The frontend will be available at `http://localhost:3000`

#### Step 2: Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
   python -m uvicorn main:app --reload 
3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Start the backend server:
   ```bash
   python -m uvicorn main:app --reload
   ```
   The backend API will be available at `http://localhost:8000`

## 🔐 Authentication Flow

1. **Registration**:
   - User submits registration form
   - Backend validates and creates user account
   - Automatic login after successful registration

2. **Login**:
   - User submits credentials
   - Backend validates and issues JWT tokens
   - Access token stored in memory
   - Refresh token stored in localStorage

3. **Token Refresh**:
   - Access token expires after 30 days (configurable)
   - System automatically refreshes 5 minutes before expiration
   - New tokens issued if refresh token is valid

## 💾 Database

The application uses SQLite as its database. The database file (`backend/hanythrift.db`) will be created automatically when you first run the application. Sample products are automatically added for demonstration purposes.

## 📁 Project Structure

```
hanythrift/
├── app/                  # Next.js pages and routes
├── components/           # React components
├── lib/                  # Utility functions and configs
├── public/               # Static assets
│   └── images/           # Image assets
├── styles/               # Global styles
├── backend/              # Python FastAPI backend
│   ├── __pycache__/      # Python cache files
│   ├── hanythrift.db     # SQLite database
│   ├── auth.py           # Authentication logic
│   ├── database.py       # Database connection
│   ├── main.py           # Main API endpoints
│   ├── models.py         # Database models
│   ├── schemas.py        # Pydantic schemas
│   └── requirements.txt  # Python dependencies
└── README.md             # This file
```

## 🛠️ Development Tips

1. **Running Both Services**
   - You need to run both the frontend and backend servers simultaneously
   - Use separate terminal windows or use the provided batch files

2. **Image Loading**
   - External images from Unsplash are used for product images
   - The Next.js configuration in `next.config.mjs` includes Unsplash in the allowed domains

3. **Authentication Issues**
   - If you encounter "Failed to refresh token" errors, ensure both frontend and backend are running
   - Check browser console for more detailed error messages

4. **Database Reset**
   - Sample products are recreated each time the backend starts
   - To keep existing data, comment out the `create_sample_products()` call in `main.py`

## 🔒 Security Features

- JWT-based authentication with token refresh
- Password hashing with bcrypt
- CORS protection
- SQLite database for simple deployment


## 💰 Payment System

HanyThrift uses a secure payment processing system that handles customer transactions for secondhand item purchases. The payment flow is designed to be user-friendly while maintaining security and reliability.

### Payment Flow

1. **Cart Checkout**:
   - User reviews items in cart and proceeds to checkout
   - System verifies product availability and calculates final price
   - Shipping information and payment method selection

2. **Payment Processing**:
   - Secure handling of payment details
   - Real-time transaction validation
   - Support for multiple payment methods:
     - Credit/Debit cards
     - Digital wallets (when configured)
     - Bank transfers (optional)

3. **Order Confirmation**:
   - Transaction receipt generation
   - Order details stored in database
   - Email confirmation sent to buyer and seller

4. **Payment Settlement**:
   - Funds held in escrow until delivery confirmation
   - Automatic transfer to seller account after delivery period
   - Commission fees automatically calculated and deducted

### Implementation Details

- Payment processing is handled through a combination of frontend UI and backend API endpoints
- Sensitive payment information is never stored in the database
- All payment data transmission uses HTTPS encryption
- The system is designed to handle payment failures gracefully with appropriate user feedback


