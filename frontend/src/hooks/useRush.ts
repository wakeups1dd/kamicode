"use client";

import { useState } from 'react';
import { api } from '@/services/api';

export interface RushSession {
    id: string;
    lives: number;
    streak: number;
    points_earned?: number;
    [key: string]: unknown;
}

export interface Puzzle {
    id: string;
    puzzle_type: string;
    question: string;
    snippet?: string;
    options: string[];
    [key: string]: unknown;
}

export function useRushSession() {
    const [session, setSession] = useState<RushSession | null>(null);
    const [currentPuzzle, setCurrentPuzzle] = useState<Puzzle | null>(null);
    const [isEnding, setIsEnding] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const startSession = async (mode: string = 'Classical') => {
        setError(null);
        try {
            const data = await api.post<{ session: RushSession; first_puzzle: Puzzle }>('/rush/start', { mode });
            setSession(data.session);
            setCurrentPuzzle(data.first_puzzle);
            return data;
        } catch (err: unknown) {
            setError(err instanceof Error ? err.message : String(err));
        }
    };

    const submitAnswer = async (answer: string) => {
        if (!session || !currentPuzzle) return;

        try {
            const data = await api.post<{ is_correct: boolean; next_puzzle?: Puzzle }>(`/rush/sessions/${session.id}/answer`, {
                puzzle_id: currentPuzzle.id,
                user_answer: answer
            });

            if (data.is_correct) {
                setSession((prev) => prev ? { ...prev, streak: prev.streak + 1 } : null);
            } else {
                setSession((prev) => prev ? { ...prev, lives: prev.lives - 1 } : null);
            }

            if (data.next_puzzle) {
                setCurrentPuzzle(data.next_puzzle);
            } else {
                setIsEnding(true);
            }
            return data;
        } catch (err: unknown) {
            setError(err instanceof Error ? err.message : String(err));
        }
    };

    return { startSession, submitAnswer, session, currentPuzzle, isEnding, error };
}
