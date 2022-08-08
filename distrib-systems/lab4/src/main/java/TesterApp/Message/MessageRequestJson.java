package TesterApp.Message;

public class MessageRequestJson {
    private final String packageID;

    public MessageRequestJson(String packageID) {
        this.packageID = packageID;
    }

    public String getPackageID() {
        return packageID;
    }
}
