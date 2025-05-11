import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  env: {
    // Default to localhost in development, will be overridden in production
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080',
  },
  // Enable static exports for hosting platforms that support it
  output: process.env.STATIC_EXPORT === 'true' ? 'export' : undefined,
  // Disable image optimization for static exports
  images: process.env.STATIC_EXPORT === 'true' ? { unoptimized: true } : {},
};

export default nextConfig;
