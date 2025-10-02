"""Example: Demonstrate elicitation engine with numbered menus."""

from bmad_pydantic_ai import ElicitationEngine


def main():
    """Demonstrate elicitation engine functionality."""
    print("BMAD Elicitation Engine Demo")
    print("=" * 80)
    
    # Initialize engine
    engine = ElicitationEngine()
    
    # Example content to elicit on
    example_content = """
    ## User Authentication
    
    The system shall provide user authentication using email and password.
    Users must verify their email address before accessing the system.
    Password requirements: minimum 8 characters, at least one uppercase letter,
    one lowercase letter, one number, and one special character.
    """
    
    # Create elicitation session for technical content
    print("\n📋 Creating elicitation session for technical content...")
    session = engine.create_session(
        context=example_content,
        content_type="technical"
    )
    
    print(f"✓ Session created with {len(session.available_methods)} methods")
    
    # Display elicitation menu
    print("\n" + "=" * 80)
    print("ELICITATION MENU")
    print("=" * 80)
    menu = engine.format_menu(session)
    print(menu)
    
    # Demonstrate applying a method
    print("\n" + "=" * 80)
    print("APPLYING METHOD: Critique and Refine")
    print("=" * 80)
    
    result = engine.apply_method(
        session,
        "critique-refine",
        example_content
    )
    
    print(f"\n✓ Applied method: {result['method']}")
    print(f"  Description: {result['description']}")
    print(f"  Iteration: {result['iteration']}")
    print(f"\nGenerated prompt:")
    print("-" * 80)
    print(result['prompt'][:500])
    print("...")
    
    # Display session state
    print("\n" + "=" * 80)
    print("SESSION STATE")
    print("=" * 80)
    print(f"Iterations: {session.iteration_count}")
    print(f"Methods applied: {len(session.selected_methods)}")
    print(f"Selected methods: {', '.join(session.selected_methods)}")
    
    # Show different context types
    print("\n" + "=" * 80)
    print("METHOD SELECTION FOR DIFFERENT CONTEXTS")
    print("=" * 80)
    
    contexts = [
        ("technical", "Technical/Architecture content"),
        ("user-facing", "User stories/Requirements"),
        ("strategic", "Strategic planning content"),
        ("creative", "Creative/Design content"),
    ]
    
    for context_type, description in contexts:
        methods = engine.select_methods(context_type, count=8)
        print(f"\n{description}:")
        for idx, method in enumerate(methods, 0):
            print(f"  {idx}. {method.name}")


if __name__ == "__main__":
    main()
