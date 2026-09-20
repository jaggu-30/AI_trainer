import type { Metadata } from "next";

import { WorkspaceShell } from "@/components/workspace-shell";

import "./globals.css";

export const metadata: Metadata = {
  title: "AI Gym & Fitness Assistant",
  description:
    "AI-powered fitness training, nutrition, habit tracking, gym assistance, and analytics.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className="h-full antialiased"
    >
      <body className="min-h-full bg-[#06070a] font-sans text-white">
        <WorkspaceShell>{children}</WorkspaceShell>
      </body>
    </html>
  );
}
