# Assets Directory

This directory contains visual assets for the AVIONAV platform.

## Required Assets

### Logo
- **File**: `logo.png`
- **Location**: `frontend/assets/logo.png`
- **Description**: AVIONAV platform logo
- **Recommended Size**: 200x200 pixels
- **Format**: PNG with transparent background

### Banner
- **File**: `banner.jpg`
- **Location**: `frontend/assets/banner.jpg`
- **Description**: Hero banner image for login page
- **Recommended Size**: 1920x1080 pixels
- **Format**: JPG or PNG

## Current Status

Assets are currently using CSS-based styling instead of image files. The platform uses:
- Gradient backgrounds
- CSS-styled text logos
- Emoji icons
- Professional color scheme

## Adding Custom Assets

To add custom assets:

1. Place `logo.png` in this directory
2. Place `banner.jpg` in this directory
3. Update the login page to load these images
4. Update the sidebar to use the custom logo

## Alternative Approach

The current implementation uses CSS gradients and text-based branding, which:
- Loads faster
- Requires no external assets
- Scales better across devices
- Maintains consistent styling

This approach is recommended for production deployment.
