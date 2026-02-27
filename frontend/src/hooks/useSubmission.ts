"use client";

import { useState } from 'react';
import { api } from '@/services/api';

export interface Submission {
    id: string;
    verdict?: string;
    [key: string]: unknown;
}

export interface Analysis {
    explanation: string;
    time_complexity: string;
    space_complexity: string;
    [key: string]: unknown;
}

export function useSubmission() {
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [submission, setSubmission] = useState<Submission | null>(null);
    const [analysis, setAnalysis] = useState<Analysis | null>(null);
    const [error, setError] = useState<string | null>(null);

    const submitCode = async (problemId: string, code: string, language: string) => {
        setIsSubmitting(true);
        setError(null);
        setAnalysis(null);

        try {
            const data = await api.post<Submission>('/submissions', {
                problem_id: problemId,
                code,
                language
            });
            setSubmission(data);

            // Poll for analysis
            pollAnalysis(data.id);
            return data;
        } catch (err: unknown) {
            setError(err instanceof Error ? err.message : String(err));
            setIsSubmitting(false);
        }
    };

    const pollAnalysis = async (submissionId: string) => {
        const maxAttempts = 10;
        let attempts = 0;

        const interval = setInterval(async () => {
            attempts++;
            try {
                const data = await api.get<Analysis>(`/submissions/${submissionId}/analysis`);
                if (data) {
                    setAnalysis(data);
                    setIsSubmitting(false);
                    clearInterval(interval);
                }
            } catch {
                if (attempts >= maxAttempts) {
                    setError("Analysis timed out");
                    setIsSubmitting(false);
                    clearInterval(interval);
                }
            }
        }, 2000);
    };

    return { submitCode, isSubmitting, submission, analysis, error };
}
