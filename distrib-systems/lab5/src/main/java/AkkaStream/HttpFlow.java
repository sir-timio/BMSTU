package AkkaStream;

import AkkaStream.Message.MessageCache;
import AkkaStream.Message.MessageRequest;
import akka.NotUsed;
import akka.actor.Actor;
import akka.actor.ActorRef;
import akka.http.javadsl.model.HttpRequest;
import akka.http.javadsl.model.HttpResponse;
import akka.http.javadsl.model.Query;
import akka.japi.Pair;
import akka.japi.function.Function2;
import akka.pattern.Patterns;
import akka.stream.ActorMaterializer;
import akka.stream.javadsl.Flow;
import akka.stream.javadsl.Keep;
import akka.stream.javadsl.Sink;
import akka.stream.javadsl.Source;
import org.asynchttpclient.AsyncHttpClient;
import org.asynchttpclient.Dsl;
import org.asynchttpclient.Response;

import java.time.Duration;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CompletionStage;
import java.util.regex.Pattern;


import org.asynchttpclient.Request;

public class HttpFlow {
    public static final int TIMEOUT_SECONDS = 5;
    public static final int NUM_OF_WORKERS = 3;
    private static final String QUERY_URL = "testUrl";
    private static final String QUERY_COUNT = "count";

    public static Flow<HttpRequest, HttpResponse, NotUsed> httpFlow(
            ActorMaterializer materializer, ActorRef actorRef
    ) {
        return Flow.of(HttpRequest.class)
                .map(request -> {
                    Query query = request.getUri().query();
                    String url = query.get(QUERY_URL).get();
                    int count = Integer.parseInt(query.get(QUERY_COUNT).get());
                    return new Pair<>(url, count);
                })
                .mapAsync(NUM_OF_WORKERS, request ->
                        Patterns.ask(
                                actorRef,
                                new MessageRequest(request.first()),
                                Duration.ofSeconds(TIMEOUT_SECONDS)
                        )
                .thenCompose(responseTime -> {
                    if (((Optional<Long>) responseTime).isPresent()) {
                        return CompletableFuture.completedFuture(
                                new Pair<>(
                                        request.first(),
                                        ((Optional<Long>) responseTime).get()
                                )
                        );
                    } else {
                        Sink<Pair<String, Integer>, CompletionStage<Long>> sink = Flow
                                .<Pair<String, Integer>>create()
                                .mapConcat(req -> new ArrayList<>(Collections.nCopies(req.second(), req.first())))
                                .mapAsync(request.second(), url -> {
                                    long start = System.currentTimeMillis();
                                    Request testRequest = Dsl.get(url).build();

                                    AsyncHttpClient client = Dsl.asyncHttpClient();
                                    return client.executeRequest(testRequest)
                                            .toCompletableFuture()
                                            .thenApply(response -> System.currentTimeMillis() - start);
                                })
                                .toMat(Sink.fold(0L, Long::sum), Keep.right());
                        return Source.from(Collections.singletonList(request))
                                .toMat(sink, Keep.right())
                                .run(materializer)
                                .thenApply(sum -> new Pair<>(request.first(), sum / request.second()));
                    }
                }))
                .map(res -> {
                    actorRef.tell(
                            new MessageCache(res.first(), res.second()),
                            ActorRef.noSender()
                    );
                    return HttpResponse.create().withEntity(res.first() + ": " + res.second().toString() + " millis");
                });
    }
}
