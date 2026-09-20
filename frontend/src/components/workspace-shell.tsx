"use client";

import { usePathname } from "next/navigation";
import type { ReactNode } from "react";

import { AppSidebar } from "@/components/app-sidebar";
import { SiteFooter } from "@/components/site-footer";

const publicRoutes = new Set([
  "/",
  "/about",
  "/how-it-works",
  "/diet-plans",
  "/login",
  "/register",
  "/admin/login",
]);

export function WorkspaceShell({ children }: { children: ReactNode }) {
  const pathname = usePathname();

  if (publicRoutes.has(pathname)) {
    return (
      <div className="min-h-screen bg-[#06070a]">
        {children}
        <SiteFooter />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#06070a] lg:flex">
      <AppSidebar />
      <div className="flex min-w-0 flex-1 flex-col">
        <div className="min-h-screen flex-1">{children}</div>
        <SiteFooter />
      </div>
    </div>
  );
}
