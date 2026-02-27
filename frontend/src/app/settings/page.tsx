import React from 'react';
import { Settings, User, Key, Bell, Shield } from 'lucide-react';

export default function SettingsPage() {
    return (
        <div className="max-w-4xl mx-auto space-y-8 py-8 animate-in fade-in duration-500">
            <div className="flex items-center gap-4">
                <div className="w-14 h-14 bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl flex items-center justify-center border border-white/10 shadow-lg shadow-black/20">
                    <Settings className="w-7 h-7 text-brand-primary" />
                </div>
                <div>
                    <h1 className="text-3xl font-extrabold tracking-tight">Settings</h1>
                    <p className="text-slate-400 mt-1">Manage your developer profile and integrations.</p>
                </div>
            </div>

            <div className="space-y-6">
                {/* Account Settings */}
                <div className="glass p-8 rounded-[32px] border border-white/5 space-y-6 relative overflow-hidden">
                    <div className="absolute top-0 right-0 w-64 h-64 bg-brand-primary/10 rounded-full blur-[80px] -z-10 translate-x-1/2 -translate-y-1/2" />
                    <div className="flex items-center gap-3 border-b border-white/5 pb-4">
                        <User className="w-5 h-5 text-brand-primary" />
                        <h2 className="text-xl font-bold">Account Preferences</h2>
                    </div>
                    <div className="space-y-5 max-w-xl relative z-10">
                        <div>
                            <label className="block text-sm font-semibold text-slate-300 mb-2">Username</label>
                            <input
                                type="text"
                                defaultValue="devuser"
                                className="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-brand-primary/50 focus:ring-1 focus:ring-brand-primary/50 transition-all font-mono text-sm"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-semibold text-slate-300 mb-2">Email Address</label>
                            <input
                                type="email"
                                defaultValue="dev@kamicode.com"
                                className="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-brand-primary/50 focus:ring-1 focus:ring-brand-primary/50 transition-all font-mono text-sm"
                            />
                        </div>
                        <div className="pt-2">
                            <button className="px-6 py-3 bg-brand-primary hover:bg-brand-primary/90 text-white font-bold rounded-xl transition-all hover:scale-[1.02] active:scale-[0.98] shadow-lg shadow-brand-primary/20">
                                Save Changes
                            </button>
                        </div>
                    </div>
                </div>

                {/* Web3 Integrations */}
                <div className="glass p-8 rounded-[32px] border border-white/5 space-y-6 relative overflow-hidden">
                    <div className="absolute top-0 left-0 w-64 h-64 bg-brand-secondary/10 rounded-full blur-[80px] -z-10 -translate-x-1/2 -translate-y-1/2" />
                    <div className="flex items-center gap-3 border-b border-white/5 pb-4">
                        <Key className="w-5 h-5 text-brand-secondary" />
                        <h2 className="text-xl font-bold">Web3 Credentials</h2>
                    </div>
                    <div className="space-y-5 max-w-xl relative z-10">
                        <div>
                            <label className="block text-sm font-semibold text-slate-300 mb-2">Wallet Address for NFT Rewards</label>
                            <div className="flex gap-3">
                                <input
                                    type="text"
                                    readOnly
                                    value="Not connected"
                                    className="flex-1 bg-black/40 border border-white/10 rounded-xl px-4 py-3 text-slate-500 font-mono text-sm"
                                />
                                <button className="px-6 py-3 bg-white/5 hover:bg-white/10 text-white font-bold rounded-xl border border-white/10 transition-all hover:scale-[1.02] active:scale-[0.98]">
                                    Connect
                                </button>
                            </div>
                            <p className="text-xs text-slate-500 mt-2">Connect your Ethereum L2 (Base) wallet to receive verifiable achievements.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
