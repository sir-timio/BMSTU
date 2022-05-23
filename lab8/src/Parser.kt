import kotlin.system.exitProcess

class Parser(private val tokens: List<Token>) {
    private var curToken = tokens.first()
    private var ntermsLeft = HashSet<String>()
    private var ntermsRight = HashSet<String>()
    var mapRule = HashMap<String, Rule>()
    private var curState = ""
    private var states = mutableListOf<String>()
    private var curStar = false

    fun parse() {
        parseS()
//        mapRule.forEach { key, value -> println("<$key $value>") }
        if (!ntermsLeft.containsAll(ntermsRight)) {
            println("Undefined NTERMs:")
            println(ntermsRight - ntermsLeft)
            exit()
        }
    }

    //    S ::= R {R}
    //    R ::= <OPEN> <NTERM> A <CLOSE>
    //    A ::= <OPEN> E <CLOSE> A | .
    //    E ::= <NTERM> E | <TERM> E | <OPEN> I <CLOSE> E | <IOPEN> E <ICLOSE> E | .
    //    I ::= <OPEN> E <CLOSE> I | .

    //    S -> R S | .
    private fun parseS() {
        states.add("S")

        while (curToken.tag == DomainTag.OPEN) {
            parseR()
        }
        if (curToken.tag != DomainTag.EOP) exit()
    }

    //    R -> <OPEN> <NTERM> A {A} <CLOSE>
    private fun parseR() {
        states.add("R")

        if (curToken.tag != DomainTag.OPEN) exit()
        nextToken()

        if (curToken.tag != DomainTag.NTERM) exit()
        val left = curToken
        val rule = Rule(RuleTag.Token, null)
        ntermsLeft.add(left.value)
        nextToken()
        parseA(rule)
        while (curToken.tag == DomainTag.OPEN) {
            rule.addAlternatives()
            parseA(rule)
        }
        mapRule[left.value] = rule
        if (curToken.tag != DomainTag.CLOSE) exit()
        nextToken()
    }

    //    A -> <OPEN> E <CLOSE> {<OPEN> E <CLOSE>} | .
    private fun parseA(rule: Rule) {
        curState = "A"
        states.add(curState)

        if (curToken.tag != DomainTag.OPEN) exit()
        nextToken()

        val newRule = Rule(RuleTag.Normal, null)
        newRule.addAlternatives()
        parseE(newRule, false)

        if (curToken.tag != DomainTag.CLOSE) exit()
        nextToken()
        rule.addAlternatives()
        rule.addRule(newRule)

        while (curToken.tag == DomainTag.OPEN) {
            nextToken()
            val newRule = Rule(RuleTag.Normal, null)
            newRule.addAlternatives()
            parseE(newRule, false)
            if (curToken.tag != DomainTag.CLOSE) exit()
            nextToken()
            rule.addAlternatives()
            rule.addRule(newRule)
        }
//        rule.addRule(newRule)
    }

    //    E -> <NTERM> {E} | <TERM> {E}| <OPEN> I <CLOSE> {E} | <IOPEN> E <ICLOSE> {E} | .
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
                parseI(rule, star)
                if (curToken.tag != DomainTag.CLOSE) exit()
                nextToken()
                parseE(rule, star)
            }
            DomainTag.IOPEN -> {
                nextToken()
                parseE(rule, true)
                if (curToken.tag != DomainTag.ICLOSE) exit()
                nextToken()
                parseE(rule, star)
            }
            DomainTag.EOP -> return
        }
    }

    //    I -> <OPEN> E <CLOSE> I | .
    private fun parseI(rule: Rule, star: Boolean) {
        curStar = star
        curState = "I"
        states.add(curState)

        when (curToken.tag) {
            DomainTag.EOP -> return
            DomainTag.OPEN -> {
                nextToken()
                parseE(rule, star)
                if (curToken.tag != DomainTag.CLOSE) exit()
                nextToken()
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