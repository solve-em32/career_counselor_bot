"""
Vercel Web Analytics Configuration
===================================

To enable Vercel Web Analytics:

1. Deploy this Streamlit app to Vercel
2. Go to your Vercel dashboard -> Project -> Analytics
3. Click "Enable Web Analytics"
4. After deployment, Vercel will generate a unique analytics path
5. Update the VERCEL_ANALYTICS_ID below with your unique path

The unique path will look something like: "/_vercel/insights/abcd1234"
You can find it in the Network tab of your browser after enabling analytics,
or in the Vercel dashboard under Analytics settings.
"""

# ── Configuration ──────────────────────────────────────────────────────────────
# Set this to your Vercel Analytics unique path after enabling it in the dashboard
# Example: "insights/abcd1234" (without the leading /_vercel/)
VERCEL_ANALYTICS_ID = None  # Set to your analytics ID, e.g., "insights/abcd1234"

# Enable/disable analytics (useful for local development)
ENABLE_ANALYTICS = True


def get_analytics_script():
    """
    Generate the Vercel Web Analytics script injection HTML.
    
    Returns:
        str: HTML script tags for Vercel Analytics, or empty string if not configured
    """
    if not ENABLE_ANALYTICS or not VERCEL_ANALYTICS_ID:
        return ""
    
    return f"""
    <script>
      window.va = window.va || function () {{ (window.vaq = window.vaq || []).push(arguments); }};
    </script>
    <script defer src="/_vercel/{VERCEL_ANALYTICS_ID}/script.js"></script>
    """


def get_setup_instructions():
    """
    Return setup instructions for enabling Vercel Analytics.
    
    Returns:
        str: Instructions for setting up Vercel Analytics
    """
    return """
    📊 Vercel Web Analytics Setup Instructions:
    
    1. Deploy your Streamlit app to Vercel (if not already deployed)
    2. Go to your Vercel dashboard: https://vercel.com/dashboard
    3. Navigate to your project
    4. Click on the "Analytics" tab
    5. Click "Enable Web Analytics"
    6. After the next deployment, open your app in a browser
    7. Open Browser DevTools (F12) → Network tab
    8. Look for a request to "/_vercel/insights/..."
    9. Copy the unique path (e.g., "insights/abcd1234")
    10. Update VERCEL_ANALYTICS_ID in vercel_analytics_config.py
    11. Redeploy your app
    
    Note: Analytics data may take a few days to appear in your dashboard.
    """
