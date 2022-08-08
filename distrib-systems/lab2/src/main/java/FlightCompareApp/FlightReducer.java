package FlightCompareApp;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;
import java.util.Iterator;

public class FlightReducer extends Reducer<FlightWritableComparable, Text, Text, Text>{

    @Override
    protected void reduce(FlightWritableComparable key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
        Iterator<Text> iterator = values.iterator();
        Text airportName = new Text(iterator.next());

        float min = Float.MAX_VALUE;
        float max = Float.MIN_NORMAL;
        float sum = 0;
        int counter = 0;

        while (iterator.hasNext()) {
            float delay = Float.parseFloat(iterator.next().toString());
            min = Float.min(min, delay);
            max = Float.max(max, delay);
            sum += delay;
            counter++;
        }
        Text stats = new Text(String.format("min: %f, max: %f, average: %f", min, max, sum / counter));
        if (counter > 0) {
            context.write(airportName, stats);
        }
    }
}
