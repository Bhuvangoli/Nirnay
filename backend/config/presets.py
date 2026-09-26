"""
Scenario presets for the NIRNAY Strategic Wargaming Platform.
Provides predefined operational templates for wargame sessions.
"""

from typing import Dict, List, Any
from pydantic import BaseModel, Field


class ScenarioPreset(BaseModel):
    preset_id: str
    name: str
    theater: str
    description: str
    default_objective: str
    default_constraints: str
    turn_durations_supported: List[str] = Field(default_factory=lambda: ["30s", "1m", "5m"])
    forces_summary: Dict[str, Any] = Field(default_factory=dict)
    terrain: str
    initial_weather: str


PRESETS: Dict[str, ScenarioPreset] = {
    "DEMO-001": ScenarioPreset(
        preset_id="DEMO-001",
        name="Operation Resolve - Eastern Valley Standoff",
        theater="Eastern Valley Corridor",
        description=(
            "Adversary 4th Armored Column advancing toward River Crossing LOC-BRAVO. "
            "Friendly 1st Mechanized Brigade tasked with defending Forward Logistics Point Alpha "
            "and deterring adversary crossing without violating border buffer."
        ),
        default_objective="Defend Forward Logistics Point Alpha, hold river crossing corridor, deter adversary penetration without violating border buffer.",
        default_constraints="No kinetic cross-border strikes; fuel floor must remain above 24 hours.",
        turn_durations_supported=["30s", "1m", "5m"],
        forces_summary={
            "blue": "1st Mechanized Brigade (94 units) at LOC-ALPHA",
            "red": "4th Armored Column (108 units) at LOC-BRAVO"
        },
        terrain="Valley Basin, Moderate traversability, River barrier",
        initial_weather="Degrading rain, 6.5km visibility, muddy trail mobility penalty"
    ),
    "BORDER-002": ScenarioPreset(
        preset_id="BORDER-002",
        name="Northern Salients Border Shield",
        theater="High-Altitude Mountain Pass",
        description=(
            "Adversary mountain recon battalions probing high-altitude perimeter passes. "
            "Blue mechanized infantry and mountain batteries must establish early-warning sensors "
            "and interdict ingress routes while avoiding escalatory engagements."
        ),
        default_objective="Establish observation posts along ridge line Bravo, prevent adversary ingress through pass, maintain strict rules of engagement.",
        default_constraints="Defensive fire only; no aircraft ingress past median coordinate line.",
        turn_durations_supported=["30s", "1m", "5m"],
        forces_summary={
            "blue": "3rd Mountain Brigade (78 units) at Ridgeline Alpha",
            "red": "7th Recon Battalions (85 units) at Northern Ingress"
        },
        terrain="Steep Alpine Ridge, Low traversability, Chokepoints",
        initial_weather="Freezing fog, 2.0km visibility, snow pack mobility penalty"
    ),
    "COASTAL-003": ScenarioPreset(
        preset_id="COASTAL-003",
        name="Littoral Bastion Defense",
        theater="Strait Archipelago",
        description=(
            "Adversary amphibious ready group maneuvering near offshore energy platforms. "
            "Blue coastal defense battery and surface combatants must maintain maritime exclusion zone."
        ),
        default_objective="Deny maritime ingress into Strait sector, protect critical energy infrastructure, conduct active electronic screening.",
        default_constraints="No engagement beyond 12nm territorial waters without human command verification.",
        turn_durations_supported=["30s", "1m", "5m"],
        forces_summary={
            "blue": "Coastal Defense Flotilla (6 vessels + 2 batteries)",
            "red": "Amphibious Task Unit (9 vessels)"
        },
        terrain="Archipelago, Shallow waters, Dispersed islets",
        initial_weather="High sea state, Gale warnings, Intermittent squalls"
    ),
    "ISLAND-004": ScenarioPreset(
        preset_id="ISLAND-004",
        name="Operation Coral Trident - Island Chain Denial",
        theater="South Maritime Archipelago",
        description=(
            "Adversary amphibious invasion fleet advancing toward Coral Atoll under escort. "
            "Blue surface-to-ship missile batteries and drone swarms must establish sea-denial zone "
            "and intercept landing craft before beachhead establishment."
        ),
        default_objective="Establish sea-denial zone around Coral Atoll, neutralize adversary landing craft, maintain coastal SAM umbrella.",
        default_constraints="No strike operations against mainland staging ports; maintain reserve battery stock above 40%.",
        turn_durations_supported=["30s", "1m", "5m"],
        forces_summary={
            "blue": "4th Coastal Defense Regiment (82 units + Drone Swarm Alpha)",
            "red": "2nd Amphibious Assault Fleet (114 units)"
        },
        terrain="Atoll Barrier Reef, Open Sea Corridors, Island Batteries",
        initial_weather="Tropical storm warnings, 4.0km visibility, 3.5m wave height penalty"
    ),
    "DESERT-005": ScenarioPreset(
        preset_id="DESERT-005",
        name="Operation Sandstorm Guard - Southern Desert Corridor",
        theater="Arid Southern Border Basin",
        description=(
            "Adversary heavy armored corps attempting rapid desert spearhead toward oil refinery hub Alpha. "
            "Blue armored cavalry and anti-tank strike groups tasked with flank interdiction and channel containment."
        ),
        default_objective="Intercept adversary armored spearhead, protect oil refinery hub Alpha, conduct mobile flank interdiction.",
        default_constraints="Maintain fuel supply line security; avoid prolonged stationary engagements in open dunes.",
        turn_durations_supported=["30s", "1m", "5m"],
        forces_summary={
            "blue": "2nd Armored Cavalry Regiment (90 units) at Refinery Alpha",
            "red": "5th Heavy Armored Division (125 units) in Southern Basin"
        },
        terrain="Open Dunes, Salt Flats, High traversability, Zero natural cover",
        initial_weather="Severe dust storm, 1.5km thermal optics visibility, vehicle overheat risk"
    ),
    "CYBER-006": ScenarioPreset(
        preset_id="CYBER-006",
        name="Operation Iron Grid - Hybrid Infrastructure Interdiction",
        theater="Industrial Strategic Core & Command Network",
        description=(
            "Coordinated cyber-physical assault targeting regional power nodes and military command hubs. "
            "Blue hybrid defense forces must maintain grid resilience, secure C2 links, and coordinate air defense interception."
        ),
        default_objective="Secure critical power sub-stations, maintain unbroken C2 link to air defense batteries, mitigate cyber disruption.",
        default_constraints="Preserve civilian power grid capacity above 70%; zero unverified automated fire release.",
        turn_durations_supported=["30s", "1m", "5m"],
        forces_summary={
            "blue": "Cyber-Physical Defense Task Force (65 units + Grid Nodes)",
            "red": "Special Operations & Hybrid Strike Element (70 units)"
        },
        terrain="Industrial Grid Corridors, Command Complex, Substation Nodes",
        initial_weather="Low overcast, 8.0km visibility, high electromagnetic interference"
    ),
    "URBAN-007": ScenarioPreset(
        preset_id="URBAN-007",
        name="Operation Citadel Sentinel - Urban Sector Containment",
        theater="Metropolitan Perimeter & Government Citadel",
        description=(
            "Infiltrating adversarial special forces attempting to isolate government district. "
            "Blue urban infantry and tactical drone units must secure key arterial intersections and prevent perimeter breach."
        ),
        default_objective="Contain adversarial infiltration within Sector 4, secure government citadel bridges, clear urban arterials.",
        default_constraints="Zero heavy artillery usage within urban density zone; minimize civilian collateral risk.",
        turn_durations_supported=["30s", "1m", "5m"],
        forces_summary={
            "blue": "5th Urban Battalion & Tactical SWAT (88 units)",
            "red": "Infiltration Vanguard & Special Recon (62 units)"
        },
        terrain="High-Rise Urban Core, Subsurface Tunnels, Chokepoint Bridges",
        initial_weather="Heavy rain, 3.5km visibility, urban acoustic echo penalty"
    ),
}


def get_preset(preset_id: str) -> ScenarioPreset:
    """Retrieve a preset by ID, defaulting to DEMO-001 if not found."""
    return PRESETS.get(preset_id, PRESETS["DEMO-001"])


def list_presets() -> List[ScenarioPreset]:
    """List all available scenario presets."""
    return list(PRESETS.values())
