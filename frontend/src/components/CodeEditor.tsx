"use client";

import React from 'react';
import Editor from '@monaco-editor/react';

interface CodeEditorProps {
    code: string;
    language: string;
    onChange: (value: string | undefined) => void;
    theme?: string;
}

export function CodeEditor({ code, language, onChange, theme = 'vs-dark' }: CodeEditorProps) {
    return (
        <div className="h-full w-full rounded-xl overflow-hidden border border-white/5 bg-[#1e1e1e]">
            <Editor
                height="100%"
                defaultLanguage={language}
                defaultValue={code}
                theme={theme}
                onChange={onChange}
                options={{
                    minimap: { enabled: false },
                    fontSize: 14,
                    fontFamily: 'var(--font-geist-mono)',
                    lineHeight: 1.5,
                    padding: { top: 16, bottom: 16 },
                    scrollBeyondLastLine: false,
                    automaticLayout: true,
                    cursorSmoothCaretAnimation: "on",
                    smoothScrolling: true,
                    roundedSelection: true,
                    scrollbar: {
                        vertical: 'hidden',
                        horizontal: 'hidden'
                    }
                }}
            />
        </div>
    );
}
