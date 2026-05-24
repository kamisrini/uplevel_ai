"""
VP Engineering leadership rubric.

Defines 10 behavioural dimensions with 1-5 scoring descriptors.
Score 1 = early Engineering Manager behaviour.
Score 3 = Senior Engineering Manager / Director behaviour.
Score 5 = VP Engineering behaviour.

The rubric text is cached at the module level so it can be passed as a
cached system prompt to the Anthropic API (reducing repeated inference cost).
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class RubricDimension(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    description: str
    vp_expectation: str
    score_descriptors: dict[int, str]


RUBRIC: list[RubricDimension] = [
    RubricDimension(
        name="strategic_influence",
        description="Shapes organisational direction beyond immediate team.",
        vp_expectation="Defines multi-quarter technical strategy and gains executive buy-in without being asked.",
        score_descriptors={
            1: "Reacts to strategy set by others; no original strategic proposals.",
            2: "Contributes ideas in strategy sessions when prompted.",
            3: "Proposes and owns team-level roadmap; occasionally influences adjacent teams.",
            4: "Drives cross-org technical strategy; seen as a thought leader by peers.",
            5: "Sets engineering-wide strategy; directly influences product and business direction.",
        },
    ),
    RubricDimension(
        name="org_leverage",
        description="Multiplies impact through people, process, and systems rather than personal output.",
        vp_expectation="Every decision and conversation is evaluated for leverage; rarely produces individual output.",
        score_descriptors={
            1: "Output-focused; personal productivity is primary contribution.",
            2: "Delegates some tasks but still heavy individual contributor.",
            3: "Scales through a team of 5-10; removes blockers proactively.",
            4: "Scales through managers; designs systems that outlast any individual.",
            5: "Multiplies entire org capacity; builds leaders who build leaders.",
        },
    ),
    RubricDimension(
        name="delegation_effectiveness",
        description="Assigns work with appropriate context, authority, and accountability.",
        vp_expectation="Delegates entire problem domains with outcomes, not tasks; follows up on commitments not methods.",
        score_descriptors={
            1: "Delegates tasks with step-by-step instructions; micromanages execution.",
            2: "Delegates tasks with clear acceptance criteria.",
            3: "Delegates projects with defined outcomes; available for support.",
            4: "Delegates problem domains; trusts judgment; reviews results not process.",
            5: "Delegates entire capability areas; develops others into domain owners.",
        },
    ),
    RubricDimension(
        name="executive_alignment",
        description="Keeps senior stakeholders informed and aligned without over-communicating.",
        vp_expectation="Proactively surfaces risks, trade-offs, and progress in the format executives need — never a surprise.",
        score_descriptors={
            1: "Rarely communicates upward proactively; escalates only when stuck.",
            2: "Sends status updates when asked; mostly reactive.",
            3: "Regular structured updates to director/VP; highlights key blockers.",
            4: "Tailors communication cadence and format to each executive; surfaces risks early.",
            5: "Drives executive decision-making with crisp framing; no surprises ever.",
        },
    ),
    RubricDimension(
        name="visibility",
        description="Ensures team and personal contributions are known across the organisation.",
        vp_expectation="Engineering impact is visible to product, finance, and CEO without self-promotion; team achievements are amplified.",
        score_descriptors={
            1: "Good work goes unnoticed; uncomfortable with self-promotion.",
            2: "Shares wins within team; limited cross-org visibility.",
            3: "Regularly showcases team work in demos and all-hands.",
            4: "Creates recurring visibility mechanisms (newsletters, showcases, metrics dashboards).",
            5: "Engineering impact is a known narrative at the board level.",
        },
    ),
    RubricDimension(
        name="ambiguity_reduction",
        description="Converts unclear situations into actionable clarity for the organisation.",
        vp_expectation="Comfortable making calls with 60% information; converts ambiguity into crisp problem statements and next steps.",
        score_descriptors={
            1: "Paralysed by ambiguity; escalates frequently for direction.",
            2: "Makes progress in ambiguous spaces but often checks in.",
            3: "Drives clarity on team-scoped problems; documents decisions.",
            4: "Reduces org-wide ambiguity; creates frameworks others use.",
            5: "Thrives in chaos; turns ambiguous mandates into executable strategies.",
        },
    ),
    RubricDimension(
        name="artifact_creation",
        description="Produces durable written artefacts (RFCs, strategy docs, principles) that outlast meetings.",
        vp_expectation="Consistently produces high-quality written artefacts that scale decision-making and onboarding across the org.",
        score_descriptors={
            1: "Rarely writes; knowledge lives in their head.",
            2: "Writes meeting notes and some design docs.",
            3: "Produces RFCs and team-level strategy docs; reasonable quality.",
            4: "Creates org-level principles, playbooks, and frameworks.",
            5: "Written artefacts become canonical references across the company.",
        },
    ),
    RubricDimension(
        name="cross_team_impact",
        description="Drives outcomes that require coordination across multiple teams or departments.",
        vp_expectation="Regularly sponsors and closes cross-functional initiatives; seen as an integrator by peers and product.",
        score_descriptors={
            1: "Focused entirely on own team's deliverables.",
            2: "Coordinates with adjacent teams when blockers arise.",
            3: "Proactively builds relationships with peer teams; resolves cross-team friction.",
            4: "Drives cross-functional programmes; aligns incentives across orgs.",
            5: "Creates structural solutions (platforms, shared services) that improve multiple orgs simultaneously.",
        },
    ),
    RubricDimension(
        name="risk_anticipation",
        description="Identifies and mitigates technical, people, and organisational risks before they materialise.",
        vp_expectation="Maintains a live mental model of org risk; proactively surfaces and plans for risks 1-2 quarters out.",
        score_descriptors={
            1: "Responds to risks after they become incidents.",
            2: "Identifies risks within sprint/iteration cycle.",
            3: "Anticipates quarterly risks; maintains a team risk register.",
            4: "Spots multi-team systemic risks; builds mitigation plans.",
            5: "Maintains a rolling 2-quarter risk radar; drives company-level mitigations.",
        },
    ),
    RubricDimension(
        name="decision_leadership",
        description="Makes and enables high-quality, timely decisions at the right level of the org.",
        vp_expectation="Pushes decisions down to the lowest competent level; reserves personal decision-making for highest-leverage choices.",
        score_descriptors={
            1: "Makes all team decisions personally; bottleneck for team.",
            2: "Delegates some decisions but stays involved in most.",
            3: "Defines decision rights; makes final call on team-level decisions.",
            4: "Creates decision frameworks; empowers managers to decide independently.",
            5: "Decisions below VP level are rare; org has clear autonomy and accountability.",
        },
    ),
]

RUBRIC_BY_NAME: dict[str, RubricDimension] = {d.name: d for d in RUBRIC}

DIMENSION_NAMES: list[str] = [d.name for d in RUBRIC]


def rubric_as_text() -> str:
    """Return the full rubric as a markdown string — used as a cached system prompt."""
    lines = ["# VP Engineering Leadership Rubric\n"]
    for dim in RUBRIC:
        lines.append(f"## {dim.name.replace('_', ' ').title()}")
        lines.append(f"**Description:** {dim.description}")
        lines.append(f"**VP Expectation:** {dim.vp_expectation}")
        lines.append("**Score descriptors:**")
        for score, desc in dim.score_descriptors.items():
            lines.append(f"- {score}/5: {desc}")
        lines.append("")
    return "\n".join(lines)
