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
