"use client";

import React from 'react';
import {
  Trophy,
  Zap,
  Target,
  ChevronRight,
  Flame,
  Code2,
  Clock
} from 'lucide-react';
import Link from 'next/link';
import { useDailyChallenge } from '@/hooks/useChallenge';
import { useUserRatings } from '@/hooks/useUserRatings';
import { useWebSocket } from '@/hooks/useWebSocket';
import { useState, useEffect } from 'react';

export interface Activity {
  username: string;
  problem_title: string;
  accuracy: string;
  timestamp: string;
}

export default function Home() {
  const { challenge, isLoading: challengeLoading } = useDailyChallenge();
  const { currentRating, isLoading: ratingsLoading } = useUserRatings();
  const { lastMessage } = useWebSocket();
  const [activities, setActivities] = useState<Activity[]>([
    { username: "CryptoWizard", problem_title: "Two Sum", accuracy: "98%", timestamp: "2 mins ago" },
    { username: "AlgoKing", problem_title: "FizzBuzz", accuracy: "100%", timestamp: "5 mins ago" },
    { username: "ByteNinja", problem_title: "LRU Cache", accuracy: "95%", timestamp: "12 mins ago" }
  ]);

  // Mock streak and efficiency for now
  const streak = 12;
  const efficiency = "98.2%";

  useEffect(() => {
    if (lastMessage && lastMessage.type === "ACTIVITY_SOLVE") {
      setTimeout(() => {
        setActivities(prev => [lastMessage.data as Activity, ...prev].slice(0, 5));
      }, 0);
    }
  }, [lastMessage]);

  const formatRating = (rating: number) => Math.round(rating);

  return (
    <div className="max-w-6xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      {/* Hero Section */}
      <section className="relative overflow-hidden rounded-3xl bg-slate-900 border border-white/5 p-8 md:p-12">
        <div className="relative z-10 flex flex-col md:flex-row items-center justify-between gap-8">
          <div className="space-y-4 max-w-xl text-center md:text-left">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-primary/10 border border-brand-primary/20 text-brand-primary text-xs font-bold uppercase tracking-wider">
              <Zap className="w-3 h-3" /> Daily Challenge
            </div>
            <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight">
              {challengeLoading ? (
                "Loading..."
              ) : challenge ? (
                <>Master <span className="gradient-text">{challenge.title}</span></>
              ) : (
                <>Master the Art of <span className="gradient-text">Efficient Code</span></>
              )}
            </h1>
            <p className="text-slate-400 text-lg">
              {challenge ? "A new problem awaits. Analyze, optimize, and submit." : "Solve today's puzzle, optimize with AI, and earn your on-chain credentials."}
            </p>
            <div className="flex flex-wrap items-center justify-center md:justify-start gap-4 pt-4">
              <Link
                href={challenge ? `/challenge/${challenge.slug}` : "/challenge/daily"}
                className="px-8 py-3 bg-brand-primary hover:bg-brand-primary/90 text-white font-bold rounded-xl transition-all hover:scale-105 shadow-lg shadow-brand-primary/20 flex items-center gap-2"
              >
                Solve Challenge <ChevronRight className="w-4 h-4" />
              </Link>
              <div className="flex items-center gap-2 px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-slate-300">
                <Clock className="w-4 h-4" /> 14:24:08 Left
              </div>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4 w-full md:w-auto">
            <div className="p-6 rounded-2xl glass space-y-2 text-center md:text-left">
              <div className="text-3xl font-bold gradient-text">
                {ratingsLoading ? "---" : formatRating(currentRating)}
              </div>
              <div className="text-xs text-slate-500 uppercase font-bold tracking-widest">Current Rating</div>
            </div>
            <div className="p-6 rounded-2xl glass space-y-2 text-center md:text-left">
              <div className="text-3xl font-bold flex items-center justify-center md:justify-start gap-2">
                {streak} <Flame className="w-6 h-6 text-orange-500" />
              </div>
              <div className="text-xs text-slate-500 uppercase font-bold tracking-widest">Day Streak</div>
            </div>
            <div className="p-6 rounded-2xl glass space-y-2 text-center md:text-left">
              <div className="text-3xl font-bold text-brand-accent">{efficiency}</div>
              <div className="text-xs text-slate-500 uppercase font-bold tracking-widest">Efficiency</div>
            </div>
            <div className="p-6 rounded-2xl glass space-y-2 text-center md:text-left">
              <div className="text-3xl font-bold text-slate-200">Silver III</div>
              <div className="text-xs text-slate-500 uppercase font-bold tracking-widest">League Tier</div>
            </div>
          </div>
        </div>

        {/* Background blobs */}
        <div className="absolute top-0 right-0 -mr-20 -mt-20 w-80 h-80 bg-brand-primary/10 rounded-full blur-[100px]" />
        <div className="absolute bottom-0 left-0 -ml-20 -mb-20 w-80 h-80 bg-brand-secondary/10 rounded-full blur-[100px]" />
      </section>

      {/* Quick Actions & Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold flex items-center gap-2">
              <Target className="w-5 h-5 text-brand-primary" /> Active Quests
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-5 rounded-2xl bg-white/5 border border-white/5 hover:border-brand-primary/30 transition-all cursor-pointer group">
              <div className="flex items-start justify-between mb-4">
                <div className="p-2 rounded-lg bg-orange-500/10 text-orange-500">
                  <Flame className="w-5 h-5" />
                </div>
                <span className="text-xs font-bold text-slate-500">75% Complete</span>
              </div>
              <h3 className="font-bold mb-1">Streak Warrior</h3>
              <p className="text-sm text-slate-400 mb-4">Solve problems for 14 consecutive days.</p>
              <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                <div className="h-full bg-orange-500 w-3/4" />
              </div>
            </div>

            <div className="p-5 rounded-2xl bg-white/5 border border-white/5 hover:border-brand-primary/30 transition-all cursor-pointer group">
              <div className="flex items-start justify-between mb-4">
                <div className="p-2 rounded-lg bg-brand-primary/10 text-brand-primary">
                  <Code2 className="w-5 h-5" />
                </div>
                <span className="text-xs font-bold text-slate-500">2/5 Done</span>
              </div>
              <h3 className="font-bold mb-1">Complexity Master</h3>
              <p className="text-sm text-slate-400 mb-4">Achieve O(1) space on 5 medium problems.</p>
              <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                <div className="h-full bg-brand-primary w-2/5" />
              </div>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <h2 className="text-xl font-bold flex items-center gap-2">
            <Trophy className="w-5 h-5 text-brand-secondary" /> Recent Activity
          </h2>
          <div className="rounded-2xl border border-white/5 bg-slate-900/50 p-4 space-y-4">
            {activities.map((act, i) => (
              <div key={i} className="flex gap-3 pb-4 border-b border-white/5 last:border-0 last:pb-0 animate-in fade-in slide-in-from-top-2 duration-500">
                <div className="w-10 h-10 rounded-full bg-slate-800 flex-shrink-0 flex items-center justify-center text-xs font-bold text-slate-500">
                  {act.username.charAt(0)}
                </div>
                <div className="space-y-1">
                  <p className="text-sm">
                    <span className="font-bold text-slate-200">{act.username}</span> solved <span className="text-brand-primary">{act.problem_title}</span>
                  </p>
                  <p className="text-xs text-slate-500">{act.timestamp} • {act.accuracy} Efficiency</p>
                </div>
              </div>
            ))}
            <button className="w-full py-2 text-sm font-medium text-slate-400 hover:text-white transition-colors">
              View Global Feed
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
