package AnonApp;
import AnonApp.Message.MessageServers;
import akka.actor.ActorRef;
import akka.pattern.Patterns;
import org.apache.zookeeper.*;

import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;

public class ZooWatcher implements Watcher {
    private static final String SERVERS_PATH = "/servers";

    private ZooKeeper zooKeeper;
    private final ActorRef actorConfigKeeper;

    public ZooWatcher(ActorRef actorConfigKeeper) throws Exception {
        this.actorConfigKeeper = actorConfigKeeper;
    }

    public void setZooKeeper(ZooKeeper zooKeeper){
        this.zooKeeper = zooKeeper;
    }

    @Override
    public void process(WatchedEvent watchedEvent) {
        List<String> servers;
        try {
            servers = zooKeeper.getChildren(SERVERS_PATH, this);
        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("Can't get children");
            return;
        }
        ArrayList<String> urls = new ArrayList<>();
        for (String s : servers) {
            String url;
            try {
                url = new String(zooKeeper.getData(SERVERS_PATH + "/" + s, false, null));
            } catch (Exception e) {
                e.printStackTrace();
                return;
            }
            urls.add(url);
            actorConfigKeeper.tell(new MessageServers(urls), ActorRef.noSender());
        }
    }
}

