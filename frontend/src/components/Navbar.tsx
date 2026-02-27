import React from 'react';
import Link from 'next/link';
import { Terminal, Bell, User } from 'lucide-react';

export function Navbar() {
    return (
        <nav className="fixed top-0 left-0 right-0 z-50 glass border-b border-white/10 h-16 px-6 flex items-center justify-between">
            <Link href="/" className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-brand-primary to-brand-secondary flex items-center justify-center">
                    <Terminal className="text-white w-5 h-5" />
                </div>
                <span className="font-bold text-xl tracking-tight gradient-text">KamiCode</span>
            </Link>

            <div className="flex items-center gap-4">
                <button className="p-2 hover:bg-white/5 rounded-full transition-colors text-slate-400 hover:text-white">
                    <Bell className="w-5 h-5" />
                </button>
                <div className="h-8 w-8 rounded-full bg-slate-800 border border-white/10 flex items-center justify-center cursor-pointer hover:border-brand-primary/50 transition-all">
                    <User className="w-4 h-4 text-slate-400" />
                </div>
            </div>
        </nav>
    );
}
