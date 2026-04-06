import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { Toaster } from "@/components/ui/sonner";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: {
    default: "PilotBI - Tableau de bord intelligent pour PME",
    template: "%s | PilotBI",
  },
  description:
    "PilotBI transforme vos donnees en decisions. Tableau de bord BI intelligent concu pour les PME marocaines.",
  keywords: [
    "BI",
    "Business Intelligence",
    "PME",
    "Maroc",
    "tableau de bord",
    "analytics",
  ],
  authors: [{ name: "PilotBI" }],
  icons: {
    icon: "/favicon.ico",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fr" className={`${inter.variable} h-full`}>
      <body className="min-h-full antialiased font-sans">
        {children}
        <Toaster
          position="top-right"
          richColors
          closeButton
          toastOptions={{
            duration: 4000,
          }}
        />
      </body>
    </html>
  );
}
