class First(val rules: HashMap<String, Rule>) {
    var first = HashMap<String, HashSet<String>>()

    private fun f(rule: Rule): HashSet<String> {
        var altSet: HashSet<String>? = null
        val set = HashSet<String>()
        for (ruleList in rule.alternatives) {
            altSet = HashSet<String>()
            var hashSet: HashSet<String>? = HashSet<String>()
            altSet.add("ε")
            for (item in ruleList) {
                if (!altSet.contains("ε"))
                    break
                if (item.token?.tag == DomainTag.NTERM) {
                    hashSet = first[item.token.value]?.clone() as HashSet<String>
                }
                if (item.token?.tag == DomainTag.TERM) {
                    hashSet?.clear()
                    hashSet?.add(item.token.value)
                }
                if (item.tag == RuleTag.TokenStar) {
                    hashSet?.add("ε")
                }
                if (item.tag == RuleTag.Normal) {
                    hashSet = f(item)
                }
                altSet.remove("ε")
                hashSet?.forEach { altSet.add(it) }
            }
            altSet.forEach { set.add(it) }
        }
        return set
    }

    private fun setFirst() {
        rules.forEach { (key, _) -> first[key] = HashSet<String>() }
        var isChanged = true
        var hs: HashSet<String>? = null
        while (isChanged) {
            isChanged = false
            rules.forEach { (key, value) ->
                hs = f(value)
                val size = first[key]?.size
                first[key] = hs?.clone() as HashSet<String>
                if (size != first[key]?.size) {
                    isChanged = true
                }
            }

        }

    }


    fun printFirst() {
        setFirst()
        first.forEach { key, value ->
            println("$key :: ${value.joinToString(", ")}")
        }
    }
}