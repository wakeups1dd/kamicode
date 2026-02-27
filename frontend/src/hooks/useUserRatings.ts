"use client";

import { useState, useEffect } from 'react';
import { api } from '@/services/api';

export interface UserRating {
    new_rating: number;
    [key: string]: unknown;
}

export function useUserRatings() {
    const [ratings, setRatings] = useState<UserRating[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        async function fetchRatings() {
            try {
                const data = await api.get<UserRating[]>('/users/me/ratings');
                setRatings(data);
            } catch (err: unknown) {
                // If 401/403, just set empty ratings (not logged in)
                const errorMessage = err instanceof Error ? err.message : String(err);
                if (errorMessage.includes('401') || errorMessage.includes('403')) {
                    setRatings([]);
                } else {
                    setError(errorMessage);
                }
            } finally {
                setIsLoading(false);
            }
        }

        fetchRatings();
    }, []);

    const currentRating = ratings.length > 0 ? ratings[0].new_rating : 1200;

    return { ratings, currentRating, isLoading, error };
}
