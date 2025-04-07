# WhatsApp Bot Django

## Overview
This repository contains a Django-based application that integrates with WhatsApp to send and receive messages. It leverages Django's framework to create a bot capable of responding to incoming inquiries, automating specific tasks, and demonstrating how WhatsApp messaging can be used within a web application.

## Features
- A Django project structured to handle inbound and outbound WhatsApp messages.  
- Clear separation of logic into Django apps, including messaging handlers and business logic.  
- Potential to integrate with external APIs (e.g., Twilio) for WhatsApp messaging.  
- Utilizes SQLite (db.sqlite3) by default for database management.

## Prerequisites
Before you begin, ensure your environment meets the following requirements:
- Python 3.9+ installed.
- A virtual environment solution (e.g., venv or conda).
- A WhatsApp-enabled messaging service (e.g., Twilio), specifically configuring your Twilio WhatsApp Sandbox.
- (Optional) A PostgreSQL or other supported database if you plan to go beyond the default SQLite setup.

## Installation and Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/RashiJyotishi/whatsapp-bot-django.git
   cd whatsapp-bot-django
   ```

2. **Create and Activate a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate      # On Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   This command will install all the required Python packages for the project.

4. **Configure Environment Variables**
   - Create a new file named `.env` in the project's root directory or set them directly in your shell.
   - If you’re using Twilio, you’ll need your Twilio Account SID, Auth Token, and a Twilio-enabled WhatsApp phone number (e.g., from your Twilio WhatsApp Sandbox):
     ```bash
     TWILIO_ACCOUNT_SID=your_account_sid
     TWILIO_AUTH_TOKEN=your_auth_token
     TWILIO_NUMBER=your_twilio_number(e.g.-whatsapp:+1234567890)
     ```
   - Use these environment variables in your Django settings or wherever your application references Twilio credentials.

5. **Apply Migrations**
   ```bash
   python manage.py migrate
   ```
   This step ensures your database schema is up to date. By default, this repository uses `db.sqlite3`.

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```
   Your local development server will start at http://127.0.0.1:8000, and the application will be ready to handle WhatsApp messages once your messaging webhook is configured to reach your local or deployed endpoint.

## Setting Up Twilio WhatsApp Sandbox

1. **Sign Up or Log In**  
   Go to the [Twilio website](https://www.twilio.com/) to create an account or log in.

2. **Create a WhatsApp Sandbox (or Use a Purchased Number)**  
   - In the Twilio console, find the “Messaging” section and configure a WhatsApp sandbox or use a purchased Twilio number with WhatsApp capabilities.  
   - Follow Twilio’s setup instructions to verify and connect your phone with the WhatsApp sandbox.

3. **Configure Webhook**  
   - Under your Twilio console “Sandbox Configuration” or phone number settings, set the “Webhook URL” to point to your server’s endpoint that handles inbound WhatsApp requests.  

4. **Use ngrok for Local Development**
   - For local development, you can use **ngrok** to create a public URL that forwards to your local machine.
   - Install ngrok from [ngrok.com](https://ngrok.com/) and run a command such as `ngrok http 8000` to expose your local server at http://127.0.0.1:8000.

5. **Update `.env` with Twilio Credentials**
   - Copy the Account SID and Auth Token from Twilio, along with the WhatsApp number, into your `.env` file or environment variables as shown above.

6. **Restart Your Django Server**
   - Once your credentials are set and your webhook is configured, restart your local server for changes to take effect. Test sending messages to your Twilio WhatsApp number to confirm everything works correctly.

## Usage
1. **Webhook Configuration**  
   - If you use Twilio, ensure your sandbox phone number or purchased phone number callback URL (or the **ngrok** forwarding URL if developing locally) points to your local or deployed server endpoint for incoming WhatsApp messages.

2. **Messaging Logic**  
   - By default, the bot may respond with basic text replies or logs to the console. Customize your message handlers as needed for additional features.
