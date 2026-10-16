from __future__ import annotations

from agents import Agent, Runner, RunConfig, trace

from team_agents import product_manager, developer
from models import GroupChatContext, SprintPhase, SpeakerRole

SPEAKER_MAP: dict[SpeakerRole, Agent] = {
    SpeakerRole.PRODUCT_MANAGER: product_manager,
    SpeakerRole.DEVELOPER: developer,
}

TURN_ORDER = [
    SpeakerRole.PRODUCT_MANAGER,
    SpeakerRole.DEVELOPER,
]


def _print_turn(speaker: SpeakerRole, message: str, turn: int) -> None:
    print(f"\n[Turn {turn}] {speaker.value}")
    print("--" * 25)
    for line in message.split("\n"):
        print(f"  {line}")


def _detect_termination(output: str) -> bool:
    for line in reversed(output.strip().split("\n")):
        stripped = line.strip()
        if stripped.upper() == "TERMINATE":
            return True
        if stripped:
            return False
    return False


def _advance_phase(ctx: GroupChatContext) -> None:
    if ctx.current_phase == SprintPhase.REQUIREMENTS and ctx.requirements:
        ctx.current_phase = SprintPhase.IMPLEMENTATION
    elif ctx.current_phase == SprintPhase.IMPLEMENTATION and ctx.code.files:
        ctx.current_phase = SprintPhase.TESTING
    elif ctx.current_phase == SprintPhase.TESTING and ctx.all_tests_passed:
        ctx.current_phase = SprintPhase.DONE


async def run_group_chat(
    feature_request: str,
    max_turns: int = 24,
) -> GroupChatContext:
    print(f"\n{'=' * 60}")
    print("  Collaborative Software Engineering Group Chat")
    print(f"{'=' * 60}\n")
    print(f"  Feature: {feature_request}\n")

    ctx = GroupChatContext(feature_request=feature_request, max_turns=max_turns)
    current_speaker = SpeakerRole.PRODUCT_MANAGER
    run_config = RunConfig(workflow_name="GroupChat")

    with trace("GroupChat"):
        for turn in range(1, max_turns + 1):
            ctx.turn_count = turn
            agent = SPEAKER_MAP[current_speaker]

            if not ctx.conversation_log:
                user_input = (
                    f"Feature request: {feature_request}\n\n"
                    "Define requirements for this feature."
                )
            else:
                last_msg = ctx.conversation_log[-1]["message"]
                user_input = (
                    f"[Turn {turn} -- {current_speaker.value}]\n\n"
                    f"Previous message:\n{last_msg}\n\n"
                    "Continue the discussion. Respond in your role."
                )

            print(f"  {current_speaker.value} is thinking...")

            try:
                result = await Runner.run(
                    starting_agent=agent,
                    input=user_input,
                    context=ctx,
                    max_turns=10,
                    run_config=run_config,
                )
            except Exception as exc:
                print(f"\n  Agent error: {exc}")
                break

            output = str(result.final_output) if result.final_output else "(no output)"
            ctx.log(current_speaker, output)
            _print_turn(current_speaker, output, turn)

            if _detect_termination(output):
                print(f"{'=' * 60}")
                print(f"  TERMINATE received. Sprint done in {turn} turns.")
                print(f"{'=' * 60}\n")
                ctx.terminate = True
                ctx.current_phase = SprintPhase.DONE
                break

            _advance_phase(ctx)

            idx = (TURN_ORDER.index(current_speaker) + 1) % len(TURN_ORDER)
            current_speaker = TURN_ORDER[idx]

        else:
            print(f"\n  Max turns ({max_turns}) reached. Stopping.\n")
            ctx.terminate = True

    return ctx


def print_summary(ctx: GroupChatContext) -> None:
    print(f"\n{'=' * 60}")
    print("  SPRINT SUMMARY")
    print(f"{'=' * 60}")
    print(f"  Feature:  {ctx.feature_request}")
    print(f"  Phase:    {ctx.current_phase.value}")
    print(f"  Turns:    {ctx.turn_count}")
    print(f"  Tests OK: {ctx.all_tests_passed}")

    if ctx.requirements:
        print("\n  Requirements:")
        for r in ctx.requirements:
            print(f"    - [{r.id}] {r.title}: {r.description[:80]}")

    if ctx.code.files:
        print("\n  Code Files:")
        for fname in ctx.code.files:
            print(f"    - {fname}")

    if ctx.test_results:
        print("\n  Test Results:")
        for tr in ctx.test_results:
            status = "PASS" if tr.passed else "FAIL"
            print(f"    - {tr.test_file}: {status}")

    print(f"\n{'=' * 60}\n")


def save_output_to_file(ctx: GroupChatContext, filename: str = "sprint_output.md") -> str:
    lines = [
        "# Sprint Output\n",
        f"## Feature: {ctx.feature_request}\n",
        f"**Phase:** {ctx.current_phase.value}  ",
        f"**Turns:** {ctx.turn_count}  ",
        f"**Tests Passed:** {ctx.all_tests_passed}\n",
    ]

    if ctx.requirements:
        lines.append("## Requirements\n")
        for r in ctx.requirements:
            lines.append(f"- **[{r.id}] {r.title}**: {r.description}")
            for ac in r.acceptance_criteria:
                lines.append(f"  - {ac}")
        lines.append("")

    if ctx.code.files:
        lines.append("## Code\n")
        for fname, content in ctx.code.files.items():
            lines.append(f"### {fname}\n")
            lines.append(f"```python\n{content}\n```\n")

    if ctx.test_results:
        lines.append("## Test Results\n")
        for tr in ctx.test_results:
            status = "PASS" if tr.passed else "FAIL"
            lines.append(f"- **{tr.test_file}**: {status} ({tr.total_tests} tests, {tr.failures} failures, {tr.errors} errors)")
        lines.append("")

    lines.append("## Conversation Log\n")
    for entry in ctx.conversation_log:
        lines.append(f"### Turn {entry['turn']} - {entry['speaker']}\n")
        lines.append(f"{entry['message']}\n")

    content = "\n".join(lines)
    with open(filename, "w") as f:
        f.write(content)

    return filename
