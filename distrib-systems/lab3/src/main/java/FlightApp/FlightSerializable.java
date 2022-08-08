package FlightApp;

import java.io.Serializable;

public class FlightSerializable implements Serializable {
    private float delay;
    private int isCancelled;

    public FlightSerializable(float delay, int isCancelled) {
        this.delay = delay;
        this.isCancelled = isCancelled;
    }

    public float getDelay() {
        return delay;
    }

    public int isDelayed() {
        return this.getDelay() > 0 ? 1 : 0;
    }

    public int isCancelled() {
        return isCancelled;
    }
}
