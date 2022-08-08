package TesterApp.Test;

import com.fasterxml.jackson.annotation.JsonProperty;

public class TestResultStore {
    private static final String PASSED_STATUS = "OK";
    private static final String FAILED_STATUS = "FAILED";
    private static final String ERROR_STATUS = "ERROR";

    private final String packageId;

    private final String status;
    private final String testName;
    private final String expectedResult;
    private final String receivedResult;


    public TestResultStore(String packageId,
                           String status,
                           String testName,
                           String expectedResult,
                           String evaluatedResult) {
        this.packageId = packageId;
        this.status = status;
        this.testName = testName;
        this.expectedResult = expectedResult;
        this.receivedResult = evaluatedResult;
    }

    public String getPackageId() {
        return packageId;
    }

    public String getResult() {

        String result = "name: " + testName + " status: " + status;
        if (status.equals(FAILED_STATUS)){
            result += " received: " + receivedResult + '\n' +
                      " expected: " + expectedResult + '\n';
        }
        return result;
    }


    @Override
    public String toString() {
        return "packageId: " + packageId + '\n';
    }
}
