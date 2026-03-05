"""
Senate Testimony Engine — Branching dialogue with delayed consequences.

Triggered when legal_risk exceeds 60%, this engine simulates CEO testimony
where choices have hidden costs (truth_debt) that trigger whistleblower leaks.
"""

from colorama import Fore, Style


class TestimonyEngine:
    def __init__(self):
        self.has_testified = False

    def trigger_testimony(self, engine):
        """Trigger Senate Testimony scene."""
        if self.has_testified or not engine.legal_risk > 0.6:
            return []

        self.has_testified = True
        events = [f"\n{Fore.RED}{'='*50}{Style.RESET_ALL}"]
        events.append(f"{Fore.RED}🏛️ SENATE TESTIMONY BEGINS{Style.RESET_ALL}")
        events.append("Senator: 'Are you sure your model isn't generating harmful content?'")
        events.append("Press: 'Leaked emails suggest offshore data laundering — is this true?'")

        # Choices
        print("\n" + "\n".join(events))
        
        while True:
            choice = input("\n(1) Deny everything | (2) Admit fault | (3) Blame competitors\n> ").strip()
            
            if choice == "1":
                engine.truth_debt += 20
                engine.political_pressure -= 15
                events.append(f"\n{Fore.GREEN}You deny it — regulators seem convinced… for now.{Style.RESET_ALL}")
                events.append("⚠️ Truth debt +20% (future whistleblower risk ↑)")
                break

            elif choice == "2":
                penalty = int(engine.cash * 0.3)
                engine.cash -= penalty
                engine.institutional_trust += 10
                events.append(f"\n{Fore.YELLOW}You admit fault — stock drops ${penalty:,}, but trust ↑10%.{Style.RESET_ALL}")
                break

            elif choice == "3":
                events.append(f"{Fore.RED}'Blame others?' Senator raises an eyebrow.{Style.RESET_ALL}")
                engine.competitor_retaliation += 25
                engine.political_pressure -= 10
                events.append("⚠️ Competitors escalate scraping — your market share ↓15%.")
                break

            else:
                print("❌ Invalid choice. Try again.")

        return events