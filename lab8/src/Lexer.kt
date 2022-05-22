import kotlin.system.exitProcess

class Lexer(program: String) {
    private var position = Position(program)

    fun nextToken(): Token {
        while (!position.isEOF()) {
            while (position.isWhiteSpace())
                position = position.next()

            if (position.isEOF())
                break

            val token = when (position.getCode().toChar()) {
                '<', '>', '{', '}'                               -> readSpecialToken(position)
                in 'A'..'Z'                                 -> readNterm(position)
                '*', '/', '+', '-', '(', ')',  in 'a'..'z'  -> readTerm(position)
                else                                             -> readUnknownToken(position)

            }

            position = token.coords.following

            return token
        }
        return Token(DomainTag.EOP,
            Fragment(position, position),
            "")
    }

    private fun readUnknownToken(position: Position): Token  {
        println("ERROR ${Fragment(position, position)}: unrecognized token")
        exitProcess(0)
    }

    private fun readSpecialToken(position: Position): Token {
        val tag = when (position.getCurSymbol()) {
            '<' -> DomainTag.OPEN
            '>' -> DomainTag.CLOSE
            '{' -> DomainTag.IOPEN
            '}' -> DomainTag.ICLOSE
            else -> DomainTag.UNK
        }
        return Token(tag,
            Fragment(position, position.next()),
            position.getCurSymbol().toString())
    }

    private fun readNterm(position: Position): Token {
        return Token(DomainTag.NTERM,
            Fragment(position, position.next()),
            position.getCurSymbol().toString())
    }

    private fun readTerm(position: Position): Token {
        return Token(DomainTag.TERM,
            Fragment(position, position.next()),
            position.getCurSymbol().toString())
    }
}