"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
  LayoutDashboard,
  FileBarChart,
  Bell,
  Database,
  Settings,
} from "lucide-react";

const NAV_ITEMS = [
  { href: "/tableau-de-bord", label: "Dashboard", icon: LayoutDashboard },
  { href: "/rapports", label: "Rapports", icon: FileBarChart },
  { href: "/alertes", label: "Alertes", icon: Bell },
  { href: "/donnees", label: "Donnees", icon: Database },
  { href: "/parametres", label: "Reglages", icon: Settings },
];

export function MobileNav() {
  const pathname = usePathname();

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 border-t border-border bg-white/95 backdrop-blur-md safe-area-bottom lg:hidden">
      <div className="flex items-center justify-around px-2 py-1">
        {NAV_ITEMS.map((item) => {
          const isActive =
            pathname === item.href || pathname.startsWith(item.href + "/");
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex flex-col items-center gap-0.5 rounded-lg px-3 py-2 text-[10px] font-medium transition-colors",
                isActive ? "text-blue-600" : "text-ink-3"
              )}
            >
              <item.icon
                className={cn(
                  "h-5 w-5",
                  isActive ? "text-blue-600" : "text-ink-3"
                )}
              />
              <span>{item.label}</span>
              {isActive && (
                <div className="h-0.5 w-4 rounded-full bg-blue-600" />
              )}
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
