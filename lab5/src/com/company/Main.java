package com.company;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashMap;

public class Main {

    public static void main(String[] args) throws IOException {
        String path = "in.txt";
        String program = new String(Files.readAllBytes(Paths.get(path)));
        Automata auto = new Automata(program);
        auto.run();
        while (auto.hasNextToken()) {
            System.out.println(auto.nextToken());
        }
        HashMap<String, Integer> idents = auto.getMap();
        for (String ident: idents.keySet()) {
            System.out.println(idents.get(ident) + " : " + ident);
        }
        auto.output_messages();
    }

}