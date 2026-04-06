"use client";

import { usePathname } from "next/navigation";
import Link from "next/link";
import { getInitials } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Bell,
  Menu,
  User,
  CreditCard,
  LogOut,
  ChevronRight,
} from "lucide-react";

const PAGE_TITLES: Record<string, string> = {
  "/tableau-de-bord": "Tableau de bord",
  "/rapports": "Rapports",
  "/alertes": "Alertes",
  "/donnees": "Donnees",
  "/parametres": "Parametres",
  "/parametres/profil": "Mon profil",
  "/parametres/facturation": "Facturation",
  "/donnees/upload": "Importer des donnees",
};

interface TopbarProps {
  onMenuClick: () => void;
  userName?: string;
  notificationCount?: number;
  onSignOut?: () => void;
}

export function Topbar({
  onMenuClick,
  userName = "Mohammed Alami",
  notificationCount = 3,
  onSignOut,
}: TopbarProps) {
  const pathname = usePathname();

  // Build breadcrumb
  const segments = pathname.split("/").filter(Boolean);
  const breadcrumbs = segments.map((_, index) => {
    const path = "/" + segments.slice(0, index + 1).join("/");
    return {
      label: PAGE_TITLES[path] || segments[index],
      href: path,
    };
  });

  return (
    <header className="sticky top-0 z-30 flex h-16 items-center gap-4 border-b border-border bg-white/80 backdrop-blur-md px-4 lg:px-6">
      {/* Mobile menu button */}
      <Button
        variant="ghost"
        size="icon"
        className="lg:hidden"
        onClick={onMenuClick}
      >
        <Menu className="h-5 w-5" />
      </Button>

      {/* Breadcrumb */}
      <nav className="flex items-center gap-1.5 text-sm">
        {breadcrumbs.map((crumb, index) => (
          <div key={crumb.href} className="flex items-center gap-1.5">
            {index > 0 && (
              <ChevronRight className="h-3.5 w-3.5 text-ink-3" />
            )}
            {index === breadcrumbs.length - 1 ? (
              <span className="font-semibold text-ink">{crumb.label}</span>
            ) : (
              <Link
                href={crumb.href}
                className="text-ink-3 hover:text-ink transition-colors"
              >
                {crumb.label}
              </Link>
            )}
          </div>
        ))}
      </nav>

      <div className="ml-auto flex items-center gap-2">
        {/* Notifications */}
        <Link href="/alertes" className="relative">
          <Button variant="ghost" size="icon">
            <Bell className="h-5 w-5 text-ink-3" />
          </Button>
          {notificationCount > 0 && (
            <Badge className="absolute -right-0.5 -top-0.5 flex h-5 w-5 items-center justify-center rounded-full bg-red-500 p-0 text-[10px] text-white border-2 border-white">
              {notificationCount}
            </Badge>
          )}
        </Link>

        {/* User menu (mobile / desktop fallback) */}
        <DropdownMenu>
          <DropdownMenuTrigger
            render={
              <button
                type="button"
                className="flex h-9 w-9 items-center justify-center rounded-full bg-blue-100 text-sm font-semibold text-blue-700 hover:bg-blue-200 transition-colors lg:hidden"
              />
            }
          >
            {getInitials(userName)}
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" className="w-56">
            <DropdownMenuItem
              render={<Link href="/parametres/profil" />}
              className="cursor-pointer"
            >
              <User className="mr-2 h-4 w-4" />
              Mon profil
            </DropdownMenuItem>
            <DropdownMenuItem
              render={<Link href="/parametres/facturation" />}
              className="cursor-pointer"
            >
              <CreditCard className="mr-2 h-4 w-4" />
              Facturation
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem
              onClick={onSignOut}
              className="text-red-600 cursor-pointer"
            >
              <LogOut className="mr-2 h-4 w-4" />
              Se deconnecter
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </header>
  );
}
