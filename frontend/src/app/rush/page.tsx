"use client";

import React from 'react';
import { Zap } from 'lucide-react';
import { motion } from 'framer-motion';

export default function RushPage() {
    return (
        <div className="max-w-4xl mx-auto h-[calc(100vh-112px)] flex flex-col justify-center items-center py-8">
            <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="text-center space-y-8 glass p-12 rounded-[40px] border-white/5 bg-slate-900/40 relative overflow-hidden"
            >
                <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-brand-primary/20 rounded-full blur-[80px]" />
                <div className="relative z-10 space-y-6">
                    <div className="w-20 h-20 bg-gradient-to-br from-brand-primary to-brand-secondary rounded-3xl mx-auto flex items-center justify-center shadow-lg shadow-brand-primary/20 animate-pulse">
                        <Zap className="text-white w-10 h-10 fill-white" />
                    </div>
                    <div className="space-y-4">
                        <h1 className="text-4xl font-extrabold tracking-tight">Rapid <span className="gradient-text">Rush</span></h1>
                        <h2 className="text-2xl font-bold text-slate-300">Coming Soon</h2>
                        <p className="text-slate-400 max-w-sm mx-auto">We are completely reimagining the Rush Mode experience. Prepare for a more intense, competitive, and rewarding arena. Stay tuned.</p>
                    </div>
                </div>
            </motion.div>
        </div>
    );
}
