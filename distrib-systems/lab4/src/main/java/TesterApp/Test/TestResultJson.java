package TesterApp.Test;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

public class TestResultJson {
    private final String status;
    private final String testName;
    private final String expectedResult;
    private final String evaluatedResult;

    @JsonCreator
    public TestResultJson(@JsonProperty("status") String status,
                          @JsonProperty("testName") String testName,
                          @JsonProperty("expectedResult") String expectedResult,
                          @JsonProperty("receivedResult") String evaluatedResult) {
        this.status = status;
        this.testName = testName;
        this.expectedResult = expectedResult;
        this.evaluatedResult = evaluatedResult;
    }

    @Override
    public String toString() {
        return "TestResult{" +
                ", status='" + status + '\'' +
                ", testName='" + testName + '\'' +
                ", expectedResult='" + expectedResult + '\'' +
                ", evaluatedResult='" + evaluatedResult + '\'' +
                '}';
    }
}
