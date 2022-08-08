package TesterApp;
import TesterApp.Actor.ActorRouter;
import TesterApp.Message.MessageRequestJson;
import TesterApp.Message.MessageTestsPackage;
import akka.NotUsed;
import akka.actor.ActorRef;
import akka.actor.ActorSystem;
import akka.actor.Props;
import akka.http.javadsl.ConnectHttp;
import akka.http.javadsl.Http;
import akka.http.javadsl.ServerBinding;
import akka.http.javadsl.marshallers.jackson.Jackson;
import akka.http.javadsl.model.HttpRequest;
import akka.http.javadsl.model.HttpResponse;
import akka.http.javadsl.server.AllDirectives;
import akka.http.javadsl.server.Route;
import akka.pattern.Patterns;
import akka.stream.ActorMaterializer;
import akka.stream.javadsl.Flow;

import scala.concurrent.Future;

import java.io.IOException;
import java.util.concurrent.CompletionStage;

public class TestApp extends AllDirectives {
    private static final String ACTOR_SYSTEM_NAME = "JS_TESTER";

    public static void main(String[] args) throws IOException {
        ActorSystem actorSystem = ActorSystem.create(ACTOR_SYSTEM_NAME);
        ActorRef actorRouter = actorSystem.actorOf(Props.create(ActorRouter.class));
        Http http = Http.get(actorSystem);
        ActorMaterializer actorMaterializer = ActorMaterializer.create(actorSystem);

        TestApp app = new TestApp();
        final Flow<HttpRequest, HttpResponse, NotUsed> routeFlow =
                app.createRoute(actorRouter).flow(actorSystem, actorMaterializer);
        final CompletionStage<ServerBinding> binging = http.bindAndHandle(
                routeFlow,
                ConnectHttp.toHost("localhost", 8080),
                actorMaterializer
        );
        System.out.println("Server online at http://localhost:8080/\nPress RETURN to stop...");
        System.in.read();
        binging.thenCompose(ServerBinding::unbind).thenAccept(unbound -> actorSystem.terminate());
    }


    private Route createRoute(ActorRef actorRouter) {
        return route(
                path("test", () ->
                        route(
                                post(
                                        () -> entity(Jackson.unmarshaller(MessageTestsPackage.class), m -> {
                                            actorRouter.tell(m, ActorRef.noSender());
                                            return complete("Start testing");
                                        })
                                )
                        )
                ),
                path("result", () ->
                        route(
                                get(
                                        () -> parameter("packageId", (id) -> {
                                            Future<Object> result = Patterns.ask(
                                                    actorRouter,
                                                    new MessageRequestJson(id),
                                                    500
                                            );
                                            return completeOKWithFuture(result, Jackson.marshaller());
                                        })
                                )
                        )
                        )
        );
    }
}

