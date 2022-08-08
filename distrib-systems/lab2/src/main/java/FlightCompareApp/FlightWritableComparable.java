package FlightCompareApp;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.WritableComparable;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;

public class FlightWritableComparable implements WritableComparable{
    private int airportID;
    private int isOverflight;

    public int getAirportID() {
        return airportID;
    }

    public FlightWritableComparable(){
        this.airportID = 0;
        this.isOverflight = 0;
    }

    public FlightWritableComparable(int airportID, int isOverflight) {
        this.airportID =  airportID;
        this.isOverflight = isOverflight;
    }

    @Override
    public void write(DataOutput dataOutput) throws IOException {
        dataOutput.writeInt(airportID);
        dataOutput.writeInt(isOverflight);
    }


    @Override
    public void readFields(DataInput dataInput) throws IOException {
        this.airportID = dataInput.readInt();
        this.isOverflight = dataInput.readInt();
    }

    @Override
    public int compareTo(Object o) {
        FlightWritableComparable other = (FlightWritableComparable) o;
        if (this.airportID == other.airportID)
            return Integer.compare(this.isOverflight, other.isOverflight);

        return (this.airportID < other.airportID) ? -1 : 1;
    }
}
