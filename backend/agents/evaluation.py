"""
Evaluation Agent.
Analyzes simulation results against objectives, constraints, and strategic stakes.
Detects emergent events, decides continuation vs conclusion, and produces ScenarioTransition.
"""

from typing import Tuple, Optional
from rich import print

from backend.schemas.contracts import (
    ScenarioContract,
    SimulationOutput,
    EvaluationOutput,
    EvaluationAssessment,
    SimulationControl,
    NextScenarioRecommendation,
    EmergentEvent,
    ScenarioTransition,
    TransitionNextScenario,
)
from backend.llm.wrapper import invoke_structured, is_fallback_allowed


def compute_next_scenario_id(current_id: str) -> str:
    """Deterministically computes sub-turn scenario ID (e.g. 1.0 -> 1.1 -> 1.2 -> 1.3)."""
    if not current_id or current_id == "NONE":
        return "1.1"
    if "." in current_id:
        parts = current_id.rsplit(".", 1)
        try:
            val = int(parts[1])
            return f"{parts[0]}.{val + 1}"
        except ValueError:
            return f"{current_id}.1"
    else:
        return f"{current_id}.1"


class EvaluationAgent:
    def __init__(self):
        self.role = "evaluation"

    def _deterministic_fallback(
        self,
        contract: ScenarioContract,
        sim_output: SimulationOutput,
        iteration_count: int,
        max_iterations: int
    ) -> EvaluationOutput:
        """Deterministic resilient fallback for Evaluation assessment."""
        is_sim_terminal = bool(sim_output.terminal or (sim_output.termination and sim_output.termination.terminal) or sim_output.status == "TERMINATED")
        concluded = is_sim_terminal or (iteration_count >= max_iterations)
        next_id = f"{contract.scenario_id}.1" if "." not in contract.scenario_id else f"{contract.scenario_id[:-1]}{int(contract.scenario_id[-1])+1}"

        conclusion_text = (
            f"Scenario {contract.scenario_id} reached terminal state: {sim_output.termination.condition} ({sim_output.termination.reason})."
            if is_sim_terminal else
            f"Scenario {contract.scenario_id} demonstrated that Blue's fortified redoubt at LOC-ALPHA successfully deterred the adversary from breaking across the river line. Casualties remained below the critical threshold."
        )

        return EvaluationOutput(
            agent="evaluation",
            scenario_id=contract.scenario_id,
            simulation_id=sim_output.simulation_id,
            assessment=EvaluationAssessment(
                objective_results=str(sim_output.objective_results),
                blue_performance=f"Losses: {sim_output.metrics.get('blue', {}).get('losses_percentage', 6.0)}% - TACTICAL_DEFENSE_SOUND",
                red_performance=f"Losses: {sim_output.metrics.get('red', {}).get('losses_percentage', 10.0)}% - OFFENSIVE_IMPEDED",
                resource_effects=str(sim_output.resource_changes),
                risks=[
                    "Stalemate at river line leaves supply road vulnerable to long-range harassment",
                    "Ammunition expenditure rate threatens sustained defensive posture in prolonged conflict"
                ],
                tradeoffs=[
                    "Static entrenchment protected personnel but conceded operational initiative north of the river",
                    "Concentrating forces at the bridgehead thinned coverage along secondary mountain routes"
                ],
                uncertainties=[
                    "Adversary reserve deployment along alternate mountain passes",
                    "Duration of monsoon-induced river swelling affecting bridging operations"
                ],
                strategic_implications=[
                    "Adversary offensive tempo significantly degraded for next 48 hours",
                    "Diplomatic leverage enhanced due to successful territorial defense"
                ]
            ),
            emergent_events=[
                EmergentEvent(
                    event_id="EVT-001",
                    type="diplomatic_development",
                    description="Third-party UN peace envoy proposes a 24-hour tactical pause." if not is_sim_terminal else "Catastrophic event observed across theater.",
                    impact="May freeze current positions and allow replenishment." if not is_sim_terminal else "Terminal outcome acknowledged.",
                    requires_response=not is_sim_terminal
                )
            ],
            simulation_control=SimulationControl(
                concluded=concluded,
                termination_reason=sim_output.termination.reason if is_sim_terminal else ("Target wargaming objectives and comparison threshold reached" if concluded else None),
                continue_reason="Unresolved standoff and emergent developments require next scenario iteration" if not concluded else "",
                next_scenario_required=not concluded
            ),
            next_scenario=NextScenarioRecommendation(
                scenario_id=next_id if not concluded else "NONE",
                parent_scenario_id=contract.scenario_id,
                reason="Incorporate diplomatic mediation rules and evaluate Blue posture under ceasefire constraints." if not concluded else "Terminal condition reached; no subsequent scenario.",
                required_changes=["Adjust Rules of Engagement", "Include UN mediator parameters"] if not concluded else [],
                required_information=["Red military command's adherence verification"] if not concluded else []
            ),
            strategic_conclusion=conclusion_text,
            human_review_required=True,
            dynamic={"source": "deterministic_fallback"}
        )

    def evaluate(
        self,
        contract: ScenarioContract,
        sim_output: SimulationOutput,
        iteration_count: int = 1,
        max_iterations: int = 2
    ) -> Tuple[EvaluationOutput, Optional[ScenarioTransition]]:
        """
        Evaluates simulation output and constructs evaluation assessment + transition contract.
        """
        system_prompt = (
            "You are the EVALUATION AGENT of the NIRNAY strategic wargaming platform.\n"
            "Analyze simulation metrics, losses, and objective completions.\n"
            "In your assessment, you MUST provide:\n"
            "- objective_results: clear summary of outcome against mission goals\n"
            "- blue_performance: detailed analysis of Blue tactical execution and resilience\n"
            "- red_performance: detailed analysis of Red offensive capability and attrition\n"
            "- resource_effects: assessment of supply, ammunition, and infrastructure state\n"
            "- risks: at least 2-3 specific operational, tactical, or strategic risks arising from this outcome\n"
            "- tradeoffs: at least 2-3 key tactical or strategic tradeoffs accepted during the engagement\n"
            "- uncertainties: at least 2 critical intelligence, operational, or environmental unknowns\n"
            "- strategic_implications: at least 2 broader implications for future scenario iterations\n"
            "Identify emergent events, decide simulation control (conclude vs continue), and recommend next scenario steps.\n"
            "CRITICAL: If the simulation is terminal or forces are annihilated, set simulation_control.concluded to true.\n"
            "Output MUST strictly adhere to the EvaluationOutput schema."
        )

        user_prompt = (
            f"Scenario: {contract.scenario_id}\n"
            f"Simulation Results: {sim_output.model_dump()}\n"
            f"Original Objectives: {contract.objectives.model_dump()}\n"
            f"Iteration: {iteration_count} of {max_iterations}\n"
        )

        try:
            eval_output = invoke_structured(
                role=self.role,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                schema=EvaluationOutput,
                temperature=0.2
            )
            # Invariant: If simulation reached a terminal condition, it is authoritative and CANNOT be overridden
            is_sim_terminal = bool(sim_output.terminal or (sim_output.termination and sim_output.termination.terminal) or sim_output.status == "TERMINATED")
            if is_sim_terminal:
                eval_output.simulation_control.concluded = True
                eval_output.simulation_control.next_scenario_required = False
                eval_output.simulation_control.termination_reason = sim_output.termination.reason or sim_output.termination.condition
            elif iteration_count < max_iterations:
                b_loss = sim_output.metrics.get("blue", {}).get("losses_percentage", 0.0)
                r_loss = sim_output.metrics.get("red", {}).get("losses_percentage", 0.0)
                if b_loss < 100.0 and r_loss < 100.0:
                    eval_output.simulation_control.concluded = False
                    eval_output.simulation_control.next_scenario_required = True
        except Exception as e:
            if not is_fallback_allowed():
                raise e
            print(f"[bold yellow][AGENT WARNING][/bold yellow] Evaluation LLM failed: {e}. Using deterministic fallback.")
            eval_output = self._deterministic_fallback(contract, sim_output, iteration_count, max_iterations)

        # Enforce Simulator terminal authority on eval_output unconditionally
        is_sim_terminal = bool(sim_output.terminal or (sim_output.termination and sim_output.termination.terminal) or sim_output.status == "TERMINATED")
        if is_sim_terminal:
            eval_output.simulation_control.concluded = True
            eval_output.simulation_control.next_scenario_required = False
            eval_output.simulation_control.termination_reason = sim_output.termination.reason or sim_output.termination.condition
        else:
            is_max_turns = iteration_count >= max_iterations
            eval_output.simulation_control.concluded = is_max_turns
            eval_output.simulation_control.next_scenario_required = not is_max_turns
            eval_output.simulation_control.termination_reason = "Maximum turns reached" if is_max_turns else None

        # Build ScenarioTransition for turn lineage progression
        next_id = compute_next_scenario_id(contract.scenario_id) if not eval_output.simulation_control.concluded else "NONE"

        transition = ScenarioTransition(
            transition_id=f"TRANS-{contract.scenario_id}",
            current_scenario_id=contract.scenario_id,
            transition_type="CONTINUE" if not eval_output.simulation_control.concluded else "CONCLUDE",
            reason=eval_output.next_scenario.reason if (eval_output.next_scenario and not eval_output.simulation_control.concluded) else (sim_output.termination.reason or "Simulation concluded"),
            evaluation_summary=eval_output.strategic_conclusion,
            emergent_events=[ev.model_dump() for ev in eval_output.emergent_events],
            required_changes=eval_output.next_scenario.required_changes if (eval_output.next_scenario and not eval_output.simulation_control.concluded) else [],
            new_information=eval_output.next_scenario.required_information if (eval_output.next_scenario and not eval_output.simulation_control.concluded) else [],
            human_input=["Review tactical developments and issue strategic guidance"],
            next_scenario=TransitionNextScenario(
                requested=not eval_output.simulation_control.concluded,
                scenario_id=next_id,
                parent_scenario_id=contract.scenario_id
            )
        )

        return eval_output, transition
