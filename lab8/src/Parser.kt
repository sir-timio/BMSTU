import kotlin.system.exitProcess

class Parser(private val tokens: List<Token>) {
    private var curToken = tokens.first()
    private var ntermsLeft = HashSet<String>()
    private var ntermsRight = HashSet<String>()
    var mapRule = HashMap<String, Rule>()
    private var curState = ""
    private var states = mutableListOf<String>()

    fun parse() {
        parseS()
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

    //    S -> R S | .
    private fun parseS() {
        curState = "S"
        states.add(curState)

    if (curToken.tag == DomainTag.EOP) {
            return
        }
        parseR()
        parseS()
    }

    //    R -> <OPEN> <NTERM> A <CLOSE>
    private fun parseR() {
        curState = "R"
        states.add(curState)


        if (curToken.tag != DomainTag.OPEN) exit()
        nextToken()

        if (curToken.tag != DomainTag.NTERM) exit()
        val left = curToken
        val rule = Rule(RuleTag.Token, null)
        ntermsLeft.add(left.value)

        nextToken()

        parseA(rule)
        mapRule[left.value] = rule
        if (curToken.tag != DomainTag.CLOSE) exit()
        nextToken()
}

    //    A -> <OPEN> E <CLOSE> A | .
    private fun parseA(rule: Rule) {
        curState = "A"
        states.add(curState)

        when (curToken.tag) {
                DomainTag.EOP -> return
                DomainTag.OPEN -> {
                    val newRule = Rule(RuleTag.Normal, null)
                    newRule.addAlternatives()
                    rule.addAlternatives()
                    nextToken()
                    parseE(newRule, false)
                    rule.addRule(newRule)
                    if (curToken.tag != DomainTag.CLOSE) exit()
                    nextToken()
                    parseA(rule)
                }
            }
        }

    //    E -> <NTERM> E | <TERM> E | <OPEN> I <CLOSE> E | <IOPEN> E <ICLOSE> E | .
    private fun parseE(rule: Rule, star: Boolean) {
        curState = "E"
        states.add(curState)

        when (curToken.tag) {
            DomainTag.NTERM, DomainTag.TERM -> {
                val token = curToken
                if (curToken.tag == DomainTag.NTERM) {
                    ntermsRight.add(token.value)
                }
                rule.addRule(Rule(if (star) RuleTag.TokenStar else RuleTag.Token, token))

                nextToken()
                parseE(rule, star)
            }
            DomainTag.OPEN -> {
                nextToken()
                parseE(rule, star)
                if (curToken.tag != DomainTag.CLOSE) exit()
                nextToken()
                parseE(rule, star)
            }
            DomainTag.IOPEN -> {
                nextToken()
                parseI(rule, true)
                if (curToken.tag != DomainTag.ICLOSE) exit()
                nextToken()
                parseE(rule, false)
            }
            DomainTag.EOP -> return
        }
    }

    //    I -> <OPEN> E <CLOSE> I | .
    private fun parseI(rule: Rule, star: Boolean) {
        curState = "I"
        states.add(curState)

        when (curToken.tag) {
            DomainTag.EOP -> return
            DomainTag.OPEN -> {
                nextToken()
                parseE(rule, star)
                if (curToken.tag != DomainTag.CLOSE) exit()
                nextToken()
                rule.addAlternatives()
                parseI(rule, star)
            }
            DomainTag.TERM, DomainTag.NTERM -> {
                nextToken()
                parseE(rule, star)
            }
        }
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