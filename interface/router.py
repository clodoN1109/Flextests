from interface.CLI.input.cli_controller import CLIController
from interface.CLI.input.cli_preprocessor import InputPreProcessor


class Router:

    @staticmethod
    def execute(args):
        preprocessed_args = [InputPreProcessor(option)
                             .normalize()
                             .get_result()
                             for option in args[1:]]
        command = preprocessed_args[0]
        args = preprocessed_args[1:]

        CLIController().execute(command, args)