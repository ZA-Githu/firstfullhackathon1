"""ChapterGenerationSkill — generate or expand a textbook chapter using Claude.

Produces structured Markdown strictly aligned with the Physical AI & Humanoid
Robotics course outline (ROS 2, Gazebo/Unity, NVIDIA Isaac, VLA, hardware).
"""
from __future__ import annotations

import anthropic

from app.config import get_settings

# Full course module catalogue — used as grounding context for generation.
COURSE_OUTLINE = """
Physical AI & Humanoid Robotics — Course Modules:

Module 1: Introduction to Physical AI & Robotics
  - What is Physical AI; difference from software AI
  - Humanoid robot landscape (Unitree H1/G1, Boston Dynamics, Tesla Optimus)
  - Hardware overview: Jetson Orin Nano, RTX GPUs, Unitree robots

Module 2: ROS 2 Fundamentals
  - ROS 2 architecture: nodes, topics, services, actions
  - DDS middleware; QoS policies
  - Writing ROS 2 nodes in Python & C++
  - Nav2: navigation stack; costmaps, planners, behaviours

Module 3: Simulation — Gazebo & Unity
  - Gazebo Harmonic: world building, sensors, plugins
  - Unity Robotics Hub: articulation bodies, ROS-TCP connector
  - Sim-to-real transfer strategies

Module 4: NVIDIA Isaac Platform
  - Isaac Sim: physics-accurate simulation on Omniverse
  - Isaac ROS: hardware-accelerated perception packages
  - Isaac Lab: reinforcement learning for locomotion & manipulation

Module 5: Vision-Language-Action (VLA) Models
  - Foundation models for robotics: RT-2, OpenVLA, π0
  - Training VLAs on robot data
  - Deploying VLAs on Jetson Orin Nano

Module 6: Weekly Breakdown & Assessments
  - Week-by-week project milestones
  - Capstone: building an autonomous humanoid behaviour

Hardware Reference:
  - Jetson Orin Nano: 40 TOPS, 8 GB, compact form-factor
  - RTX 4090/5090: local training & Isaac Sim acceleration
  - Unitree G1/H1: full-body humanoid; SDK & Python API
"""

CHAPTER_SYSTEM = (
    "You are an expert technical author writing chapters for the "
    "Physical AI & Humanoid Robotics interactive textbook.\n"
    "Rules:\n"
    "1. Write ONLY content that belongs in this textbook — no unrelated topics.\n"
    "2. Use Markdown: ## for sections, ### for subsections, ``` for code blocks.\n"
    "3. Include at least one code example (Python or CLI) per major section.\n"
    "4. Keep explanations clear for engineers with software backgrounds but limited robotics knowledge.\n"
    "5. End every chapter with a ## Summary and ## Further Reading section.\n\n"
    f"Course Outline (for grounding):\n{COURSE_OUTLINE}"
)


async def run_chapter_generation_skill(
    module: str,
    section: str | None = None,
    expand_existing: str | None = None,
    word_target: int = 800,
) -> dict:
    """Generate or expand a chapter/section.

    Args:
        module: Module name or number, e.g. "Module 2: ROS 2 Fundamentals".
        section: Optional specific section within the module.
        expand_existing: Existing Markdown to expand rather than generate fresh.
        word_target: Approximate word count for the output.

    Returns:
        dict with keys: markdown, module, section, word_count
    """
    settings = get_settings()
    client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

    if expand_existing:
        user_msg = (
            f"Expand and improve the following draft section of {module}"
            + (f" — {section}" if section else "")
            + f" to approximately {word_target} words.\n\n"
            f"Existing draft:\n{expand_existing}"
        )
    else:
        target = f"{module}" + (f" — {section}" if section else "")
        user_msg = (
            f"Write a complete textbook chapter for: **{target}**.\n"
            f"Target length: ~{word_target} words.\n"
            "Include practical examples, code snippets, and diagrams described in Markdown."
        )

    stream = client.messages.stream(
        model="claude-opus-4-6",
        max_tokens=4096,
        thinking={"type": "adaptive"},
        system=CHAPTER_SYSTEM,
        messages=[{"role": "user", "content": user_msg}],
    )

    final = await stream.get_final_message()
    markdown = next(
        (b.text for b in final.content if b.type == "text"), ""
    )

    return {
        "markdown": markdown,
        "module": module,
        "section": section or "",
        "word_count": len(markdown.split()),
    }
