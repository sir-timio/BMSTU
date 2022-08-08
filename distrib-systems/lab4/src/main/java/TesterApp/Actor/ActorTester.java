package TesterApp.Actor;

import TesterApp.Actor.ActorRouter;
import TesterApp.Message.MessageTest;
import TesterApp.Test.TestResultStore;
import akka.actor.AbstractActor;

import javax.script.Invocable;
import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;
import javax.script.ScriptException;
import java.util.ArrayList;

public class ActorTester extends AbstractActor {
    private static final String EVAL_ENGINE = "nashorn";
    private static final String PASSED_STATUS = "OK";
    private static final String FAILED_STATUS = "FAILED";
    private static final String ERROR_STATUS = "ERROR";

    @Override
    public Receive createReceive() {
        return receiveBuilder()
                .match(
                        MessageTest.class,
                        m -> sender().tell(
                                evalTest(m),
                                self()
                        )
                )
                .build();
    }

    private String evalJS(String jscript, String functionName, ArrayList<Object> params) throws ScriptException, NoSuchMethodException {
        ScriptEngine engine = new ScriptEngineManager().getEngineByName(EVAL_ENGINE);
        engine.eval(jscript);
        Invocable invocable = (Invocable) engine;
        return invocable.invokeFunction(functionName, params.toArray()).toString();
    }


    private TestResultStore evalTest(MessageTest messageTest) {
        String evaluated;
        String status;
        String expected = messageTest.getTest().getExpectedResult();

        try {
            evaluated = evalJS(
                    messageTest.getJsScript(),
                    messageTest.getFunctionName(),
                    messageTest.getTest().getParams()
            );
            status = expected.equals(evaluated) ? PASSED_STATUS : FAILED_STATUS;
        } catch (ScriptException | NoSuchMethodException e) {
            evaluated = "";
            status = ERROR_STATUS + ": " + e;
        }
        return new  TestResultStore(
                messageTest.getPackageId(),
                status,
                messageTest.getTest().getTestName(),
                expected,
                evaluated
        );
    }
}
