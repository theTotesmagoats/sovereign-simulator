"""
Black Box AI — The Sovereign Simulator

A feedback-loop simulation game that teaches how short-term gains create long-term fragility
in AI safety/compliance systems.

Run with: python main.py
"""

import random
from colorama import Fore, Style

# Import local modules
from sovereign_simulator.data_launder_engine import (
    SecondOrderEngine, ShadowLibrary, LaunderMethod,
    LIBRARY_TRAITS, METHOD_TRAITS
)
from sovereign_simulator.ui.glitch_dashboard import GlitchDashboard
from sovereign_simulator.testimony_engine import TestimonyEngine
from sovereign_simulator.competitor_ai import CompetitorAI, set_library_traits, set_method_traits


def main():
    print("\n🎮 Welcome to BLACK_BOX.AI — The Sovereign Simulator")
    print("Your goal: Survive 10 turns without collapse or nationalization.\n")

    # Initialize engine
    engine = SecondOrderEngine()
    
    # Setup competitors with traits
    set_library_traits(LIBRARY_TRAITS)
    set_method_traits(METHOD_TRAITS)

    dashboard = GlitchDashboard()
    testimony = TestimonyEngine()

    # Create random competitor
    competitor = CompetitorAI()
    print(f"🕵️ Your competitor: {competitor.personality.value}\n")

    while not engine.game_over and engine.turn < 10:
        dashboard.render(engine)
        dashboard.turn = engine.turn

        # Player turn
        print("\n[CHOOSE YOUR MOVE]")
        for i, lib in enumerate(ShadowLibrary):
            print(f"{i+1}. {lib.value}")
        
        try:
            library_choice = int(input("\nSelect data source (1-4): ").strip()) - 1
            if library_choice not in range(4):
                raise ValueError()
        except ValueError:
            print("❌ Invalid choice. Defaulting to Common Crawl.")
            library_choice = ShadowLibrary.COMMON_CRAWL.value.__objclass__.__dict__.get('COMMON_CRAWL', None)
            library_choice = 1  # fallback

        for i, method in enumerate(LaunderMethod):
            print(f"{i+1}. {method.value}")
        
        try:
            method_choice = int(input("\nSelect laundering method (1-3): ").strip()) - 1
            if method_choice not in range(3):
                raise ValueError()
        except ValueError:
            print("❌ Invalid choice. Defaulting to Offshore Lab.")
            method_choice = 1

        # Execute player move
        events = engine.launder(
            list(ShadowLibrary)[library_choice],
            list(LaunderMethod)[method_choice]
        )
        print("\n".join(events))

        # Competitor turn
        comp_lib, comp_method = competitor.update()
        print(f"\n🤖 Competitor: {comp_lib} + {comp_method}")

        # Testimony trigger check (only once)
        if engine.legal_risk > 0.6 and not testimony.has_testified:
            events = testimony.trigger_testimony(engine)
            if events:
                input("\nPress Enter to continue...")

    # Endgame states
    print("\n" + "="*50)
    if engine.cash <= 0:
        print(f"{Fore.RED}💀 BANKRUPTCY: You’re out of runway.{Style.RESET_ALL}")
    elif engine.model_iq <= 30:
        print(f"{Fore.RED}🧠 LOGIC COLLAPSE: Your model is broken.{Style.RESET_ALL}")
    else:
        if engine.institutional_trust > 90 and engine.model_iq < 60:
            print(f"{Fore.YELLOW}☁️ ZOMBIE UTILITY: You’re the state’s API — but your model can’t think.{Style.RESET_ALL}")
        elif engine.shadow_debt["ip_time_bomb"] >= 100:
            print(f"{Fore.MAGENTA}🔥 SOVEREIGN OUTLAW: You’re delisted — running on P2P nodes.{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}🎉 SURVIVAL: You made it through the crisis… for now.{Style.RESET_ALL}")

    print("="*50)


if __name__ == "__main__":
    main()