import java.io.File


fun main() {
    val file = File("test_2.txt")
    val lexer = Lexer(file.readText())
    val tokens = mutableListOf<Token>()
    do {
        val token = lexer.nextToken()
        tokens += token
    } while (token.tag != DomainTag.EOP)
    val parser = Parser(tokens)
    parser.parse()

    val first = First(parser.mapRule)
    first.printFirst()
}

