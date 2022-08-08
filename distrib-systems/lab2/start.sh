mvn package

stop-yarn.sh
stop-dfs.sh

rm -rf ~/hdata/namenode
rm -rf ~/hdata/datanode

mkdir ~/hdata/namenode
mkdir ~/hdata/datanodeS

hdfs namenode -format

start-dfs.sh
start-yarn.sh

hdfs dfs -mkdir /user
hdfs dfs -mkdir /user/parallels

hadoop fs -rm -r -f  hdfs://localhost:9000/user/parallels/output

hadoop fs -copyFromLocal ../data/flights.csv
hadoop fs -copyFromLocal ../data/airports.csv

export HADOOP_CLASSPATH=target/FlightCompareApp-1.0.jar

hadoop FlightCompareApp.AirportStatsApp flights.csv airports.csv output

rm -rf output
mkdir output
hadoop fs -copyToLocal output