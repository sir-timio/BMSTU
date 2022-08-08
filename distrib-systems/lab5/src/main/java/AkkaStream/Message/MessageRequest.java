package AkkaStream.Message;

public class MessageRequest {
    private final String url;

    public MessageRequest(String url) {
        this.url = url;
    }

    public String getUrl() {
        return url;
    }
}
