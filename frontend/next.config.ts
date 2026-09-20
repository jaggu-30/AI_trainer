import type { NextConfig } from "next";
import path from "node:path";

const nextConfig: NextConfig = {
  // Keep generated Next output outside OneDrive's occasionally locked .next
  // reparse point so local development and production builds remain reliable.
  distDir: ".next-ai-gym",
  // Use the workspace lockfile when Turbopack resolves project dependencies.
  turbopack: {
    root: path.resolve(process.cwd(), ".."),
  },
};

export default nextConfig;
