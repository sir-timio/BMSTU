package TesterApp.Message;

import TesterApp.Test.TestJson;
import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

public class MessageTest {
    private final String packageId;
    private final String jsScript;
    private final String functionName;
    private final TestJson test;

    @JsonCreator
    public MessageTest(@JsonProperty("packageId") String packageID,
                       @JsonProperty("jsScript") String jsScript,
                       @JsonProperty("functionName") String functionName,
                       @JsonProperty("test") TestJson test) {
        this.packageId = packageID;
        this.functionName = functionName;
        this.jsScript = jsScript;
        this.test = test;
    }

    public String getPackageId() {
        return packageId;
    }

    public String getJsScript() {
        return jsScript;
    }

    public String getFunctionName() {
        return functionName;
    }

    public TestJson getTest() {
        return test;
    }
}