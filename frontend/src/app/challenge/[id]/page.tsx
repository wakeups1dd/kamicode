"use client";

import React, { useState, useEffect } from 'react';
import {
    Play,
    Send,
    Settings,
    Maximize2,
    Info,
    Terminal as TerminalIcon,
    ChevronLeft,
    AlertCircle,
    CheckCircle2
} from 'lucide-react';
import Link from 'next/link';
import { CodeEditor } from '@/components/CodeEditor';
import { cn } from '@/lib/utils';
import { api } from '@/services/api';
import { useSubmission } from '@/hooks/useSubmission';

export interface Problem {
    id: string;
    title: string;
    description: string;
    difficulty: string;
    daily_date?: string;
    constraints?: string;
    tags?: string[];
    sample_test_cases?: { input: string; expected: string }[];
    [key: string]: unknown;
}

export default function ChallengePage({ params }: { params: Promise<{ id: string }> }) {
    const resolvedParams = React.use(params);
    const [problem, setProblem] = useState<Problem | null>(null);
    const [code, setCode] = useState('');
    const [language, setLanguage] = useState('python');
    const [isLoading, setIsLoading] = useState(true);

    const { submitCode, isSubmitting, submission, analysis, error: submissionError } = useSubmission();

    useEffect(() => {
        async function fetchProblem() {
            try {
                const identifier = resolvedParams.id === 'daily' ? 'daily' : resolvedParams.id;
                const endpoint = identifier === 'daily' ? '/problems/daily' : `/problems/${identifier}`;
                const data = await api.get<Problem>(endpoint);
                setProblem(data);
                // Set default code template if available or some generic one
                setCode(language === 'python' ? 'def solution():\n    # Write your code here\n    pass' : '');
            } catch (err) {
                console.error("Failed to fetch problem", err);
            } finally {
                setIsLoading(false);
            }
        }
        fetchProblem();
    }, [resolvedParams.id, language]);

    const handleSubmit = async () => {
        if (!problem || !code) return;
        await submitCode(problem.id, code, language);
    };

    if (isLoading) {
        return (
            <div className="flex items-center justify-center h-[calc(100vh-112px)]">
                <div className="w-8 h-8 border-4 border-brand-primary border-t-transparent rounded-full animate-spin" />
            </div>
        );
    }

    if (!problem) {
        return (
            <div className="flex flex-col items-center justify-center h-[calc(100vh-112px)] gap-4">
                <AlertCircle className="w-12 h-12 text-slate-500" />
                <h1 className="text-xl font-bold">Problem not found</h1>
                <Link href="/" className="text-brand-primary hover:underline">Return Home</Link>
            </div>
        );
    }

    return (
        <div className="flex flex-col h-[calc(100vh-112px)] gap-4 animate-in fade-in duration-500">
            {/* Header / Toolbar */}
            <div className="flex items-center justify-between glass p-2 rounded-2xl border-white/5">
                <div className="flex items-center gap-4 px-2">
                    <Link href="/" className="p-2 hover:bg-white/5 rounded-lg transition-colors">
                        <ChevronLeft className="w-5 h-5" />
                    </Link>
                    <div className="h-6 w-px bg-white/10" />
                    <div>
                        <h1 className="font-bold text-sm tracking-tight">{problem.title}</h1>
                        <p className="text-[10px] text-slate-500 uppercase font-bold tracking-widest">
                            {problem.daily_date ? "Daily Challenge" : "Practice"} • {problem.difficulty}
                        </p>
                    </div>
                </div>

                <div className="flex items-center gap-2">
                    <select
                        value={language}
                        onChange={(e) => setLanguage(e.target.value)}
                        className="bg-slate-800 border-white/10 text-xs rounded-lg px-3 py-1.5 focus:ring-1 ring-brand-primary outline-none"
                    >
                        <option value="python">Python</option>
                        <option value="javascript">JavaScript</option>
                        <option value="cpp">C++</option>
                    </select>
                    <div className="h-6 w-px bg-white/10 mx-1" />
                    <button className="p-2 hover:bg-white/5 rounded-lg transition-colors text-slate-400">
                        <Settings className="w-4 h-4" />
                    </button>
                    <button className="p-2 hover:bg-white/5 rounded-lg transition-colors text-slate-400">
                        <Maximize2 className="w-4 h-4" />
                    </button>
                </div>
            </div>

            <div className="flex flex-1 gap-4 overflow-hidden">
                {/* Left Side: Problem & Console */}
                <div className="flex-[0.4] flex flex-col gap-4 overflow-hidden">
                    <div className="flex-1 glass rounded-2xl border-white/5 p-6 overflow-y-auto custom-scrollbar">
                        <div className="flex items-center gap-2 text-slate-400 mb-4">
                            <Info className="w-4 h-4" />
                            <span className="text-xs font-bold uppercase tracking-wider">Description</span>
                        </div>
                        <div className="prose prose-invert prose-slate max-w-none">
                            <p className="text-slate-200 leading-relaxed text-sm">{problem.description}</p>

                            {problem.constraints && (
                                <>
                                    <h4 className="text-sm font-bold mt-6 mb-2">Constraints:</h4>
                                    <p className="text-xs text-slate-400 font-mono italic">{problem.constraints}</p>
                                </>
                            )}

                            {problem.sample_test_cases?.map((test, idx) => (
                                <div key={idx} className="mt-6">
                                    <h4 className="text-sm font-bold mb-2">Example {idx + 1}:</h4>
                                    <pre className="bg-black/30 border border-white/5 rounded-lg p-3 text-[11px] leading-relaxed font-mono">
                                        Input: {test.input}{"\n"}
                                        Output: {test.expected}
                                    </pre>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Mini Console / AI Results */}
                    <div className="h-48 glass rounded-2xl border-white/5 p-4 flex flex-col">
                        <div className="flex items-center justify-between mb-2">
                            <div className="flex items-center gap-2 text-slate-400">
                                <TerminalIcon className="w-4 h-4" />
                                <span className="text-xs font-bold uppercase tracking-wider">Console & AI</span>
                            </div>
                            {submission && (
                                <span className={cn(
                                    "text-[10px] font-bold px-2 py-0.5 rounded-full",
                                    submission.verdict === 'Accepted' ? "bg-brand-accent/20 text-brand-accent" : "bg-red-500/20 text-red-500"
                                )}>
                                    {submission.verdict}
                                </span>
                            )}
                        </div>
                        <div className="flex-1 bg-black/20 rounded-xl p-3 font-mono text-xs text-slate-400 overflow-y-auto">
                            {isSubmitting ? (
                                <div className="flex flex-col gap-2">
                                    <p className="animate-pulse">{'>'} Processing submission...</p>
                                    <p className="text-[10px] text-slate-600 italic animate-pulse delay-75">{'>'} AI is analyzing your complexity...</p>
                                </div>
                            ) : analysis ? (
                                <div className="space-y-4">
                                    <div className="flex items-center gap-2 text-brand-accent">
                                        <CheckCircle2 className="w-3 h-3" />
                                        <span className="font-bold">AI Analysis Complete</span>
                                    </div>
                                    <div className="space-y-2">
                                        <p className="text-slate-200">{analysis.explanation}</p>
                                        <div className="grid grid-cols-2 gap-2 mt-2">
                                            <div className="bg-white/5 p-2 rounded-lg border border-white/5">
                                                <div className="text-[10px] text-slate-500 uppercase">Time</div>
                                                <div className="font-bold text-brand-primary">{analysis.time_complexity}</div>
                                            </div>
                                            <div className="bg-white/5 p-2 rounded-lg border border-white/5">
                                                <div className="text-[10px] text-slate-500 uppercase">Space</div>
                                                <div className="font-bold text-brand-secondary">{analysis.space_complexity}</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ) : submissionError ? (
                                <p className="text-red-500">{'>'} Error: {submissionError}</p>
                            ) : (
                                <p className="text-slate-600">{'>'} Ready for submission.</p>
                            )}
                        </div>
                    </div>
                </div>

                {/* Right Side: Editor */}
                <div className="flex-[0.6] flex flex-col gap-4">
                    <div className="flex-1 glass rounded-2xl border-white/5 p-2 overflow-hidden">
                        <CodeEditor
                            code={code}
                            language={language}
                            onChange={(val) => setCode(val || '')}
                        />
                    </div>

                    <div className="glass rounded-2xl border-white/5 p-3 flex items-center justify-between">
                        <div className="text-[10px] text-slate-500 flex items-center gap-2 px-2 italic">
                            {problem.tags?.map((tag) => (
                                <span key={tag}>#{tag}</span>
                            ))}
                        </div>
                        <div className="flex items-center gap-3">
                            <button
                                onClick={() => { }}
                                className="flex items-center gap-2 px-4 py-2 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl text-sm font-semibold transition-all"
                            >
                                <Play className="w-4 h-4" /> Run code
                            </button>
                            <button
                                onClick={handleSubmit}
                                disabled={isSubmitting || !code}
                                className={cn(
                                    "flex items-center gap-2 px-6 py-2 bg-brand-primary hover:bg-brand-primary/90 text-white rounded-xl text-sm font-bold transition-all shadow-lg shadow-brand-primary/20",
                                    (isSubmitting || !code) && "opacity-50 cursor-not-allowed"
                                )}
                            >
                                <Send className="w-4 h-4" /> {isSubmitting ? "Submitting..." : "Submit"}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
