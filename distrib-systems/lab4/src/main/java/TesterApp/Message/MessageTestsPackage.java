package TesterApp.Message;

import TesterApp.Test.TestJson;
import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

public class MessageTestsPackage {
    private final String packageId;
    private final String jsScript;
    private final String functionName;
    private final List<TestJson> tests;

    @JsonCreator
    public MessageTestsPackage(@JsonProperty("packageId") String packageID,
                               @JsonProperty("jsScript") String jsScript,
                               @JsonProperty("functionName") String functionName,
                               @JsonProperty("tests") List<TestJson> tests) {
        this.packageId = packageID;
        this.jsScript = jsScript;
        this.functionName = functionName;
        this.tests = tests;
    }

    public List<TestJson> getTests() {
        return tests;
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
}
