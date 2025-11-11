# Firebase Authentication Setup Guide

This guide will help you set up Firebase Authentication for the Exam Portal application, including OTP (One-Time Password) verification for phone numbers.

## Prerequisites

- A Google account
- Firebase project created at [Firebase Console](https://console.firebase.google.com/)

## Step 1: Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project"
3. Enter your project name (e.g., "exam-portal")
4. Follow the setup wizard to create your project

## Step 2: Enable Authentication

1. In your Firebase project, go to **Build > Authentication**
2. Click **Get Started**
3. Enable the following sign-in methods:
   - **Email/Password** (for basic authentication)
   - **Phone** (for OTP verification)

## Step 3: Get Firebase Configuration

1. In your Firebase project, go to **Project Settings** (gear icon)
2. Scroll down to **Your apps** section
3. Click the web icon (`</>`) to add a web app
4. Register your app with a nickname (e.g., "Exam Portal Web")
5. Copy the Firebase configuration object

## Step 4: Configure Environment Variables

Create a `.env` file in the project root directory and add the following variables with your Firebase configuration:

```env
# Firebase Configuration
FIREBASE_API_KEY=your-api-key
FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_STORAGE_BUCKET=your-project.appspot.com
FIREBASE_MESSAGING_SENDER_ID=your-sender-id
FIREBASE_APP_ID=your-app-id
FIREBASE_DATABASE_URL=https://your-project.firebaseio.com
```

## Step 5: (Optional) Set Up Firebase Admin SDK

For server-side verification of Firebase tokens:

1. In Firebase Console, go to **Project Settings > Service Accounts**
2. Click **Generate New Private Key**
3. Save the JSON file securely in your project (e.g., `firebase-admin-key.json`)
4. Add the path to your `.env` file:

```env
FIREBASE_ADMIN_CREDENTIAL_PATH=/path/to/firebase-admin-key.json
```

**Important**: Add `firebase-admin-key.json` to your `.gitignore` to prevent committing sensitive credentials.

## Step 6: Configure Phone Authentication

1. In Firebase Console, go to **Authentication > Sign-in method > Phone**
2. Enable phone authentication
3. Add your authorized domains (e.g., `localhost`, `yourdomain.com`)
4. Configure reCAPTCHA settings if needed

## How It Works

### Signup Flow with OTP Verification

1. User enters email, phone number (with country code), and password
2. If Firebase is configured and phone number is provided:
   - Firebase sends an OTP to the user's phone
   - User enters the OTP code
   - Phone number is verified via Firebase
3. User account is created in Django
4. User is automatically logged in and redirected to the dashboard

### Without Firebase Configuration

If Firebase credentials are not configured in the `.env` file:
- Signup works normally without OTP verification
- Users can still create accounts with email and password
- Phone numbers are stored but not verified

## Testing

To test OTP verification locally:

1. Use a phone number with a valid country code (e.g., `+1234567890` for US)
2. Firebase will send an SMS with the verification code
3. Enter the code when prompted

**Note**: Firebase has test phone numbers you can use for development:
- In Firebase Console, go to **Authentication > Sign-in method > Phone**
- Scroll to **Phone numbers for testing**
- Add test phone numbers and verification codes

Example test phone number:
```
Phone: +1234567890
Code: 123456
```

## Troubleshooting

### reCAPTCHA Not Working

If you see reCAPTCHA errors:
1. Make sure your domain is added to Firebase authorized domains
2. Check browser console for specific error messages
3. Try using Firebase test phone numbers

### OTP Not Received

1. Verify the phone number format includes country code (e.g., `+1` for US)
2. Check Firebase Console for quota limits
3. Review Firebase usage and billing settings

### "Firebase is not defined" Error

This error appears when:
- Firebase configuration is not set in `.env`
- Firebase SDK scripts are blocked by browser extensions
- The application will fall back to signup without OTP verification

## Security Best Practices

1. **Never commit** `firebase-admin-key.json` or `.env` files to version control
2. Add appropriate entries to `.gitignore`:
   ```
   .env
   firebase-admin-key.json
   ```
3. Use environment-specific configuration for development, staging, and production
4. Regularly rotate Firebase Admin SDK keys
5. Monitor Firebase Authentication usage and set up alerts for suspicious activity

## Additional Resources

- [Firebase Authentication Documentation](https://firebase.google.com/docs/auth)
- [Phone Authentication](https://firebase.google.com/docs/auth/web/phone-auth)
- [Firebase Security Rules](https://firebase.google.com/docs/rules)
