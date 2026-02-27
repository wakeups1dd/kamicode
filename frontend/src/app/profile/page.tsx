"use client";

import React from 'react';
import {
    Trophy,
    Zap,
    Calendar,
    MapPin,
    Link as LinkIcon,
    Twitter,
    Github,
    Award,
    Layers,
    History,
    TrendingUp,
    Share2,
    ExternalLink
} from 'lucide-react';

export default function ProfilePage() {
    return (
        <div className="max-w-6xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
            {/* Profile Header Card */}
            <div className="relative overflow-hidden rounded-[40px] bg-slate-900 border border-white/5 p-8 md:p-12">
                <div className="relative z-10 flex flex-col md:flex-row items-center md:items-start gap-10">
                    {/* Avatar & Badge */}
                    <div className="relative">
                        <div className="w-40 h-40 rounded-[2rem] bg-slate-800 border-4 border-slate-950 shadow-2xl overflow-hidden relative group">
                            <div className="absolute inset-0 bg-gradient-to-tr from-brand-primary/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
                            <div className="w-full h-full flex items-center justify-center text-4xl font-black text-slate-500">K</div>
                        </div>
                        <div className="absolute -bottom-4 -right-4 w-16 h-16 rounded-2xl bg-slate-900 border-4 border-slate-950 flex items-center justify-center shadow-xl rotate-12">
                            <Trophy className="w-8 h-8 text-yellow-500 drop-shadow-[0_0_8px_rgba(234,179,8,0.4)]" />
                        </div>
                    </div>

                    {/* Info */}
                    <div className="flex-1 space-y-6 text-center md:text-left">
                        <div className="space-y-1">
                            <div className="flex flex-wrap items-center justify-center md:justify-start gap-3">
                                <h1 className="text-4xl font-extrabold tracking-tight italic">Kami<span className="gradient-text">Master</span></h1>
                                <span className="px-3 py-1 rounded-lg bg-brand-primary/10 border border-brand-primary/20 text-brand-primary text-[10px] font-black uppercase tracking-[0.2em]">Grandmaster</span>
                            </div>
                            <p className="text-slate-400 font-medium">AI-Native Architect & Competitive Programmer</p>
                        </div>

                        <div className="flex flex-wrap items-center justify-center md:justify-start gap-6 text-sm text-slate-500 font-medium">
                            <div className="flex items-center gap-2"><MapPin className="w-4 h-4" /> San Francisco, CA</div>
                            <div className="flex items-center gap-2 font-bold text-slate-400 cursor-pointer hover:text-white transition-colors">
                                <LinkIcon className="w-4 h-4 text-slate-600" /> kamicode.ai
                            </div>
                            <div className="flex items-center gap-2"><Calendar className="w-4 h-4 mt-[-2px]" /> Joined Jan 2024</div>
                        </div>

                        <div className="flex flex-wrap items-center justify-center md:justify-start gap-3 pt-2">
                            <button className="px-6 py-2.5 bg-brand-primary text-white font-bold rounded-xl hover:scale-105 transition-all shadow-lg shadow-brand-primary/20">Edit Profile</button>
                            <button className="p-2.5 rounded-xl bg-white/5 border border-white/10 text-slate-400 hover:text-white transition-colors"><Share2 className="w-5 h-5" /></button>
                            <button className="p-2.5 rounded-xl bg-white/5 border border-white/10 text-slate-400 hover:text-white transition-colors"><Twitter className="w-5 h-5" /></button>
                            <button className="p-2.5 rounded-xl bg-white/5 border border-white/10 text-slate-400 hover:text-white transition-colors"><Github className="w-5 h-5" /></button>
                        </div>
                    </div>

                    {/* Stats Column */}
                    <div className="w-full md:w-64 grid grid-cols-2 gap-3">
                        <div className="p-4 rounded-2xl glass border-white/5 text-center">
                            <div className="text-2xl font-black italic">2,845</div>
                            <div className="text-[10px] text-slate-500 uppercase font-black tracking-widest">Classical</div>
                        </div>
                        <div className="p-4 rounded-2xl glass border-white/5 text-center">
                            <div className="text-2xl font-black italic">2,150</div>
                            <div className="text-[10px] text-slate-500 uppercase font-black tracking-widest">Blitz</div>
                        </div>
                        <div className="p-4 rounded-2xl glass border-white/5 text-center">
                            <div className="text-2xl font-black text-brand-accent italic">98%</div>
                            <div className="text-[10px] text-slate-500 uppercase font-black tracking-widest">Accuracy</div>
                        </div>
                        <div className="p-4 rounded-2xl glass border-white/5 text-center">
                            <div className="text-2xl font-black text-orange-500 italic">42</div>
                            <div className="text-[10px] text-slate-500 uppercase font-black tracking-widest">Streak</div>
                        </div>
                    </div>
                </div>

                {/* Decorative elements */}
                <div className="absolute top-0 right-0 w-96 h-96 bg-brand-primary/5 rounded-full blur-[120px] -mr-48 -mt-48" />
                <div className="absolute bottom-0 left-0 w-64 h-64 bg-brand-secondary/5 rounded-full blur-[100px] -ml-32 -mb-32" />
            </div>

            {/* Main Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Left: Achievements & Gallery */}
                <div className="lg:col-span-2 space-y-8">
                    <div className="flex items-center justify-between">
                        <h2 className="text-2xl font-bold flex items-center gap-3">
                            <Award className="w-6 h-6 text-brand-primary" /> Credentials <span className="text-slate-500 text-sm font-medium">12 Minted</span>
                        </h2>
                        <button className="text-sm font-bold text-brand-primary hover:underline">View on BaseScan</button>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                        {[1, 2, 3, 4].map((i) => (
                            <div key={i} className="group relative glass rounded-3xl border-white/5 p-4 hover:border-brand-primary/40 transition-all cursor-pointer overflow-hidden">
                                <div className="aspect-square rounded-2xl bg-gradient-to-br from-slate-800 to-slate-950 p-6 flex flex-col items-center justify-center text-center space-y-4 mb-4 relative overflow-hidden">
                                    <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')] opacity-10" />
                                    <div className="relative z-10 w-20 h-20 bg-brand-primary/10 rounded-full flex items-center justify-center border border-brand-primary/20 shadow-inner">
                                        <Trophy className="w-10 h-10 text-brand-primary animate-pulse" />
                                    </div>
                                    <div className="relative z-10">
                                        <div className="text-xs font-black text-brand-primary uppercase tracking-[0.3em] mb-1">Elite Solver</div>
                                        <div className="text-lg font-black italic leading-tight">First Solver<br />Day 42</div>
                                    </div>
                                </div>
                                <div className="space-y-1 px-1 flex items-center justify-between">
                                    <div>
                                        <h4 className="font-bold text-sm">Season 3 Champion</h4>
                                        <p className="text-[10px] text-slate-500 font-medium">Minted 2 days ago</p>
                                    </div>
                                    <ExternalLink className="w-4 h-4 text-slate-700 group-hover:text-brand-primary transition-colors" />
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Right: Detailed Stats & Activity */}
                <div className="space-y-8">
                    <h2 className="text-2xl font-bold flex items-center gap-3">
                        <History className="w-6 h-6 text-brand-secondary" /> Statistics
                    </h2>
                    <div className="glass rounded-[32px] border-white/5 p-6 space-y-6">
                        <div className="space-y-2">
                            <div className="flex items-center justify-between text-xs font-black uppercase tracking-widest text-slate-500">
                                <span>Rating Evolution</span>
                                <TrendingUp className="w-3 h-3 text-brand-accent" />
                            </div>
                            <div className="h-40 w-full bg-black/20 rounded-2xl border border-white/5 flex items-center justify-center">
                                <span className="text-xs italic text-slate-600 font-medium font-mono text-center px-8">Chart visualization placeholder (Glicko-2 ratings over time)</span>
                            </div>
                        </div>

                        <div className="space-y-4 pt-2">
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-3">
                                    <div className="w-10 h-10 rounded-xl bg-brand-secondary/10 flex items-center justify-center text-brand-secondary">
                                        <Zap className="w-5 h-5" />
                                    </div>
                                    <div>
                                        <div className="text-xs font-bold text-slate-500 uppercase tracking-tighter">Blitz High</div>
                                        <div className="font-black text-lg italic">2,420</div>
                                    </div>
                                </div>
                                <div className="w-8 h-8 rounded-full border border-white/10 flex items-center justify-center text-[10px] font-black italic">TOP 1%</div>
                            </div>

                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-3">
                                    <div className="w-10 h-10 rounded-xl bg-orange-500/10 flex items-center justify-center text-orange-500">
                                        <Layers className="w-5 h-5" />
                                    </div>
                                    <div>
                                        <div className="text-xs font-bold text-slate-500 uppercase tracking-tighter">Problems Solved</div>
                                        <div className="font-black text-lg italic">142</div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="pt-4 border-t border-white/5">
                            <h4 className="text-[10px] font-black uppercase tracking-[0.2em] text-slate-600 mb-4 text-center">Language Distribution</h4>
                            <div className="flex gap-2">
                                <div className="h-2 bg-brand-primary rounded-full" style={{ width: '70%' }} />
                                <div className="h-2 bg-brand-secondary rounded-full" style={{ width: '20%' }} />
                                <div className="h-2 bg-slate-700 rounded-full" style={{ width: '10%' }} />
                            </div>
                            <div className="flex justify-between mt-3 text-[10px] font-bold text-slate-500 px-1">
                                <span className="flex items-center gap-1.5"><div className="w-2 h-2 rounded-full bg-brand-primary" /> Python</span>
                                <span className="flex items-center gap-1.5"><div className="w-2 h-2 rounded-full bg-brand-secondary" /> JS</span>
                                <span className="flex items-center gap-1.5"><div className="w-2 h-2 rounded-full bg-slate-700" /> C++</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
