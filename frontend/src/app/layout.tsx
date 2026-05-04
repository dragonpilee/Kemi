import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Kemi | Biochemical Lab Analyzer",
  description: "AI-powered biochemical analysis of lab reports.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
