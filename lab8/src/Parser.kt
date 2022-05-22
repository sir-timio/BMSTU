import kotlin.system.exitProcess

class Parser(private val tokens: List<Token>) {
    private var curToken = tokens.first()
    private var ntermsLeft = HashSet<String>()
    private var ntermsRight = HashSet<String>()
    var mapRule = HashMap<String, Rule>()
    private var curState = ""
    private var states = mutableListOf<String>()

    fun parse() {
        parseExprs()
//        mapRule.forEach { key, value -> println("<$key $value>") }
        if (!ntermsLeft.containsAll(ntermsRight)) {
            println("Undefined NTERMs:")
            println(ntermsRight - ntermsLeft)
            exit()
        }
    }
    //    S ::= R S | .
    //    R ::= <OPEN> <NTERM> A <CLOSE>
    //    A ::= <OPEN> E <CLOSE> A | .
    //    E ::= <NTERM> E | <TERM> E | <OPEN> I <CLOSE> E | <IOPEN> E <ICLOSE> E | .
    //    I ::= <OPEN> E <CLOSE> I | .

    /*
        Exprs = Expr { Expr }
        Expr = <OPEN> NonTerm Alt <CLOSE>
        Alt = "(" Rp { Rp } { "," Rp { Rp } } ")"
        Rp = NonTerm | Term | "{" Rp { Rp } "}" | Alt
     */

    private fun parseExprs() {
        parseExpr()
        while (curToken.tag == DomainTag.OPEN) {
            parseExpr()
        }
        if (curToken.tag != DomainTag.EOP)
            exit()
    }

//    Expr = <OPEN> NTerm Alt <CLOSE>
    private fun parseExpr() {
        if (curToken.tag == DomainTag.OPEN) {
            nextToken()
            if (curToken.tag != DomainTag.NTERM)
                exit()
            val nterm = curToken.value
            val rule = Rule(RuleTag.Normal, null)
            ntermsLeft.add(nterm)
            nextToken()
            parseAlt(rule)
        }
    }

//    Alt = <OPEN> Rp { Rp } { Rp { Rp } } <CLOSE>
    private fun parseAlt(rule: Rule) {
        if (curToken.tag == DomainTag.OPEN) {
            val subRule = Rule(RuleTag.Normal, null)
            nextToken()
            parseRp(subRule)
        }
    }

    private fun parseRp(rule: Rule) {

    }



    private fun nextToken() {
        val index = tokens.indexOf(curToken)
        curToken = tokens[index + 1]
//        print("curToken: $curToken on state $curState\n")
    }



    private fun printNextTokens() {
        println("Next tokens! :")
        val index = tokens.indexOf(curToken)
        for (i in index until tokens.size)
            println(tokens[i])
        println("End of next tokens! ")
    }

    private fun exit() {
        println("ERROR")
        println("On token: $curToken")
        println(curState)
//        println("passed states: $states")
        exitProcess(0)
    }
}