package FlightCompareApp;

import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.mapreduce.lib.input.MultipleInputs;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.io.IOException;

public class AirportStatsApp {

    public static void main(String[] args) throws IOException, InterruptedException, ClassNotFoundException {
        if (args.length != 3) {
            System.err.println("flights airports output");
            System.exit(-1);
        }

        Job job = Job.getInstance();
        job.setJarByClass(AirportStatsApp.class);
        job.setJobName("Reduce side join fligths stats");
        MultipleInputs.addInputPath(job, new Path(args[0]),
                                    TextInputFormat.class, FlightMapper.class);
        MultipleInputs.addInputPath(job, new Path(args[1]),
                                    TextInputFormat.class, AirportMapper.class);

        job.setPartitionerClass(FlightPartitioner.class);
        job.setGroupingComparatorClass(AirportGroupingComparator.class);
        job.setReducerClass(FlightReducer.class);

        job.setMapOutputKeyClass(FlightWritableComparable.class);
        job.setMapOutputValueClass(Text.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        FileOutputFormat.setOutputPath(job, new Path(args[2]));

        job.setNumReduceTasks(2);
        System.exit(job.waitForCompletion(true) ? 0 : 1);

    }
}
