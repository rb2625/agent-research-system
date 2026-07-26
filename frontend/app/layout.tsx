import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Agent Research System",
  description: "An autonomous multi-agent research assistant",
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
