"use client";

import { useState, useEffect } from 'react';
import { api } from '@/services/api';

export interface Challenge {
    id: string;
    title: string;
    slug: string;
    description?: string;
    difficulty?: string;
    [key: string]: unknown;
}

export function useDailyChallenge() {
    const [challenge, setChallenge] = useState<Challenge | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        async function fetchChallenge() {
            try {
                const data = await api.get<Challenge>('/problems/daily');
                setChallenge(data);
            } catch (err: unknown) {
                setError(err instanceof Error ? err.message : String(err));
            } finally {
                setIsLoading(false);
            }
        }

        fetchChallenge();
    }, []);

    return { challenge, isLoading, error };
}
