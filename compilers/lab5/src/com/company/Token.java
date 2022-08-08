package com.company;

public class Token {
    String domain, attribute;
    Fragment fragment;


    Token(String domain, String attribute, Fragment fragment) {
        this.domain = domain;
        this.attribute = attribute;
        this.fragment = fragment;
    }

    public String getDomain() {
        return domain;
    }

    public String getAttribute() {
        return attribute;
    }

    @Override
    public String toString() {
        return  domain + " " + fragment.toString() + ": " + attribute ;

    }
}