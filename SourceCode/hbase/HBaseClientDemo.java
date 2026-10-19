package vn.edu.hunre.bigdata.hbase;

import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.NamespaceDescriptor;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Admin;
import org.apache.hadoop.hbase.client.ColumnFamilyDescriptor;
import org.apache.hadoop.hbase.client.ColumnFamilyDescriptorBuilder;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.ConnectionFactory;
import org.apache.hadoop.hbase.client.Delete;
import org.apache.hadoop.hbase.client.Get;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.ResultScanner;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.client.TableDescriptor;
import org.apache.hadoop.hbase.client.TableDescriptorBuilder;
import org.apache.hadoop.hbase.io.compress.Compression.Algorithm;
import org.apache.hadoop.hbase.util.Bytes;

/**
 * CLIENT API JAVA CHO HBASE:
 * Thực hiện đầy đủ các tác vụ Create Table, Put, Get, Scan, Delete
 * phục vụ tra cứu ngẫu nhiên tốc độ cao (low latency) trong hệ thống Viễn thông.
 */
public class HBaseClientDemo {

    private static final String TABLE_NAME = "telecom_kpi";
    private static final byte[] CF_KPI = Bytes.toBytes("cf_kpi");
    private static final byte[] CF_CELL = Bytes.toBytes("cf_cell");
    private static final byte[] CF_ALERT = Bytes.toBytes("cf_alert");

    public static Configuration getHBaseConfig() {
        Configuration config = HBaseConfiguration.create();
        config.set("hbase.zookeeper.quorum", "masternode,datanode1,datanode2");
        config.set("hbase.zookeeper.property.clientPort", "2181");
        config.set("zookeeper.znode.parent", "/hbase");
        return config;
    }

    /**
     * Tạo RowKey theo định dạng: tower_id#reverse_timestamp
     */
    public static byte[] generateRowKey(String towerId, long timestampMs) {
        long reverseTimestamp = Long.MAX_VALUE - timestampMs;
        String rowKeyStr = String.format("%s#%019d", towerId, reverseTimestamp);
        return Bytes.toBytes(rowKeyStr);
    }

    /**
     * 1. CREATE TABLE: Tạo bảng telecom_kpi với 3 Column Families và Pre-splitting
     */
    public static void createTable(Connection connection) throws IOException {
        try (Admin admin = connection.getAdmin()) {
            TableName tableName = TableName.valueOf(TABLE_NAME);
            if (admin.tableExists(tableName)) {
                System.out.println(">>> Bảng " + TABLE_NAME + " đã tồn tại. Đang tiến hành xóa để tạo mới...");
                admin.disableTable(tableName);
                admin.deleteTable(tableName);
            }

            // Cấu hình Column Families: VERSIONS=3, Compression=SNAPPY, TTL=90 ngày
            ColumnFamilyDescriptor cfKpi = ColumnFamilyDescriptorBuilder.newBuilder(CF_KPI)
                    .setMaxVersions(3)
                    .setCompressionType(Algorithm.SNAPPY)
                    .setTimeToLive(7776000) // 90 days
                    .build();

            ColumnFamilyDescriptor cfCell = ColumnFamilyDescriptorBuilder.newBuilder(CF_CELL)
                    .setMaxVersions(1)
                    .setCompressionType(Algorithm.SNAPPY)
                    .build();

            ColumnFamilyDescriptor cfAlert = ColumnFamilyDescriptorBuilder.newBuilder(CF_ALERT)
                    .setMaxVersions(3)
                    .setCompressionType(Algorithm.SNAPPY)
                    .build();

            TableDescriptor tableDesc = TableDescriptorBuilder.newBuilder(tableName)
                    .setColumnFamily(cfKpi)
                    .setColumnFamily(cfCell)
                    .setColumnFamily(cfAlert)
                    .build();

            // Phân vùng trước (Pre-splitting) theo dải mã trạm
            byte[][] splitKeys = new byte[][] {
                    Bytes.toBytes("TOWER_005#"),
                    Bytes.toBytes("TOWER_010#"),
                    Bytes.toBytes("TOWER_015#")
            };

            admin.createTable(tableDesc, splitKeys);
            System.out.println(">>> [HBase API] Tạo bảng thành công: " + TABLE_NAME);
        }
    }

    /**
     * 2. PUT: Ghi bản ghi sự kiện KPI mới vào HBase
     */
    public static void putData(Connection connection, String towerId, long timestampMs,
                               double throughput, double latency, double packetLoss,
                               int callDropped, String cellId, String tech, String status) throws IOException {
        TableName tableName = TableName.valueOf(TABLE_NAME);
        try (Table table = connection.getTable(tableName)) {
            byte[] rowKey = generateRowKey(towerId, timestampMs);
            Put put = new Put(rowKey);

            // Ghi vào cf_kpi
            put.addColumn(CF_KPI, Bytes.toBytes("throughput_mbps"), Bytes.toBytes(String.valueOf(throughput)));
            put.addColumn(CF_KPI, Bytes.toBytes("latency_ms"), Bytes.toBytes(String.valueOf(latency)));
            put.addColumn(CF_KPI, Bytes.toBytes("packet_loss_pct"), Bytes.toBytes(String.valueOf(packetLoss)));
            put.addColumn(CF_KPI, Bytes.toBytes("call_dropped"), Bytes.toBytes(String.valueOf(callDropped)));

            // Ghi vào cf_cell
            put.addColumn(CF_CELL, Bytes.toBytes("cell_id"), Bytes.toBytes(cellId));
            put.addColumn(CF_CELL, Bytes.toBytes("technology"), Bytes.toBytes(tech));

            // Ghi vào cf_alert
            put.addColumn(CF_ALERT, Bytes.toBytes("status"), Bytes.toBytes(status));

            table.put(put);
            System.out.println(">>> [HBase API] Ghi thành công bản ghi với RowKey: " + Bytes.toString(rowKey));
        }
    }

    /**
     * 3. GET: Tra cứu ngẫu nhiên một bản ghi cụ thể theo RowKey
     */
    public static void getData(Connection connection, byte[] rowKey) throws IOException {
        TableName tableName = TableName.valueOf(TABLE_NAME);
        try (Table table = connection.getTable(tableName)) {
            Get get = new Get(rowKey);
            Result result = table.get(get);

            if (!result.isEmpty()) {
                String tp = Bytes.toString(result.getValue(CF_KPI, Bytes.toBytes("throughput_mbps")));
                String lat = Bytes.toString(result.getValue(CF_KPI, Bytes.toBytes("latency_ms")));
                String status = Bytes.toString(result.getValue(CF_ALERT, Bytes.toBytes("status")));

                System.out.println(">>> [HBase API] GET Thành công RowKey: " + Bytes.toString(rowKey));
                System.out.println("    - Throughput: " + tp + " Mbps");
                System.out.println("    - Latency: " + lat + " ms");
                System.out.println("    - Alert Status: " + status);
            } else {
                System.out.println(">>> [HBase API] Không tìm thấy dữ liệu cho RowKey: " + Bytes.toString(rowKey));
            }
        }
    }

    /**
     * 4. SCAN: Quét chuỗi dữ liệu mới nhất của một trạm BTS (nhờ reverse_timestamp)
     */
    public static void scanTowerRecentEvents(Connection connection, String towerId, int limit) throws IOException {
        TableName tableName = TableName.valueOf(TABLE_NAME);
        try (Table table = connection.getTable(tableName)) {
            byte[] startRow = Bytes.toBytes(towerId + "#");
            byte[] stopRow = Bytes.toBytes(towerId + "~");

            Scan scan = new Scan().withStartRow(startRow).withStopRow(stopRow);
            scan.setLimit(limit);

            System.out.println(">>> [HBase API] Quét (SCAN) " + limit + " sự kiện mới nhất của trạm: " + towerId);
            try (ResultScanner scanner = table.getScanner(scan)) {
                int count = 0;
                for (Result res : scanner) {
                    count++;
                    String rKey = Bytes.toString(res.getRow());
                    String lat = Bytes.toString(res.getValue(CF_KPI, Bytes.toBytes("latency_ms")));
                    String tp = Bytes.toString(res.getValue(CF_KPI, Bytes.toBytes("throughput_mbps")));
                    String cell = Bytes.toString(res.getValue(CF_CELL, Bytes.toBytes("cell_id")));
                    System.out.printf("    [%d] RowKey=%s | Cell=%s | Latency=%sms | Throughput=%sMbps\n",
                            count, rKey, cell, lat, tp);
                }
            }
        }
    }

    /**
     * 5. DELETE: Xóa dữ liệu lỗi thời hoặc đã giải quyết
     */
    public static void deleteData(Connection connection, byte[] rowKey) throws IOException {
        TableName tableName = TableName.valueOf(TABLE_NAME);
        try (Table table = connection.getTable(tableName)) {
            Delete delete = new Delete(rowKey);
            table.delete(delete);
            System.out.println(">>> [HBase API] Xóa thành công bản ghi: " + Bytes.toString(rowKey));
        }
    }

    public static void main(String[] args) {
        Configuration config = getHBaseConfig();
        try (Connection connection = ConnectionFactory.createConnection(config)) {
            System.out.println("=== BẮT ĐẦU CHẠY THỬ NGHIỆM HBASE CLIENT API ===");

            // 1. Tạo bảng
            createTable(connection);

            // 2. Thêm dữ liệu
            long now = System.currentTimeMillis();
            putData(connection, "TOWER_003", now, 3.8, 160.5, 9.2, 1, "CELL_TOWER_003_4G_1800", "4G", "CRITICAL_OVERLOAD");
            putData(connection, "TOWER_003", now - 60000, 4.1, 145.0, 7.8, 0, "CELL_TOWER_003_4G_1800", "4G", "WARNING_DEGRADED");

            byte[] sampleRowKey = generateRowKey("TOWER_003", now);

            // 3. Đọc dữ liệu (GET)
            getData(connection, sampleRowKey);

            // 4. Quét chuỗi (SCAN)
            scanTowerRecentEvents(connection, "TOWER_003", 5);

            // 5. Xóa dữ liệu (DELETE)
            // deleteData(connection, sampleRowKey);

            System.out.println("=== KẾT THÚC THỬ NGHIỆM HBASE CLIENT API ===");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
