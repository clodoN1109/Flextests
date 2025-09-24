class CLIHelp:
    @staticmethod
    def cli_help() -> str:
        """Prints an organized description of how to use the CLI interface."""

        help_text = """
    =====================================================
                    FLEXTESTS CLI HELP
    =====================================================

    Available Commands:
        """

        commands_info = {
            "help": {
                "desc": "Displays this help message.",
                "syntax": "help"
            },
            "gui": {
                "desc": "Launches the GUI.",
                "syntax": "gui"
            },
            "new-test": {
                "desc": "Creates a new test.",
                "syntax": "new-test <test_name> [description]"
            },
            "new-sim": {
                "desc": "Creates a new simulation.",
                "syntax": "new-sim <simulation_name> <script_path> [description]"
            },
            "set-sim": {
                "desc": "Assigns a simulation to a test.",
                "syntax": "set-sim <test_name> <simulation_name>"
            },
            "run-sim": {
                "desc": "Runs a simulation.",
                "syntax": "run-sim <simulation_name>"
            },
            "run-test": {
                "desc": "Runs a test with optional repetitions.",
                "syntax": "run-test <test_name> [repetitions]"
            },
            "set-criterion": {
                "desc": "Sets a criterion for a test.",
                "syntax": "set-criterion <test_name> <criterion_name> <criterion_value>"
            },
            "set-ref": {
                "desc": "Sets reference values for a test.",
                "syntax": "set-ref <test_name> [reference_source] [breadth]"
            },
        }

        for cmd, info in commands_info.items():
            help_text += (
                f"\n    - {cmd}"
                f"\n        Description: {info['desc']}"
                f"\n        Syntax     : {info['syntax']}\n"
            )

        help_text += """
    =====================================================
        """
        return help_text

