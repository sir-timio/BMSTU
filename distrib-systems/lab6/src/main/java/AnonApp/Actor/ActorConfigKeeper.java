package AnonApp.Actor;

import AnonApp.Message.MessageGetRandom;
import AnonApp.Message.MessageServers;
import akka.actor.AbstractActor;
import akka.actor.Actor;
import akka.japi.pf.ReceiveBuilder;

import java.util.ArrayList;
import java.util.Random;

public class ActorConfigKeeper extends AbstractActor{
    private ArrayList<String> servers;
    private final Random random = new Random();

    @Override
    public Receive createReceive() {
        return ReceiveBuilder.create()
                .match(MessageGetRandom.class,
                        msg -> sender()
                                .tell(
                                        servers.get(random.nextInt(servers.size())),
                                        Actor.noSender()
                                )
                )
                .match(MessageServers.class,
                        msg -> servers = msg.getServers())
                .build();
    }
}
