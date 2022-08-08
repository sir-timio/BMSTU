package TesterApp.Message;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

public class MessageResponseJson {
    private final String packageId;
    private final List<String> results;

    @JsonCreator
    public MessageResponseJson(
            @JsonProperty("packageId") String packageId,
            @JsonProperty("results") List<String> results) {
        this.packageId = packageId;
        this.results = results;
    }

    public String getPackageId() {
        return packageId;
    }

    public List<String > getResults() {
        return results;
    }
}
