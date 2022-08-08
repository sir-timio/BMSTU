package FlightCompareApp;
import org.apache.hadoop.mapreduce.Partitioner;
import org.apache.hadoop.io.Text;

public class FlightPartitioner extends Partitioner<FlightWritableComparable, Text>{

    @Override
    public int getPartition(FlightWritableComparable flightWritableComparable, Text text, int numPartitions) {
       return Integer.hashCode(flightWritableComparable.getAirportID()) % numPartitions;
    }
}
