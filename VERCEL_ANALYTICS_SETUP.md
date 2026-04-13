# Vercel Web Analytics Setup Guide

This guide explains how to enable and configure Vercel Web Analytics for this Streamlit application.

## Overview

Vercel Web Analytics has been integrated into this Streamlit app using the HTML5/vanilla JavaScript implementation method. Since this is a Python application (not a JavaScript framework), we use Streamlit's HTML injection capabilities to add the analytics tracking script.

## Prerequisites

- Vercel account (free tier works)
- Project deployed to Vercel
- Access to Vercel dashboard

## Step-by-Step Setup Instructions

### 1. Enable Web Analytics in Vercel Dashboard

1. Deploy your Streamlit app to Vercel (if not already deployed)
2. Go to [Vercel Dashboard](https://vercel.com/dashboard)
3. Select your project
4. Navigate to the **Analytics** tab in the project menu
5. Click the **"Enable Web Analytics"** button
6. Vercel will add analytics routes to your deployment

### 2. Find Your Unique Analytics Path

After enabling analytics and redeploying:

1. Visit your deployed Streamlit app
2. Open Browser Developer Tools (press `F12` or right-click → Inspect)
3. Go to the **Network** tab
4. Refresh the page
5. Look for requests to paths containing `/_vercel/insights/`
6. The full path will look like: `/_vercel/insights/abcd1234/script.js`
7. Copy the unique ID part (e.g., `insights/abcd1234`)

**Alternative method:**
- Check the HTML source of your deployed app
- Look for `<script>` tags with `/_vercel/` paths

### 3. Configure the Analytics ID

1. Open `vercel_analytics_config.py` in your project
2. Find the line: `VERCEL_ANALYTICS_ID = None`
3. Update it with your unique path:
   ```python
   VERCEL_ANALYTICS_ID = "insights/abcd1234"  # Replace with your actual ID
   ```
4. Save the file

### 4. Deploy the Updated Configuration

```bash
# Commit your changes
git add vercel_analytics_config.py
git commit -m "Configure Vercel Analytics ID"

# Push to trigger redeployment
git push
```

Or use Vercel CLI:
```bash
vercel deploy --prod
```

### 5. Verify Analytics is Working

1. Visit your deployed app
2. Open Browser DevTools → Network tab
3. Look for successful requests to:
   - `/_vercel/insights/<your-id>/script.js` (should return 200 OK)
   - `/_vercel/insights/<your-id>/view` (analytics data being sent)
4. Check your Vercel dashboard after a few hours/days for visitor data

## Configuration Options

### Enable/Disable Analytics

In `vercel_analytics_config.py`:

```python
# Disable analytics (useful for local development)
ENABLE_ANALYTICS = False

# Enable analytics (for production)
ENABLE_ANALYTICS = True
```

### Local Development

By default, analytics won't activate locally if `VERCEL_ANALYTICS_ID` is not set. This prevents test traffic from being tracked.

## Troubleshooting

### Analytics not showing data

- **Wait time**: Analytics data can take 24-48 hours to appear in the dashboard
- **Check requests**: Verify analytics requests are successful (200 status) in Network tab
- **Verify ID**: Double-check your `VERCEL_ANALYTICS_ID` matches the actual path

### Script not loading

- **Path format**: Ensure the ID format is correct (e.g., `insights/abcd1234`, not `/_vercel/insights/abcd1234`)
- **Redeploy**: After updating the config, make sure you've redeployed
- **Check console**: Look for JavaScript errors in the browser console

### 404 errors on analytics endpoints

- **Enable first**: Make sure Web Analytics is enabled in Vercel dashboard
- **Redeploy**: You must redeploy after enabling for routes to be added
- **Correct ID**: Verify you're using the correct unique path for your project

## How It Works

### Implementation Details

1. **Configuration** (`vercel_analytics_config.py`):
   - Stores your unique analytics ID
   - Provides enable/disable toggle
   - Generates the HTML script injection

2. **Integration** (`app.py`):
   - Imports the analytics configuration
   - Injects the script using `st.components.v1.html()`
   - Script runs in the browser to track page views

3. **Analytics Script**:
   ```html
   <script>
     window.va = window.va || function () { (window.vaq = window.vaq || []).push(arguments); };
   </script>
   <script defer src="/_vercel/insights/{YOUR_ID}/script.js"></script>
   ```

### What Gets Tracked

Vercel Web Analytics tracks:
- Page views
- Unique visitors
- Referrer sources
- Geographic location (country)
- Device type (desktop/mobile)

**Privacy-friendly**: No cookies, no personal data, no tracking across sites.

## Additional Resources

- [Vercel Analytics Documentation](https://vercel.com/docs/analytics)
- [Vercel Analytics Quickstart](https://vercel.com/docs/analytics/quickstart)
- [Streamlit Documentation](https://docs.streamlit.io/)

## Support

If you encounter issues:
1. Check the [Vercel Status Page](https://www.vercel-status.com/)
2. Review the [Vercel Community](https://github.com/vercel/vercel/discussions)
3. Contact Vercel Support through your dashboard

---

**Note**: This implementation uses the HTML5 method since `@vercel/analytics` npm package is designed for JavaScript frameworks and not compatible with Python/Streamlit applications.
