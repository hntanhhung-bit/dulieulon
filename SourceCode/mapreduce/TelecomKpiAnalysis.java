package vn.edu.hunre.bigdata.telecom;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;
import java.text.DecimalFormat;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.Writable;
import org.apache.hadoop.io.WritableComparable;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Partitioner;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

/**
 * THUẬT TOÁN MAPREDUCE TÍNH THÔNG LƯỢNG, ĐỘ TRỄ VÀ TỶ LỆ RỚT CUỘC GỌI
 * THEO TRẠM VÀ CÔNG NGHỆ (TOWER_ID & TECHNOLOGY)
 */
public class TelecomKpiAnalysis extends Configured implements Tool {

    // =========================================================================
    // 1. CUSTOM COMPOSITE KEY: TowerTechKey (tower_id, technology)
    // =========================================================================
    public static class TowerTechKey implements WritableComparable<TowerTechKey> {
        private String towerId;
        private String technology;

        public TowerTechKey() {
            this.towerId = "";
            this.technology = "";
        }

        public TowerTechKey(String towerId, String technology) {
            this.towerId = towerId;
            this.technology = technology;
        }

        public String getTowerId() { return towerId; }
        public String getTechnology() { return technology; }

        @Override
        public void write(DataOutput out) throws IOException {
            out.writeUTF(towerId);
            out.writeUTF(technology);
        }

        @Override
        public void readFields(DataInput in) throws IOException {
            this.towerId = in.readUTF();
            this.technology = in.readUTF();
        }

        @Override
        public int compareTo(TowerTechKey o) {
            int cmp = this.towerId.compareTo(o.towerId);
            if (cmp != 0) {
                return cmp;
            }
            return this.technology.compareTo(o.technology);
        }

        @Override
        public String toString() {
            return towerId + "\t" + technology;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            TowerTechKey that = (TowerTechKey) o;
            return towerId.equals(that.towerId) && technology.equals(that.technology);
        }

        @Override
        public int hashCode() {
            return towerId.hashCode() * 31 + technology.hashCode();
        }
    }

    // =========================================================================
    // 2. CUSTOM VALUE TUPLE: KpiTuple (lưu các giá trị tích lũy số học)
    // =========================================================================
    public static class KpiTuple implements Writable {
        private double throughputSum;
        private double latencySum;
        private double packetLossSum;
        private long callDroppedCount;
        private long totalCallsCount;
        private long eventCount;

        public KpiTuple() {}

        public KpiTuple(double throughputSum, double latencySum, double packetLossSum,
                        long callDroppedCount, long totalCallsCount, long eventCount) {
            this.throughputSum = throughputSum;
            this.latencySum = latencySum;
            this.packetLossSum = packetLossSum;
            this.callDroppedCount = callDroppedCount;
            this.totalCallsCount = totalCallsCount;
            this.eventCount = eventCount;
        }

        public double getThroughputSum() { return throughputSum; }
        public double getLatencySum() { return latencySum; }
        public double getPacketLossSum() { return packetLossSum; }
        public long getCallDroppedCount() { return callDroppedCount; }
        public long getTotalCallsCount() { return totalCallsCount; }
        public long getEventCount() { return eventCount; }

        @Override
        public void write(DataOutput out) throws IOException {
            out.writeDouble(throughputSum);
            out.writeDouble(latencySum);
            out.writeDouble(packetLossSum);
            out.writeLong(callDroppedCount);
            out.writeLong(totalCallsCount);
            out.writeLong(eventCount);
        }

        @Override
        public void readFields(DataInput in) throws IOException {
            this.throughputSum = in.readDouble();
            this.latencySum = in.readDouble();
            this.packetLossSum = in.readDouble();
            this.callDroppedCount = in.readLong();
            this.totalCallsCount = in.readLong();
            this.eventCount = in.readLong();
        }
    }

    // =========================================================================
    // 3. MAPPER: Parse dòng CSV, lọc bản ghi lỗi, phát sinh (TowerTechKey, KpiTuple)
    // Input:  <LongWritable offset, Text recordLine>
    // Output: <TowerTechKey, KpiTuple>
    // =========================================================================
    public static class KpiMapper extends Mapper<LongWritable, Text, TowerTechKey, KpiTuple> {
        private TowerTechKey outKey = new TowerTechKey();
        private KpiTuple outValue = new KpiTuple();

        @Override
        protected void map(LongWritable key, Text value, Context context)
                throws IOException, InterruptedException {
            String line = value.toString().trim();
            if (line.isEmpty() || line.startsWith("event_id")) {
                // Bỏ qua dòng trống hoặc dòng tiêu đề header
                return;
            }

            String[] tokens = line.split(",");
            // Kiểm tra tối thiểu 10 trường theo schema:
            // 0:event_id, 1:timestamp, 2:tower_id, 3:cell_id, 4:technology,
            // 5:throughput_mbps, 6:latency_ms, 7:packet_loss_pct, 8:call_dropped, 9:num_active_users
            if (tokens.length < 10) {
                context.getCounter("DataQuality", "MalformedRecords").increment(1);
                return;
            }

            try {
                String towerId = tokens[2].trim();
                String tech = tokens[4].trim();
                double tp = Double.parseDouble(tokens[5].trim());
                double lat = Double.parseDouble(tokens[6].trim());
                double loss = Double.parseDouble(tokens[7].trim());
                int dropped = Integer.parseInt(tokens[8].trim());

                // Kiểm tra tính hợp lệ nghiệp vụ:
                if (tp < 0.0 || lat < 0.0 || loss < 0.0 || loss > 100.0) {
                    context.getCounter("DataQuality", "InvalidRangeValues").increment(1);
                    return;
                }

                outKey = new TowerTechKey(towerId, tech);
                // Mỗi event tương ứng với 1 mẫu (eventCount=1, totalCallsCount=1 nếu có phiên thoại)
                outValue = new KpiTuple(tp, lat, loss, dropped, 1L, 1L);
                context.write(outKey, outValue);

            } catch (NumberFormatException e) {
                context.getCounter("DataQuality", "ParseErrors").increment(1);
            }
        }
    }

    // =========================================================================
    // 4. COMBINER: Tính tổng gộp cục bộ trên từng Mapper Node
    // Giúp giảm đáng kể lưu lượng truyền tải trên mạng (Network I/O) ở bước Shuffle
    // Input:  <TowerTechKey, Iterable<KpiTuple>>
    // Output: <TowerTechKey, KpiTuple>
    // =========================================================================
    public static class KpiCombiner extends Reducer<TowerTechKey, KpiTuple, TowerTechKey, KpiTuple> {
        @Override
        protected void reduce(TowerTechKey key, Iterable<KpiTuple> values, Context context)
                throws IOException, InterruptedException {
            double sumTp = 0.0;
            double sumLat = 0.0;
            double sumLoss = 0.0;
            long sumDropped = 0;
            long sumCalls = 0;
            long countEvents = 0;

            for (KpiTuple val : values) {
                sumTp += val.getThroughputSum();
                sumLat += val.getLatencySum();
                sumLoss += val.getPacketLossSum();
                sumDropped += val.getCallDroppedCount();
                sumCalls += val.getTotalCallsCount();
                countEvents += val.getEventCount();
            }

            context.write(key, new KpiTuple(sumTp, sumLat, sumLoss, sumDropped, sumCalls, countEvents));
        }
    }

    // =========================================================================
    // 5. CUSTOM PARTITIONER: Phân vùng theo tower_id
    // Đảm bảo mọi công nghệ (3G, 4G, 5G) của cùng một trạm BTS đều đến cùng một Reducer,
    // giúp cân bằng tải và phục vụ phân tích toàn diện cấp trạm mà không bị lệch dữ liệu (Data Skew).
    // =========================================================================
    public static class TowerPartitioner extends Partitioner<TowerTechKey, KpiTuple> {
        @Override
        public int getPartition(TowerTechKey key, KpiTuple value, int numPartitions) {
            return (key.getTowerId().hashCode() & Integer.MAX_VALUE) % numPartitions;
        }
    }

    // =========================================================================
    // 6. REDUCER: Tổng hợp toàn mạng, tính trung bình và tỷ lệ rớt cuộc gọi
    // Input:  <TowerTechKey, Iterable<KpiTuple>>
    // Output: <TowerTechKey, Text summaryMetrics>
    // =========================================================================
    public static class KpiReducer extends Reducer<TowerTechKey, KpiTuple, TowerTechKey, Text> {
        private DecimalFormat df = new DecimalFormat("#.##");

        @Override
        protected void reduce(TowerTechKey key, Iterable<KpiTuple> values, Context context)
                throws IOException, InterruptedException {
            double totalTp = 0.0;
            double totalLat = 0.0;
            double totalLoss = 0.0;
            long totalDropped = 0;
            long totalCalls = 0;
            long totalEvents = 0;

            for (KpiTuple val : values) {
                totalTp += val.getThroughputSum();
                totalLat += val.getLatencySum();
                totalLoss += val.getPacketLossSum();
                totalDropped += val.getCallDroppedCount();
                totalCalls += val.getTotalCallsCount();
                totalEvents += val.getEventCount();
            }

            if (totalEvents == 0) return;

            double avgTp = totalTp / totalEvents;
            double avgLat = totalLat / totalEvents;
            double avgLoss = totalLoss / totalEvents;
            // Xử lý an toàn tránh chia cho 0:
            double dropRatePct = (totalCalls > 0) ? ((double) totalDropped * 100.0) / totalCalls : 0.0;

            String status = "NORMAL";
            if (avgLat > 80.0 || dropRatePct > 2.0 || avgLoss > 3.0) {
                status = "DEGRADED_QUALITY";
            }

            String outputLine = String.format(
                "Events=%d\tAvg_Throughput_Mbps=%s\tAvg_Latency_ms=%s\tAvg_Packet_Loss_pct=%s\tCall_Drop_Rate_pct=%s%%\tStatus=%s",
                totalEvents,
                df.format(avgTp),
                df.format(avgLat),
                df.format(avgLoss),
                df.format(dropRatePct),
                status
            );

            context.write(key, new Text(outputLine));
        }
    }

    // =========================================================================
    // 7. DRIVER & JOB CONFIGURATION
    // =========================================================================
    @Override
    public int run(String[] args) throws Exception {
        if (args.length < 2) {
            System.err.println("Usage: TelecomKpiAnalysis <input_path> <output_path>");
            return -1;
        }

        Configuration conf = getConf();
        Job job = Job.getInstance(conf, "Telecom Network KPI Analysis");
        job.setJarByClass(TelecomKpiAnalysis.class);

        // Đặt Mapper, Combiner, Partitioner, Reducer
        job.setMapperClass(KpiMapper.class);
        job.setCombinerClass(KpiCombiner.class);
        job.setPartitionerClass(TowerPartitioner.class);
        job.setReducerClass(KpiReducer.class);

        // Kiểu dữ liệu trung gian giữa Map và Reduce
        job.setMapOutputKeyClass(TowerTechKey.class);
        job.setMapOutputValueClass(KpiTuple.class);

        // Kiểu dữ liệu đầu ra cuối cùng của Reducer
        job.setOutputKeyClass(TowerTechKey.class);
        job.setOutputValueClass(Text.class);

        // Định dạng Input / Output
        job.setInputFormatClass(TextInputFormat.class);
        job.setOutputFormatClass(TextOutputFormat.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        return job.waitForCompletion(true) ? 0 : 1;
    }

    public static void main(String[] args) throws Exception {
        int exitCode = ToolRunner.run(new Configuration(), new TelecomKpiAnalysis(), args);
        System.exit(exitCode);
    }
}
