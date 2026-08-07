from parsers.docker_parser import docker_parser


class ParserManager:

    def parse(self, command: str, output: str):

        if command == "docker ps":
            return docker_parser.parse_ps(output)

        return output


parser_manager = ParserManager()