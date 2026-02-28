"use client";

import { useState } from 'react';
import { createClient } from '@/lib/supabase/client';
import { useRouter } from 'next/navigation';
import { Zap } from 'lucide-react';

export default function LoginPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isRegistering, setIsRegistering] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const router = useRouter();
    const supabase = createClient();

    const handleAuth = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            if (isRegistering) {
                const { error } = await supabase.auth.signUp({
                    email,
                    password,
                });
                if (error) throw error;
                // Depending on Supabase settings, sign up may require email verification.
                alert('Check your email for the confirmation link or try logging in if auto-confirm is enabled!');
            } else {
                const { error } = await supabase.auth.signInWithPassword({
                    email,
                    password,
                });
                if (error) throw error;
                router.push('/');
                router.refresh();
            }
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col items-center justify-center h-[calc(100vh-100px)]">
            <div className="glass p-8 rounded-3xl border border-white/10 w-full max-w-md bg-slate-900/40 relative overflow-hidden">
                <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-brand-primary/20 rounded-full blur-[80px] pointer-events-none" />

                <div className="relative z-10 text-center space-y-2 mb-8">
                    <div className="w-16 h-16 bg-gradient-to-br from-brand-primary to-brand-secondary rounded-2xl mx-auto flex items-center justify-center shadow-lg shadow-brand-primary/20 mb-4">
                        <Zap className="text-white w-8 h-8 fill-white" />
                    </div>
                    <h1 className="text-2xl font-bold">{isRegistering ? 'Create an Account' : 'Welcome Back'}</h1>
                    <p className="text-slate-400 text-sm">Enter your details to proceed to the arena.</p>
                </div>

                <form onSubmit={handleAuth} className="relative z-10 space-y-4">
                    {error && <div className="p-3 bg-red-500/10 border border-red-500/20 rounded-xl text-red-500 text-sm text-center">{error}</div>}
                    <div className="space-y-2">
                        <label className="text-xs font-bold text-slate-500 uppercase tracking-widest pl-1">Email</label>
                        <input
                            type="email"
                            placeholder="you@example.com"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                            className="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-3 text-slate-200 focus:outline-none focus:border-brand-primary transition-colors"
                        />
                    </div>
                    <div className="space-y-2">
                        <label className="text-xs font-bold text-slate-500 uppercase tracking-widest pl-1">Password</label>
                        <input
                            type="password"
                            placeholder="••••••••"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            className="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-3 text-slate-200 focus:outline-none focus:border-brand-primary transition-colors"
                        />
                    </div>
                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full py-3 bg-brand-primary hover:bg-brand-primary/90 text-white font-bold rounded-xl transition-all hover:scale-[1.02] active:scale-[0.98] mt-6 disabled:opacity-50 disabled:pointer-events-none"
                    >
                        {loading ? 'Processing...' : (isRegistering ? 'Sign Up' : 'Sign In')}
                    </button>
                </form>

                <div className="relative z-10 mt-6 text-center">
                    <button
                        type="button"
                        onClick={() => setIsRegistering(!isRegistering)}
                        className="text-sm text-slate-400 hover:text-white transition-colors"
                    >
                        {isRegistering ? 'Already have an account? Sign in' : "Don't have an account? Sign up"}
                    </button>
                </div>

            </div>
        </div>
    );
}
