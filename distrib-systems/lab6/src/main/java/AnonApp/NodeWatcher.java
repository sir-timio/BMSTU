package AnonApp;

import AnonApp.Message.MessageServers;
import akka.actor.ActorRef;
import org.apache.zookeeper.*;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class NodeWatcher implements Watcher {
    public static String ZOO_CONNECT_STRING = "127.0.0.1:2181";
    public static int SESSION_TIMEOUT = 3000;
    private final ZooKeeper zoo;
    private final ActorRef actorConfigKeeper;

    public NodeWatcher(ActorRef actorConfigKeeper, String host, Integer port) throws IOException, InterruptedException, KeeperException {
        this.zoo = new ZooKeeper(ZOO_CONNECT_STRING, SESSION_TIMEOUT, this);
        String akkaAddress = "http://" + host + ":" + port.toString();
        zoo.create("/servers/s",
                akkaAddress.getBytes(),
                ZooDefs.Ids.OPEN_ACL_UNSAFE ,
                CreateMode.EPHEMERAL_SEQUENTIAL
        );
        this.actorConfigKeeper = actorConfigKeeper;
    }

    @Override
    public void process(WatchedEvent watchedEvent) {
        try {
            List<String> servers = zoo.getChildren("/servers", this);
            ArrayList<String> serversForAkka = new ArrayList<>();
            for (String server : servers) {
                byte[] data = zoo.getData("/servers/" + server, false, null);
                serversForAkka.add(new String(data));
            }
            actorConfigKeeper.tell(new MessageServers(serversForAkka), ActorRef.noSender());
        } catch (KeeperException | InterruptedException e) {
            e.printStackTrace();
        }

    }
}
