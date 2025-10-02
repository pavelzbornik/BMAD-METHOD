"""Elicitation engine for interactive multi-turn workflows."""

from typing import List, Optional

from ..models import ElicitationMethod, ElicitationSession


class ElicitationEngine:
    """Drive BMAD advanced elicitation workflows with numbered menus."""

    # Predefined elicitation methods based on BMAD advanced-elicitation.md
    CORE_METHODS = [
        ElicitationMethod(
            id="expand-contract",
            name="Expand or Contract for Audience",
            description="Adjust detail level for different audiences",
            category="core",
            context_types=["all"],
        ),
        ElicitationMethod(
            id="critique-refine",
            name="Critique and Refine",
            description="Critical analysis and improvement suggestions",
            category="core",
            context_types=["all"],
        ),
        ElicitationMethod(
            id="identify-risks",
            name="Identify Potential Risks",
            description="Assess risks and mitigation strategies",
            category="core",
            context_types=["all"],
        ),
        ElicitationMethod(
            id="assess-alignment",
            name="Assess Alignment with Goals",
            description="Verify alignment with project goals",
            category="core",
            context_types=["all"],
        ),
    ]

    TECHNICAL_METHODS = [
        ElicitationMethod(
            id="tree-of-thoughts",
            name="Tree of Thoughts",
            description="Explore multiple reasoning paths",
            category="technical",
            context_types=["technical", "architecture", "design"],
        ),
        ElicitationMethod(
            id="rewoo",
            name="ReWOO Analysis",
            description="Reasoning without observation - plan then execute",
            category="technical",
            context_types=["technical", "complex"],
        ),
        ElicitationMethod(
            id="meta-prompting",
            name="Meta-Prompting",
            description="Generate improved prompts for the task",
            category="technical",
            context_types=["technical", "requirements"],
        ),
    ]

    COLLABORATIVE_METHODS = [
        ElicitationMethod(
            id="agile-team-perspective",
            name="Agile Team Perspective",
            description="Review from different agile role perspectives",
            category="collaborative",
            context_types=["user-facing", "stories", "requirements"],
        ),
        ElicitationMethod(
            id="stakeholder-roundtable",
            name="Stakeholder Roundtable",
            description="Multi-stakeholder discussion simulation",
            category="collaborative",
            context_types=["strategic", "user-facing"],
        ),
        ElicitationMethod(
            id="red-team-blue-team",
            name="Red Team vs Blue Team",
            description="Adversarial review from opposing perspectives",
            category="collaborative",
            context_types=["security", "strategic", "architecture"],
        ),
    ]

    CREATIVE_METHODS = [
        ElicitationMethod(
            id="innovation-tournament",
            name="Innovation Tournament",
            description="Generate and compete alternative approaches",
            category="creative",
            context_types=["creative", "design", "strategic"],
        ),
        ElicitationMethod(
            id="escape-room-challenge",
            name="Escape Room Challenge",
            description="Find creative solutions to constraints",
            category="creative",
            context_types=["creative", "problem-solving"],
        ),
        ElicitationMethod(
            id="hindsight-reflection",
            name="Hindsight Reflection",
            description="Post-mortem from future perspective",
            category="strategic",
            context_types=["strategic", "planning"],
        ),
    ]

    def __init__(self):
        """Initialize elicitation engine."""
        self.all_methods = (
            self.CORE_METHODS
            + self.TECHNICAL_METHODS
            + self.COLLABORATIVE_METHODS
            + self.CREATIVE_METHODS
        )

    def select_methods(
        self, content_type: str, complexity: str = "moderate", count: int = 8
    ) -> List[ElicitationMethod]:
        """Select appropriate elicitation methods for context.
        
        Args:
            content_type: Type of content (technical, user-facing, strategic, etc.)
            complexity: Complexity level (simple, moderate, complex)
            count: Number of methods to select (default 8, plus "Proceed" makes 9)
            
        Returns:
            List of selected ElicitationMethod objects
        """
        selected = []

        # Always include 3-4 core methods
        selected.extend(self.CORE_METHODS[:4])

        # Add context-specific methods
        for method in self.all_methods:
            if len(selected) >= count:
                break
            if method not in selected and content_type in method.context_types:
                selected.append(method)

        # Fill remaining slots with other methods
        for method in self.all_methods:
            if len(selected) >= count:
                break
            if method not in selected:
                selected.append(method)

        return selected[:count]

    def create_session(
        self, context: str, content_type: str = "general"
    ) -> ElicitationSession:
        """Create a new elicitation session.
        
        Args:
            context: Context or content to elicit on
            content_type: Type of content
            
        Returns:
            New ElicitationSession
        """
        methods = self.select_methods(content_type)
        return ElicitationSession(
            context=context, content_type=content_type, available_methods=methods
        )

    def format_menu(self, session: ElicitationSession) -> str:
        """Format elicitation menu for display.
        
        Args:
            session: Current elicitation session
            
        Returns:
            Formatted menu string
        """
        lines = [
            "## Elicitation Options",
            "",
            "Select a method to apply (type the number):",
            "",
        ]

        for idx, method in enumerate(session.available_methods):
            lines.append(f"{idx}. **{method.name}**")

        lines.append(f"{len(session.available_methods)}. **Proceed / No Further Actions**")
        lines.append("")
        lines.append(
            "Type the number to select an option, or suggest direct changes to the content."
        )

        return "\n".join(lines)

    def apply_method(
        self, session: ElicitationSession, method_id: str, content: str
    ) -> dict:
        """Apply an elicitation method to content.
        
        Args:
            session: Current elicitation session
            method_id: ID of method to apply
            content: Content to apply method to
            
        Returns:
            Result dictionary with prompts and context
        """
        method = next((m for m in session.available_methods if m.id == method_id), None)
        if not method:
            raise ValueError(f"Method not found: {method_id}")

        session.selected_methods.append(method_id)
        session.iteration_count += 1

        return {
            "method": method.name,
            "description": method.description,
            "prompt": self._generate_method_prompt(method, content),
            "iteration": session.iteration_count,
        }

    def _generate_method_prompt(self, method: ElicitationMethod, content: str) -> str:
        """Generate prompt for applying elicitation method.
        
        Args:
            method: Elicitation method to apply
            content: Content to apply method to
            
        Returns:
            Generated prompt string
        """
        prompts = {
            "expand-contract": f"Review this content and adjust the detail level. Identify areas that could be expanded for technical audiences or simplified for non-technical stakeholders:\n\n{content}",
            "critique-refine": f"Critically analyze this content. Identify weaknesses, gaps, or areas for improvement:\n\n{content}",
            "identify-risks": f"Identify potential risks, issues, or challenges with this content. Suggest mitigation strategies:\n\n{content}",
            "assess-alignment": f"Assess how well this content aligns with the project goals and requirements. Identify any misalignments:\n\n{content}",
            "tree-of-thoughts": f"Explore multiple reasoning paths for this content. Consider at least 3 different approaches or perspectives:\n\n{content}",
            "agile-team-perspective": f"Review this content from the perspective of different agile roles (PM, Dev, QA, UX). What would each role notice or question?\n\n{content}",
            "stakeholder-roundtable": f"Simulate a stakeholder discussion about this content. Consider different stakeholder perspectives and concerns:\n\n{content}",
            "red-team-blue-team": f"Review this content from adversarial perspectives. Blue team defends, red team critiques and finds vulnerabilities:\n\n{content}",
        }

        return prompts.get(
            method.id,
            f"Apply {method.name} ({method.description}) to this content:\n\n{content}",
        )
