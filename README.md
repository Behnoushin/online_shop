# 🛒 My Online Shop API

<p align="center">
  <img src="images/online_shop.png" alt="Online Shop Logo" width="300"/>
</p>

Welcome to **My Online Shop**, a powerful Django REST Framework-based e-commerce backend system designed to handle everything from user management and product handling to CRM, shipping, and order processing — all built with scalability and modularity in mind.

---

## 🧩 Overview

This project provides a robust and scalable API for:

- 🛍️ **Product & Brand Management**  
  Handles product listings, brands, warranties, stock, discounts, and ratings.

- 📦 **Order & Delivery System**  
  Complete order placement, payment tracking, and real-time delivery status updates.

- 🔐 **User Authentication & Profiles**  
  Secure JWT authentication, profile management, OTP, and purchase history.

- 🧾 **CRM Dashboard for Admins**  
  Advanced panel for admin to monitor users, orders, logs, and more.

- 💬 **Messaging & Customer Support**  
  Built-in messaging system, product Q&A, contact form, and more.

- 🛠️ **Smart Utilities & Error Handling**  
  Central utility logic, signal-based workflows, and detailed error logging.

---

## 🔧 Features

### 👥 User System & Authentication
- JWT-based authentication system
- Secure registration and login with OTP support
- Password change with old password validation
- Profile update with custom validation
- Purchase history tracking
- Unique email validation
- Signal-based welcome email system

### 🛒 Product & Brand System
- Product and brand management with categories
- Ratings & Reviews for both products and brands
- Add to cart and wishlist functionality
- Discount and coupon system with time range
- Product-level Q&A and comments
- Warranty management per product
- Auto stock validation and availability system

### 📦 Shipping & Delivery
- Dynamic shipping methods and policies
- Delivery status tracking
- Integration with order and payment modules

### 🧾 Orders
- Create and manage orders with multiple items
- Real-time stock update on order placement/deletion
- Order total price with applied discounts
- Order payment status and confirmation
- Admin, user, and CRM-specific views for order control

### 📊 CRM & Dashboard
- Full admin panel for overview and monitoring
- User stats, order statuses, and customer activity
- Real-time messaging, logs, and notifications

### 💬 Contact & Messaging
- About Us, Contact Us, FAQs, and Rules pages
- Messaging system between user and admin
- Logging system for admin-side events and errors

---

## 📦 Technologies Used

- 🐍 Python 3.x  
- 🕸️ Django 4.x  
- ⚙️ Django REST Framework  
- 📦 JWT Authentication  
- 🧪 Django Validators & Signals  
- 🔎 Django Filter  
- 🐳 Docker & Docker Compose  
- 📨 SMTP Email (for notifications/OTP)

---

## 🗂️ Apps Structure

- `info` – About, Contact, FAQs, Rules, and location  
- `utility` – Base classes, shared validators, permissions  
- `user_management` – Login, registration, profile, purchase history, OTP  
- `shipping` – Shipping details and delivery status  
- `product` – Products, brands, rating/review, comments, wishlist, cart, discounts  
- `order` – Order placement, payment, and tracking  
- `crm` – Admin dashboard and overview system  
- `messaging` – Messaging system and event logs  
- `errors_handler` – Error handling and logging system

---

## 🚀 Getting Started

### ✅ Backend Setup

```bash
git clone https://github.com/Behnoushin/online_shop
cd online_shop

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```

Crafted with ❤️ by Behnoushin (Behnoush Shahraeini)
