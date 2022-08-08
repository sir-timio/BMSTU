package FlightCompareApp;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

public class FlightMapper extends Mapper<LongWritable, Text, FlightWritableComparable, Text>{
    private static final String DELIMITER = ",";
    private static final int DEST_AIRPORT_ID_COLUMN =  14;
    private static final int ARR_DELAY_COLUMN = 18;
    private static final int DATA_TYPE = 1;

    @Override
    protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        if (key.get() != 0){
            String[] row = value.toString().split(DELIMITER);
            String rawDelay = row[ARR_DELAY_COLUMN];

            if (!rawDelay.isEmpty() && Float.parseFloat(rawDelay) != 0){
                int destAirportID = Integer.parseInt(row[DEST_AIRPORT_ID_COLUMN]);

                context.write(new FlightWritableComparable(destAirportID, DATA_TYPE),
                        new Text(rawDelay));
            }
        }
    }
}
