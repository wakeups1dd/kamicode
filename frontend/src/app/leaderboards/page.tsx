"use client";

import React, { useState, useEffect } from 'react';
import {
    Trophy,
    ChevronRight,
    Search,
    Filter,
    Medal,
    TrendingUp,
    Zap,
    Globe
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { api } from '@/services/api';

export interface Leader {
    rank?: number;
    name: string;
    rating: number;
    tier: string;
    winrate: string;
    active: boolean;
    [key: string]: unknown;
}

export default function LeaderboardsPage() {
    const [activeTab, setActiveTab] = useState<'classical' | 'blitz'>('classical');
    const [leaders, setLeaders] = useState<Leader[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        async function fetchLeaders() {
            setIsLoading(true);
            try {
                // Hypothetical rankings endpoint
                const data = await api.get<Leader[]>(`/users/rankings?mode=${activeTab}`);
                setLeaders(data);
            } catch {
                // Fallback to static mock if API fails
                setLeaders([
                    { rank: 1, name: 'CryptoWizard', rating: 2845, tier: 'GM', winrate: '78%', active: true },
                    { rank: 2, name: 'AliceCode', rating: 2790, tier: 'GM', winrate: '74%', active: true },
                    { rank: 3, name: 'BitMaster', rating: 2755, tier: 'GM', winrate: '72%', active: false },
                    { rank: 4, name: 'ZeroDay', rating: 2610, tier: 'Diamond', winrate: '68%', active: true },
                    { rank: 5, name: 'AlgoFlow', rating: 2585, tier: 'Diamond', winrate: '65%', active: true },
                ]);
            } finally {
                setIsLoading(false);
            }
        }
        fetchLeaders();
    }, [activeTab]);

    return (
        <div className="max-w-6xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
            {/* Header */}
            <div className="flex flex-col md:flex-row md:items-end justify-between gap-6">
                <div className="space-y-2">
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-primary/10 border border-brand-primary/20 text-brand-primary text-xs font-bold uppercase tracking-wider">
                        <Globe className="w-3 h-3" /> Global Rankings
                    </div>
                    <h1 className="text-4xl font-extrabold tracking-tight italic">Hall of <span className="gradient-text">Fame</span></h1>
                    <p className="text-slate-400">The world&apos;s most efficient problem solvers, ranked by merit.</p>
                </div>

                <div className="flex bg-slate-900/50 p-1.5 rounded-2xl border border-white/5">
                    <button
                        onClick={() => setActiveTab('classical')}
                        className={cn(
                            "flex items-center gap-2 px-6 py-2.5 rounded-xl font-bold text-sm transition-all",
                            activeTab === 'classical' ? "bg-brand-primary text-white shadow-lg shadow-brand-primary/20" : "text-slate-400 hover:text-slate-200"
                        )}
                    >
                        <Trophy className="w-4 h-4" /> Classical
                    </button>
                    <button
                        onClick={() => setActiveTab('blitz')}
                        className={cn(
                            "flex items-center gap-2 px-6 py-2.5 rounded-xl font-bold text-sm transition-all",
                            activeTab === 'blitz' ? "bg-brand-secondary text-white shadow-lg shadow-brand-secondary/20" : "text-slate-400 hover:text-slate-200"
                        )}
                    >
                        <Zap className="w-4 h-4" /> Blitz
                    </button>
                </div>
            </div>

            {/* Podium (Top 3) */}
            {!isLoading && leaders.length >= 3 && (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-end">
                    {/* Silver - Rank 2 */}
                    <div className="glass rounded-[32px] p-8 border-white/5 bg-slate-900/40 text-center space-y-4 order-2 md:order-1 scale-95 opacity-80">
                        <div className="relative inline-block">
                            <div className="w-20 h-20 rounded-full bg-slate-800 mx-auto border-4 border-slate-400/20" />
                            <div className="absolute -bottom-2 -right-2 w-8 h-8 rounded-full bg-slate-400 text-slate-900 font-bold flex items-center justify-center border-4 border-slate-900">2</div>
                        </div>
                        <div>
                            <h3 className="font-bold text-lg">{leaders[1].name}</h3>
                            <p className="text-slate-500 text-xs font-bold uppercase tracking-widest">{leaders[1].tier} Tier</p>
                        </div>
                        <div className="text-2xl font-black text-slate-300 italic">{leaders[1].rating}</div>
                    </div>

                    {/* Gold - Rank 1 */}
                    <div className="glass rounded-[40px] p-10 border-brand-primary/20 bg-slate-900/60 text-center space-y-6 order-1 md:order-2 shadow-2xl shadow-brand-primary/10 relative overflow-hidden">
                        <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-right from-brand-primary to-brand-secondary" />
                        <div className="relative inline-block">
                            <div className="w-28 h-28 rounded-full bg-slate-800 mx-auto border-4 border-brand-primary/30" />
                            <div className="absolute -bottom-2 -right-2 w-10 h-10 rounded-full bg-brand-primary text-white font-bold flex items-center justify-center border-4 border-slate-900">1</div>
                        </div>
                        <div>
                            <div className="flex items-center justify-center gap-2 text-brand-primary mb-1">
                                <Medal className="w-4 h-4" />
                                <span className="text-[10px] font-black uppercase tracking-[0.2em]">Grandmaster</span>
                            </div>
                            <h3 className="font-black text-2xl">{leaders[0].name}</h3>
                        </div>
                        <div className="text-4xl font-black gradient-text italic">{leaders[0].rating}</div>
                    </div>

                    {/* Bronze - Rank 3 */}
                    <div className="glass rounded-[32px] p-8 border-white/5 bg-slate-900/40 text-center space-y-4 order-3 scale-95 opacity-80">
                        <div className="relative inline-block">
                            <div className="w-20 h-20 rounded-full bg-slate-800 mx-auto border-4 border-orange-700/20" />
                            <div className="absolute -bottom-2 -right-2 w-8 h-8 rounded-full bg-orange-700 text-white font-bold flex items-center justify-center border-4 border-slate-900">3</div>
                        </div>
                        <div>
                            <h3 className="font-bold text-lg">{leaders[2].name}</h3>
                            <p className="text-slate-500 text-xs font-bold uppercase tracking-widest">{leaders[2].tier} Tier</p>
                        </div>
                        <div className="text-2xl font-black text-orange-400 italic">{leaders[2].rating}</div>
                    </div>
                </div>
            )}

            {/* Main Table */}
            <div className="glass rounded-[32px] border-white/5 overflow-hidden">
                <div className="p-6 border-b border-white/5 flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div className="relative flex-1 max-w-md">
                        <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                        <input
                            type="text"
                            placeholder="Search solvers..."
                            className="w-full bg-white/5 border-white/10 rounded-xl pl-12 pr-4 py-2.5 text-sm outline-none focus:ring-1 ring-brand-primary border-transparent transition-all"
                        />
                    </div>
                    <div className="flex items-center gap-2">
                        <button className="flex items-center gap-2 px-4 py-2.5 rounded-xl border border-white/10 text-sm font-medium text-slate-400 hover:bg-white/5 hover:text-white transition-all">
                            <Filter className="w-4 h-4" /> All Tiers
                        </button>
                    </div>
                </div>

                <div className="overflow-x-auto">
                    <table className="w-full text-left">
                        <thead>
                            <tr className="text-[10px] font-black uppercase tracking-widest text-slate-500 border-b border-white/5">
                                <th className="px-8 py-4">Rank</th>
                                <th className="px-8 py-4">User</th>
                                <th className="px-8 py-4 text-right">Rating</th>
                                <th className="px-8 py-4 text-right">Tier</th>
                                <th className="px-8 py-4 text-right">Win Rate</th>
                                <th className="px-8 py-4"></th>
                            </tr>
                        </thead>
                        <tbody>
                            {isLoading ? (
                                [...Array(5)].map((_, i) => (
                                    <tr key={i} className="animate-pulse">
                                        <td colSpan={6} className="px-8 py-6 h-16 bg-white/[0.01]" />
                                    </tr>
                                ))
                            ) : leaders.map((user, idx) => (
                                <tr key={user.rank || idx} className="group hover:bg-white/[0.02] transition-colors border-b border-white/5 last:border-0 cursor-pointer">
                                    <td className="px-8 py-6">
                                        <span className={cn(
                                            "font-black italic text-lg",
                                            (user.rank || idx + 1) <= 3 ? "gradient-text" : "text-slate-500"
                                        )}>
                                            #{user.rank || idx + 1}
                                        </span>
                                    </td>
                                    <td className="px-8 py-6">
                                        <div className="flex items-center gap-4">
                                            <div className="w-10 h-10 rounded-xl bg-slate-800 border border-white/5 relative overflow-hidden flex items-center justify-center">
                                                {user.active && <div className="absolute top-0 right-0 w-2.5 h-2.5 bg-brand-accent border-2 border-slate-900 rounded-full" />}
                                                <span className="text-xs font-bold text-slate-500">{user.name[0]}</span>
                                            </div>
                                            <div>
                                                <div className="font-bold text-slate-200 group-hover:text-brand-primary transition-colors">{user.name}</div>
                                                <div className="text-[10px] font-bold text-slate-600 flex items-center gap-1 uppercase tracking-tighter">
                                                    <TrendingUp className="w-3 h-3 text-brand-accent" /> +12 this week
                                                </div>
                                            </div>
                                        </div>
                                    </td>
                                    <td className="px-8 py-6 text-right">
                                        <div className="font-black text-slate-200">{user.rating}</div>
                                    </td>
                                    <td className="px-8 py-6 text-right">
                                        <span className={cn(
                                            "text-[10px] font-black uppercase px-2 py-1 rounded-md border",
                                            user.tier === 'GM' ? "border-brand-primary/40 text-brand-primary bg-brand-primary/10" : "border-slate-700 text-slate-500 bg-slate-800/50"
                                        )}>
                                            {user.tier}
                                        </span>
                                    </td>
                                    <td className="px-8 py-6 text-right">
                                        <div className="text-sm font-medium text-slate-400">{user.winrate}</div>
                                    </td>
                                    <td className="px-8 py-6 text-right">
                                        <ChevronRight className="w-4 h-4 text-slate-700 group-hover:text-slate-400 transition-colors ml-auto" />
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                <div className="p-6 border-t border-white/5 flex items-center justify-center">
                    <button className="text-sm font-bold text-slate-500 hover:text-brand-primary transition-colors uppercase tracking-widest">
                        Load More Rankings
                    </button>
                </div>
            </div>
        </div>
    );
}
