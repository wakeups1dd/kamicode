import React from 'react';
import Link from 'next/link';
import { Terminal, Bell, User, LogOut } from 'lucide-react';
import { createClient } from '@/lib/supabase/server';

export async function Navbar() {
    const supabase = await createClient();
    const { data: { user } } = await supabase.auth.getUser();

    return (
        <nav className="fixed top-0 left-0 right-0 z-50 glass border-b border-white/10 h-16 px-6 flex items-center justify-between">
            <Link href="/" className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-brand-primary to-brand-secondary flex items-center justify-center">
                    <Terminal className="text-white w-5 h-5" />
                </div>
                <span className="font-bold text-xl tracking-tight gradient-text">KamiCode</span>
            </Link>

            <div className="flex items-center gap-4">
                {user ? (
                    <>
                        <button className="p-2 hover:bg-white/5 rounded-full transition-colors text-slate-400 hover:text-white">
                            <Bell className="w-5 h-5" />
                        </button>
                        <Link href="/profile" className="h-8 w-8 rounded-full bg-slate-800 border border-white/10 flex items-center justify-center cursor-pointer hover:border-brand-primary/50 transition-all">
                            <User className="w-4 h-4 text-slate-400" />
                        </Link>
                        <form action="/auth/signout" method="POST">
                            <button className="p-2 hover:bg-white/5 rounded-full transition-colors text-slate-400 hover:text-red-400" type="submit" title="Sign out">
                                <LogOut className="w-5 h-5" />
                            </button>
                        </form>
                    </>
                ) : (
                    <Link href="/login" className="px-4 py-2 bg-white/10 hover:bg-white/20 text-white font-medium rounded-lg text-sm transition-colors border border-white/5">
                        Sign In
                    </Link>
                )}
            </div>
        </nav>
    );
}

