package AkkaStream.Message;

public class MessageCache {
    private final String url;
    private final long responseTime;

    public MessageCache(String url, Long responseTime) {
        this.url = url;
        this.responseTime = responseTime;
    }

    public String getUrl() {
        return url;
    }

    public long getResponseTime() {
        return responseTime;
    }
}
