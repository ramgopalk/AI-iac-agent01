from rich.console import Console
from rich.panel import Panel

from config import validate_config
from agent.agent import AzureAgent


console = Console()


def main():

    validate_config()

    agent = AzureAgent()

    console.print(
        Panel.fit(
            "Azure Terraform AI Agent Started",
            style="bold green"
        )
    )

    console.print(
        "[bold yellow]Type 'exit' to quit[/bold yellow]\n"
    )

    while True:

        user_input = console.input(
            "[bold cyan]You > [/bold cyan]"
        )

        if user_input.lower() == "exit":
            break

        try:

            response = agent.chat(user_input)

            console.print(
                f"\n[bold green]Agent > [/bold green]{response}\n"
            )

        except Exception as e:

            console.print(
                f"\n[bold red]ERROR:[/bold red] {str(e)}\n"
            )


if __name__ == "__main__":
    main()