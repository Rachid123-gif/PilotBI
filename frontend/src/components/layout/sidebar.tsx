"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { getInitials } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  LayoutDashboard,
  FileBarChart,
  Bell,
  Database,
  Settings,
  ChevronLeft,
  ChevronRight,
  LogOut,
  User,
  CreditCard,
} from "lucide-react";

const NAV_ITEMS = [
  {
    href: "/tableau-de-bord",
    label: "Tableau de bord",
    icon: LayoutDashboard,
  },
  {
    href: "/rapports",
    label: "Rapports",
    icon: FileBarChart,
  },
  {
    href: "/alertes",
    label: "Alertes",
    icon: Bell,
  },
  {
    href: "/donnees",
    label: "Donnees",
    icon: Database,
  },
  {
    href: "/parametres",
    label: "Parametres",
    icon: Settings,
  },
];

interface SidebarProps {
  collapsed: boolean;
  onToggle: () => void;
  userName?: string;
  userEmail?: string;
  plan?: string;
  onSignOut?: () => void;
}

export function Sidebar({
  collapsed,
  onToggle,
  userName = "Mohammed Alami",
  userEmail = "m.alami@entreprise.ma",
  plan = "starter",
  onSignOut,
}: SidebarProps) {
  const pathname = usePathname();

  return (
    <aside
      className={cn(
        "hidden lg:flex flex-col border-r border-border bg-sidebar h-screen sticky top-0 transition-all duration-300",
        collapsed ? "w-[72px]" : "w-64"
      )}
    >
      {/* Logo */}
      <div className="flex h-16 items-center gap-2.5 border-b border-border px-4">
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-blue-600">
          <svg
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            className="text-white"
          >
            <path
              d="M3 13h4v8H3v-8Zm7-5h4v13h-4V8Zm7-5h4v18h-4V3Z"
              fill="currentColor"
            />
          </svg>
        </div>
        {!collapsed && (
          <span className="text-lg font-bold text-ink tracking-tight">
            PilotBI
          </span>
        )}
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-1 p-3">
        {NAV_ITEMS.map((item) => {
          const isActive =
            pathname === item.href || pathname.startsWith(item.href + "/");
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all duration-200",
                isActive
                  ? "bg-blue-50 text-blue-700 shadow-sm"
                  : "text-ink-3 hover:bg-gray-50 hover:text-ink",
                collapsed && "justify-center px-0"
              )}
              title={collapsed ? item.label : undefined}
            >
              <item.icon
                className={cn(
                  "h-5 w-5 shrink-0",
                  isActive ? "text-blue-600" : "text-ink-3"
                )}
              />
              {!collapsed && <span>{item.label}</span>}
            </Link>
          );
        })}
      </nav>

      {/* Plan badge */}
      {!collapsed && (
        <div className="mx-3 mb-3 rounded-xl bg-gradient-to-r from-blue-50 to-blue-100 p-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-blue-700">Plan actuel</span>
            <Badge
              variant="secondary"
              className="bg-blue-600 text-white text-[10px] hover:bg-blue-700"
            >
              {plan.charAt(0).toUpperCase() + plan.slice(1)}
            </Badge>
          </div>
          <Link
            href="/parametres/facturation"
            className="mt-1.5 block text-xs text-blue-600 hover:text-blue-700 font-medium"
          >
            Mettre a niveau
          </Link>
        </div>
      )}

      {/* Collapse toggle */}
      <button
        type="button"
        onClick={onToggle}
        className="mx-3 mb-2 flex items-center justify-center rounded-lg p-2 text-ink-3 hover:bg-gray-100 transition-colors"
      >
        {collapsed ? (
          <ChevronRight className="h-4 w-4" />
        ) : (
          <ChevronLeft className="h-4 w-4" />
        )}
      </button>

      {/* User section */}
      <div className="border-t border-border p-3">
        <DropdownMenu>
          <DropdownMenuTrigger
            render={
              <button
                type="button"
                className={cn(
                  "flex w-full items-center gap-3 rounded-xl p-2 text-left hover:bg-gray-50 transition-colors",
                  collapsed && "justify-center"
                )}
              />
            }
          >
            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-blue-100 text-sm font-semibold text-blue-700">
              {getInitials(userName)}
            </div>
            {!collapsed && (
              <div className="min-w-0 flex-1">
                <p className="truncate text-sm font-medium text-ink">
                  {userName}
                </p>
                <p className="truncate text-xs text-ink-3">{userEmail}</p>
              </div>
            )}
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
    </aside>
  );
}
