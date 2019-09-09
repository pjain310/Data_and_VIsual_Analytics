package edu.gatech.cse6242;

import java.io.IOException;
import java.util.StringTokenizer;
import java.lang.Object;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import java.io.IOException;

public class Q4 {

  public static class DegreeMapper
  extends Mapper<Object, Text, IntWritable, IntWritable>{

  private IntWritable source = new IntWritable();
  private IntWritable target = new IntWritable();

  public void map(Object key, Text value, Context context
                  ) throws IOException, InterruptedException {
    StringTokenizer itr = new StringTokenizer(value.toString(),"\n");
  
    while (itr.hasMoreTokens()) {
    
        String line =itr.nextToken();
        String tokens[]=line.split("\t");

	source.set(Integer.parseInt(tokens[0]));
        target.set(Integer.parseInt(tokens[1]));

        IntWritable in_deg = new IntWritable(-1);
        IntWritable out_deg = new IntWritable(1);

        context.write(source, out_deg);
        context.write(target, in_deg);
      }
    }
  }


  public static class DiffMapper
    extends Mapper<Object, Text, IntWritable, IntWritable>{

    public void map(Object key, Text value, Context context
                    ) throws IOException, InterruptedException {
      StringTokenizer itr = new StringTokenizer(value.toString(), "\n");
      while (itr.hasMoreTokens()) {
        String line = itr.nextToken();
        String tokens[] = line.split("\t");
 
	IntWritable diff = new IntWritable(Integer.parseInt(tokens[1]));
	IntWritable count = new IntWritable(1);

        context.write(diff, count);
      }
    }
  }

  public static class FrequencyReducer
       extends Reducer<IntWritable,IntWritable,IntWritable,IntWritable> {
    private IntWritable result = new IntWritable();

    public void reduce(IntWritable key, Iterable<IntWritable> values,
                       Context context
                       ) throws IOException, InterruptedException {
      int sum = 0;
      for (IntWritable val : values) {
        sum += val.get();
      }
      result.set(sum);
      context.write(key, result);
    }
  }

  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();

    //Firs Job: Get sum in-degree and out-degree for each node
    Job job1 = Job.getInstance(conf, "job1");

    job1.setJarByClass(Q4.class);
    job1.setMapperClass(DegreeMapper.class);
    job1.setReducerClass(FrequencyReducer.class);
    job1.setOutputKeyClass(IntWritable.class);
    job1.setOutputValueClass(IntWritable.class);

    FileInputFormat.addInputPath(job1, new Path(args[0]));
    FileOutputFormat.setOutputPath(job1, new Path("first_output"));

    job1.waitForCompletion(true);

    //Second Job get all values for diffs  and put diff as key
    Job job2 = Job.getInstance(conf, "job2");
    
    job2.setJarByClass(Q4.class);
    job2.setMapperClass(DiffMapper.class);
    job2.setReducerClass(FrequencyReducer.class);
    job2.setOutputKeyClass(IntWritable.class);
    job2.setOutputValueClass(IntWritable.class);

    FileInputFormat.addInputPath(job2, new Path("first_output"));
    FileOutputFormat.setOutputPath(job2, new Path(args[1]));
    System.exit(job2.waitForCompletion(true) ? 0 : 1);
  }
}
