// Example deployment configuration
// Copy this file to deployment.config.js and update the values as needed

module.exports = {
  // Backend API URL - update this when deploying
  apiUrl: 'http://localhost:8080', // Local development
  // apiUrl: 'https://your-backend-url.onrender.com', // Production

  // Deployment settings
  staticExport: false, // Set to true for static site hosting
  basePath: '', // Set to your repo name if deploying to GitHub Pages
};
