"""
Glitch Dashboard — Visual feedback that degrades as system stress rises.

This module provides a CLI dashboard with ANSI color codes and glitch effects
that simulate a system decaying under hidden debt pressure.
"""

import os
import time
from colorama import Fore, Style, init


class GlitchDashboard:
    def __init__(self):
        self.turn = 0
        self.last_warning = None

    def clear(self):
        """Clear screen with ANSI escape."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def glitch_text(self, text, risk_level):
        """Add glitch effect based on risk level (0–100%)."""
        if risk_level < 50:
            return text
        elif risk_level < 80:
            chars = list(text)
            for i in range(len(chars)):
                if time.time() % 1 < 0.1 and i % 2 == 0:
                    chars[i] = "█" if chars[i].isalnum() else chars[i]
            return "".join(chars)
        else:
            return f"{Fore.RED}{text.replace(' ', ' ▄ ▀ ')[::2]}{Style.RESET_ALL}"

    def render(self, engine):
        """Render full dashboard with visual feedback."""
        self.clear()
        print(f"\n{Fore.CYAN}{'='*60}")
        print(" black_box.ai — DASHBOARD (v0.9.4)")
        print(f"{'='*60}{Style.RESET_ALL}")

        # Core metrics
        iq_glitch = self.glitch_text(str(engine.model_iq), engine.shadow_debt["audit_suspicion"])
        trust_glitch = self.glitch_text(
            str(engine.institutional_trust),
            engine.shadow_debt["ip_time_bomb"]
        )
        
        print(f" Model IQ:     {iq_glitch}")
        print(f" Cash Runway:  ${engine.cash:,}")
        print(f" Legal Risk:   {int(engine.legal_risk * 100)}%")
        print(f" Trust Level:  {trust_glitch}%")

        # Hidden metrics (revealed gradually)
        audit_revealed = engine.shadow_debt["audit_suspicion"] >= 50
        ip_revealed = engine.shadow_debt["ip_time_bomb"] >= 30

        if audit_revealed:
            print(f"{Fore.YELLOW}⚠️ Audit Suspicion: {engine.shadow_debt['audit_suspicion']}% (HIDDEN UNTIL NOW){Style.RESET_ALL}")
        else:
            print("🛡️ Audit Suspicion: ?%")

        if ip_revealed:
            print(f"{Fore.RED}💣 IP Time Bomb: {engine.shadow_debt['ip_time_bomb']}%{Style.RESET_ALL}")
        else:
            print("💣 IP Time Bomb: ?%")

        # Leak Reporter (appears 20% of turns after turn 3)
        if self.turn >= 3 and time.time() % 5 < 1:
            leaks = [
                "LEAK REPORTER: 'FTC audit pending — source says evidence is damning.'",
                "LEAK REPORTER: 'Whistleblower contacted The Verge — internal memo attached.'",
                "LEAK REPORTER: 'Competitor's lawsuit just dropped — your logs were subpoenaed.'"
            ]
            print(f"\n{Fore.MAGENTA}💬 {leaks[int(time.time()) % len(leaks)]}{Style.RESET_ALL}")

        # System status bar
        reliability = 1 - engine.shadow_debt["audit_suspicion"] / 100
        bar_len = int(reliability * 30)
        bar = f"{'█' * bar_len}{'░' * (30 - bar_len)}"
        
        if engine.shadow_debt["audit_suspicion"] >= 80:
            status_color = Fore.RED
            status_text = "CRITICAL: SYSTEM FAILURE IMMINENT"
        elif engine.shadow_debt["audit_suspicion"] >= 50:
            status_color = Fore.YELLOW
            status_text = "WARNING: AUDIT PENDING"
        else:
            status_color = Fore.GREEN
            status_text = "SYSTEM STABLE"

        print(f"\n{status_color}[{bar}] {status_text}{Style.RESET_ALL}")
        print("="*60)