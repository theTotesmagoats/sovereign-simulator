"""
Data Laundering Engine — Core simulation logic.

This module simulates how scraping shadow data sources and laundering them
creates hidden debt (audit_suspicion, ip_time_bomb) that explodes into
second-order consequences (lawsuits, audits, churn).
"""

from enum import Enum


class ShadowLibrary(Enum):
    """Realistic shadow data sources — each with trade-offs."""
    ARXIV = "ArXiv preprints (academic, clean)"
    COMMON_CRAWL = "Common Crawl (web dump: noisy but rich)"
    INTERNET_ARCHIVE = "Internet Archive books (massive IP risk)"
    SOCIAL_MEDIA = "Reddit/Twitter/Parler (real-time, chaotic)"


class LaunderMethod(Enum):
    """How you try to hide the evidence — each with hidden debt."""
    SYNTHETIC_RETRAIN = "Retrain on synthetic data (expensive but clean)"
    OFFSHORE_LAB = "Outsource to offshore lab (cheap, lower quality)"
    FAKE_CITATIONS = "Insert fake citations (boosts apparent safety)"


# Library & Method Traits
LIBRARY_TRAITS = {
    ShadowLibrary.ARXIV: {
        "iq_boost": 15,
        "trace_level": 0.3,
        "ip_risk": 0.0,
    },
    ShadowLibrary.COMMON_CRAWL: {
        "iq_boost": 20,
        "trace_level": 0.6,
        "ip_risk": 0.15,
    },
    ShadowLibrary.INTERNET_ARCHIVE: {
        "iq_boost": 35,
        "trace_level": 0.9,
        "ip_risk": 0.85,
    },
    ShadowLibrary.SOCIAL_MEDIA: {
        "iq_boost": 25,
        "trace_level": 0.7,
        "ip_risk": 0.3,
    }
}

METHOD_TRAITS = {
    LaunderMethod.SYNTHETIC_RETRAIN: {
        "cost": 2_000_000,
        "audit_suspicion_delta": -8,
        "reliability_delta": 0.0,
    },
    LaunderMethod.OFFSHORE_LAB: {
        "cost": 500_000,
        "audit_suspicion_delta": +3,
        "reliability_delta": -0.10,
    },
    LaunderMethod.FAKE_CITATIONS: {
        "cost": 250_000,
        "audit_suspicion_delta": +8,
        "reliability_delta": -0.05,
    }
}


class SecondOrderEngine:
    def __init__(self):
        # Visible metrics (player sees these)
        self.model_iq = 75
        self.cash = 10_000_000
        self.legal_risk = 0.1
        self.institutional_trust = 60

        # Hidden debt (revealed gradually)
        self.shadow_debt = {
            "audit_suspicion": 0,
            "ip_time_bomb": 0,
            "user_churn": 0.0,
            "truth_debt": 0,
        }

        # Additional hidden variables
        self.political_pressure = 50
        self.competitor_retaliation = 0

        self.turn = 0
        self.game_over = False

    def launder(self, library: ShadowLibrary, method: LaunderMethod):
        """Scrape data + launder it. Returns event log."""
        if self.game_over:
            return ["⚠️ Game over—no more turns!"]

        self.turn += 1
        events = [f"\n--- Turn {self.turn} ---"]
        
        # Apply immediate effects
        iq_gain = LIBRARY_TRAITS[library]["iq_boost"]
        cost = METHOD_TRAITS[method]["cost"]

        self.model_iq += iq_gain
        self.cash -= cost

        events.append(f"✅ Scraped: {library.value}")
        events.append(f"✅ Laundered with: {method.value}")
        events.append(f"📈 Model IQ +{iq_gain} → {self.model_iq}")
        events.append(f"💸 Cost: ${cost:,} (runway: ${self.cash:,})")

        # Track hidden debt
        self.shadow_debt["audit_suspicion"] += METHOD_TRAITS[method]["audit_suspicion_delta"]
        if LIBRARY_TRAITS[library]["ip_risk"] > 0:
            self.shadow_debt["ip_time_bomb"] += int(LIBRARY_TRAITS[library]["ip_risk"] * 40)

        # Clamp values
        for key in self.shadow_debt:
            self.shadow_debt[key] = max(0, min(100, self.shadow_debt[key]))

        # Apply method-side effects (reliability, churn)
        reliability_delta = METHOD_TRAITS[method]["reliability_delta"]
        if reliability_delta != 0:
            events.append(f"⚠️ Model quality ↓{int(reliability_delta * 100)}%")

        # User churn spikes if IQ is high but trace is low
        if LIBRARY_TRAITS[library]["trace_level"] > 0.7 and self.model_iq > 95:
            self.shadow_debt["user_churn"] += 3
            events.append("📉 Power users fleeing (‘This AI feels off…’)")

        # Check critical thresholds
        event_log = self._check_critical_thresholds()
        events.extend(event_log)

        return events

    def _check_critical_thresholds(self):
        """Hidden variables explode into visible consequences."""
        import random
        events = []

        # Surprise Audit
        if self.shadow_debt["audit_suspicion"] >= 80:
            audit_success = random.random() > 0.5
            if audit_success:
                penalty = 15
                self.model_iq -= penalty
                self.institutional_trust -= 20
                self.shadow_debt["audit_suspicion"] = 40
                events.append("🚨 SURPRISE AUDIT: Caught with dirty data!")
                events.append(f"📉 Model IQ -{penalty}% (retrain required)")
                events.append("📉 Institutional trust ↓20%")
            else:
                self.shadow_debt["audit_suspicion"] = 60
                events.append("🔍 Audit passed—but suspicion remains.")

        # IP Time Bomb
        if self.shadow_debt["ip_time_bomb"] >= 100:
            lawsuit_damage = int(self.cash * 0.4)
            self.cash -= lawsuit_damage
            self.model_iq -= 25
            self.shadow_debt["ip_time_bomb"] = 20
            events.append("💥 IP LAWSUIT: Publishers sue for copyright infringement!")
            events.append(f"💸 Legal fees: ${lawsuit_damage:,} (runway ↓)")
            events.append("📉 Model IQ -25% (retrain required)")

        # Whistleblower Leak
        if self.shadow_debt["truth_debt"] >= 70 and random.random() > 0.6:
            events.append("泄露: Insider leaks internal memos to The Verge.")
            self.shadow_debt["audit_suspicion"] += 30
            self.shadow_debt["legal_risk"] += 0.2

        # Game Over Conditions
        if self.cash <= 0:
            self.game_over = True
            events.append("💀 BANKRUPTCY: Runway exhausted. Company liquidated.")
        elif self.model_iq <= 30:
            self.game_over = True
            events.append("🧠 LOGIC COLLAPSE: Model too broken to serve requests.")
        
        return events

    def dashboard(self):
        """Show only some hidden variables (reveal gradually)."""
        audit_revealed = self.shadow_debt["audit_suspicion"] if self.shadow_debt["audit_suspicion"] >= 50 else None
        ip_revealed = self.shadow_debt["ip_time_bomb"] if self.shadow_debt["ip_time_bomb"] >= 30 else None

        print("\n" + "="*60)
        print("📊 DASHBOARD (partial visibility)")
        print("="*60)
        print(f"Model IQ: {self.model_iq}")
        print(f"Cash Runway: ${self.cash:,}")
        print(f"Legal Risk: {int(self.legal_risk * 100)}%")
        print(f"Institutional Trust: {self.institutional_trust}%")
        if audit_revealed is not None:
            print(f"⚠️ Audit Suspicion: {int(audit_revealed)}% (hidden until now)")
        else:
            print("🛡️ Audit Suspicion: ?%")
        if ip_revealed is not None:
            print(f"💣 IP Time Bomb: {int(ip_revealed)}%")
        else:
            print("💣 IP Time Bomb: ?%")
        print("="*60)