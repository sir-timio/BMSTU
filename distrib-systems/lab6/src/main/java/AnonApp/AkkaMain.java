package AnonApp;

import java.util.concurrent.CompletionStage;

import AnonApp.Actor.ActorConfigKeeper;
import akka.NotUsed;
import akka.actor.ActorSystem;
import akka.actor.ActorRef;
import akka.actor.Props;
import akka.http.javadsl.ConnectHttp;
import akka.http.javadsl.Http;
import akka.http.javadsl.ServerBinding;
import akka.http.javadsl.model.HttpRequest;
import akka.http.javadsl.model.HttpResponse;
import akka.stream.ActorMaterializer;
import akka.stream.javadsl.Flow;
import org.apache.log4j.BasicConfigurator;
import org.apache.zookeeper.ZooKeeper;


public class AkkaMain {

    private static final String HOST = "127.0.0.1";
    private static final String ZOO_PORT = "2181";
    private static final int SESSION_TIMEOUT = 5000;

    public static void main(String[] args) throws Exception {
        if (args.length != 1) {
            System.err.println("Usage: AnonApp <port>");
            System.exit(-1);
        }
        BasicConfigurator.configure();
        int port = Integer.parseInt(args[0]);
        ActorSystem system = ActorSystem.create();
        ActorRef actorConfigKeeper = system.actorOf(Props.create(ActorConfigKeeper.class));
        new NodeWatcher(actorConfigKeeper, HOST, port);




        final Http http = Http.get(system);
        final ActorMaterializer materializer = ActorMaterializer.create(system);
        final Flow<HttpRequest, HttpResponse, NotUsed> routeFlow = new AnonRouter(actorConfigKeeper, http)
                .createRoute().flow(system, materializer);
        final CompletionStage<ServerBinding> binding = http.bindAndHandle(routeFlow,
                ConnectHttp.toHost(HOST, port), materializer);
        System.out.println("Server online at http://" + HOST + ":" + port + "/\nPress RETURN to stop...");
        System.in.read();
        binding
                .thenCompose(ServerBinding::unbind)
                .thenAccept(unbound ->  system.terminate());

    }
}
