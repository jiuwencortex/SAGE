from ...scenario import Scenario
from .._oracle_builder import build_oracle_from_examples
from .skill.body import SKILL_BODY
from .skill.frontmatter import SKILL_FRONTMATTER
from .golden_examples.all import GOLDEN_EXAMPLES


def load_scenario():
    name = get_scenario_name()
    return Scenario(
            name=name,
            skill_body=SKILL_BODY,
            skill_frontmatter=SKILL_FRONTMATTER,
            description="SmartHub customer support — generic baseline vs product-specific knowledge (exec demo scenario)",
            loader=lambda n, seed: GOLDEN_EXAMPLES,
            oracle_builder=lambda d, n, ow: build_oracle_from_examples(d, name, GOLDEN_EXAMPLES, ow),
            oracle_skill_name=name,
            sample_query=GOLDEN_EXAMPLES[0]["task_input"],
        )


def get_scenario_name():
    return "smarthub-support"
