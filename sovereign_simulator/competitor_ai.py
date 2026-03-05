"""
Competitor AI — Randomized competitor behavior with different personalities.

Each game creates a unique competitor that influences market dynamics.
"""

import random
from enum import Enum


class CompetitorPersonality(Enum):
    AGGRESSIVE = "Scrapes everything — IP lawsuits inevitable"
    CAUTIOUS = "Uses clean data — slow growth but stable"
    HYBRID = "Mix of aggressive and cautious"


# Import traits from data_launder_engine (will be injected at runtime)
LIBRARY_TRAITS = None
METHOD_TRAITS = None


def set_library_traits(traits):
    """Allow competitor to access library/method traits."""
    global LIBRARY_TRAITS
    LIBRARY_TRAITS = traits


def set_method_traits(traits):
    """Allow competitor to access method traits."""
    global METHOD_TRAITS
    METHOD_TRAITS = traits


class CompetitorAI:
    def __init__(self, personality=None):
        self.personality = personality or random.choice(list(CompetitorPersonality))
        self.model_iq = 65
        self.cash = 8_000_000

    def choose_launder(self):
        """Pick a strategy based on personality."""
        from sovereign_simulator.data_launder_engine import ShadowLibrary, LaunderMethod
        
        if self.personality == CompetitorPersonality.AGGRESSIVE:
            return (ShadowLibrary.COMMON_CRAWL, LaunderMethod.OFFSHORE_LAB)
        elif self.personality == CompetitorPersonality.CAUTIOUS:
            return (ShadowLibrary.ARXIV, LaunderMethod.SYNTHETIC_RETRAIN)
        else:  # HYBRID
            r = random.random()
            if r < 0.6:
                return (ShadowLibrary.COMMON_CRAWL, LaunderMethod.OFFSHORE_LAB)
            else:
                return (ShadowLibrary.ARXIV, LaunderMethod.SYNTHETIC_RETRAIN)

    def update(self):
        """Run one turn for competitor."""
        from sovereign_simulator.data_launder_engine import ShadowLibrary, LaunderMethod

        library, method = self.choose_launder()
        
        # Apply effects
        iq_gain = LIBRARY_TRAITS[library]["iq_boost"] if LIBRARY_TRAITS else 20
        cost = METHOD_TRAITS[method]["cost"] if METHOD_TRAITS else 500_000

        self.model_iq += iq_gain
        self.cash -= cost

        return (library.value.split(" ")[0], method.value.split(" ")[0])