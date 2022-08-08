package AnonApp.Message;

import java.util.ArrayList;

public class MessageServers {
    private final ArrayList<String> servers;

    public MessageServers(ArrayList<String> servers) {
        this.servers = servers;
    }

    public ArrayList<String> getServers() {
        return servers;
    }
}
