"use client";

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
    LayoutDashboard,
    Code2,
    Zap,
    Trophy,
    UserCircle,
    Settings as SettingsIcon
} from 'lucide-react';
import { cn } from '@/lib/utils';

const navItems = [
    { label: 'Dashboard', icon: LayoutDashboard, href: '/' },
    { label: 'Daily Challenge', icon: Code2, href: '/challenge/daily' },
    { label: 'Rush Mode', icon: Zap, href: '/rush' },
    { label: 'Leaderboards', icon: Trophy, href: '/leaderboards' },
    { label: 'Profile', icon: UserCircle, href: '/profile' },
    { label: 'Settings', icon: SettingsIcon, href: '/settings' },
];

export function Sidebar() {
    const pathname = usePathname();

    return (
        <aside className="fixed left-0 top-16 bottom-0 w-64 glass border-r border-white/10 p-4 hidden md:block">
            <div className="space-y-2">
                {navItems.map((item) => {
                    const isActive = pathname === item.href || (item.href !== '/' && pathname.startsWith(item.href));
                    return (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={cn(
                                "flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group",
                                isActive
                                    ? "bg-brand-primary/10 text-brand-primary shadow-[inset_0_0_20px_rgba(139,92,246,0.05)]"
                                    : "text-slate-400 hover:text-slate-200 hover:bg-white/5"
                            )}
                        >
                            <item.icon className={cn(
                                "w-5 h-5 transition-transform group-hover:scale-110",
                                isActive ? "text-brand-primary" : "text-slate-400"
                            )} />
                            <span className="font-medium">{item.label}</span>
                            {isActive && (
                                <div className="ml-auto w-1.5 h-1.5 rounded-full bg-brand-primary shadow-[0_0_8px_rgba(139,92,246,0.5)]" />
                            )}
                        </Link>
                    );
                })}
            </div>

            <div className="absolute bottom-8 left-4 right-4">
                <div className="p-4 rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-white/5">
                    <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Season 1</h4>
                    <div className="flex items-center justify-between mb-1">
                        <span className="text-sm font-medium text-slate-200">Silver III</span>
                        <span className="text-xs text-brand-primary font-bold">1420 RP</span>
                    </div>
                    <div className="w-full h-1.5 bg-slate-700 rounded-full overflow-hidden">
                        <div className="h-full bg-brand-primary w-2/3" />
                    </div>
                </div>
            </div>
        </aside>
    );
}
