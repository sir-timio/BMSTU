package AnonApp;

import AnonApp.Message.MessageGetRandom;
import akka.actor.ActorRef;
import akka.http.javadsl.Http;
import akka.http.javadsl.model.HttpRequest;
import akka.http.javadsl.model.HttpResponse;
import akka.http.javadsl.model.Query;
import akka.http.javadsl.model.Uri;
import akka.http.javadsl.server.Route;
import akka.japi.Pair;
import akka.pattern.Patterns;

import java.time.Duration;
import java.util.concurrent.CompletionStage;

import static akka.http.javadsl.server.Directives.*;

public class AnonRouter {
    private final ActorRef actorConfigKeeper;
    private final Http client;

    private static final Duration TIMEOUT = Duration.ofSeconds(5);
    private static final int ZERO_COUNT = 0;

    private static final String QUERY_URL = "url";
    private static final String QUERY_COUNT = "count";
    private static final String PATH = "";

    public AnonRouter(ActorRef actorConfigKeeper, Http client) {
        this.actorConfigKeeper = actorConfigKeeper;
        this.client = client;
    }

    public Route createRoute() {
        return route(
                path(PATH, () ->
                        route(
                                get(() ->
                                        parameter(QUERY_URL, (url) ->
                                        parameter(QUERY_COUNT, (countRaw) -> {
                                            int count = Integer.parseInt(countRaw);
                                            if (count == ZERO_COUNT) {
                                                return completeWithFuture(
                                                        client.singleRequest(HttpRequest.create(url))
                                                );
                                            } else {
                                                return completeWithFuture(sendNext(url, count-1));
                                            }
                                        })))
                        )));
    }

    private CompletionStage<HttpResponse> sendNext(String url, Integer count) {
        return Patterns.ask(
                actorConfigKeeper,
                new MessageGetRandom(),
                TIMEOUT
        )
        .thenCompose(port -> {
            Uri uri = Uri.create((String) port)
                    .query(Query.create(
                            Pair.create("url", url),
                            Pair.create("count", count.toString())
                    ));
            return client.singleRequest(HttpRequest.create(uri.toString()));
        });
    }

}

