echo "jackhammering"
rgn/data_processing/jackhmmer.sh data/workspace/1 data/database.fa
echo "convert to proteinnet"
python3 rgn/data_processing/convert_to_proteinnet.py data/workspace/1
echo "convert to tfrecord"
python3 rgn/data_processing/convert_to_tfrecord.py data/workspace/1.proteinnet data/workspace/1.tfrecord 42
echo "copying tfrecord to rgn input"
cp data/workspace/1.tfrecord data/prediction_input/1.tfrecord
echo "perform rgn"
python3 rgn/model/protling.py data/rgn_config -d data/RGN12 -g 0 -p -e weighted_testing
echo "finished"