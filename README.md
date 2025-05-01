<<<<<<< HEAD
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

## 🚀 Quick Start Guide

### Prerequisites

- Node.js (v18 or higher)
- Python (v3.8 or higher)
- Git

### Step 1: Frontend Setup

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

### Step 2: Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the backend server:
   ```bash
   python -m uvicorn main:app --reload
   # Or use the batch file
   ./run_backend.bat
   ```

   The backend API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the backend server is running, you can access:
- Interactive API docs (Swagger UI): `http://localhost:8000/docs`
- Alternative API docs (ReDoc): `http://localhost:8000/redoc`

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

## 📋 API Endpoints

### Authentication
- `POST /token` - Login to get access token
- `POST /token/refresh` - Refresh access token
- `POST /users/` - Create new user

### Products
- `GET /products/` - List all products
- `GET /products/{product_id}` - Get product details
- `POST /products/` - Create new product (seller only)

### Cart
- `GET /cart/` - Get user's cart items
- `POST /cart/` - Add item to cart
- `PUT /cart/{cart_item_id}` - Update cart item quantity
- `DELETE /cart/{cart_item_id}` - Remove item from cart

### Orders
- `GET /orders/` - List user's orders
- `POST /orders/` - Create new order

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

## 🔧 Configuration

### Frontend Configuration
- API base URL is configured in `lib/api.ts`
- Image handling is configured in `next.config.mjs`

### Backend Configuration
- JWT secret key and algorithm in `auth.py`
- CORS settings in `main.py`
- Database connection in `database.py`

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

## 🌐 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## 📱 Mobile Responsiveness

The application is fully responsive and tested on:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (320px - 767px)

## 📞 Troubleshooting

**Images Not Loading?**
- Ensure the Next.js server has been restarted after config changes
- Check browser console for CORS or other network errors
- Verify that the `remotePatterns` in `next.config.mjs` includes `images.unsplash.com`

**Authentication Errors?**
- Make sure both frontend and backend servers are running
- Check that the API base URL in `lib/api.ts` matches your backend URL
- Clear browser localStorage and try logging in again

**Backend Connection Issues?**
- Verify the backend is running on port 8000
- Check for any errors in the terminal running the backend
- Make sure all required Python packages are installed 
=======
# FINAL-SYSTEM
>>>>>>> 027d31e3a26870027cd6a0a701ca06a8149efe33
