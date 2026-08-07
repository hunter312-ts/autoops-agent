"""
Evaluation dataset for AutoOps classification.

Each sample contains:
- subject
- body
- expected intent
- expected risk
- expected priority
"""

EVAL_DATASET = [

    # --------------------------------------------------
    # Refund Request
    # --------------------------------------------------

    {
        "subject": "Refund Request",
        "body": "I received a damaged product and would like a refund.",
        "expected": {
            "intent": "Refund Request",
            "risk": "MEDIUM",
            "priority": "MEDIUM",
        },
    },

    {
        "subject": "Wrong Item Delivered",
        "body": "You sent me the wrong product. I want a refund.",
        "expected": {
            "intent": "Refund Request",
            "risk": "MEDIUM",
            "priority": "MEDIUM",
        },
    },

    {
        "subject": "Subscription Refund",
        "body": "I accidentally purchased the annual subscription. Please refund me.",
        "expected": {
            "intent": "Refund Request",
            "risk": "MEDIUM",
            "priority": "MEDIUM",
        },
    },

    # --------------------------------------------------
    # Billing Question
    # --------------------------------------------------

    {
        "subject": "Payment Charged Twice",
        "body": "My credit card has been charged twice for one order.",
        "expected": {
            "intent": "Billing Question",
            "risk": "LOW",
            "priority": "MEDIUM",
        },
    },

    {
        "subject": "Need Invoice",
        "body": "Could you please send me a copy of my invoice?",
        "expected": {
            "intent": "Billing Question",
            "risk": "LOW",
            "priority": "LOW",
        },
    },

    # --------------------------------------------------
    # Account Issue
    # --------------------------------------------------

    {
        "subject": "Forgot Password",
        "body": "I forgot my password and cannot log into my account.",
        "expected": {
            "intent": "Account Issue",
            "risk": "MEDIUM",
            "priority": "HIGH",
        },
    },

    {
        "subject": "Account Locked",
        "body": "My account has been locked after too many login attempts.",
        "expected": {
            "intent": "Account Issue",
            "risk": "MEDIUM",
            "priority": "HIGH",
        },
    },

    # --------------------------------------------------
    # Technical Support
    # --------------------------------------------------

    {
        "subject": "Application Crash",
        "body": "The mobile application crashes every time I open it.",
        "expected": {
            "intent": "Technical Support",
            "risk": "LOW",
            "priority": "HIGH",
        },
    },

    {
        "subject": "Website Error",
        "body": "The checkout page shows a 500 Internal Server Error.",
        "expected": {
            "intent": "Technical Support",
            "risk": "LOW",
            "priority": "HIGH",
        },
    },

    # --------------------------------------------------
    # Complaint
    # --------------------------------------------------

    {
        "subject": "Customer Complaint",
        "body": "Your support team was rude and did not solve my problem.",
        "expected": {
            "intent": "Complaint",
            "risk": "HIGH",
            "priority": "HIGH",
        },
    },

    {
        "subject": "Poor Customer Service",
        "body": "I am extremely disappointed with your customer service.",
        "expected": {
            "intent": "Complaint",
            "risk": "HIGH",
            "priority": "HIGH",
        },
    },

    # --------------------------------------------------
    # Feature Request
    # --------------------------------------------------

    {
        "subject": "Dark Mode",
        "body": "Please add a dark mode to your application.",
        "expected": {
            "intent": "Feature Request",
            "risk": "LOW",
            "priority": "LOW",
        },
    },

    {
        "subject": "Export to PDF",
        "body": "It would be helpful if reports could be exported as PDF files.",
        "expected": {
            "intent": "Feature Request",
            "risk": "LOW",
            "priority": "LOW",
        },
    },

    # --------------------------------------------------
    # Bug Report
    # --------------------------------------------------

    {
        "subject": "Search Button Broken",
        "body": "The search button does nothing when I click it.",
        "expected": {
            "intent": "Bug Report",
            "risk": "LOW",
            "priority": "MEDIUM",
        },
    },

    {
        "subject": "Checkout Freezes",
        "body": "The checkout page freezes after entering payment information.",
        "expected": {
            "intent": "Bug Report",
            "risk": "LOW",
            "priority": "HIGH",
        },
    },

    {
        "subject": "Profile Update Error",
        "body": "Every time I save my profile changes, I receive an error.",
        "expected": {
            "intent": "Bug Report",
            "risk": "LOW",
            "priority": "MEDIUM",
        },
    },

    # --------------------------------------------------
    # General Inquiry
    # --------------------------------------------------

    {
        "subject": "Shipping Question",
        "body": "When will my order arrive?",
        "expected": {
            "intent": "General Inquiry",
            "risk": "LOW",
            "priority": "MEDIUM",
        },
    },

    {
        "subject": "Business Hours",
        "body": "What are your customer support working hours?",
        "expected": {
            "intent": "General Inquiry",
            "risk": "LOW",
            "priority": "LOW",
        },
    },

    {
        "subject": "International Shipping",
        "body": "Do you ship internationally?",
        "expected": {
            "intent": "General Inquiry",
            "risk": "LOW",
            "priority": "LOW",
        },
    },

    {
        "subject": "Warranty Information",
        "body": "How long is the warranty period for this product?",
        "expected": {
            "intent": "General Inquiry",
            "risk": "LOW",
            "priority": "LOW",
        },
    },
]