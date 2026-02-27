"use client";

import React, { useState, useEffect } from 'react';
import {
    Zap,
    Heart,
    Timer,
    ChevronRight,
    AlertCircle,
    RefreshCcw,
    ArrowRight
} from 'lucide-react';
import Link from 'next/link';
import { cn } from '@/lib/utils';
import { motion, AnimatePresence } from 'framer-motion';
import { useRushSession } from '@/hooks/useRush';

export default function RushPage() {
    const [gameState, setGameState] = useState<'idle' | 'playing' | 'gameover'>('idle');
    const [timeLeft, setTimeLeft] = useState(180);

    const { startSession, submitAnswer, session, currentPuzzle, isEnding } = useRushSession();

    useEffect(() => {
        let timer: NodeJS.Timeout;
        if (gameState === 'playing' && timeLeft > 0) {
            timer = setInterval(() => setTimeLeft((prev) => prev - 1), 1000);
        } else if (timeLeft === 0 || isEnding || (session && session.lives <= 0)) {
            setTimeout(() => setGameState('gameover'), 0);
        }
        return () => clearInterval(timer);
    }, [gameState, timeLeft, isEnding, session]);

    const formatTime = (seconds: number) => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    };

    const handleStart = async () => {
        const data = await startSession();
        if (data) {
            setGameState('playing');
            setTimeLeft(180);
        }
    };

    const handleAnswer = async (answer: string) => {
        await submitAnswer(answer);
    };

    return (
        <div className="max-w-4xl mx-auto h-[calc(100vh-112px)] flex flex-col justify-center items-center py-8">
            <AnimatePresence mode="wait">
                {gameState === 'idle' && (
                    <motion.div
                        key="idle"
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 1.05 }}
                        className="text-center space-y-8 glass p-12 rounded-[40px] border-white/5 bg-slate-900/40 relative overflow-hidden"
                    >
                        <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-brand-primary/20 rounded-full blur-[80px]" />
                        <div className="relative z-10 space-y-6">
                            <div className="w-20 h-20 bg-gradient-to-br from-brand-primary to-brand-secondary rounded-3xl mx-auto flex items-center justify-center shadow-lg shadow-brand-primary/20 animate-pulse">
                                <Zap className="text-white w-10 h-10 fill-white" />
                            </div>
                            <div className="space-y-2">
                                <h1 className="text-4xl font-extrabold tracking-tight">Rapid <span className="gradient-text">Rush</span></h1>
                                <p className="text-slate-400 max-w-sm mx-auto">Solve as many puzzles as you can in 3 minutes. Speed is weight, and time is the only master.</p>
                            </div>
                            <div className="grid grid-cols-2 gap-4 max-w-sm mx-auto">
                                <div className="bg-white/5 border border-white/10 p-4 rounded-2xl flex flex-col items-center">
                                    <Timer className="w-5 h-5 text-slate-500 mb-1" />
                                    <span className="text-xs font-bold text-slate-500 uppercase tracking-widest">3 Minutes</span>
                                </div>
                                <div className="bg-white/5 border border-white/10 p-4 rounded-2xl flex flex-col items-center">
                                    <Heart className="w-5 h-5 text-slate-500 mb-1" />
                                    <span className="text-xs font-bold text-slate-500 uppercase tracking-widest">3 Lives</span>
                                </div>
                            </div>
                            <button
                                onClick={handleStart}
                                className="w-full py-4 bg-brand-primary hover:bg-brand-primary/90 text-white font-bold rounded-2xl transition-all hover:scale-[1.02] active:scale-[0.98] shadow-lg shadow-brand-primary/30 flex items-center justify-center gap-2 group"
                            >
                                Enter the Arena <ChevronRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                            </button>
                        </div>
                    </motion.div>
                )}

                {gameState === 'playing' && session && currentPuzzle && (
                    <motion.div
                        key="playing"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="w-full h-full flex flex-col gap-6"
                    >
                        {/* Top Bar */}
                        <div className="flex items-center justify-between glass p-4 rounded-2xl border-white/5">
                            <div className="flex items-center gap-6">
                                <div className="flex items-center gap-2">
                                    <Timer className={cn("w-5 h-5", timeLeft < 30 ? "text-red-500 animate-pulse" : "text-brand-primary")} />
                                    <span className={cn("text-2xl font-black tabular-nums font-mono", timeLeft < 30 ? "text-red-500" : "text-slate-100")}>
                                        {formatTime(timeLeft)}
                                    </span>
                                </div>
                                <div className="h-8 w-px bg-white/10" />
                                <div className="flex items-center gap-2 text-red-500">
                                    {[...Array(3)].map((_, i) => (
                                        <Heart key={i} className={cn("w-5 h-5", i >= session.lives && "opacity-20 fill-none text-slate-600")} fill={i < session.lives ? "currentColor" : "none"} />
                                    ))}
                                </div>
                            </div>

                            <div className="flex items-center gap-4 bg-white/5 px-6 py-2 rounded-xl border border-white/5">
                                <span className="text-xs font-bold text-slate-500 uppercase tracking-widest">Streak</span>
                                <span className="text-2xl font-black text-brand-primary italic shadow-brand-primary/20 drop-shadow-lg">{session.streak}</span>
                            </div>
                        </div>

                        {/* Puzzle Content */}
                        <div className="flex-1 flex flex-col gap-6">
                            <div className="flex-1 glass p-10 rounded-[40px] border-white/5 bg-slate-900/40 relative overflow-hidden flex flex-col justify-center">
                                <div className="space-y-8 relative z-10">
                                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-lg bg-brand-primary/10 border border-brand-primary/20 text-brand-primary text-xs font-bold uppercase tracking-widest">
                                        {currentPuzzle.puzzle_type}
                                    </div>
                                    <h2 className="text-2xl font-bold leading-relaxed">
                                        {currentPuzzle.question}
                                    </h2>
                                    {currentPuzzle.snippet && (
                                        <div className="bg-black/40 rounded-3xl p-6 font-mono text-sm leading-8 border border-white/5">
                                            <pre className="text-slate-300">
                                                {currentPuzzle.snippet}
                                            </pre>
                                        </div>
                                    )}

                                    <div className="grid grid-cols-2 gap-4 pt-4">
                                        {currentPuzzle.options.map((option: string, idx: number) => (
                                            <button
                                                key={idx}
                                                onClick={() => handleAnswer(option)}
                                                className="group relative p-6 bg-white/5 hover:bg-white/10 border border-white/10 rounded-2xl text-left transition-all hover:scale-[1.02] active:scale-[0.98] active:bg-brand-primary/20"
                                            >
                                                <div className="flex items-center justify-between">
                                                    <span className="font-mono text-slate-300">{option}</span>
                                                    <div className="w-8 h-8 rounded-lg border border-white/10 flex items-center justify-center text-xs font-bold text-slate-500 group-hover:border-brand-primary/50 group-hover:text-brand-primary transition-colors">
                                                        {String.fromCharCode(65 + idx)}
                                                    </div>
                                                </div>
                                            </button>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </motion.div>
                )}

                {gameState === 'gameover' && (
                    <motion.div
                        key="gameover"
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="text-center space-y-8 glass p-12 rounded-[40px] border-white/5 bg-slate-900/60 w-full max-w-md"
                    >
                        <div className="w-20 h-20 bg-red-500/10 rounded-3xl mx-auto flex items-center justify-center border border-red-500/20">
                            <AlertCircle className="text-red-500 w-10 h-10" />
                        </div>
                        <div className="space-y-2">
                            <h1 className="text-4xl font-black text-white italic">SESSION ENDED</h1>
                            <p className="text-slate-400">The arena demands perfection. You solved {session?.streak || 0} puzzles.</p>
                        </div>

                        <div className="grid grid-cols-2 gap-4 py-4">
                            <div className="p-6 rounded-3xl bg-white/5 border border-white/5">
                                <div className="text-3xl font-black text-brand-primary italic">{session?.streak || 0}</div>
                                <div className="text-[10px] text-slate-500 uppercase font-black tracking-widest mt-1">Final Streak</div>
                            </div>
                            <div className="p-6 rounded-3xl bg-white/5 border border-white/5">
                                <div className="text-3xl font-black text-brand-secondary italic">{session?.points_earned || 0}</div>
                                <div className="text-[10px] text-slate-500 uppercase font-black tracking-widest mt-1">ELO Earned</div>
                            </div>
                        </div>

                        <div className="space-y-3">
                            <button
                                onClick={handleStart}
                                className="w-full py-4 bg-white text-slate-900 font-black rounded-2xl hover:bg-slate-200 transition-all flex items-center justify-center gap-2"
                            >
                                <RefreshCcw className="w-5 h-5" /> RE-ENTER ARENA
                            </button>
                            <Link
                                href="/leaderboards"
                                className="w-full py-4 bg-white/5 hover:bg-white/10 border border-white/10 text-white font-bold rounded-2xl transition-all flex items-center justify-center gap-2 group"
                            >
                                VIEW RANKINGS <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                            </Link>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
