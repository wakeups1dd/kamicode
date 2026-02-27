"use client";

import { useEffect, useRef, useState } from 'react';

const WS_URL = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000/ws';

export function useWebSocket() {
    const [lastMessage, setLastMessage] = useState<Record<string, unknown> | null>(null);
    const [isConnected, setIsConnected] = useState(false);
    const ws = useRef<WebSocket | null>(null);
    const isIntentionallyClosed = useRef(false);

    useEffect(() => {
        let reconnectTimer: NodeJS.Timeout;

        function connect() {
            isIntentionallyClosed.current = false;
            ws.current = new WebSocket(WS_URL);

            ws.current.onopen = () => {
                // eslint-disable-next-line no-console
                console.log("WebSocket Connected");
                setIsConnected(true);
            };

            ws.current.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    setLastMessage(data);
                } catch (err) {
                    // eslint-disable-next-line no-console
                    console.error("Failed to parse WS message", err);
                }
            };

            ws.current.onclose = () => {
                // eslint-disable-next-line no-console
                console.log("WebSocket Disconnected");
                setIsConnected(false);
                // Simple reconnect logic, if not unmounted
                if (!isIntentionallyClosed.current) {
                    reconnectTimer = setTimeout(connect, 3000);
                }
            };

            ws.current.onerror = () => {
                // Note: We don't use console.error here because React Strict Mode unmounts 
                // the component while the WS is connecting, which naturally triggers an onerror.
                // console.error triggers the Next.js dev overlay, so we silently handle it.
                if (ws.current?.readyState === WebSocket.OPEN) {
                    ws.current?.close();
                }
            };
        }

        connect();

        return () => {
            isIntentionallyClosed.current = true;
            clearTimeout(reconnectTimer);
            if (ws.current) {
                ws.current.close();
            }
        };
    }, []);

    const sendMessage = (message: Record<string, unknown>) => {
        if (ws.current && isConnected) {
            ws.current.send(JSON.stringify(message));
        }
    };

    return { lastMessage, isConnected, sendMessage };
}
