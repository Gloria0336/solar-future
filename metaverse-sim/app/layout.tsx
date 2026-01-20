import "./globals.css";
import type { ReactNode } from "react";

export const metadata = {
  title: "Metaverse Sim UI Test",
  description: "UI integration test for a minimal simulation engine"
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="zh-Hant">
      <body>{children}</body>
    </html>
  );
}
