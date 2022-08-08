package AkkaStream.Actor;

import AkkaStream.Message.MessageCache;
import AkkaStream.Message.MessageRequest;
import akka.actor.AbstractActor;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

public class ActorKeeper extends AbstractActor {
    private final Map<String, Long> results = new HashMap<>();

    @Override
    public Receive createReceive() {
        return receiveBuilder()
                .match(
                        MessageRequest.class,
                        message -> sender().tell(
                                Optional.ofNullable(results.get(message.getUrl())),
                                self())
                )
                .match(
                        MessageCache.class,
                        message -> results.put(message.getUrl(), message.getResponseTime())
                )
                .build();
    }
}
